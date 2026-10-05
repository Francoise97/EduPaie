"""Repository des paiements."""
from datetime import datetime
from src.database.db_manager import DatabaseManager
from src.models.paiement import Paiement


class PaiementRepository:
    def __init__(self):
        self.conn = DatabaseManager.get_connection()

    def ajouter(self, paiement):
        cur = self.conn.execute(
            """INSERT INTO paiement (eleve_id, recu_id, montant, date_paiement,
                                      mode_paiement, reference, observation)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (paiement.eleve_id, paiement.recu_id, paiement.montant,
             paiement.date_paiement, paiement.mode_paiement,
             paiement.reference, paiement.observation),
        )
        self.conn.commit()
        return cur.lastrowid

    def annuler(self, paiement_id, raison):
        """Marque un paiement comme annule (soft delete)."""
        date_annulation = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.conn.execute(
            """UPDATE paiement
               SET annule = 1,
                   raison_annulation = ?,
                   date_annulation = ?
               WHERE id = ?""",
            (raison, date_annulation, paiement_id),
        )
        self.conn.commit()

    def lister_par_eleve(self, eleve_id):
        """Retourne tous les paiements d'un eleve (actifs + annules)."""
        rows = self.conn.execute(
            """SELECT p.*, r.numero_unique AS numero_recu,
                      r.solde_apres AS solde_apres
               FROM paiement p
               LEFT JOIN recu r ON r.id = p.recu_id
               WHERE p.eleve_id = ?
               ORDER BY p.date_paiement DESC, p.id DESC""",
            (eleve_id,),
        ).fetchall()
        return [Paiement.from_row(r) for r in rows]

    def lister_tous(self):
        """Retourne tous les paiements (actifs + annules)."""
        rows = self.conn.execute(
            """SELECT p.*, r.numero_unique AS numero_recu,
                      r.solde_apres AS solde_apres,
                      e.nom AS eleve_nom, e.prenom AS eleve_prenom
               FROM paiement p
               LEFT JOIN recu r ON r.id = p.recu_id
               LEFT JOIN eleve e ON e.id = p.eleve_id
               ORDER BY p.date_paiement DESC, p.id DESC"""
        ).fetchall()
        return [Paiement.from_row(r) for r in rows]

    def lister_actifs_par_eleve(self, eleve_id):
        """Retourne uniquement les paiements actifs d'un eleve."""
        rows = self.conn.execute(
            """SELECT p.*, r.numero_unique AS numero_recu,
                      r.solde_apres AS solde_apres
               FROM paiement p
               LEFT JOIN recu r ON r.id = p.recu_id
               WHERE p.eleve_id = ? AND p.annule = 0
               ORDER BY p.date_paiement DESC, p.id DESC""",
            (eleve_id,),
        ).fetchall()
        return [Paiement.from_row(r) for r in rows]

    def derniers(self, limite=5):
        """Les N derniers paiements actifs."""
        rows = self.conn.execute(
            """SELECT p.*, r.numero_unique AS numero_recu,
                      r.solde_apres AS solde_apres,
                      e.nom AS eleve_nom, e.prenom AS eleve_prenom
               FROM paiement p
               LEFT JOIN recu r ON r.id = p.recu_id
               LEFT JOIN eleve e ON e.id = p.eleve_id
               WHERE p.annule = 0
               ORDER BY p.date_paiement DESC, p.id DESC
               LIMIT ?""",
            (limite,),
        ).fetchall()
        return [Paiement.from_row(r) for r in rows]

    def obtenir(self, paiement_id):
        row = self.conn.execute(
            """SELECT p.*, r.numero_unique AS numero_recu,
                      r.solde_apres AS solde_apres
               FROM paiement p
               LEFT JOIN recu r ON r.id = p.recu_id
               WHERE p.id = ?""",
            (paiement_id,),
        ).fetchone()
        return Paiement.from_row(row) if row else None

    def total_par_eleve(self, eleve_id):
        row = self.conn.execute(
            "SELECT COALESCE(SUM(montant), 0) FROM paiement WHERE eleve_id = ? AND annule = 0",
            (eleve_id,),
        ).fetchone()
        return row[0]

    def supprimer(self, paiement_id):
        """Suppression DEFINITIVE (a eviter - utiliser annuler)."""
        self.conn.execute("DELETE FROM paiement WHERE id = ?", (paiement_id,))
        self.conn.commit()