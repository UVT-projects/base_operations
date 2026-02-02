from .parser import citeste_input, char_to_val, val_to_char, NumarIntern

def base_b_to_decimal(text, baza, verbose=False):
    """
    Convertește numărul din baza b în NumarIntern (reprezentare baza 10).
    """
    # Citim input-ul
    semn, sir_intreg, sir_frac = citeste_input(text, baza)
    
    if verbose:
        print(f"\n[Pasul 1] Conversie {text} (Baza {baza}) -> Baza 10")
        print(f"  Semn: {{'-' if semn == -1 else '+'}}")

    val_intreaga = 0
    if verbose:
        print("  Calcul Parte Întreagă:")
        termeni = []
        putere = len(sir_intreg) - 1
        for char in sir_intreg:
            val = char_to_val(char)
            termeni.append(f"{val}*{baza}^{putere}")
            putere -= 1
        print(f"    {{' + '.join(termeni)}}")
    
    # Calculam valoarea intreaga
    for char in sir_intreg:
        val_intreaga = val_intreaga * baza + char_to_val(char)
        
    if verbose:
        print(f"    = {val_intreaga}")

    numarator = 0
    numitor = 1
    
    if sir_frac:
        if verbose:
            print("  Calcul Parte Fracționară:")
            termeni = []
            putere = -1
            for char in sir_frac:
                val = char_to_val(char)
                termeni.append(f"{val}*{baza}^{{{putere}}}")
                putere -= 1
            print(f"    {{' + '.join(termeni)}}")

        numarator_curent = 0
        for char in sir_frac:
            numarator_curent = numarator_curent * baza + char_to_val(char)
            numitor = numitor * baza
            
        numarator = numarator_curent
        
        if verbose:
            print(f"    = {numarator} / {numitor}")

    return NumarIntern(semn, val_intreaga, numarator, numitor)

def get_base_b_digits(numar_intern, baza, precizie=20, verbose=False):
    """
    Convertește NumarIntern în liste de valori ale cifrelor.
    """
    if verbose:
        print(f"\n[Pasul 2] Conversie Intern (Baza 10) -> Baza {baza}")
    
    # Partea întreagă
    val_int = numar_intern.p_intreaga
    cifre_intregi = []
    
    if verbose:
        print(f"  Împărțiri Succesive Parte Întreagă ({val_int}):")
        
    if val_int == 0:
        cifre_intregi = [0]
        if verbose:
            print(f"    0 / {baza} = 0 rest 0")
    else:
        temp_val = val_int
        while temp_val > 0:
            cifra_val = temp_val % baza
            noua_val = temp_val // baza
            if verbose:
                print(f"    {temp_val} / {baza} = {noua_val} rest {cifra_val} ({{val_to_char(cifra_val)}})")
            cifre_intregi.append(cifra_val)
            temp_val = noua_val
        # Inversam lista ca e invers
        cifre_intregi.reverse()

    # Partea fracționară cu Detecție Perioadă
    cifre_frac = []
    num = numar_intern.numarator
    den = numar_intern.numitor
    
    stari_vazute = {} # Map rest -> index
    start_perioada = -1
    
    if num != 0:
        if verbose:
            print(f"  Înmulțiri Succesive Parte Fracționară ({num}/{den}) (Max {precizie} iterații):")
            
        contor = 0
        while num > 0 and contor < precizie:
            # Verificare ciclu
            if num in stari_vazute:
                start_perioada = stari_vazute[num]
                if verbose:
                    print(f"    -> Ciclu detectat! Restul {num} văzut la indexul {start_perioada}.")
                break
            
            stari_vazute[num] = contor
            
            num *= baza
            cifra_val = num // den
            rest = num % den
            
            if verbose:
                print(f"    iter {contor}: ... -> Cifră {{val_to_char(cifra_val)}}, Rest Nou {rest}")
            
            cifre_frac.append(cifra_val)
            num = rest
            contor += 1
            
    return numar_intern.semn, cifre_intregi, cifre_frac, start_perioada

def format_output(semn, cifre_intregi, cifre_frac, start_perioada=-1):
    """
    Formatează cifrele în reprezentarea finală string.
    """
    rezultat = ""
    if semn == -1:
        rezultat += "-"
    
    rezultat += "".join(val_to_char(d) for d in cifre_intregi)
    
    if cifre_frac:
        rezultat += "."
        if start_perioada == -1:
            rezultat += "".join(val_to_char(d) for d in cifre_frac)
        else:
            # Parte neperiodică
            rezultat += "".join(val_to_char(d) for d in cifre_frac[:start_perioada])
            # Parte periodică
            rezultat += "(" + "".join(val_to_char(d) for d in cifre_frac[start_perioada:]) + ")"
        
    return rezultat

def decimal_to_base_b(numar_intern, baza, precizie=20, verbose=False):
    semn, cifre_intregi, cifre_frac, start_perioada = get_base_b_digits(numar_intern, baza, precizie, verbose)
    return format_output(semn, cifre_intregi, cifre_frac, start_perioada)

def convert_base(input_str, baza_sursa, baza_dest, precizie=20, verbose=False):
    rep_interna = base_b_to_decimal(input_str, baza_sursa, verbose)
    output_str = decimal_to_base_b(rep_interna, baza_dest, precizie, verbose)
    return output_str