from .core import base_b_to_decimal, decimal_to_base_b, citeste_input
from .parser import NumarIntern, val_to_char, char_to_val

def hex_pad(s, length):
    return s.zfill(length)

def bin_pad(s, length):
    return s.zfill(length)

def decode_ieee754(sir_input, baza_input, verbose=False):
    """
    Convertește un șir IEEE 754 (Binar, Hex, Octal) în valoarea sa Decimală.
    """
    if verbose:
        print(f"\n[IEEE 754] Decodificare {sir_input} (Baza {baza_input})")
        
    # 1. Normalizare la Binar 32-biți
    sir_binar_32 = ""
    
    if baza_input == 2:
        # Trebuie sa aiba 32 biti. Daca nu, facem padding sau trunchiere?
        # Presupunem input corect sau padding la stanga
        if len(sir_input) > 32:
             sir_binar_32 = sir_input[-32:] # Luam ultimii 32
        else:
             sir_binar_32 = sir_input.zfill(32)
             
    elif baza_input == 16:
        # Hex -> Bin
        for char in sir_input:
            val = char_to_val(char)
            # 4 biti
            bin_chunk = ""
            temp = val
            for _ in range(4):
                bin_chunk = str(temp % 2) + bin_chunk
                temp //= 2
            sir_binar_32 += bin_chunk
            
        if len(sir_binar_32) > 32:
            sir_binar_32 = sir_binar_32[-32:]
        else:
            sir_binar_32 = sir_binar_32.zfill(32)
            
    elif baza_input == 8:
        # Octal -> Bin
        for char in sir_input:
            val = char_to_val(char)
            # 3 biti
            bin_chunk = ""
            temp = val
            for _ in range(3):
                bin_chunk = str(temp % 2) + bin_chunk
                temp //= 2
            sir_binar_32 += bin_chunk
            
        # Octalul pe 32 biti ocupa 11 cifre -> 33 biti. Primul e 0 sau 1 (daca e overflow)
        # Luam ultimii 32
        if len(sir_binar_32) > 32:
            sir_binar_32 = sir_binar_32[-32:]
        else:
            sir_binar_32 = sir_binar_32.zfill(32)
    else:
        raise ValueError("Baza input trebuie să fie 2, 8 sau 16.")
        
    if verbose:
        print(f"  Binar Intern (32 biți): {sir_binar_32}")
        spatiat = " ".join([sir_binar_32[0], sir_binar_32[1:9], sir_binar_32[9:]])
        print(f"  Structură: {spatiat}")

    # 2. Extragere Componente
    s_bit = sir_binar_32[0]
    e_bits = sir_binar_32[1:9]
    m_bits = sir_binar_32[9:]
    
    semn = -1 if s_bit == '1' else 1
    
    # Exponent integer
    exp_bias = 0
    for bit in e_bits:
        exp_bias = exp_bias * 2 + int(bit)
        
    # Mantisa integer
    mant_int = 0
    for bit in m_bits:
        mant_int = mant_int * 2 + int(bit)
        
    if verbose:
        print(f"  Semn: {semn}, Exp Bias: {exp_bias}, Mantisa Int: {mant_int}")

    # Cazuri Speciale
    if exp_bias == 255:
        if mant_int == 0:
            return "-Infinity" if semn == -1 else "+Infinity"
        else:
            return "NaN"
            
    if exp_bias == 0:
        if mant_int == 0:
            if verbose: print("  Caz: Zero")
            return "0" if semn == 1 else "-0"
        else:
            # Denormalizat
            exponent = 1 - 127 # -126
            # Fara 1 implicit
            numarator_mantisa = mant_int
            if verbose: print("  Caz: Denormalizat")
    else:
        # Normalizat
        exponent = exp_bias - 127
        # 1 implicit -> 1.M -> (2^23 + M) / 2^23
        numarator_mantisa = (1 << 23) + mant_int
        
    # Valoare = semn * numarator_mantisa * 2^(exponent - 23)
    # exponentul efectiv al partii intregi a mantisei este exponent - 23
    
    shift = exponent - 23
    
    val_numarator = numarator_mantisa
    val_numitor = 1
    
    if shift >= 0:
        val_numarator = val_numarator * (2 ** shift)
    else:
        val_numitor = 2 ** (-shift)
        
    # Construim NumarIntern
    p_intreaga = val_numarator // val_numitor
    rest = val_numarator % val_numitor
    
    # Simplificare fractie
    def cmmdc(a, b):
        while b:
            a, b = b, a % b
        return a
        
    comun = cmmdc(rest, val_numitor)
    p_frac_num = rest // comun
    p_frac_den = val_numitor // comun
    
    intern = NumarIntern(semn, p_intreaga, p_frac_num, p_frac_den)
    
    # Conversie la string zecimal
    rezultat = decimal_to_base_b(intern, 10, precizie=20, verbose=verbose)
    return rezultat

def convert_to_ieee754(sir_numar, baza_sursa, verbose=False):
    """
    Convertește un număr (string în baza sursă) în IEEE 754 Simplă Precizie (32-biți).
    """
    if verbose:
        print(f"\n[IEEE 754] Procesare {sir_numar} (Baza {baza_sursa})")

    # 1. Parsare
    numar_intern = base_b_to_decimal(sir_numar, baza_sursa, verbose=False)
    
    # Tratare Zero
    if numar_intern.p_intreaga == 0 and numar_intern.numarator == 0:
        if verbose: print("  Valoarea este Zero.")
        return ("0" * 32, "00000000")

    # 1. Bit de Semn (1 bit)
    bit_semn = '1' if numar_intern.semn == -1 else '0'
    if verbose: print(f"  Bit de Semn: {bit_semn} ({'Negativ' if bit_semn=='1' else 'Pozitiv'})")

    # 2. Valoare Absoluta
    # Facem un numar pozitiv temporar
    abs_intern = NumarIntern(1, numar_intern.p_intreaga, numar_intern.numarator, numar_intern.numitor)
    
    # Obtinem reprezentarea binara cu precizie mare
    # Vrem multe cifre
    
    sir_binar = decimal_to_base_b(abs_intern, 2, precizie=150)
    # Scoatem parantezele de perioada
    sir_binar = sir_binar.replace('(', '').replace(')', '')
    
    if '.' in sir_binar:
        int_binar, frac_binar = sir_binar.split('.')
    else:
        int_binar = sir_binar
        frac_binar = ""
        
    # 3. Normalizare: 1.M * 2^E
    exponent = 0
    mantisa_bits = ""
    
    # Gasim primul '1'
    primul_unu = -1
    
    if '1' in int_binar:
        # Exponentul e pozitiv
        primul_unu = int_binar.find('1')
        exponent = len(int_binar) - 1 - primul_unu
        
        # Mantisa e tot ce e dupa primul 1
        mantisa_full = int_binar[primul_unu+1:] + frac_binar
        
    else:
        # E in partea fractionara
        if '1' in frac_binar:
            primul_unu = frac_binar.find('1')
            # E negativ
            exponent = -1 - primul_unu
            mantisa_full = frac_binar[primul_unu+1:]
        else:
            # Caz de 0 tratat mai sus
             return ("0" * 32, "00000000")

    if verbose:
        print(f"  Normalizat: 1.{mantisa_full[:23]}... * 2^{exponent}")

    # 4. Exponent (8 biți, Bias 127)
    exp_biasat = exponent + 127
    if exp_biasat < 0 or exp_biasat > 255:
        print("  Avertisment: Depășire Exponent.")
        # Clampare simpla
        if exp_biasat < 0: exp_biasat = 0
        if exp_biasat > 255: exp_biasat = 255

    # Conversie exponent la binar 8-biți
    exp_binar = ""
    temp = exp_biasat
    for _ in range(8):
        exp_binar = str(temp % 2) + exp_binar
        temp //= 2
        
    if verbose:
        print(f"  Exponent Biasat: {exponent} + 127 = {exp_biasat} -> {exp_binar} (Binar)")

    # 5. Mantisa (23 biți)
    # Completam cu 0
    mantisa_23 = mantisa_full.ljust(23, '0')[:23]
    if verbose:
        print(f"  Mantisă (23 biți): {mantisa_23}")

    # 6. Lipim tot
    ieee_bin = bit_semn + exp_binar + mantisa_23
    
    # 7. Conversie la Hex
    hex_str = ""
    for i in range(0, 32, 4):
        bucata = ieee_bin[i:i+4]
        # Binar la int manual
        val = 0
        for bit in bucata:
            val = val * 2 + (1 if bit == '1' else 0)
        hex_str += val_to_char(val)

    # 8. Conversie la Octal
    # 32 biți nu se împart exact la 3 (rest 2).
    # Considerăm numărul ca valoare pe 32 biți.
    # Pentru a grupa câte 3, adăugăm un 0 imaginar la stânga -> 33 biți total.
    bin_pt_octal = "0" + ieee_bin
    oct_str = ""
    for i in range(0, 33, 3):
        bucata = bin_pt_octal[i:i+3]
        val = 0
        for bit in bucata:
            val = val * 2 + (1 if bit == '1' else 0)
        oct_str += val_to_char(val)
        
    return ieee_bin, hex_str, oct_str