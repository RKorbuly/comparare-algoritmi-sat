# Descriere

Programul generează un set de formule FNC (Formă normală conjunctivă) de dimensiuni configurabile, apoi rulează fiecare dintre cele trei algoritmi de satisfiabilitate pe fiecare formulă și măsoară timpii de execuție.

- **resolution_sat**: aplică metoda bazată pe rezoluție până când găsește un contradicție sau ajunge la stabilitate.
- **dp_sat**: implementare a algoritmului Davis–Putnam prin eliminarea recursivă a variabilelor.
- **dpll_sat**: implementarea algoritmului DPLL cu propagare unitară și literal pur.

De asemenea, programul include:
- Generarea aleatorie de formule FNC (`gen_random_cnf`).
- Afișarea unui tabel comparativ al timpii de execuție pentru fiecare instanță.
# Utilizare
Introduceți, la prompt:

- Number of samples: numărul de instanțe CNF care vor fi generate și testate.

- Number of variables: numărul de variabile per formulă.

- Number of clauses: numărul de clauze per formulă.
