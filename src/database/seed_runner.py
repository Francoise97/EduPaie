"""Peuple la base avec 15 eleves + historique de paiements varie."""
import sys
from pathlib import Path
from datetime import datetime, timedelta
import random

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.database.db_manager import DatabaseManager, DB_PATH


def generer_numero_recu(conn, annee):
    row = conn.execute(
        "SELECT COALESCE(MAX(sequence), 0) + 1 FROM recu WHERE annee = ?",
        (annee,),
    ).fetchone()
    seq = row[0]
    return "REC-" + str(annee) + "-" + str(seq).zfill(3), seq


def inserer_paiement(conn, eleve_id, montant, date_paiement,
                     mode, reference, observation, solde_apres, annee):
    numero, seq = generer_numero_recu(conn, annee)

    cur = conn.execute(
        """INSERT INTO recu (numero_unique, annee, sequence, eleve_id,
                             date_emission, montant_paye, solde_apres)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (numero, annee, seq, eleve_id, date_paiement, montant, solde_apres),
    )
    recu_id = cur.lastrowid

    conn.execute(
        """INSERT INTO paiement (eleve_id, recu_id, montant, date_paiement,
                                 mode_paiement, reference, observation)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (eleve_id, recu_id, montant, date_paiement,
         mode, reference, observation),
    )
    return numero


def main():
    if DB_PATH.exists():
        DB_PATH.unlink()

    DatabaseManager.initialize()
    conn = DatabaseManager.get_connection()

    with open(Path(__file__).parent / "seed.sql", "r", encoding="utf-8") as f:
        conn.executescript(f.read())

    eleves = conn.execute(
        "SELECT id, frais_totaux FROM eleve ORDER BY id"
    ).fetchall()

    modes = ["Especes", "Cheque", "Virement", "Mobile Money"]
    annee = 2025

    scenarios = {
        0:  [250000],
        1:  [150000, 150000],
        2:  [],
        3:  [100000],
        4:  [100000, 100000, 100000],
        5:  [],
        6:  [175000],
        7:  [250000],
        8:  [100000, 50000],
        9:  [],
        10: [350000],
        11: [125000],
        12: [300000],
        13: [200000],
        14: [100000],
    }

    date_base = datetime(2024, 10, 1)

    for idx, eleve in enumerate(eleves):
        eleve_id = eleve["id"]
        frais    = eleve["frais_totaux"]
        cumul    = 0
        for i, montant in enumerate(scenarios.get(idx, [])):
            cumul += montant
            solde_apres = frais - cumul
            date_p = (date_base + timedelta(days=idx * 3 + i * 20)).strftime("%Y-%m-%d")
            mode = random.choice(modes)
            ref = "REF-" + str(eleve_id).zfill(3) + "-" + str(i+1) if mode != "Especes" else None
            numero = inserer_paiement(
                conn, eleve_id, montant, date_p, mode, ref,
                None, solde_apres, annee
            )
            print("  OK Recu " + numero + " - eleve " + str(eleve_id) + " - " + str(montant) + " FCFA")

    conn.commit()

    print("")
    print("Resume du jeu de test :")
    stats = conn.execute("""
        SELECT statut, COUNT(*) as nb, SUM(solde_restant) as restant
        FROM vue_solde_eleve GROUP BY statut
    """).fetchall()
    for s in stats:
        print("   " + str(s['statut']).ljust(20) + " : " + str(s['nb']).rjust(2) + " eleves - restant " + str(int(s['restant'] or 0)).rjust(10) + " FCFA")

    total = conn.execute("SELECT SUM(montant) FROM paiement").fetchone()[0]
    print("")
    print("   Total encaisse : " + str(int(total)) + " FCFA")
    print("   Base : " + str(DB_PATH))

    DatabaseManager.close()


if __name__ == "__main__":
    main()
