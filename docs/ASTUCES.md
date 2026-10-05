# Astuces et raccourcis - EduPaie

## Raccourcis clavier

### Application

| Raccourci | Action |
|-----------|--------|
| Ctrl + Q | Quitter |
| Ctrl + N | Nouvel eleve |
| Ctrl + P | Nouveau paiement |
| Ctrl + F | Rechercher |
| F5 | Rafraichir |

### VSCode (developpement)

| Raccourci | Action |
|-----------|--------|
| Ctrl + P | Ouvrir fichier |
| Ctrl + Shift + E | Explorateur |
| Ctrl + Shift + G | Git |
| Ctrl + ù | Terminal |
| Ctrl + S | Sauvegarder |
| Shift + Alt + F | Formater |

## Astuces utilisateur

### 1. Recherche rapide

Tapez les 3 premieres lettres du nom dans la barre de recherche.

### 2. Filtres combines

Vous pouvez combiner :
- Filtre par classe
- Filtre par statut
- Recherche par nom

### 3. Verifier un solde

1. Allez sur la fiche de l'eleve
2. Le solde restant est en rouge

### 4. Annuler un paiement

1. Selectionnez le paiement
2. Cliquez sur "Annuler le paiement"
3. Choisissez la raison

### 5. Generer un recu

1. Allez dans l'onglet Recus
2. Selectionnez le recu
3. Cliquez sur "Voir le recu"
4. Cliquez sur "Generer PDF"

## Astuces developpeur

### Debug

    import pdb; pdb.set_trace()

### Verifier la base

    python -c "import sqlite3; c=sqlite3.connect('data/edupaie.db'); print(c.execute('SELECT COUNT(*) FROM eleve').fetchone())"

### Reinitialiser la base

    python -m src.database.seed_runner
