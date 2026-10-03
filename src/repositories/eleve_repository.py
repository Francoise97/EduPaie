"""Repository des élèves : encapsule toutes les requêtes SQL."""
from typing import Optional, List
from src.database.db_manager import DatabaseManager
from src.models.eleve import Eleve


class EleveRepository:
    """Accès aux données de la table eleve."""

    def __init__(self):
        self.conn = DatabaseManager.get_connection()

    # ---------- CREATE ----------
    def ajouter(self, eleve: Eleve) -> int:
        """Insère un nouvel élève. Retourne l'id créé."""
        cur = self.conn.execute(
            """INSERT INTO eleve (nom, prenom, classe, annee_scolaire,
                                   frais_totaux, telephone, nom_parent)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (eleve.nom, eleve.prenom, eleve.classe, eleve.annee_scolaire,
             eleve.frais_totaux, eleve.telephone, eleve.nom_parent),
        )
        self.conn.commit()
        return cur.lastrowid

    # ---------- READ ----------
    def lister_tous(self) -> List[Eleve]:
        """Retourne tous les élèves avec leur solde calculé."""
        rows = self.conn.execute(
            "SELECT * FROM vue_solde_eleve ORDER BY nom, prenom"
        ).fetchall()
        return [Eleve.from_row(r) for r in rows]

    def lister_par_classe(self, classe: str) -> List[Eleve]:
        rows = self.conn.execute(
            "SELECT * FROM vue_solde_eleve WHERE classe = ? ORDER BY nom, prenom",
            (classe,),
        ).fetchall()
        return [Eleve.from_row(r) for r in rows]

    def rechercher(self, terme: str) -> List[Eleve]:
        """Recherche par nom, prénom ou classe."""
        motif = f"%{terme}%"
        rows = self.conn.execute(
            """SELECT * FROM vue_solde_eleve
               WHERE nom LIKE ? OR prenom LIKE ? OR classe LIKE ?
               ORDER BY nom, prenom""",
            (motif, motif, motif),
        ).fetchall()
        return [Eleve.from_row(r) for r in rows]

    def obtenir(self, eleve_id: int) -> Optional[Eleve]:
        """Retourne un élève par son id (avec solde calculé)."""
        row = self.conn.execute(
            "SELECT * FROM vue_solde_eleve WHERE id = ?", (eleve_id,)
        ).fetchone()
        return Eleve.from_row(row) if row else None

    def lister_classes(self) -> List[str]:
        """Retourne la liste des classes distinctes."""
        rows = self.conn.execute(
            "SELECT DISTINCT classe FROM eleve ORDER BY classe"
        ).fetchall()
        return [r["classe"] for r in rows]

    def lister_annees(self) -> List[str]:
        rows = self.conn.execute(
            "SELECT DISTINCT annee_scolaire FROM eleve ORDER BY annee_scolaire DESC"
        ).fetchall()
        return [r["annee_scolaire"] for r in rows]

    # ---------- UPDATE ----------
    def modifier(self, eleve: Eleve) -> None:
        if eleve.id is None:
            raise ValueError("Impossible de modifier un élève sans id.")
        self.conn.execute(
            """UPDATE eleve
               SET nom = ?, prenom = ?, classe = ?, annee_scolaire = ?,
                   frais_totaux = ?, telephone = ?, nom_parent = ?
               WHERE id = ?""",
            (eleve.nom, eleve.prenom, eleve.classe, eleve.annee_scolaire,
             eleve.frais_totaux, eleve.telephone, eleve.nom_parent, eleve.id),
        )
        self.conn.commit()

    # ---------- DELETE ----------
    def supprimer(self, eleve_id: int) -> None:
        """Supprime un élève et tous ses paiements (via CASCADE)."""
        self.conn.execute("DELETE FROM eleve WHERE id = ?", (eleve_id,))
        self.conn.commit()

    # ---------- STATS ----------
    def compter(self) -> int:
        return self.conn.execute("SELECT COUNT(*) FROM eleve").fetchone()[0]

    def statistiques(self) -> dict:
        """Retourne les stats globales pour le tableau de bord."""
        row = self.conn.execute("""
            SELECT
                COUNT(*)                              AS nb_eleves,
                COALESCE(SUM(frais_totaux), 0)        AS total_du,
                COALESCE(SUM(total_paye), 0)          AS total_encaisse,
                COALESCE(SUM(solde_restant), 0)       AS total_restant,
                SUM(CASE WHEN statut = 'Non paye' THEN 1 ELSE 0 END) AS nb_non_payes,
                SUM(CASE WHEN statut = 'Partiellement paye' THEN 1 ELSE 0 END) AS nb_partiels,
                SUM(CASE WHEN statut = 'Solde' THEN 1 ELSE 0 END) AS nb_soldes
            FROM vue_solde_eleve
        """).fetchone()
        return dict(row) if row else {}
