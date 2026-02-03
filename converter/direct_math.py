from .parser import char_to_val, val_to_char

def _split_num(s):
    if '.' in s:
        p = s.split('.')
        return p[0], p[1]
    return s, ""

def _align_points(s1, s2):
    """
    Aliniază două numere la virgulă prin padding cu zerouri.
    Returnează (int1, frac1, int2, frac2, max_len_frac).
    """
    i1, f1 = _split_num(s1)
    i2, f2 = _split_num(s2)
    
    # Padding fractionar (la dreapta)
    max_f = max(len(f1), len(f2))
    f1 = f1.ljust(max_f, '0')
    f2 = f2.ljust(max_f, '0')
    
    return i1, f1, i2, f2

def _compare_magnitudes(s1, s2, baza):
    """
    Returnează 1 dacă |s1| > |s2|, -1 dacă |s1| < |s2|, 0 egal.
    Presupune s1, s2 pozitive, aliniate.
    """
    i1, f1, i2, f2 = _align_points(s1, s2)
    
    i1 = i1.lstrip('0') or '0'
    i2 = i2.lstrip('0') or '0'
    
    if len(i1) > len(i2): return 1
    if len(i2) > len(i1): return -1
    
    if i1 > i2: return 1
    if i2 > i1: return -1
    
    if f1 > f2: return 1
    if f2 > f1: return -1
    
    return 0

def add_direct(s1, s2, baza, verbose=False):
    if verbose:
        print(f"  [Adunare] {s1} + {s2} (Baza {baza})")

    i1, f1, i2, f2 = _align_points(s1, s2)
    
    num1 = i1 + f1
    num2 = i2 + f2
    
    max_len = max(len(num1), len(num2))
    num1 = num1.zfill(max_len)
    num2 = num2.zfill(max_len)
    
    carry = 0
    res_digits = []
    
    if verbose:
        print("    Procesare cifră cu cifră (dreapta -> stânga):")

    for idx in range(max_len - 1, -1, -1):
        v1 = char_to_val(num1[idx])
        v2 = char_to_val(num2[idx])
        
        suma = v1 + v2 + carry
        cifra = suma % baza
        new_carry = suma // baza
        
        if verbose:
            print(f"      {val_to_char(v1)} + {val_to_char(v2)} + c{carry} = {suma} -> Cifră {val_to_char(cifra)}, Transport {new_carry}")
            
        carry = new_carry
        res_digits.append(val_to_char(cifra))
        
    if carry > 0:
        if verbose:
            print(f"      Transport final rămas: {carry}")
        res_digits.append(val_to_char(carry))
        
    res_digits.reverse()
    full_res = "".join(res_digits)
    
    len_frac = len(f1)
    if len_frac > 0:
        if len(full_res) <= len_frac:
            full_res = full_res.zfill(len_frac + 1)
        int_part = full_res[:-len_frac]
        frac_part = full_res[-len_frac:]
        return f"{int_part}.{frac_part}"
    
    return full_res

def sub_direct(s1, s2, baza, verbose=False):
    if verbose:
        print(f"  [Scădere] {s1} - {s2} (Baza {baza})")
        
    i1, f1, i2, f2 = _align_points(s1, s2)
    
    num1 = i1 + f1
    num2 = i2 + f2
    
    max_len = max(len(num1), len(num2))
    num1 = num1.zfill(max_len)
    num2 = num2.zfill(max_len)
    
    borrow = 0
    res_digits = []
    
    if verbose:
        print("    Procesare cifră cu cifră (dreapta -> stânga):")
        
    for idx in range(max_len - 1, -1, -1):
        v1 = char_to_val(num1[idx])
        v2 = char_to_val(num2[idx])
        
        diff = v1 - v2 - borrow
        
        current_borrow = 0
        if diff < 0:
            diff += baza
            current_borrow = 1
            
        if verbose:
            print(f"      {val_to_char(v1)} - {val_to_char(v2)} - b{borrow} = ... -> Rez {val_to_char(diff)}, Împrumut {current_borrow}")

        borrow = current_borrow
        res_digits.append(val_to_char(diff))
        
    res_digits.reverse()
    full_res = "".join(res_digits)
    
    len_frac = len(f1)
    if len_frac > 0:
        int_part = full_res[:-len_frac]
        frac_part = full_res[-len_frac:]
        int_part = int_part.lstrip('0') or '0'
        return f"{int_part}.{frac_part}"
    
    full_res = full_res.lstrip('0') or '0'
    return full_res

def mul_direct(s1, s2, baza, verbose=False):
    if verbose:
        print(f"  [Înmulțire] {s1} * {s2} (Baza {baza})")

    i1, f1 = _split_num(s1)
    i2, f2 = _split_num(s2)
    decimals = len(f1) + len(f2)
    
    n1_str = i1 + f1
    n2_str = i2 + f2
    
    total_sum_str = "0"
    
    # Iteram prin n2 de la dreapta la stanga
    if verbose:
        print("    Calcule parțiale:")
        
    for idx_2, digit_char in enumerate(reversed(n2_str)):
        digit_val = char_to_val(digit_char)
        if digit_val == 0:
            if verbose:
                print(f"      Cifra {digit_char}: Skip (0)")
            continue
            
        # Inmultire n1_str * digit_val
        carry = 0
        current_res = []
        for idx_1 in range(len(n1_str) - 1, -1, -1):
            val1 = char_to_val(n1_str[idx_1])
            prod = val1 * digit_val + carry
            
            cifra = prod % baza
            carry = prod // baza
            current_res.append(val_to_char(cifra))
            
        if carry > 0:
            current_res.append(val_to_char(carry))
            
        current_res.reverse()
        partial_prod = "".join(current_res)
        
        # Adaugam zerouri la dreapta (shiftare)
        shifted_prod = partial_prod + "0" * idx_2
        
        if verbose:
            print(f"      x {digit_char} -> {partial_prod} (shiftat: {shifted_prod})")
            
        # Adunam la total
        # Folosim add_direct dar fara verbose recursiv excesiv, decat daca vrem debug full
        # Dezactivam verbose la adunarea interna pentru claritate, sau il lasam?
        # Mai bine fara verbose la adunari interne, ar fi prea mult text.
        total_sum_str = add_direct(total_sum_str, shifted_prod, baza, verbose=False)
        if verbose:
            print(f"      Suma curentă: {total_sum_str}")
        
    if decimals > 0:
        if len(total_sum_str) <= decimals:
            total_sum_str = total_sum_str.zfill(decimals + 1)
        
        int_part = total_sum_str[:-decimals]
        frac_part = total_sum_str[-decimals:]
        
        return f"{int_part}.{frac_part}"
        
    return total_sum_str

def div_direct(s1, s2, baza, precision=10, verbose=False):
    if verbose:
        print(f"  [Împărțire] {s1} / {s2} (Baza {baza})")

    i1, f1 = _split_num(s1)
    i2, f2 = _split_num(s2)
    
    max_frac = max(len(f1), len(f2))
    
    s1_norm = (i1 + f1.ljust(max_frac, '0')).lstrip('0') or '0'
    s2_norm = (i2 + f2.ljust(max_frac, '0')).lstrip('0') or '0'
    
    if s2_norm == '0':
        raise ValueError("Împărțire la zero.")
    
    if verbose:
        print(f"    Normalizare (fără virgulă): {s1_norm} / {s2_norm}")
        
    quotient = ""
    remainder_str = "0"
    
    idx = 0
    # Partea intreaga
    if verbose:
        print("    Calcul Parte Întreagă:")
        
    while idx < len(s1_norm):
        remainder_str = remainder_str + s1_norm[idx]
        remainder_str = remainder_str.lstrip('0') or '0'
        
        best_q = 0
        for q in range(baza - 1, -1, -1):
            q_char = val_to_char(q)
            prod = mul_direct(s2_norm, q_char, baza, verbose=False)
            if _compare_magnitudes(prod, remainder_str, baza) <= 0:
                best_q = q
                remainder_str = sub_direct(remainder_str, prod, baza, verbose=False)
                break
        
        quotient += val_to_char(best_q)
        if verbose and (quotient != '0' or best_q != 0): # Doar cand avem ceva relevant
             print(f"      Rest curent {remainder_str}. Cât estimat: {val_to_char(best_q)}")
             
        idx += 1
        
    quotient = quotient.lstrip('0') or '0'
    
    if remainder_str == '0':
        return quotient
        
    quotient += "."
    count = 0
    
    if verbose:
        print("    Calcul Parte Fracționară:")
        
    while remainder_str != '0' and count < precision:
        remainder_str += "0"
        remainder_str = remainder_str.lstrip('0') or '0'
        
        best_q = 0
        for q in range(baza - 1, -1, -1):
            q_char = val_to_char(q)
            prod = mul_direct(s2_norm, q_char, baza, verbose=False)
            if _compare_magnitudes(prod, remainder_str, baza) <= 0:
                best_q = q
                remainder_str = sub_direct(remainder_str, prod, baza, verbose=False)
                break
                
        quotient += val_to_char(best_q)
        if verbose:
             print(f"      Iter {count}: Rest {remainder_str} -> Cifră {val_to_char(best_q)}")
        count += 1
        
    return quotient

def perform_direct_op(val1, val2, baza, op, verbose=False):
    semn1 = -1 if val1.startswith('-') else 1
    semn2 = -1 if val2.startswith('-') else 1
    
    s1 = val1.lstrip('-')
    s2 = val2.lstrip('-')
    
    res_str = ""
    res_semn = 1
    
    if op == '*':
        res_semn = semn1 * semn2
        res_str = mul_direct(s1, s2, baza, verbose)
        
    elif op == '/':
        res_semn = semn1 * semn2
        res_str = div_direct(s1, s2, baza, precision=10, verbose=verbose)
        
    elif op == '+':
        if semn1 == semn2:
            res_semn = semn1
            res_str = add_direct(s1, s2, baza, verbose)
        else:
            cmp = _compare_magnitudes(s1, s2, baza)
            if cmp >= 0:
                res_semn = semn1
                res_str = sub_direct(s1, s2, baza, verbose)
            else:
                res_semn = semn2
                res_str = sub_direct(s2, s1, baza, verbose)
                
    elif op == '-':
        semn2_new = -semn2
        if semn1 == semn2_new:
            res_semn = semn1
            res_str = add_direct(s1, s2, baza, verbose)
        else:
            cmp = _compare_magnitudes(s1, s2, baza)
            if cmp >= 0:
                res_semn = semn1
                res_str = sub_direct(s1, s2, baza, verbose)
            else:
                res_semn = semn2_new
                res_str = sub_direct(s2, s1, baza, verbose)
                
    if res_str == '0' or res_str == '0.0': 
        return '0'
        
    if res_semn == -1:
        return "-" + res_str
    return res_str
