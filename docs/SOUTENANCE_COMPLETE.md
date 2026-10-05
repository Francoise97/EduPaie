# Soutenance - EduPaie

> Document complet de preparation pour la soutenance orale
> Duree cible : 12-15 minutes
> Auteur : Francoise97

---

# SOMMAIRE

1. Presentation orale (12 slides)
2. Demonstration live (5 minutes)
3. Questions / Reponses (10 questions)
4. Check-list avant la soutenance

---

# PARTIE 1 - PRESENTATION ORALE

## SLIDE 1 - Page de titre

**Contenu :**
- Titre : EduPaie
- Sous-titre : Gestion des paiements scolaires
- Auteur : Francoise97
- Certification : Developpeur web et web mobile (2018)
- Date : Octobre 2026

**A dire :**
"Bonjour a tous. Je m'appelle Francoise et je vais vous presenter EduPaie,
une application desktop de gestion des paiements scolaires. Cette presentation
durera environ 12 minutes, suivie d'une demonstration et de vos questions."

---

## SLIDE 2 - Contexte

**Contenu :**

PROBLEME ACTUEL :
- Suivi manuel (cahier, Excel)
- Aucune vue fiable sur qui a paye quoi
- Recus non numerotes
- Litiges impossibles a resoudre
- Pertes financieres

ENJEU :
- Automatiser pour une secretaire NON TECHNIQUE

**A dire :**
"Dans la plupart des ecoles, les paiements sont encore suivis a la main,
sur des cahiers ou des fichiers Excel. Resultat : impossible de savoir qui
a paye quoi, les recus ne sont pas numerotes, et en cas de litige, on ne peut
rien prouver. Le probleme n'est pas technique, il est organisationnel.
Mon objectif est donc d'automatiser tout ca pour une secretaire qui n'a
aucune connaissance technique."

---

## SLIDE 3 - Mission

**Contenu :**

Automatiser la gestion des paiements scolaires

- Enregistrer les eleves et leurs frais
- Enregistrer chaque paiement avec validation
- Calculer automatiquement le solde restant
- Generer un recu PDF numerote unique
- Offrir une interface simple et intuitive

Une secretaire doit pouvoir l'utiliser en moins d'une heure.

**A dire :**
"Ma mission est claire : automatiser tout le processus. Enregistrer les eleves,
valider chaque paiement, calculer automatiquement le solde, generer un recu
numerote, et tout ca avec une interface simple qu'une secretaire peut
maitriser en moins d'une heure."

---

## SLIDE 4 - Les 6 ecrans

**Contenu :**

1. DASHBOARD - Stats temps reel
2. ELEVES - CRUD + Filtres
3. FICHE ELEVE - Historique
4. PAIEMENT - Validation
5. RECUS - Liste + PDF
6. PARAMETRES - Config

**A dire :**
"L'application se compose de 6 ecrans. Le tableau de bord pour la vue
d'ensemble, la liste des eleves pour la gestion, la fiche eleve avec son
historique, le dialogue d'enregistrement des paiements, la liste des recus,
et les parametres. Chaque ecran repond a un besoin precis."

---

## SLIDE 5 - Apercu du tableau de bord

**Contenu :**

4 cartes :
- ELEVES : 18
- TOTAL ENCAISSE : 3 450 000 FCFA
- RESTANT DU : 1 175 000 FCFA
- NON SOLDES : 8

Repartition :
- Soldes    : XXXXXXXXXXXX......  10 (55%)
- Partiels  : XXXXXX............   6 (33%)
- Non payes : XX................   2 (12%)

**A dire :**
"Voici le tableau de bord. On voit en un coup d'oeil les 18 eleves,
le total encaisse, le restant du, et la repartition par statut avec
des barres colorees."

---

## SLIDE 6 - Apercu de la liste des eleves

**Contenu :**

Barre de recherche + Filtres (Classe, Statut)
Bouton "+ Nouvel eleve"

Tableau :
| ID | Nom | Prenom | Classe | Du | Paye | Statut |
|----|-----|--------|--------|-----|------|--------|
| 1  | DIALLO | Amadou | 6eme A | 250000 | 250000 | Solde |
| 2  | SOW | Fatou | 5eme B | 300000 | 300000 | Solde |
| 3  | BA | Ousmane | 4eme A | 200000 | 0 | Non paye |
| 4  | NDIAYE | Aissatou | 6eme A | 250000 | 100000 | Partiel |
| 5  | FALL | Ibrahima | 5eme B | 300000 | 300000 | Solde |

Boutons : Voir fiche / Enregistrer paiement / Modifier

**A dire :**
"La liste des eleves avec recherche instantanee, filtres par classe et par
statut. Les statuts sont colores : vert pour solde, orange pour partiel,
rouge pour non paye."

---

## SLIDE 7 - Apercu de la fiche eleve

**Contenu :**

Fiche de FALL Ibrahima

Infos :
- Nom : FALL
- Prenom : Ibrahima
- Classe : 5eme B
- Annee scolaire : 2026-2027
- Parent : M. Fall Cheikh

Situation financiere :
- Total du : 300 000 FCFA
- Total paye : 300 000 FCFA
- Solde restant : 0 FCFA
- Statut : Solde

Historique :
- REC-2025-007 | 22/11/24 | 100 000 | Virement

**A dire :**
"La fiche eleve regroupe toutes les infos : situation financiere et
historique complet des paiements."

---

## SLIDE 8 - Apercu du dialogue de paiement

**Contenu :**

Dialogue "Enregistrer un paiement" :

Info eleve :
- Eleve : FALL Ibrahima (5eme B)
- Total du : 300 000 FCFA
- Deja paye : 300 000 FCFA
- Solde restant : 0 FCFA

Formulaire :
- Montant * : [ 50 000 ] FCFA
- Date * : [ 05/10/2026 ]
- Mode * : [ Especes v ]
- Reference : [ CHQ-12345 ]

Apercu : "Nouveau solde apres paiement : 250 000 FCFA"

Boutons : [Annuler] [Enregistrer + Recu]

**A dire :**
"Le dialogue de paiement affiche le solde restant et calcule en temps reel
le nouveau solde. Si je saisis un montant trop eleve, l'app refuse."

---

## SLIDE 9 - Apercu du recu PDF

**Contenu :**

En-tete bleu : ECOLE MA VICTOIRE
              Lome, Togo

Titre : RECU DE PAIEMENT
        N REC-2026-005

Recu de : FALL Ibrahima
Classe  : 5eme B
Annee   : 2026-2027

Montant paye : 50 000 FCFA
Mode         : Especes
Date         : 05/10/2026

Total du      : 300 000 FCFA
Total paye    : 250 000 FCFA
Solde restant : 50 000 FCFA

Signatures :
La Secretaire          L'Etablissement
___________            ___________

**A dire :**
"Chaque paiement genere un recu PDF numerote, avec le nom de l'ecole,
les infos de l'eleve, le montant, et le solde restant apres paiement."

---

## SLIDE 10 - Architecture en 3 couches

**Contenu :**

Couche 1 : INTERFACE (PySide6)
           widgets / dialogs / main_window.py

Couche 2 : METIER (Services)
           Validation / Calcul solde / Numerotation / PDF

Couche 3 : DONNEES (Repositories)
           SQL encapsule / SQLite / Transactions

REGLE D'OR : Aucun widget n'execute de SQL directement

**A dire :**
"J'ai applique une architecture en 3 couches strictes : l'interface ne fait
aucun SQL, la logique metier est isolee, et l'acces aux donnees est encapsule.
C'est la regle d'or de mon projet."

---

## SLIDE 11 - Base de donnees

**Contenu :**

3 tables :

Table ELEVE :
- id (PK)
- nom, prenom
- classe
- frais_totaux

Table PAIEMENT :
- id (PK)
- eleve_id (FK)
- recu_id (FK)
- montant
- annule (0/1)

Table RECU :
- id (PK)
- numero_unique
- montant_paye
- solde_apres

Contraintes : CHECK, UNIQUE, FOREIGN KEY
Vue SQL : vue_solde_eleve (calcul automatique)

**A dire :**
"Trois tables : eleve, paiement, recu. Une vue SQL calcule automatiquement
le solde. Les contraintes garantissent l'integrite : CHECK, UNIQUE,
FOREIGN KEY."

---

## SLIDE 12 - Conclusion

**Contenu :**

6 FONCTIONNALITES DEMANDEES :
- Gestion eleves
- Paiements
- Solde auto
- Historique
- Recus PDF
- Tableau de bord

BONUS (Version PRO) :
- Annulation avec tracabilite
- Interface modernisee
- 92 commits Git
- Documentation complete

STATISTIQUES :
- 92 commits
- 15+ branches
- ~3000 lignes de code
- 25+ fichiers de documentation

Merci de votre attention. Des questions ?

**A dire :**
"Voila. J'ai livre les 6 fonctionnalites demandees, plus une Version PRO
avec tracabilite. Le projet compte 92 commits Git et une documentation
complete. Merci de votre attention. Je suis maintenant pret a repondre
a vos questions, et je peux aussi faire une demonstration en direct si
vous le souhaitez."

---

# PARTIE 2 - DEMONSTRATION LIVE (5 minutes)

## Ordre a suivre

1. Tableau de bord - 30 s
2. Recherche eleve "diallo" - 20 s
3. Fiche eleve avec historique - 30 s
4. Enregistrer un paiement (10 000 FCFA) - 1 min
5. Voir le recu PDF - 1 min
6. Annuler un paiement (Version PRO) - 1 min
7. Parametres (ECOLE MA VICTOIRE) - 30 s

## Points cles a montrer

- La recherche est instantanee
- Les statuts sont colores
- Le solde se recalcule automatiquement
- Le PDF contient toutes les infos
- L'annulation conserve l'historique

---

# PARTIE 3 - QUESTIONS / REPONSES

## Q1 : Pourquoi avoir choisi SQLite ?

SQLite est parfait pour une application mono-poste. Pas de serveur a installer,
un fichier unique portable, et le module sqlite3 est natif en Python.

## Q2 : Expliquez votre architecture.

3 couches : Interface (PySide6), Metier (Services), Donnees (Repositories).
Aucun widget n'execute de SQL. C'est la regle d'or.

## Q3 : Comment empechez-vous un paiement de depasser le solde ?

Double validation : cote interface ET cote service. Le service
PaiementService.enregistrer() refuse tout montant superieur au solde restant.

## Q4 : Comment fonctionne l'annulation ?

C'est un soft delete. On ne supprime pas le paiement, on le marque
annule = 1 avec une raison et une date. Le solde est recalcule
automatiquement par la vue SQL.

## Q5 : Comment garantissez-vous l'unicite des numeros de recu ?

Contrainte SQL UNIQUE(annee, sequence). La sequence est calculee dans
une transaction. Impossible d'avoir deux fois REC-2026-001.

## Q6 : Combien de temps avez-vous mis ?

Environ 40 heures de developpement sur 10 jours.

## Q7 : Quelles sont les limites ?

3 limites : mono-poste (pas de reseau), pas d'authentification, pas d'export
Excel. Ce sont les priorites de la roadmap v1.1.

## Q8 : Comment testez-vous l'application ?

Deux niveaux : tests unitaires (formatters, validators) et tests
d'integration (services, repositories). J'ai 8 fichiers de tests.

## Q9 : Pourquoi ces couleurs ?

Bleu #1E3A8A pour la confiance et le serieux. Vert pour le succes, orange
pour l'alerte, rouge pour le danger.

## Q10 : Si vous recommenciez ?

J'ajouterais une authentification multi-utilisateurs des le depart,
et j'utiliserais SQLAlchemy (ORM) au lieu de SQL brut pour la maintenabilite.

---

# PARTIE 4 - CHECK-LIST AVANT LA SOUTENANCE

## Materiel

- [ ] PC charge a 100%
- [ ] Tous les programmes fermes
- [ ] Cle USB de secours (exe + data + slides)
- [ ] Bouteille d'eau

## Application

- [ ] Exe teste
- [ ] Base a jour
- [ ] Raccourci fonctionne
- [ ] Version PRO testee

## Documentation

- [ ] Guide de soutenance imprime
- [ ] Slides ouvertes
- [ ] Schema BDD imprime
- [ ] Guide Q/R imprime

## Mental

- [ ] Respiration profonde
- [ ] Sourire
- [ ] Confiance en soi

---

# LES 3 MESSAGES CLES

## 1. Probleme reel

"Les ecoles gerent encore les paiements a la main (cahier, Excel),
sans tracabilite."

## 2. Architecture propre

"J'ai concu une architecture en 3 couches : Interface, Metier, Donnees.
Aucun widget n'execute de SQL directement."

## 3. Solution pro

"Chaque paiement genere un recu PDF numerote. Les transactions sont
atomiques (recu + paiement ensemble). Et la Version PRO permet d'annuler
un paiement en conservant l'historique."

---

# EN CAS DE BUG PENDANT LA DEMO

1. Reste calme
2. Dis : "Je vais relancer l'application"
3. Relance l'app
4. Si ca plante encore : "Passons a la slide suivante"

N'aie pas peur - le jury veut voir que tu maitrises ton sujet,
pas que tout soit parfait.

---

FIN DU DOCUMENT

Bonne chance pour ta soutenance !