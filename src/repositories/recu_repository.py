"""Repository des reçus : gestion de la numérotation unique."""
from typing import Optional, List
from src.database.db_manager import DatabaseManager
from src.models.recu import Recu


class RecuRepository:
    """Accès aux données de la table recu."""

    def __init__(self):
        self.conn = DatabaseManager.get_connection()

    # ---------- Numérotation ----------
    def prochain_numero(self, annee: int) -> tuple[str, int]:
        """Retourne (numero_unique, sequence) pour la prochaine émission."""
        row = self.conn.execute(
            "SELECT COALESCE(MAX(sequence), 0) + 1 FROM recu WHERE annee = ?",
            (annee,),
        ).fetchone()
        seq = row[0]
        return f"REC-{annee}-{seq:03d}", seq

    # ---------- CREATE ----------
    def ajouter(self, recu: Recu) -> int:
        cur = self.conn.execute(
            """INSERT INTO recu (numero_unique, annee, sequence, eleve_id,
                                  date_emission, montant_paye, solde_apres,
                                  chemin_pdf)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (recu.numero_unique, recu.annee, recu.sequence, recu.eleve_id,
             recu.date_emission, recu.montant_paye, recu.solde_apres,
             recu.chemin_pdf),
        )
        self.conn.commit()
        return cur.lastrowid

    # ---------- READ ----------
    def obtenir(self, recu_id: int) -> Optional[Recu]:
        row = self.conn.execute(
            "SELECT * FROM recu WHERE id = ?", (recu_id,)
        ).fetchone()
        return Recu.from_row(row) if row else None

    def obtenir_par_numero(self, numero: str) -> Optional[Recu]:
        row = self.conn.execute(
            "SELECT * FROM recu WHERE numero_unique = ?", (numero,)
        ).fetchone()
        return Recu.from_row(row) if row else None

    def lister_par_eleve(self, eleve_id: int) -> List[Recu]:
        rows = self.conn.execute(
            "SELECT * FROM recu WHERE eleve_id = ? ORDER BY date_emission DESC, id DESC",
            (eleve_id,),
        ).fetchall()
        return [Recu.from_row(r) for r in rows]

    def lister_tous(self) -> List[Recu]:
        rows = self.conn.execute(
            "SELECT * FROM recu ORDER BY date_emission DESC, id DESC"
        ).fetchall()
        return [Recu.from_row(r) for r in rows]

    # ---------- UPDATE ----------
    def mettre_a_jour_pdf(self, recu_id: int, chemin_pdf: str) -> None:
        self.conn.execute(
            "UPDATE recu SET chemin_pdf = ? WHERE id = ?",
            (chemin_pdf, recu_id),
        )
        self.conn.commit()

    # ---------- DELETE ----------
    def supprimer(self, recu_id: int) -> None:
        self.conn.execute("DELETE FROM recu WHERE id = ?", (recu_id,))
        self.conn.commit()
