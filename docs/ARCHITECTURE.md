# Architecture - EduPaie

## Vue d'ensemble

EduPaie suit une architecture en 3 couches :

    +-----------------------------+
    |   INTERFACE (PySide6)       |
    |   widgets / dialogs         |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    |   METIER (Services)         |
    |   validation / calcul / PDF |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    |   DONNEES (Repositories)    |
    |   SQL encapsule / SQLite    |
    +-----------------------------+

## Regle d'or

Aucun widget n'execute de SQL directement.

## Flux d'un paiement

1. L'utilisateur clique "Enregistrer un paiement"
2. Le dialog PaiementDialog collecte les donnees
3. Le dialog appelle PaiementService.enregistrer()
4. Le service valide les donnees
5. Le service ouvre une transaction SQL
6. Le service cree le recu via RecuService
7. Le service cree le paiement via PaiementRepository
8. La transaction est commitee
9. L'interface se met a jour via un signal

## Avantages

- Testabilite : on peut tester la logique sans interface
- Maintenabilite : changer l'UI ne touche pas au metier
- Evolutivite : migrer vers PostgreSQL ne change que le repository
