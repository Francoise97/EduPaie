# Guide de soutenance - EduPaie

> Document de preparation pour la soutenance orale
> Duree cible : 12-15 minutes
> Auteur : Francoise97

---

# PARTIE 1 - PLAN DE SOUTENANCE

## Slide 1 - Titre (30 sec)

**Points cles a dire :**
- Se presenter : "Bonjour, je m'appelle [nom]"
- Nom du projet : EduPaie
- Description : "Application desktop pour gerer les paiements scolaires"
- Duree : "Je vais vous presenter mon projet en 12 minutes"

---

## Slide 2 - Contexte (1 min)

**Points cles :**
- Probleme reel : les ecoles utilisent cahier/Excel
- Consequences :
  - Pas de vue fiable sur qui a paye
  - Recus non numerotes
  - Litiges impossibles a resoudre
- Enjeu : automatiser pour une secretaire non technique

**Phrase cle :** "Le probleme n'est pas technique, il est organisationnel."

---

## Slide 3 - Mission (30 sec)

**Points cles :**
- Objectif : remplacer la gestion manuelle
- 5 missions :
  - Enregistrer eleves + paiements
  - Calculer solde automatiquement
  - Generer recu unique
  - Interface simple
  - Statut visuel (Solde/Partiel/Non paye)

---

## Slide 4 - Fonctionnalites (2 min)

**Les 6 ecrans :**
1. Tableau de bord -> stats temps reel
2. Eleves -> CRUD + recherche + filtres
3. Fiche eleve -> historique + situation
4. Paiements -> validation + recu
5. Recus -> liste + PDF
6. Parametres -> config centralisee

**Phrase cle :** "Chaque ecran repond a un besoin precis."

---

## Slide 5 - Architecture (1 min 30)

**3 couches :**
- Couche 1 - Interface (PySide6) : widgets, dialogs
- Couche 2 - Metier (Services) : validation, calcul, numerotation
- Couche 3 - Donnees (Repositories) : SQL encapsule

**Phrase cle :** "Aucun widget n'execute de SQL directement - c'est la regle d'or."

**Argument fort :** separation permet de tester la logique sans interface.

---

## Slide 6 - Base de donnees (1 min 30)

**3 tables + 1 vue :**
- eleve : nom, prenom, classe, frais_totaux
- recu : numero_unique (REC-2026-001), montant_paye, solde_apres
- paiement : montant, date, mode, reference, observation
- vue_solde_eleve : calcule automatiquement le solde et statut

**Contraintes importantes :**
- CHECK (montant > 0) - pas de montant negatif
- UNIQUE(annee, sequence) - pas de doublon de recu
- ON DELETE CASCADE - suppression propre

**Phrase cle :** "Les contraintes sont dans la base, pas seulement dans le code."

---

## Slide 7 - Regles metier (1 min)

**Points cles :**
- Formule : solde = frais_totaux - somme(paiements)
- Garde-fou : le solde ne peut JAMAIS etre negatif
- Numerotation : REC-{ANNEE}-{NUMERO:03d}
- Transaction atomique : recu + paiement crees ensemble (rollback si erreur)

**Phrase cle :** "Le recu et le paiement sont crees dans la meme transaction - soit tout reussit, soit tout est annule."

---

## Slide 8 - Choix techniques (1 min 30)

**SQLite :**
- Pas de serveur a installer
- Fichier unique portable
- Module sqlite3 natif Python

**PySide6 :**
- Framework Qt moderne
- Signaux/slots clairs
- Licence LGPL

**reportlab :**
- PDF professionnel
- Controle total de la mise en page

**Phrase cle :** "J'ai choisi la simplicite pour le deploiement."

---

## Slide 9 - DEMO LIVE (5 min)

**Plan de la demo (dans l'ordre) :**

1. Tableau de bord (30 sec)
   - "Vue d'ensemble : 18 eleves, 3.4M FCFA encaisses"

2. Liste eleves (30 sec)
   - Recherche "diallo" -> filtre instantane
   - Filtre "Non paye" -> affiche 3 eleves

3. Enregistrer un paiement (2 min)
   - Selectionner un eleve partiel
   - Montant : 50 000
   - Mode : Especes
   - Valider
   - "Le solde se met a jour instantanement"

4. Generer le PDF (1 min 30)
   - Onglet Recus -> selectionner le nouveau recu
   - "Voir le recu selectionne" -> "Generer PDF" -> "Ouvrir le PDF"
   - Montrer le PDF avec le logo ECOLE MA VICTOIRE

5. Fiche eleve (30 sec)
   - Historique avec colonne Observation

**Attention :** Si ca plante, reste calme, passe a la slide suivante.

---

## Slide 10 - Chiffres cles (30 sec)

**Points cles :**
- 26 commits Git
- 11 branches
- ~2500 lignes de code
- 6 ecrans
- 18 eleves en base
- 3 tests

**Phrase cle :** "Ce projet represente environ 40 heures de developpement."

---

## Slide 11 - Limites & evolutions (1 min)

**Limites (sois honnete) :**
- Mono-poste (pas de reseau)
- Pas d'authentification
- Pas d'export Excel

**Evolutions :**
- Multi-utilisateurs
- Synchronisation cloud
- Envoi recus par SMS

**Phrase cle :** "J'ai identifie ces limites - c'est ce que je ferais en V2."

---

## Slide 12 - Merci (30 sec)

- "Merci de votre attention"
- "Je suis pret a repondre a vos questions"

---

## RECAP - LE FIL ROUGE

**3 messages a faire passer :**
1. Probleme reel -> j'ai identifie un besoin concret
2. Architecture propre -> 3 couches, SQL encapsule
3. Solution pro -> recu PDF numerote, transaction atomique

**Si tu dis ces 3 choses, tu as gagne.**

---

## LES 5 ERREURS A EVITER

1. Ne pas savoir expliquer une ligne de code que tu montres
2. Dire "je ne sais pas" sans nuance (dis plutot "je vais verifier")
3. Rester bloque sur un bug en demo (passe a la suite)
4. Parler trop vite (respire)
5. Ne pas montrer la generation de PDF (c'est ton point fort)

---

## CONSEILS DE PRESENTATION

| Point | Conseil |
|---|---|
| Debit | Lent, articule |
| Regard | Alterne entre slides et jury |
| Mains | Stables, pas dans les poches |
| Erreur | Reste calme, continue |
| Chiffres | Cite-en 2-3 maximum |

---



---

# PARTIE 2 - QUESTIONS / REPONSES ANTICIPEES

## CATEGORIE 1 - Architecture

### Q1 : Expliquez-moi votre architecture en 3 couches

**Reponse :**
L'application est divisee en 3 couches distinctes :
- La couche Interface (PySide6) contient les widgets et dialogues - elle ne fait AUCUN SQL.
- La couche Metier (Services) contient la logique : validation, calcul du solde, numerotation des recus.
- La couche Donnees (Repositories) encapsule toutes les requetes SQL.

L'avantage : on peut tester la logique sans interface, et changer l'UI sans toucher au metier.

### Q2 : Pourquoi cette separation ?

**Reponse :** 3 raisons :
- Maintenabilite : si on change une regle metier, on ne touche qu'un seul fichier.
- Testabilite : on peut tester la logique sans lancer l'interface.
- Evolutivite : si on migre vers PostgreSQL, seul le repository change.

### Q3 : Comment communiquent vos couches ?

**Reponse :**
L'interface appelle les Services via des methodes. Les Services appellent les Repositories.
Les widgets communiquent entre eux via des signaux PySide6 (Signal, Slot).
Exemple : quand j'enregistre un paiement, la fiche eleve emet un signal paiement_enregistre qui rafraichit le tableau de bord.

### Q4 : Que se passe-t-il si la base est corrompue ?

**Reponse :**
La base SQLite est un fichier unique (data/edupaie.db). En cas de probleme :
- On peut la regenerer avec python -m src.database.seed_runner
- On peut la sauvegarder regulierement (elle fait 53 Ko)
- Les contraintes CHECK et UNIQUE empechent la corruption logique

---

## CATEGORIE 2 - Base de donnees

### Q5 : Montrez-moi votre MCD/MLD

**Reponse :**
J'ai 3 tables :
- eleve : id, nom, prenom, classe, annee_scolaire, frais_totaux
- recu : id, numero_unique, annee, sequence, eleve_id, montant_paye, solde_apres
- paiement : id, eleve_id, recu_id, montant, date_paiement, mode_paiement, reference, observation

Une vue SQL vue_solde_eleve calcule automatiquement le total paye, le solde restant et le statut.

### Q6 : Pourquoi une table recu separee de paiement ?

**Reponse :** Pour 2 raisons :
- Le recu est un document comptable qui a un numero unique (REC-2026-001).
- Le paiement est un mouvement financier rattache a un recu.

Cette separation permet de regenerer un recu a l'identique meme si le paiement est modifie.

### Q7 : Comment garantissez-vous l'unicite des numeros de recu ?

**Reponse :** Avec 2 mecanismes :
- Contrainte SQL UNIQUE(annee, sequence) - impossible d'avoir 2 fois REC-2026-001.
- La sequence est calculee dans une transaction : on lit le MAX, on incremente, on insere.
- De plus, numero_unique a une contrainte UNIQUE globale.

### Q8 : Que se passe-t-il si on supprime un eleve ?

**Reponse :**
Grace a ON DELETE CASCADE :
- Tous ses paiements sont supprimes.
- Tous ses recus sont supprimes.
- Les fichiers PDF associes restent dans recus/ (pas supprimes automatiquement).

C'est une decision de conception : on garde une trace des PDF meme si l'eleve est supprime.

---

## CATEGORIE 3 - Regles metier

### Q9 : Comment empechez-vous un paiement de depasser le solde ?

**Reponse :**
Dans PaiementService.enregistrer(), avant tout enregistrement :
- Je recupere le solde restant de l'eleve.
- Je compare le montant saisi au solde.
- Si le montant est superieur -> je retourne une erreur.

C'est une validation cote service, pas cote interface. Comme ca, meme un script qui appelle le service directement sera protege.

### Q10 : Que se passe-t-il si deux paiements sont enregistres en meme temps ?

**Reponse :**
L'application est mono-poste. Deux paiements simultanes sont impossibles dans la pratique.
MAIS : la transaction SQL protege contre les erreurs. Si un probleme survient entre la creation du recu et celle du paiement, un ROLLBACK annule tout.

### Q11 : Comment calculez-vous le statut d'un eleve ?

**Reponse :**
C'est fait automatiquement par la vue SQL vue_solde_eleve :
- Si total_paye = 0 -> Non paye
- Si total_paye >= frais_totaux -> Solde
- Sinon -> Partiellement paye

Aucune logique Python : tout est dans la base.

---

## CATEGORIE 4 - Interface

### Q12 : Comment gerez-vous les erreurs de saisie ?

**Reponse :** A 2 niveaux :
- Interface : champs obligatoires, montant numerique, date valide.
- Service : re-validation complete + regles metier (montant > solde, etc.).

Toute erreur affiche un QMessageBox explicite.

### Q13 : Pourquoi avoir choisi PySide6 et pas Tkinter ?

**Reponse :** 3 raisons :
- PySide6 est moderne (Qt 6, 2024).
- Il supporte QSS (feuilles de style) -> j'ai cree une charte graphique proche d'une app web.
- Il a un systeme de signaux/slots tres clair pour la communication entre widgets.

---

## CATEGORIE 5 - Recus PDF

### Q14 : Comment reimprimer un recu deja emis ?

**Reponse :**
Le PDF est stocke dans recus/ avec le nom REC-2026-001.pdf. On peut :
- Le rouvrir depuis l'app (onglet Recus -> Voir le recu).
- Le retrouver directement dans le dossier.

Si le PDF est supprime, il est regenere a l'identique depuis les donnees de la base (numero, montant, solde, date).

### Q15 : Le recu contient quelles informations ?

**Reponse :**
- En-tete : nom de l'ecole, adresse (config.py)
- Numero unique (REC-2026-XXX)
- Nom, prenom, classe, annee scolaire
- Montant paye, mode, date, reference
- Situation financiere : total du / paye / solde restant
- Deux zones de signature
- Date et heure de generation

---

## CATEGORIE 6 - Questions pieges

### Q16 : Pourquoi avoir mis la base dans Git ?

**Reponse :**
Bonne question. Le fichier data/edupaie.db est inclus dans Git pour 2 raisons :
- C'est un jeu de demonstration (18 eleves, 24 recus).
- Ca permet au jury de tester l'app immediatement apres un git clone.

En production, on ne versionnerait PAS la base - on la regenererait avec seed_runner.py.

### Q17 : Qu'est-ce qui n'est PAS dans votre projet ?

**Reponse :** 3 choses manquent volontairement :
- Authentification : pas de gestion multi-utilisateurs (pas necessaire pour un mono-poste).
- Export Excel : fonctionnalite bonus, pas obligatoire.
- Montant en lettres : le recu affiche uniquement le montant en chiffres.

Ces 3 points sont dans la slide Evolutions.

### Q18 : Comment savez-vous que votre code est de qualite ?

**Reponse :** 4 indicateurs :
- Separation stricte en couches (aucun SQL dans l'UI).
- 26 commits Git avec messages conventionnels (feat:, docs:...).
- Validation en profondeur (interface + service + base).
- Tests unitaires (tests/test_services.py, tests/test_repositories.py).

---

## CATEGORIE 7 - Questions finales

### Q19 : Combien de temps avez-vous mis ?

**Reponse :**
Environ 40 heures de developpement reparties sur ~10 jours :
- Jour 1-2 : modelisation + base de donnees
- Jour 3-4 : couche metier
- Jour 5-6 : interface PySide6
- Jour 7 : generation PDF
- Jour 8 : tests + documentation
- Jour 9-10 : packaging + soutenance

### Q20 : Si vous recommenciez, que feriez-vous differemment ?

**Reponse :** 3 choses :
- J'ajouterais une couche d'authentification des le depart.
- J'utiliserais SQLAlchemy (ORM) au lieu de SQL brut - plus maintenable.
- Je ferais plus de tests unitaires (aujourd'hui j'en ai 3).

---

## RECAP - 5 REGLES POUR LES QUESTIONS

| Regle | Exemple |
|---|---|
| Reformuler la question | "Si je comprends bien, vous me demandez..." |
| Structurer la reponse | "3 raisons. Premierement..." |
| Admettre si on ne sait pas | "Je n'ai pas implemente ca, mais voici comment je ferais..." |
| Ne pas bluffer | Mieux vaut dire "je ne sais pas" |
| Ne pas s'excuser | Pas de "desole, c'est nul" |



---

# PARTIE 3 - REPETITION GENERALE

## J-1 : LA VEILLE

### Preparation technique

- [ ] Verifier que l'app se lance : python main.py
- [ ] Verifier que l'exe fonctionne : dist/EduPaie.exe
- [ ] Verifier que les PDF se generent
- [ ] Fermer tous les autres programmes (Chrome, VSCode...)
- [ ] Charger le PC (batterie a 100%)
- [ ] Prevoir une prise secteur
- [ ] Tester le retroprojecteur (si presentiel)
- [ ] Avoir une cle USB de secours avec :
  - L'exe EduPaie
  - Le dossier dist/data/
  - Le PDF des slides

### Preparation orale

- [ ] Relire ce guide en entier
- [ ] Repeter les 20 questions a voix haute
- [ ] Chronometrer la presentation complete
- [ ] S'entrainer a la demo (3 fois minimum)

---

## JOUR J : CHECK-LIST AVANT

- [ ] PC allume et charge
- [ ] Aucune fenetre parasite ouverte
- [ ] Application lancee et minimised
- [ ] Slides PowerPoint ouvertes
- [ ] Guide imprime a cote de soi
- [ ] Bouteille d'eau a portee
- [ ] Telephone en silencieux
- [ ] Sourire :)

---

## CHRONOMETRAGE CIBLE

| Phase | Duree | Cumul |
|---|---|---|
| Slide 1-3 (Intro) | 2 min | 2 min |
| Slide 4-6 (Architecture) | 4 min | 6 min |
| Slide 7-8 (Regles + Choix) | 2 min 30 | 8 min 30 |
| Slide 9 (DEMO) | 5 min | 13 min 30 |
| Slide 10-12 (Bilan) | 1 min 30 | 15 min |

**Objectif :** rester entre 12 et 15 minutes.

---

## SCRIPT DE REPETITION

### Etape 1 - Seul, devant le miroir (2 fois)

1. Lire les slides et points cles a voix haute
2. Chronometrer
3. Noter les passages ou on hesite

### Etape 2 - Enregistrement video (1 fois)

1. Ouvrir la camera du telephone
2. Se filmer en presentant
3. Regarder la video et noter :
   - Debit de parole
   - Gestuelle
   - Contact visuel
   - Tics de langage

### Etape 3 - Repetition avec un proche (1 fois)

1. Presenter a un ami/famille
2. Lui demander de poser 3 questions au hasard
3. Repondre comme en conditions reelles

### Etape 4 - Simulation complete (1 fois)

1. Lancer l'app
2. Faire la demo complete en live
3. S'arreter si bug -> noter pour corriger avant le jour J

---

## LES 10 PHRASES A NE PAS DIRE

1. "Je n'ai pas eu le temps de..."
2. "J'espere que ca va marcher..."
3. "Ce n'est pas parfait mais..."
4. "Je ne sais pas coder en..."
5. "C'est complique a expliquer..."
6. "En fait..." (trop repetitif)
7. "Euh..." (bannir)
8. "Desole pour les bugs..."
9. "Je pense que..." (affirme plutot)
10. "C'est pas ma faute si..."

---

## LES 10 PHRASES A DIRE

1. "J'ai concu une architecture en 3 couches..."
2. "La regle metier est..."
3. "Le choix de SQLite se justifie par..."
4. "Grace aux contraintes SQL, on garantit..."
5. "En production, on pourrait..."
6. "Ce point est une limite que j'ai identifiee."
7. "Voici comment je repondrais a ce probleme..."
8. "J'ai teste et valide ce scenario."
9. "L'utilisateur final peut..."
10. "Merci, je suis pret pour vos questions."

---

## QUE FAIRE EN CAS DE PROBLEME

### Si l'app plante pendant la demo

1. Reste calme
2. Dis : "Je vais relancer l'application"
3. Relance : python main.py
4. Si ca replante : "Passons a la slide suivante, je vous montrerai le code."

### Si tu ne sais pas repondre

1. "Bonne question. Je n'ai pas traite ce cas precis."
2. "Voici comment je m'y prendrais si je devais le faire : ..."
3. Ne jamais inventer.

### Si tu perds le fil

1. Respire 3 secondes
2. Regarde tes slides
3. Reprends : "Pour revenir a la slide X, je disais que..."

### Si le jury est agressif

1. Ne te justifie pas
2. Reformule : "Si je comprends bien, vous me demandez..."
3. Reponds calmement et factuellement

---

## RESSOURCES A AVOIR SOUS LES YEUX

1. Ce guide (imprime)
2. Le schema de la base de donnees (imprime)
3. La liste des 20 questions (imprime)
4. Les slides ouvertes sur PowerPoint
5. L'app lancee et minimisee

---

## MESSAGE FINAL POUR TOI

Tu as construit une vraie application. Tu maitrises :
- Une architecture en 3 couches
- Une base de donnees relationnelle
- Une interface graphique moderne
- Un systeme de generation PDF
- Un workflow Git professionnel

Le jury veut voir que tu COMPRENDS ce que tu as fait. Pas que tu sois parfait.

Respire. Souris. Fais confiance a ton travail.

Tu vas reussir.

---

**FIN DU GUIDE DE SOUTENANCE**

*Bonne chance pour ta soutenance !*
