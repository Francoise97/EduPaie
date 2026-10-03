# Manuel utilisateur - EduPaie

## 1. Lancer l'application

Double-cliquez sur EduPaie.exe (ou lancez `python main.py` en developpement).

La fenetre principale s'ouvre sur le Tableau de bord.

## 2. Enregistrer un nouvel eleve

1. Cliquez sur Eleves dans la barre laterale
2. Cliquez sur le bouton vert "+ Nouvel eleve"
3. Remplissez le formulaire :
   - Nom et prenom (obligatoires)
   - Classe (obligatoire)
   - Annee scolaire (obligatoire)
   - Frais totaux (montant du)
   - Telephone et parent (optionnels)
4. Cliquez sur Enregistrer

L'eleve apparait avec le statut "Non paye".

## 3. Enregistrer un paiement

Depuis la liste des eleves :

1. Selectionnez un eleve dans le tableau
2. Cliquez sur "Enregistrer un paiement"
3. Dans le dialogue :
   - Saisissez le montant (le solde restant s'affiche en haut)
   - Verifiez la date (par defaut : aujourd'hui)
   - Choisissez le mode (Especes, Cheque, Virement, Mobile Money)
   - Ajoutez une reference si besoin
4. L'apercu du nouveau solde s'affiche en bas
5. Cliquez sur "Enregistrer + Recu"

Un message confirme l'enregistrement avec le numero de recu.

Note : le montant saisi ne peut pas depasser le solde restant.

## 4. Consulter la fiche d'un eleve

1. Onglet Eleves
2. Selectionnez un eleve
3. Cliquez sur "Voir la fiche et historique" (ou double-cliquez)

Vous voyez :
- Informations personnelles
- Situation financiere (du / paye / solde restant)
- Historique des paiements avec le numero de recu

## 5. Imprimer / voir un recu

Depuis la fiche eleve :

1. Double-cliquez sur une ligne de l'historique
2. Le dialogue "Recu de paiement" s'ouvre
3. Cliquez sur "Ouvrir le PDF" pour afficher le recu

Depuis l'ecran Paiements :

1. Onglet Paiements
2. Double-cliquez sur n'importe quel paiement

Le PDF est enregistre dans le dossier recus/ au format REC-AAAA-NNN.pdf.

## 6. Tableau de bord

Affiche en temps reel :
- Nombre total d'eleves
- Total encaisse
- Restant du
- Nombre d'eleves non soldes
- Repartition par statut
- Derniers paiements

## 7. Conseils

- Sauvegardez regulierement data/edupaie.db
- Les recus PDF sont dans recus/
- En cas d'erreur, verifiez que l'eleve est selectionne
