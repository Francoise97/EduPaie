# FAQ - EduPaie

## Comment ajouter un nouvel eleve ?

Onglet **Eleves** > bouton **+ Nouvel eleve** > remplir le formulaire.

## Comment enregistrer un paiement ?

Selectionner un eleve > bouton **Enregistrer un paiement** > saisir le montant.

## Que se passe-t-il si je saisis un montant trop eleve ?

L'application refuse le paiement et affiche un message d'erreur.

## Ou sont sauvegardes les PDF des recus ?

Dans le dossier **recus/** a la racine du projet.

## Comment modifier le nom de l'ecole sur les recus ?

Modifier le fichier **src/config.py** (variable `ECOLE_NOM`).

## Comment sauvegarder les donnees ?

Copier le fichier **data/edupaie.db** regulierement.

## Comment faire une sauvegarde de securite ?

git add .
git commit -m "Sauvegarde avant modification"
