# Documentation technique - EduPaie

## Technologies

| Composant | Technologie | Version |
|-----------|-------------|---------|
| Langage | Python | 3.10+ |
| Interface | PySide6 | 6.7+ |
| Base de donnees | SQLite | 3.x |
| PDF | reportlab | 4.0+ |
| Packaging | PyInstaller | 6.0+ |

## Architecture

Architecture en 3 couches :

1. Couche presentation (src/ui/)
2. Couche metier (src/services/)
3. Couche donnees (src/repositories/)

## Flux d'une requete

Utilisateur -> Widget -> Service -> Repository -> BDD
                                        <- Resultat <- 

## Securite

- Validation en profondeur
- Transactions atomiques (BEGIN/COMMIT/ROLLBACK)
- Contraintes SQL (CHECK, UNIQUE, FOREIGN KEY)

## Performance

- Index sur les colonnes filtrees
- Vue SQL pour les calculs complexes
- Pagination pour les grandes listes

## Tests

- Tests unitaires (formatters, validators)
- Tests d'integration (services, repositories)
- Couverture cible : 60%+

## Deploiement

- Creation d'un exe autonome avec PyInstaller
- Distribution via cle USB ou archive ZIP
- Aucune installation requise

## Maintenance

- Sauvegarde de data/edupaie.db
- Logs dans logs/annulations.log
- Rollback via git reset --hard
