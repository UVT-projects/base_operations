from .core import base_b_to_decimal, decimal_to_base_b, citeste_input
from .parser import NumarIntern, val_to_char

def hex_pad(s, length):
    return s.zfill(length)

def bin_pad(s, length):
    return s.zfill(length)

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
        
    return ieee_bin, hex_str