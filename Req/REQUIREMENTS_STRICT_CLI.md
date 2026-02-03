# STRICT REQUIREMENTS -- Numeric Base Converter (Python, CLI)

## 0. Contract de conformitate (OBLIGATORIU)

Acest document reprezintă un contract strict. Orice abatere de la
cerințe (chiar dacă produce rezultate corecte) este considerată EȘEC al
implementării.

Agentul AI trebuie să respecte LITERAL toate cerințele de mai jos.

------------------------------------------------------------------------

## 1. Scop

Implementarea unui convertor numeric **CLI (Command Line Interface)**
între bazele: - 2 (binar) - 8 (octal) - 10 (zecimal) - 16 (hexazecimal)

cu suport complet pentru: - numere pozitive - numere negative - numere
cu parte fracționară finită - reprezentare semn + modul - reprezentare
în complement (Radix și Diminished Radix) pentru toate bazele suportate

------------------------------------------------------------------------

## 2. Interfață utilizator (CLI) -- OBLIGATORIU

### 2.1 Modalitate de input

Aplicația trebuie să citească datele **exclusiv de la tastatură**,
folosind un loop principal de comenzi.

Comenzi disponibile în meniul principal:
1. `[număr]` - Intră în **Modul Conversie Standard**. Utilizatorul introduce numărul, apoi i se cer interactiv baza sursă și baza destinație.
2. `math` - Intră în **Modul Aritmetică în Baze**.
3. `vir_mob` - Intră în **Modul Convertor IEEE 754**.
4. `test` - Rulează suita de teste obligatorii.
5. `exit` - Închide aplicația.

### 2.2 Input Conversie Standard
Dacă utilizatorul introduce un număr (care nu este o comandă), fluxul este:
1. Se detectează input-ul ca fiind numărul de convertit.
2. Se cere **baza sursă** (2, 8, 10 sau 16).
3. Se cere **baza destinație** (2, 8, 10 sau 16).
4. Se afișează rezultatul.
5. (Workflow Integrat) Se oferă opțiunea de calculare a complementului (dacă e întreg).

### 2.3 Modul Verbose (Show Your Work)
- Aplicația trebuie să suporte flag-ul `--v` introdus împreună cu comanda sau numărul (ex: `math --v` sau `101 --v`).
- Când este activat, programul trebuie să afișeze toți pașii matematici:
    - Descompunerea polinomială pentru conversia în baza 10.
    - Împărțirile succesive pentru partea întreagă în baza destinație.
    - Înmulțirile succesive pentru partea fracționară în baza destinație.
    - Detaliile calculelor aritmetice (transport, împrumut etc.) în modul math.

------------------------------------------------------------------------

## 3. Interdicții absolute (CRITICE)

Este STRICT INTERZISĂ folosirea: - int(x, base) - float(), double,
Decimal, Fraction - bin(), oct(), hex() - eval(), ast - orice librărie
externă - orice conversie indirectă mascată prin Python - orice operație
care delegă conversia limbajului

⚠ Orice apariție a acestor mecanisme = implementare INVALIDĂ.

------------------------------------------------------------------------

## 4. Reprezentare internă obligatorie

Orice număr trebuie reprezentat intern exclusiv prin: - semn: +1 sau
-1 - parte întreagă: int (baza 10) - parte fracționară: fracție
rațională EXACTĂ: - numărător (int) - numitor = putere a bazei

Este interzisă orice formă de aproximare internă.

------------------------------------------------------------------------

## 5. Arhitectura conversiei (NEMODIFICABILĂ)

Orice conversie trebuie să urmeze EXCLUSIV schema:

baza_sursă → baza 10 → baza_destinație

Conversiile directe între baze sunt STRICT INTERZISE (cu excepția operațiilor aritmetice "math" în aceeași bază).

------------------------------------------------------------------------

## 6. Conversie bază b → bază 10

### 6.1 Parte întreagă

Se va folosi EXCLUSIV formula matematică: Σ aᵢ · bⁱ

### 6.2 Parte fracționară

Se va folosi EXCLUSIV formula: Σ a₋ᵢ · b⁻ⁱ

Fracția se va păstra exact, fără rotunjiri.

------------------------------------------------------------------------

## 7. Conversie bază 10 → bază b

### 7.1 Parte întreagă

-   împărțiri succesive la baza b

### 7.2 Parte fracționară

-   înmulțiri succesive cu baza b
-   **OBLIGATORIU:** Detecția perioadei (fracții infinite periodice).
    - Se monitorizează resturile. Dacă un rest se repetă, se marchează începutul și sfârșitul perioadei.
    - Format output: `0.12(45)` unde `45` este perioada.
    - Dacă nu există perioadă în limita a N iterații, se trunchiază (dar se specifică acest lucru).

------------------------------------------------------------------------

## 8. Numere negative

-   semnul se separă strict de modul
-   conversia se aplică DOAR pe modul
-   semnul se reaplică la final

------------------------------------------------------------------------

## 9. Complemente (Generalizat)

### 9.1 Domeniu
-   doar pentru numere întregi
-   disponibil pentru toate bazele (2, 8, 10, 16)
-   fracțiile sunt STRICT INTERZISE în complement

### 9.2 Tipuri suportate
1.  **Complementul Restrâns (Diminished Radix - $C_{b-1}$)**
    -   Ex: C1 (baza 2), C7 (baza 8), C9 (baza 10), C15 (baza 16)
2.  **Complementul față de Bază (Radix Complement - $C_b$)**
    -   Ex: C2 (baza 2), C8 (baza 8), C10 (baza 10), C16 (baza 16)

### 9.3 Algoritm obligatoriu
1.  **Fixare lungime:** Utilizatorul specifică numărul de cifre/biți ($N$).
    - **Automatizare:** Aplicația trebuie să sugereze automat cel mai mic standard de biți (8, 16, 32, 64) care poate cuprinde valoarea absolută a numărului.
    - Dacă utilizatorul apasă Enter fără a introduce o valoare, se va folosi sugestia automată (Default).
2.  **Obținere magnitudine:** Se convertește valoarea absolută a numărului în baza țintă.
3.  **Padding:** Se completează cu 0 la stânga până la lungimea $N$.
4.  **Inversare ($C_{b-1}$):** Fiecare cifră $d$ devine $(base - 1) - d$.
5.  **Ajustare ($C_b$):** Dacă se cere complementul față de bază, se adună 1 la rezultatul pasului 4 (ignoring overflow peste $N$ cifre).

------------------------------------------------------------------------

## 10. Validare input (OBLIGATORIE)

-   caractere valide pentru baza specificată
-   un singur semn minus
-   un singur separator fracționar
-   mesaje de eroare clare în CLI
-   aplicația NU trebuie să se închidă brusc la input invalid

------------------------------------------------------------------------

## 11. Output

-   afișare exclusiv în CLI
-   fără spații inutile
-   litere A--F pentru hexazecimal
-   semn explicit pentru negative
-   fără normalizări ascunse

------------------------------------------------------------------------

## 12. Flux de lucru Integrat (Workflow)

- După orice conversie standard sau operație aritmetică (`math`), dacă rezultatul este un număr întreg, aplicația **trebuie** să întrebe automat utilizatorul dacă dorește calcularea complementului (C sau C-1).
- Această tranziție trebuie să fie fluidă, fără a cere reintroducerea manuală a rezultatului obținut anterior.

------------------------------------------------------------------------

## 13. Convenții de Cod (Stil "Începător")

- Structura internă trebuie să folosească Programarea Orientată pe Obiecte (OOP) într-un stil accesibil (ex: clase cu nume intuitive în Română).
- Variabilele interne și denumirile atributelor trebuie să folosească o terminologie mixtă sau preponderent în Română (ex: `p_intreaga`, `numarator`, `semn`).
- Se vor folosi comentarii explicative pentru pașii principali.
- Se acceptă utilizarea `f-strings` și `list comprehensions`.

------------------------------------------------------------------------

## 14. Teste MINIME obligatorii

-   -101.101 (baza 2) → -5.625 (baza 10)
-   -13.625 (baza 10) → -1101.101 (baza 2)
-   AF.3 (baza 16) → 175.1875 (baza 10)
-   -5 (baza 10) → 11111011 (binar, 8 biți, complement)
-   Rulează prin comanda `test`.

------------------------------------------------------------------------

## 15. Structură impusă

Codul trebuie să conțină module distincte pentru:
- `cli.py`: interfață și loop principal
- `parser.py`: parsing și structuri de date
- `core.py`: algoritmi de conversie (b → 10 și 10 → b)
- `complement.py`: logică complemente
- `arithmetic.py`: logică aritmetică generală
- `direct_math.py`: algoritmi aritmetici direcți (bază la bază)
- `vir_mob.py`: logică IEEE 754

------------------------------------------------------------------------

## 16. Virgulă Mobilă (IEEE 754 - Single Precision)

-   Accesibil prin comanda `vir_mob`.
-   **Codificare:** Conversie manuală din număr real în reprezentare pe 32 biți.
-   **Decodificare:** Conversie manuală din reprezentare IEEE 754 (Binar, Hex, Octal) în valoare Zecimală.
-   **Structură:** 1 bit Semn | 8 biți Exponent (Exces 127) | 23 biți Mantisă.
-   **Interdicții:** Nu se vor folosi funcții de sistem pentru împachetare biți (struct.pack) sau conversii automate de tip float. Totul se calculează matematic.
-   **Output (Codificare):** Binar (32 biți), Hexazecimal și Octal (cu padding corespunzător).

------------------------------------------------------------------------

## 17. Aritmetică în Baze

-   Accesibil prin comanda `math`.
-   Suport pentru Adunare (+), Scădere (-), Înmulțire (*) și Împărțire (/).
-   **Mod Mixt:** Dacă operanzii sunt în baze diferite, calculul se face prin reprezentarea internă (baza 10).
-   **Mod Direct (Aceeași Bază):** Dacă operanzii și baza rezultat sunt identice (ex: Baza 2 + Baza 2 -> Baza 2), operațiile se vor efectua **DIRECT** în baza respectivă, folosind algoritmi specifici (adunare cu transport, scădere cu împrumut etc.), fără conversie intermediară a numerelor întregi în baza 10.
-   Rezultatul final poate fi convertit ulterior dacă utilizatorul cere o bază diferită de cea a operanzilor.

Implementarea este ACCEPTATĂ doar dacă: - respectă toate interdicțiile -
produce rezultate exacte - nu folosește nicio funcție interzisă -
folosește exclusiv input CLI - urmează arhitectura impusă

Orice abatere = RESPINS.