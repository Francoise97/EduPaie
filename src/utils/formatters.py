"""Fonctions de formatage."""
from datetime import datetime


def formater_montant(montant):
    try:
        return "{:,.0f} FCFA".format(float(montant)).replace(",", " ")
    except (ValueError, TypeError):
        return "0 FCFA"


def formater_date(date_str):
    if not date_str:
        return ""
    try:
        dt = datetime.strptime(str(date_str)[:10], "%Y-%m-%d")
        return dt.strftime("%d/%m/%Y")
    except (ValueError, TypeError):
        return str(date_str)


def formater_datetime(dt_str):
    if not dt_str:
        return ""
    try:
        dt = datetime.strptime(str(dt_str), "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%d/%m/%Y %H:%M")
    except (ValueError, TypeError):
        return str(dt_str)


def libelle_statut(statut):
    correspondance = {
        "Solde": "Solde",
        "Partiellement paye": "Partiellement paye",
        "Non paye": "Non paye",
    }
    return correspondance.get(statut, statut)


def formater_pourcentage(valeur, total):
    if total == 0:
        return "0%"
    return str(int(valeur * 100 / total)) + "%"
