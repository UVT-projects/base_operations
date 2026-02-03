from .core import convert_base
from .complement import compute_complement
from .vir_mob import convert_to_ieee754, decode_ieee754
from .arithmetic import perform_arithmetic

# Import run_tests din modulul separat de teste
try:
    from tests.test_mandatory import run_tests
except ImportError:
    def run_tests():
        print("Modulul de teste nu a fost găsit.")

def read_cli_input():
    """
    Gestionează interacțiunea cu utilizatorul prin CLI.
    """
    print("\n--- Convertor Baze Numerice (Unealtă Examen) ---")
    print("Comenzi:")
    print("  exit            - Ieșire")
    # print("  test            - Rulare teste obligatorii")
    print("  vir_mob         - Mod Convertor IEEE 754 (Real <-> IEEE)")
    print("  math            - Mod Aritmetică în Baze")
    print("  [număr]         - Mod Conversie Standard (implicit)")
    
    while True:
        try:
            print("\n------------------------------------------------")
            # Citim de la tastatura
            raw_input = input("Introduceți comandă sau număr (adăugați --v pentru verbose): ").strip()
            
            if not raw_input:
                continue

            # Verificare flag verbose
            verbose = False
            if '--v' in raw_input:
                verbose = True
                # Scoatem flagul din input
                raw_input = raw_input.replace('--v', '').strip()

            cmd_lower = raw_input.lower()
            
            if cmd_lower == 'exit':
                print("Ieșire...")
                break
                
            elif cmd_lower == 'test':
                run_tests()
                continue
                
            elif cmd_lower == 'vir_mob':
                print("\n--- Mod Simplă Precizie IEEE 754 ---")
                print("1. Codificare (Real -> IEEE)")
                print("2. Decodificare (IEEE -> Real)")
                opt = input("Opțiune (1/2): ").strip()
                
                if opt == '2':
                     # Decodificare
                     sir_numar = input("Introduceți reprezentarea IEEE (Hex/Bin/Oct): ").strip()
                     baza_input_str = input("Baza inputului (2, 8, 16): ").strip()
                     
                     if baza_input_str.isdigit() and int(baza_input_str) in [2, 8, 16]:
                         res = decode_ieee754(sir_numar, int(baza_input_str), verbose)
                         print(f"\nRezultat Decimal: {res}")
                     else:
                         print("Bază invalidă pentru decodificare (doar 2, 8, 16).")
                else:
                    # Codificare (Default)
                    sir_numar = input("Introduceți număr real: ").strip()
                    baza_sursa = input("Baza Sursă (ex: 10): ").strip()
                    if baza_sursa.isdigit():
                        b_bin, b_hex, b_oct = convert_to_ieee754(sir_numar, int(baza_sursa), verbose)
                        print(f"\nRezultat (32-biți Binar): {b_bin}")
                        print(f"Rezultat (Hex):          {b_hex}")
                        print(f"Rezultat (Octal):        {b_oct}")
                        # Formatare binar spațiat pentru lizibilitate
                        spatiat = " ".join([b_bin[0], b_bin[1:9], b_bin[9:]])
                        print(f"Structură (S Exp Mant):  {spatiat}")
                    else:
                        print("Bază invalidă.")
                    
            elif cmd_lower == 'math':
                print("\n--- Mod Aritmetică în Baze ---")
                val1 = input("Valoare 1: ").strip()
                baza1 = int(input("Baza 1: ").strip())
                op = input("Operație (+, -, *, /): ").strip()
                val2 = input("Valoare 2: ").strip()
                baza2 = int(input("Baza 2: ").strip())
                baza_rezultat = int(input("Baza Rezultat: ").strip())
                
                res = perform_arithmetic(val1, baza1, val2, baza2, op, baza_rezultat, verbose)
                print(f"\nRezultat (Baza {baza_rezultat}): {res}")
                
                # Verificare Opțională Complement pentru rezultatul aritmetic
                # Nota: original_val_str nu este relevant aici pentru recalculare din sursă,
                # dar funcția helper folosește oricum 'res' (rezultatul) convertit înapoi în baza 10.
                _ofera_prompt_complement(res, None, None, baza_rezultat)
                
            else:
                # Mod Conversie Standard
                # Presupunem că raw_input este numărul
                sir_numar = raw_input
                
                baza_sursa_str = input("Baza sursă (2, 8, 10, 16): ").strip()
                if not baza_sursa_str.isdigit():
                    print("Eroare: Baza trebuie să fie un număr.")
                    continue
                baza_sursa = int(baza_sursa_str)
                
                baza_dest_str = input("Baza țintă (2, 8, 10, 16): ").strip()
                if not baza_dest_str.isdigit():
                    print("Eroare: Baza trebuie să fie un număr.")
                    continue
                baza_dest = int(baza_dest_str)
                
                # Executare Conversie
                rezultat = convert_base(sir_numar, baza_sursa, baza_dest, verbose=verbose)
                print(f"\nRezultat: {rezultat}")
                
                # Verificare Opțională Complement
                _ofera_prompt_complement(rezultat, sir_numar, baza_sursa, baza_dest)

            # Mesaj de așteptare
            print("\nIntroduceți noua comandă (vir_mob, math, [număr]). Folosiți --v pentru verbose.")

        except ValueError as e:
            print(f"Eroare Input: {e}")
        except Exception as e:
            print(f"Eroare Neașteptată: {e}")

def _ofera_prompt_complement(sir_rezultat, val_originala_str, baza_sursa, baza_tinta):
    """
    Funcție helper pentru a oferi utilizatorului opțiunea de a calcula complementul
    unui rezultat, dacă acesta este un număr întreg valid.
    """
    # Verificam daca nu are virgula sau paranteza
    if "." not in sir_rezultat and "(" not in sir_rezultat:
        try:
            fa_comp = input(f"Calculați complement în Baza {baza_tinta}? (y/n): ").strip().lower()
            if fa_comp == 'y':
                print(f"1. Complement față de Bază (C{baza_tinta})")
                print(f"2. Complement Restrâns (C{baza_tinta-1})")
                
                alegere = input("Selectați tipul (1 sau 2): ").strip()
                e_radix = True
                if alegere == '2':
                    e_radix = False
                
                # Calculam lungimea minima (fara semn)
                sir_curat = sir_rezultat.replace('-', '')
                lungime_minima = len(sir_curat)
                
                # Cautam standardul potrivit (8, 16, 32, 64)
                standarde = [8, 16, 32, 64]
                default_ales = 0
                restul_optiunilor = []
                
                # Iteram babeste
                gasit = False
                for s in standarde:
                    if s >= lungime_minima:
                        if not gasit:
                            default_ales = s
                            gasit = True
                        else:
                            restul_optiunilor.append(s)
                            
                # Daca e prea mare, default e lungimea minima
                if default_ales == 0:
                    default_ales = lungime_minima
                    
                # Construim mesajul
                mesaj_optiuni = ""
                if len(restul_optiunilor) > 0:
                    mesaj_optiuni = f" ({restul_optiunilor} etc)"
                
                input_msg = f"Număr de cifre/biți [Default: {default_ales}]{mesaj_optiuni}: "
                biti_str = input(input_msg).strip()
                
                if biti_str == "":
                    # A dat enter, folosim default
                    biti = default_ales
                    print(f"-> Folosim default: {biti}")
                elif biti_str.isdigit():
                    biti = int(biti_str)
                else:
                    print("Valoare invalidă, folosim default.")
                    biti = default_ales

                # Restul logicii ramane la fel...
                # Pentru a calcula complementul, avem nevoie de valoarea în baza 10.
                sir_val_zecimala = convert_base(sir_rezultat, baza_tinta, 10, verbose=False)
                
                if '.' in sir_val_zecimala:
                        print("Eroare: Complementele sunt permise doar pentru întregi.")
                else:
                        res_comp = compute_complement(sir_val_zecimala, baza_tinta, biti, e_radix)
                        tip_c = f"C{baza_tinta}" if e_radix else f"C{baza_tinta-1}"
                        print(f"{tip_c} ({biti} cifre): {res_comp}")

        except ValueError as e:
            print(f"Eroare Complement: {e}")