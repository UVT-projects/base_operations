from .core import base_b_to_decimal, decimal_to_base_b
from .parser import char_to_val, val_to_char, NumarIntern

def compute_complement(sir_zecimal, baza_tinta, nr_cifre, e_complement_baza):
    """
    Calculează Complementele Generalizate.
    """
    # 1. Verificam sa nu fie fractie
    if '.' in sir_zecimal:
        raise ValueError("Fracțiile sunt strict interzise în complement.")
        
    # Verificam si intern
    numar_intern = base_b_to_decimal(sir_zecimal, 10)
    if numar_intern.numarator != 0:
         raise ValueError("Fracțiile sunt strict interzise în complement.")
    
    valoare = numar_intern.p_intreaga
    
    # 2. Facem magnitudine in baza tinta
    # Facem un numar pozitiv temporar
    temp_intern = NumarIntern(1, valoare, 0, 1)
    sir_tinta = decimal_to_base_b(temp_intern, baza_tinta)
    
    if len(sir_tinta) > nr_cifre:
        raise ValueError(f"Valoarea '{sir_tinta}' încape în {len(sir_tinta)} cifre, dar au fost furnizate doar {nr_cifre}.")

    # 3. Punem zerouri in fata (Padding)
    sir_plin = sir_tinta.zfill(nr_cifre)
    
    # 4. Inversam cifrele (Complement Diminuat)
    # Valoarea maxima a unei cifre
    max_cifra = baza_tinta - 1
    
    cifre_inversate = []
    for char in sir_plin:
        val_cifra = char_to_val(char)
        noua_val = max_cifra - val_cifra
        cifre_inversate.append(val_to_char(noua_val))
        
    sir_complement_diminuat = "".join(cifre_inversate)
    
    if not e_complement_baza:
        return sir_complement_diminuat
        
    # 5. Adunam 1 daca e Complement fata de Baza
    # Adunare babeste
    cifre = list(sir_complement_diminuat)
    transport = 1
    
    # Mergem de la coada la cap
    for i in range(nr_cifre - 1, -1, -1):
        if transport == 0:
            break
            
        val_curenta = char_to_val(cifre[i])
        suma = val_curenta + transport
        
        if suma >= baza_tinta:
            cifre[i] = val_to_char(suma % baza_tinta)
            transport = 1
        else:
            cifre[i] = val_to_char(suma)
            transport = 0
            
    # Daca transportul a ramas 1, il ignoram (asa e regula)
    return "".join(cifre)

def ones_complement(sir_zecimal, nr_cifre):
    """Helper pentru C1."""
    return compute_complement(sir_zecimal, 2, nr_cifre, False)

def twos_complement(sir_zecimal, nr_cifre):
    """Helper pentru C2."""
    return compute_complement(sir_zecimal, 2, nr_cifre, True)