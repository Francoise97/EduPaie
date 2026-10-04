"""Genere un schema visuel de la base de donnees en PNG."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


fig, ax = plt.subplots(figsize=(14, 9))
ax.set_xlim(0, 14)
ax.set_ylim(0, 9)
ax.axis("off")

BLEU = "#1E3A8A"
VERT = "#10B981"
ORANGE = "#F59E0B"
VIOLET = "#8B5CF6"


def dessiner_table(x, y, w, h, titre, colonnes, couleur):
    box = FancyBboxPatch((x, y), w, h,
                          boxstyle="round,pad=0.05",
                          linewidth=2, edgecolor=couleur,
                          facecolor="white")
    ax.add_patch(box)

    header = FancyBboxPatch((x, y + h - 0.5), w, 0.5,
                             boxstyle="round,pad=0.05",
                             linewidth=2, edgecolor=couleur,
                             facecolor=couleur)
    ax.add_patch(header)

    ax.text(x + w / 2, y + h - 0.25, titre,
            ha="center", va="center",
            fontsize=12, fontweight="bold", color="white")

    for i, col in enumerate(colonnes):
        ax.text(x + 0.15, y + h - 0.8 - i * 0.32, col,
                ha="left", va="center", fontsize=9,
                color="#1E293B")


dessiner_table(0.5, 4.5, 4, 4, "ELEVE",
               ["id (PK)", "nom", "prenom", "classe",
                "annee_scolaire", "frais_totaux",
                "telephone", "nom_parent", "date_creation"], BLEU)

dessiner_table(5.5, 4.5, 4, 4, "PAIEMENT",
               ["id (PK)", "eleve_id (FK)", "recu_id (FK, UQ)",
                "montant", "date_paiement", "mode_paiement",
                "reference", "observation", "date_creation"], VERT)

dessiner_table(10.5, 4.5, 3, 4, "RECU",
               ["id (PK)", "numero_unique (UQ)", "annee",
                "sequence", "eleve_id (FK)", "date_emission",
                "montant_paye", "solde_apres", "chemin_pdf"], ORANGE)

dessiner_table(3, 0.5, 8, 2.5, "VUE_SOLDE_ELEVE (calculee)",
               ["id, nom, prenom, classe, frais_totaux",
                "total_paye  (= SUM paiement.montant)",
                "solde_restant  (= frais_totaux - total_paye)",
                "statut  (= Non paye / Partiellement paye / Solde)"], VIOLET)

ax.annotate("", xy=(5.5, 6), xytext=(4.5, 6),
            arrowprops=dict(arrowstyle="->", color="#64748B", lw=2))
ax.text(5.0, 6.2, "1,N", ha="center", fontsize=10, color="#64748B")

ax.annotate("", xy=(10.5, 6), xytext=(9.5, 6),
            arrowprops=dict(arrowstyle="->", color="#64748B", lw=2))
ax.text(10.0, 6.2, "1,1", ha="center", fontsize=10, color="#64748B")

ax.text(7, 8.7, "Schema de la base de donnees EduPaie",
        ha="center", fontsize=16, fontweight="bold", color="#1E3A8A")

plt.tight_layout()
plt.savefig("docs/schema_bdd.png", dpi=150, bbox_inches="tight", facecolor="white")
print("OK docs/schema_bdd.png genere")
