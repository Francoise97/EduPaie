"""Service de generation PDF des recus."""
import sys
from datetime import datetime
from pathlib import Path
from reportlab.lib.pagesizes import A5
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas

from src.services.eleve_service import EleveService
from src.services.paiement_service import PaiementService
from src.services.recu_service import RecuService
from src.config import ECOLE_NOM as CFG_ECOLE_NOM, ECOLE_ADRESSE as CFG_ECOLE_ADRESSE, DEVISE as CFG_DEVISE


# Dossier des PDF : a cote de l'exe ou du projet
if hasattr(sys, "_MEIPASS"):
    RECUS_DIR = Path(sys.executable).parent / "recus"
else:
    RECUS_DIR = Path(__file__).resolve().parents[2] / "recus"


class PDFService:
    ECOLE_NOM = CFG_ECOLE_NOM
    ECOLE_ADRESSE = CFG_ECOLE_ADRESSE
    DEVISE = CFG_DEVISE

    def __init__(self):
        self.eleve_service = EleveService()
        self.paiement_service = PaiementService()
        self.recu_service = RecuService()
        RECUS_DIR.mkdir(parents=True, exist_ok=True)

    def chemin_pdf(self, numero_recu):
        return RECUS_DIR / (numero_recu + ".pdf")

    def generer_recu(self, recu_id):
        recu = self.recu_service.obtenir(recu_id)
        if not recu:
            raise ValueError("Recu introuvable : " + str(recu_id))

        eleve = self.eleve_service.obtenir(recu.eleve_id)
        if not eleve:
            raise ValueError("Eleve introuvable : " + str(recu.eleve_id))

        paiements = self.paiement_service.lister_par_eleve(recu.eleve_id)
        paiement = None
        for p in paiements:
            if p.recu_id == recu.id:
                paiement = p
                break

        chemin = self.chemin_pdf(recu.numero_unique)
        self._dessiner_recu(str(chemin), recu, eleve, paiement)
        self.recu_service.mettre_a_jour_pdf(recu.id, str(chemin))
        return chemin

    def _dessiner_recu(self, chemin, recu, eleve, paiement):
        c = canvas.Canvas(chemin, pagesize=A5)
        largeur, hauteur = A5
        marge = 15 * mm

        c.setFillColor(colors.HexColor("#1E3A8A"))
        c.rect(0, hauteur - 25 * mm, largeur, 25 * mm, fill=1, stroke=0)

        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(largeur / 2, hauteur - 12 * mm, self.ECOLE_NOM)

        c.setFont("Helvetica", 8)
        c.drawCentredString(largeur / 2, hauteur - 18 * mm, self.ECOLE_ADRESSE)

        c.setFillColor(colors.HexColor("#1E3A8A"))
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(largeur / 2, hauteur - 38 * mm, "RECU DE PAIEMENT")

        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(colors.HexColor("#EF4444"))
        c.drawCentredString(largeur / 2, hauteur - 46 * mm, "N " + recu.numero_unique)

        c.setStrokeColor(colors.HexColor("#CBD5E1"))
        c.setLineWidth(0.5)
        c.line(marge, hauteur - 52 * mm, largeur - marge, hauteur - 52 * mm)

        y = hauteur - 60 * mm
        c.setFillColor(colors.HexColor("#1E293B"))

        lignes = [
            ("Recu de :", eleve.nom_complet),
            ("Classe :", eleve.classe),
            ("Annee scolaire :", eleve.annee_scolaire),
        ]

        for label, valeur in lignes:
            c.setFont("Helvetica-Bold", 10)
            c.drawString(marge, y, label)
            c.setFont("Helvetica", 10)
            c.drawString(marge + 35 * mm, y, str(valeur))
            y -= 6 * mm

        y -= 2 * mm
        c.line(marge, y, largeur - marge, y)
        y -= 8 * mm

        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(colors.HexColor("#1E293B"))
        c.drawString(marge, y, "Montant paye :")
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(colors.HexColor("#10B981"))
        c.drawString(marge + 35 * mm, y, self._fmt(recu.montant_paye))
        y -= 8 * mm

        c.setFillColor(colors.HexColor("#1E293B"))
        details = [
            ("Mode de paiement :", paiement.mode_paiement if paiement else "-"),
            ("Date :", self._fmt_date(paiement.date_paiement if paiement else recu.date_emission)),
        ]
        if paiement and paiement.reference:
            details.append(("Reference :", paiement.reference))
        if paiement and paiement.observation:
            details.append(("Observation :", paiement.observation))

        for label, valeur in details:
            c.setFont("Helvetica-Bold", 9)
            c.drawString(marge, y, label)
            c.setFont("Helvetica", 9)
            c.drawString(marge + 35 * mm, y, str(valeur))
            y -= 5 * mm

        y -= 4 * mm
        c.setFillColor(colors.HexColor("#F1F5F9"))
        c.rect(marge, y - 20 * mm, largeur - 2 * marge, 20 * mm, fill=1, stroke=0)

        y -= 4 * mm
        c.setFillColor(colors.HexColor("#1E293B"))
        c.setFont("Helvetica-Bold", 9)
        c.drawString(marge + 3 * mm, y, "Total du :")
        c.setFont("Helvetica", 9)
        c.drawString(marge + 30 * mm, y, self._fmt(eleve.frais_totaux))

        y -= 6 * mm
        c.setFont("Helvetica-Bold", 9)
        c.drawString(marge + 3 * mm, y, "Total paye :")
        c.setFont("Helvetica", 9)
        c.drawString(marge + 30 * mm, y, self._fmt(eleve.total_paye))

        y -= 6 * mm
        c.setFont("Helvetica-Bold", 9)
        c.drawString(marge + 3 * mm, y, "Solde restant :")
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(colors.HexColor("#EF4444"))
        c.drawString(marge + 30 * mm, y, self._fmt(recu.solde_apres))

        y_sig = 30 * mm
        c.setStrokeColor(colors.HexColor("#94A3B8"))
        c.setFillColor(colors.HexColor("#1E293B"))
        c.setFont("Helvetica", 9)

        c.line(marge, y_sig, marge + 50 * mm, y_sig)
        c.drawString(marge + 5 * mm, y_sig - 5 * mm, "La Secretaire")

        c.line(largeur - marge - 50 * mm, y_sig, largeur - marge, y_sig)
        c.drawString(largeur - marge - 45 * mm, y_sig - 5 * mm, "L'Etablissement")

        c.setFont("Helvetica-Oblique", 7)
        c.setFillColor(colors.HexColor("#94A3B8"))
        c.drawCentredString(
            largeur / 2, 10 * mm,
            "Genere le " + datetime.now().strftime("%d/%m/%Y a %H:%M")
        )

        c.save()

    def _fmt(self, montant):
        try:
            return "{:,.0f}".format(float(montant)).replace(",", " ") + " " + self.DEVISE
        except (ValueError, TypeError):
            return "0 " + self.DEVISE

    def _fmt_date(self, date_str):
        if not date_str:
            return "-"
        try:
            dt = datetime.strptime(str(date_str)[:10], "%Y-%m-%d")
            return dt.strftime("%d/%m/%Y")
        except (ValueError, TypeError):
            return str(date_str)
