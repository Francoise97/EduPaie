# Guide des cas d'usage - EduPaie

## Cas d'usage 1 : Inscription d'un nouvel eleve

Acteur : Secretaire
Precondition : L'application est lancee

1. La secretaire clique sur "Nouvel eleve"
2. Elle saisit les informations (nom, prenom, classe, frais)
3. Elle valide le formulaire
4. L'eleve apparait dans la liste avec le statut "Non paye"

Postcondition : L'eleve est enregistre en base

## Cas d'usage 2 : Enregistrement d'un paiement

Acteur : Secretaire
Precondition : L'eleve existe dans le systeme

1. La secretaire selectionne l'eleve
2. Elle clique sur "Enregistrer un paiement"
3. Elle saisit le montant et le mode de paiement
4. Le systeme valide le montant (<= solde restant)
5. Le systeme genere un recu numerote
6. Le solde de l'eleve est recalcule

Postcondition : Le paiement est enregistre, le recu est genere

## Cas d'usage 3 : Annulation d'un paiement

Acteur : Secretaire
Precondition : Le paiement existe et est actif

1. La secretaire selectionne le paiement
2. Elle clique sur "Annuler le paiement"
3. Elle choisit la raison de l'annulation
4. Elle confirme l'annulation
5. Le systeme marque le paiement comme annule
6. Le solde de l'eleve est recalcule

Postcondition : Le paiement est marque annule, l'historique est conserve

## Cas d'usage 4 : Generation d'un recu PDF

Acteur : Secretaire
Precondition : Le paiement existe

1. La secretaire selectionne le paiement
2. Elle clique sur "Voir le recu"
3. Elle clique sur "Generer PDF"
4. Le systeme genere le PDF
5. Le PDF est ouvert

Postcondition : Le recu PDF est disponible

## Cas d'usage 5 : Consultation du tableau de bord

Acteur : Directeur
Precondition : L'application est lancee

1. Le directeur ouvre le tableau de bord
2. Il consulte les statistiques
3. Il peut identifier les eleves non soldes

Postcondition : Le directeur a une vue d'ensemble
