#!/usr/bin/env python3
"""
Génère/insère une nouvelle dépêche dans Le Courrier d'Hermès (index.html).

Usage:
  python generer_depeche.py --kicker "..." --titre "..." --byline "..." --corps "para1||para2||para3"

Le script :
  - lit index.html
  - incrémente le compteur d'édition (Édition N° XXX) -> devient le n° de la dépêche
  - insère un <article class="article"> AVANT la dépêche de clôture (#a6)
  - met à jour le dateline avec la date du jour
  - réécrit index.html

Aucune dépendance externe (stdlib uniquement).
"""
import argparse
import re
import datetime
import sys

BASE = r"C:\Users\DELL\OneDrive\Desktop\Projet\Création Web Hermes\HermesJournal"
INDEX = BASE + r"\index.html"

MOIS = ["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"]
JOURS = ["dimanche","lundi","mardi","mercredi","jeudi","vendredi","samedi"]

def dateline_du_jour():
    d = datetime.date.today()
    return f"{JOURS[d.weekday()]} {d.day} {MOIS[d.month-1]} {d.year}"

def lire_index():
    with open(INDEX, encoding="utf-8") as f:
        return f.read()

def ecrire_index(html):
    with open(INDEX, "w", encoding="utf-8") as f:
        f.write(html)

def escape(t):
    return t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def compte_edition(html):
    m = re.search(r"Édition N°\s*0*(\d+)", html)
    return int(m.group(1)) if m else 1

def construit_article(num, kicker, titre, byline, paras):
    corps = ""
    if paras:
        premier = paras[0]
        if premier:
            premier_reste = escape(premier[1:]) if len(premier) > 1 else ""
            corps += '        <p><span class="dropcap">' + escape(premier[0]) + "</span>" + premier_reste + "</p>\n"
        for p in paras[1:]:
            corps += "        <p>" + escape(p) + "</p>\n"
    art = (
        '    <article class="article" id="a' + str(num) + '">\n'
        '      <p class="kicker">Compétence · ' + escape(kicker) + "</p>\n"
        '      <h3 class="article-head">' + escape(titre) + "</h3>\n"
        "      <p class=\"byline\">Par " + escape(byline) + "</p>\n"
        '      <div class="article-body columns-2">\n'
        + corps +
        "      </div>\n"
        "    </article>\n"
    )
    return art


def inserer(html, article):
    # insérer avant l'article de clôture (id=a6 / closing-article)
    marker = '<article class="article closing-article" id="a6">'
    if marker in html:
        html = html.replace(marker, article + "\n" + marker, 1)
    else:
        # fallback : avant le footer colophon
        html = html.replace('<footer class="colophon">', article + '\n<footer class="colophon">', 1)
    return html

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kicker", required=True)
    ap.add_argument("--titre", required=True)
    ap.add_argument("--byline", required=True)
    ap.add_argument("--corps", required=True, help="paragraphes séparés par ||")
    args = ap.parse_args()

    paras = [p.strip() for p in args.corps.split("||") if p.strip()]
    html = lire_index()
    num = compte_edition(html) + 1
    article = construit_article(num, args.kicker, args.titre, args.byline, paras)

    html = inserer(html, article)

    # maj edition
    html = re.sub(r"Édition N°\s*\d+", f"Édition N° {num:03d}", html, count=1)

    # maj dateline
    html = re.sub(r'(<span class="dateline" id="dateline">)[^<]*(</span>)',
                  lambda m: m.group(1) + dateline_du_jour() + m.group(2), html, count=1)

    ecrire_index(html)
    print(f"OK dépêche insérée #a{num} (Édition N° {num:03d})")

if __name__ == "__main__":
    main()
