# Guide de securite - EduPaie

## Principes

1. Validation en profondeur
2. Transactions atomiques
3. Contraintes SQL
4. Aucune donnee sensible

## Validation en profondeur

### Couche interface
- Champs obligatoires
- Format numerique
- Date valide

### Couche service
- Re-validation complete
- Regles metier
- Verification du solde

### Couche donnees
- Contraintes CHECK
- Contraintes UNIQUE
- Contraintes FOREIGN KEY

## Transactions

Toute operation critique utilise :
    conn.execute("BEGIN")
    try:
        # operations
        conn.commit()
    except:
        conn.rollback()

## Mots de passe

Aucun mot de passe n'est stocke (pas d'authentification).

## Sauvegarde

- Fichier unique : data/edupaie.db
- Copie de sauvegarde : scripts/backup.sh

## Risques connus

1. Pas de chiffrement de la base
2. Pas d'authentification
3. Mono-utilisateur
