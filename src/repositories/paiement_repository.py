"""Repository des paiements."""
from typing import Optional, List
from src.database.db_manager import DatabaseManager
from src.models.paiement import Paiement


class PaiementRepository:
    """Accès aux données de la table paiement."""

    def __init__(self):
        self.conn = DatabaseManager.get_connection()

    # ---------- CREATE ----------
    def ajouter(self, paiement: Paiement) -> int:
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

    # ---------- READ ----------
    def lister_par_eleve(self, eleve_id: int) -> List[Paiement]:
        """Historique chronologique des paiements d'un élève."""
        rows = self.conn.execute(
            """SELECT p.*, r.numero_unique AS numero_recu
               FROM paiement p
               LEFT JOIN recu r ON r.id = p.recu_id
               WHERE p.eleve_id = ?
               ORDER BY p.date_paiement DESC, p.id DESC""",
            (eleve_id,),
        ).fetchall()
        return [Paiement.from_row(r) for r in rows]

    def lister_tous(self) -> List[Paiement]:
        rows = self.conn.execute(
            """SELECT p.*, r.numero_unique AS numero_recu,
                      e.nom AS eleve_nom, e.prenom AS eleve_prenom
               FROM paiement p
               LEFT JOIN recu r ON r.id = p.recu_id
               LEFT JOIN eleve e ON e.id = p.eleve_id
               ORDER BY p.date_paiement DESC, p.id DESC"""
        ).fetchall()
        return [Paiement.from_row(r) for r in rows]

    def derniers(self, limite: int = 5) -> List[Paiement]:
        """Les N derniers paiements (pour le tableau de bord)."""
        rows = self.conn.execute(
            """SELECT p.*, r.numero_unique AS numero_recu,
                      e.nom AS eleve_nom, e.prenom AS eleve_prenom
               FROM paiement p
               LEFT JOIN recu r ON r.id = p.recu_id
               LEFT JOIN eleve e ON e.id = p.eleve_id
               ORDER BY p.date_paiement DESC, p.id DESC
               LIMIT ?""",
            (limite,),
        ).fetchall()
        return [Paiement.from_row(r) for r in rows]

    def obtenir(self, paiement_id: int) -> Optional[Paiement]:
        row = self.conn.execute(
            "SELECT * FROM paiement WHERE id = ?", (paiement_id,)
        ).fetchone()
        return Paiement.from_row(row) if row else None

    def total_par_eleve(self, eleve_id: int) -> float:
        row = self.conn.execute(
            "SELECT COALESCE(SUM(montant), 0) FROM paiement WHERE eleve_id = ?",
            (eleve_id,),
        ).fetchone()
        return row[0]

    # ---------- DELETE ----------
    def supprimer(self, paiement_id: int) -> None:
        self.conn.execute("DELETE FROM paiement WHERE id = ?", (paiement_id,))
        self.conn.commit()
