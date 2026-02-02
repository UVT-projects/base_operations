# Constante pentru conversia cifrelor
CIFRE = "0123456789ABCDEF"
# Aici facem un dictionar ca sa gasim repede valoarea
DictionarValori = {c: i for i, c in enumerate(CIFRE)}

class NumarIntern:
    def __init__(self, semn, p_intreaga, numarator, numitor):
        # Aici salvam datele numarului
        """
        semn: +1 sau -1
        p_intreaga: int (baza 10)
        numarator: int (baza 10)
        numitor: int (baza 10, putere a bazei sursă)
        """
        self.semn = semn
        self.p_intreaga = p_intreaga
        self.numarator = numarator
        self.numitor = numitor

    def __str__(self):
        # Afisare simpla pentru debug
        return f"NumarIntern(semn={self.semn}, int={self.p_intreaga}, frac={self.numarator}/{self.numitor})"

def verifica_input(text, baza):
    """
    Validează caracterele de intrare, numărul de semne și numărul de separatori.
    Returnează textul curățat (majuscule).
    """
    # Verificam daca baza e buna
    if baza not in (2, 8, 10, 16):
        raise ValueError(f"Baza {baza} nu este suportată. Trebuie să fie 2, 8, 10 sau 16.")
    
    # Scoatem spatiile si facem mare
    text = text.strip().upper()
    if not text:
        raise ValueError("Input gol.")

    # Verificare caractere valide
    caractere_valide = set(CIFRE[:baza])
    caractere_valide.add('.')
    caractere_valide.add('-')
    
    for char in text:
        if char not in caractere_valide:
            raise ValueError(f"Caracter invalid '{char}' pentru baza {baza}.")

    # Verificare semn
    if text.count('-') > 1:
        raise ValueError("Nu sunt permise mai multe semne.")
    if '-' in text and text.index('-') != 0:
        raise ValueError("Semnul trebuie să fie la început.")

    # Verificare separator
    if text.count('.') > 1:
        raise ValueError("Nu sunt permiși mai mulți separatori fracționari.")

    return text

def citeste_input(text, baza):
    """
    Parsează șirul de intrare în componente (semn, string_intreg, string_fractionar).
    """
    # Validam intai
    text = verifica_input(text, baza)
    
    semn = 1
    # Verificam daca e negativ
    if text.startswith('-'):
        semn = -1
        text = text[1:]
        
    if '.' in text:
        sir_intreg, sir_frac = text.split('.')
    else:
        sir_intreg = text
        sir_frac = ""
        
    # Returnam partile gasite
    return semn, sir_intreg, sir_frac

def char_to_val(char):
    if char not in DictionarValori:
        raise ValueError(f"Caracter cifră invalid: {char}")
    return DictionarValori[char]

def val_to_char(val):
    if 0 <= val < len(CIFRE):
        return CIFRE[val]
    raise ValueError(f"Valoarea {val} în afara intervalului pentru caracter cifră.")