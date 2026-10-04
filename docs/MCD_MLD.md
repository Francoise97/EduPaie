# Modele de donnees - EduPaie

## 1. MCD (Modele Conceptuel de Donnees)

ELEVE (id, nom, prenom, classe, annee_scolaire, frais_totaux, telephone, nom_parent)
   |
   | 1,N
   v
PAIEMENT (id, eleve_id, recu_id, montant, date_paiement, mode_paiement, reference, observation)
   |
   | 1,1
   v
RECU (id, numero_unique, annee, sequence, eleve_id, date_emission, montant_paye, solde_apres, chemin_pdf)

## 2. Regles de gestion

- RG1 : Un eleve peut avoir 0 ou plusieurs paiements (relation 1,N)
- RG2 : Un paiement correspond a exactement 1 recu (relation 1,1)
- RG3 : Un recu est rattache a exactement 1 eleve
- RG4 : Le solde = frais_totaux - somme(montant des paiements)
- RG5 : Le solde ne peut jamais etre negatif
- RG6 : Le numero de recu est unique par annee : REC-{ANNEE}-{SEQ:03d}

## 3. MLD

### Table ELEVE
| Colonne | Type | Contraintes |
|---|---|---|
| id | INTEGER | PK AUTOINCREMENT |
| nom | TEXT | NOT NULL |
| prenom | TEXT | NOT NULL |
| classe | TEXT | NOT NULL, INDEX |
| annee_scolaire | TEXT | NOT NULL, INDEX |
| frais_totaux | REAL | NOT NULL, CHECK >= 0 |
| telephone | TEXT | NULL |
| nom_parent | TEXT | NULL |
| date_creation | TEXT | NOT NULL, DEFAULT now |

### Table RECU
| Colonne | Type | Contraintes |
|---|---|---|
| id | INTEGER | PK AUTOINCREMENT |
| numero_unique | TEXT | NOT NULL, UNIQUE |
| annee | INTEGER | NOT NULL |
| sequence | INTEGER | NOT NULL |
| eleve_id | INTEGER | NOT NULL, FK eleve(id) ON DELETE CASCADE |
| date_emission | TEXT | NOT NULL, DEFAULT now |
| montant_paye | REAL | NOT NULL, CHECK > 0 |
| solde_apres | REAL | NOT NULL, CHECK >= 0 |
| chemin_pdf | TEXT | NULL |
| UNIQUE(annee, sequence) |

### Table PAIEMENT
| Colonne | Type | Contraintes |
|---|---|---|
| id | INTEGER | PK AUTOINCREMENT |
| eleve_id | INTEGER | NOT NULL, FK eleve(id) ON DELETE CASCADE |
| recu_id | INTEGER | NOT NULL, UNIQUE, FK recu(id) ON DELETE CASCADE |
| montant | REAL | NOT NULL, CHECK > 0 |
| date_paiement | TEXT | NOT NULL |
| mode_paiement | TEXT | NOT NULL, CHECK IN (Especes, Cheque, Virement, Mobile Money) |
| reference | TEXT | NULL |
| observation | TEXT | NULL |
| date_creation | TEXT | NOT NULL, DEFAULT now |

## 4. Vue VUE_SOLDE_ELEVE

| Colonne calculee | Formule |
|---|---|
| total_paye | COALESCE(SUM(paiement.montant), 0) |
| solde_restant | frais_totaux - total_paye |
| statut | CASE WHEN total_paye = 0 THEN Non paye WHEN total_paye >= frais THEN Solde ELSE Partiellement paye END |

## 5. Index

- idx_eleve_classe : accelere le filtre par classe
- idx_eleve_annee : accelere le filtre par annee
- idx_recu_eleve : accelere la recherche des recus d'un eleve
- idx_paiement_eleve : accelere la recherche des paiements d'un eleve
- idx_paiement_date : accelere le tri chronologique

## 6. Contraintes d'integrite

- Integrite d'entite : chaque table a une cle primaire (id)
- Integrite referentielle : les FK empechent les orphelins
- Integrite de domaine : les CHECK limitent les valeurs valides
- Integrite utilisateur : UNIQUE empeche les doublons
