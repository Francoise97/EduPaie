PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS eleve (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    nom             TEXT    NOT NULL,
    prenom          TEXT    NOT NULL,
    classe          TEXT    NOT NULL,
    annee_scolaire  TEXT    NOT NULL,
    frais_totaux    REAL    NOT NULL CHECK (frais_totaux >= 0),
    telephone       TEXT,
    nom_parent      TEXT,
    date_creation   TEXT    NOT NULL DEFAULT (datetime('now','localtime'))
);

CREATE INDEX IF NOT EXISTS idx_eleve_classe ON eleve(classe);
CREATE INDEX IF NOT EXISTS idx_eleve_annee  ON eleve(annee_scolaire);

CREATE TABLE IF NOT EXISTS recu (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_unique   TEXT    NOT NULL UNIQUE,
    annee           INTEGER NOT NULL,
    sequence        INTEGER NOT NULL,
    eleve_id        INTEGER NOT NULL,
    date_emission   TEXT    NOT NULL DEFAULT (datetime('now','localtime')),
    montant_paye    REAL    NOT NULL CHECK (montant_paye > 0),
    solde_apres     REAL    NOT NULL CHECK (solde_apres >= 0),
    chemin_pdf      TEXT,
    FOREIGN KEY (eleve_id) REFERENCES eleve(id) ON DELETE CASCADE,
    UNIQUE (annee, sequence)
);

CREATE INDEX IF NOT EXISTS idx_recu_eleve ON recu(eleve_id);

CREATE TABLE IF NOT EXISTS paiement (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    eleve_id        INTEGER NOT NULL,
    recu_id         INTEGER NOT NULL UNIQUE,
    montant         REAL    NOT NULL CHECK (montant > 0),
    date_paiement   TEXT    NOT NULL,
    mode_paiement   TEXT    NOT NULL CHECK (mode_paiement IN
                       ('Especes','Cheque','Virement','Mobile Money')),
    reference       TEXT,
    observation     TEXT,
    date_creation   TEXT    NOT NULL DEFAULT (datetime('now','localtime')),
    FOREIGN KEY (eleve_id) REFERENCES eleve(id) ON DELETE CASCADE,
    FOREIGN KEY (recu_id)  REFERENCES recu(id)   ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_paiement_eleve ON paiement(eleve_id);
CREATE INDEX IF NOT EXISTS idx_paiement_date  ON paiement(date_paiement);

CREATE VIEW IF NOT EXISTS vue_solde_eleve AS
SELECT
    e.id, e.nom, e.prenom, e.classe, e.annee_scolaire, e.frais_totaux,
    COALESCE(SUM(p.montant), 0)                  AS total_paye,
    e.frais_totaux - COALESCE(SUM(p.montant), 0) AS solde_restant,
    CASE
        WHEN COALESCE(SUM(p.montant), 0) = 0 THEN 'Non paye'
        WHEN COALESCE(SUM(p.montant), 0) >= e.frais_totaux THEN 'Solde'
        ELSE 'Partiellement paye'
    END AS statut
FROM eleve e
LEFT JOIN paiement p ON p.eleve_id = e.id
GROUP BY e.id;
