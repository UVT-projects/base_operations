from .parser import NumarIntern
from .core import base_b_to_decimal, decimal_to_base_b

def cmmdc(a, b):
    # Facem cmmdc ca sa simplificam
    while b:
        a, b = b, a % b
    return a

def simplifica_fractie(num, den):
    comun = cmmdc(num, den)
    return num // comun, den // comun

def aduna_interne(n1, n2):
    """
    Adună două obiecte NumarIntern.
    """
    # 1. Transformam in fractii improprii
    # n1
    d1 = n1.numitor
    total_n1 = n1.p_intreaga * d1 + n1.numarator
    if n1.semn == -1:
        total_n1 = -total_n1
        
    # n2
    d2 = n2.numitor
    total_n2 = n2.p_intreaga * d2 + n2.numarator
    if n2.semn == -1:
        total_n2 = -total_n2
        
    # 2. Adunare propriu-zisa
    # Numitor comun
    res_d = d1 * d2
    # Numarator rezultat
    res_n = total_n1 * d2 + total_n2 * d1
    
    # 3. Vedem semnul si simplificam
    semn_rez = 1
    if res_n < 0:
        semn_rez = -1
        res_n = -res_n
        
    if res_n == 0:
        return NumarIntern(1, 0, 0, 1)

    # Convertim inapoi la mixt (intreg + fractie)
    # Partea întreagă
    res_int = res_n // res_d
    res_rest = res_n % res_d
    
    final_num, final_den = simplifica_fractie(res_rest, res_d)
    
    return NumarIntern(semn_rez, res_int, final_num, final_den)

def scade_interne(n1, n2):
    # n1 - n2 e ca n1 + (-n2)
    # Facem negativul lui n2
    neg_n2 = NumarIntern(-n2.semn, n2.p_intreaga, n2.numarator, n2.numitor)
    return aduna_interne(n1, neg_n2)

def inmulteste_interne(n1, n2):
    """
    Înmulțește două obiecte NumarIntern.
    """
    # 1. Transformam in fractii
    d1 = n1.numitor
    total_n1 = n1.p_intreaga * d1 + n1.numarator
    
    d2 = n2.numitor
    total_n2 = n2.p_intreaga * d2 + n2.numarator
    
    # 2. Inmultire
    res_n = total_n1 * total_n2
    res_d = d1 * d2
    
    # 3. Semne
    semn_final = n1.semn * n2.semn
    
    if res_n == 0:
        return NumarIntern(1, 0, 0, 1)
        
    # 4. Simplificare
    res_int = res_n // res_d
    res_rest = res_n % res_d
    
    final_num, final_den = simplifica_fractie(res_rest, res_d)
    
    return NumarIntern(semn_final, res_int, final_num, final_den)

def imparte_interne(n1, n2):
    """
    Împarte două numere.
    """
    # 1. Fractii
    d1 = n1.numitor
    total_n1 = n1.p_intreaga * d1 + n1.numarator
    
    d2 = n2.numitor
    total_n2 = n2.p_intreaga * d2 + n2.numarator
    
    if total_n2 == 0:
        raise ValueError("Împărțire la zero")
        
    # 2. Impartire = inmultire cu inversul
    res_n = total_n1 * d2
    res_d = d1 * total_n2
    
    # 3. Semne
    semn_final = n1.semn * n2.semn
    
    if res_n == 0:
        return NumarIntern(1, 0, 0, 1)

    # 4. Refacem numarul
    res_int = res_n // res_d
    res_rest = res_n % res_d
    
    final_num, final_den = simplifica_fractie(res_rest, res_d)
    
    return NumarIntern(semn_final, res_int, final_num, final_den)

def perform_arithmetic(val1, base1, val2, base2, operation, target_base, verbose=False):
    if verbose:
        print(f"\n[Aritmetică] {val1} (Baza {base1}) {operation} {val2} (Baza {base2})")
    
    # 1. Conversie la intern
    int1 = base_b_to_decimal(val1, base1, verbose=False)
    int2 = base_b_to_decimal(val2, base2, verbose=False)
    
    # 2. Operatia
    if operation == '+':
        res_internal = aduna_interne(int1, int2)
    elif operation == '-':
        res_internal = scade_interne(int1, int2)
    elif operation == '*':
        res_internal = inmulteste_interne(int1, int2)
    elif operation == '/':
        res_internal = imparte_interne(int1, int2)
    else:
        raise ValueError("Operație necunoscută. Suportate: +, -, *, /")
        
    if verbose:
        # Debugging print
        print(f"  Rezultat Intern (Baza 10): Semn={res_internal.semn}, Int={res_internal.p_intreaga}, Frac={res_internal.numarator}/{res_internal.numitor}")

    # 3. Rezultatul final
    return decimal_to_base_b(res_internal, target_base, precizie=20, verbose=verbose)