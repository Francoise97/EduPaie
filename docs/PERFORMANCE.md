# Performance - EduPaie

## Mesures actuelles

### Temps de lancement

- Demarrage : 2-5 secondes
- Chargement des donnees : < 1 seconde

### Operations

| Operation | Temps |
|-----------|-------|
| Ajout d'un eleve | < 100 ms |
| Enregistrement d'un paiement | < 200 ms |
| Generation PDF | < 500 ms |
| Annulation | < 100 ms |

### Capacite

- 1000 eleves : OK
- 10000 paiements : OK
- 100000 paiements : Ralentissement possible

## Optimisations

### Index

- idx_eleve_classe
- idx_eleve_annee
- idx_recu_eleve
- idx_paiement_eleve
- idx_paiement_date
- idx_paiement_annule

### Vue SQL

Utilisation de vue_solde_eleve pour les calculs.

### Requetes

- Requetes preparees (parametres)
- Pas de SELECT *
- Limitation des resultats

## Limites

- Mono-poste
- Pas de cache
- SQLite (pas de PostgreSQL)

## Ameliorations possibles

- Cache memoire
- Pagination
- Migration vers PostgreSQL
