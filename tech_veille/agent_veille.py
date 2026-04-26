"""
==========================================================
  AGENT DE VEILLE TECHNOLOGIQUE
  Scrape → Résume avec Groq → HTML → Email
==========================================================
"""

import smtplib
import requests
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
from groq import Groq

# ──────────────────────────────────────────────────────────
# ⚙️  CONFIGURATION
# ──────────────────────────────────────────────────────────

from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY   = os.getenv("GROQ_API_KEY")
GMAIL_ADDRESS  = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASS = os.getenv("GMAIL_APP_PASS")
DESTINATAIRE   = os.getenv("DESTINATAIRE")

SOURCES = [
    {
        "nom": "Hacker News",
        "url": "https://news.ycombinator.com/",
        "selecteur": "span.titleline > a",
        "limite": 8,
    },
    {
        "nom": "Le Monde Informatique",
        "url": "https://www.lemondeinformatique.fr/",
        "selecteur": "h2 a, h3 a",
        "limite": 5,
    },
    {
        "nom": "Dev.to Trending",
        "url": "https://dev.to/",
        "selecteur": "h2.crayons-story__title a",
        "limite": 6,
    },
]

# ──────────────────────────────────────────────────────────
# 🕷️  ÉTAPE 1 : Scraper
# ──────────────────────────────────────────────────────────

def scraper_news(source):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"}
    try:
        resp = requests.get(source["url"], headers=headers, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        elements = soup.select(source["selecteur"])
        titres = []
        for el in elements[: source["limite"]]:
            texte = el.get_text(strip=True)
            if texte and len(texte) > 10:
                titres.append(texte)
        print(f"  ✅ {source['nom']} : {len(titres)} titres récupérés")
        return titres
    except Exception as e:
        print(f"  ❌ Erreur sur {source['nom']} : {e}")
        return []


def collecter_toutes_news():
    print("\n🕷️  Scraping des sources...")
    resultats = {}
    for source in SOURCES:
        resultats[source["nom"]] = scraper_news(source)
    return resultats


# ──────────────────────────────────────────────────────────
# 🤖  ÉTAPE 2 : Résumer avec Groq
# ──────────────────────────────────────────────────────────

def resumer_avec_groq(news_par_source):
    print("\n🤖 Résumé par IA (Groq)...")
    client = Groq(api_key=GROQ_API_KEY)

    contenu = ""
    for source, titres in news_par_source.items():
        if titres:
            contenu += f"\n## {source}\n"
            for i, titre in enumerate(titres, 1):
                contenu += f"{i}. {titre}\n"

    if not contenu.strip():
        return "Aucune news collectée aujourd'hui."

    prompt = f"""Tu es un assistant de veille technologique en français.

Voici les titres de news tech collectés aujourd'hui :
{contenu}

Ta mission :
1. Identifie les 5 thèmes/tendances les plus importants
2. Pour chaque thème, écris 2-3 phrases de résumé en français, clair et concis
3. Ajoute une section "À retenir" avec 3 points clés maximum
4. Ton style : professionnel mais accessible, pas de jargon inutile

Format de réponse : HTML avec des balises <h3>, <p>, <ul>, <li> uniquement.
Pas de markdown, pas de blocs de code. Directement du HTML propre."""

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1500,
    )

    resume = completion.choices[0].message.content
    print("  ✅ Résumé généré avec succès")
    return resume


# ──────────────────────────────────────────────────────────
# 🎨  ÉTAPE 3 : Générer HTML
# ──────────────────────────────────────────────────────────

def generer_html(resume, news_brutes):
    date_str = datetime.now().strftime("%A %d %B %Y").capitalize()
    heure_str = datetime.now().strftime("%H:%M")

    icones = {
        "Hacker News": "🟠",
        "Le Monde Informatique": "🔵",
        "Dev.to Trending": "🟣",
    }

    couleurs = {
        "Hacker News": "#FF6B35",
        "Le Monde Informatique": "#4A90D9",
        "Dev.to Trending": "#9B59B6",
    }

    html_sources = ""
    for source, titres in news_brutes.items():
        if titres:
            icone = icones.get(source, "📡")
            couleur = couleurs.get(source, "#e94560")
            items = "".join(f"<li>{t}</li>" for t in titres)
            html_sources += f"""
        <div class="section" style="border-left: 4px solid {couleur};">
            <div class="section-title" style="color: {couleur};">{icone} {source}</div>
            <ul class="news-list">{items}</ul>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Veille Tech — {date_str}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', system-ui, sans-serif; background: #0f0f13; color: #e8e6e1; min-height: 100vh; }}
        .header {{ background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); padding: 48px 32px; text-align: center; border-bottom: 2px solid #e94560; }}
        .header h1 {{ font-size: 2.4rem; font-weight: 800; letter-spacing: -1px; color: #fff; }}
        .header h1 span {{ color: #e94560; }}
        .header .date {{ margin-top: 10px; color: #8892b0; font-size: 0.95rem; text-transform: uppercase; }}
        .badge {{ display: inline-block; background: #e94560; color: #fff; font-size: 0.7rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; padding: 4px 12px; border-radius: 20px; margin-bottom: 16px; }}
        .container {{ max-width: 780px; margin: 0 auto; padding: 40px 24px; }}
        .section {{ background: #1a1a2e; border: 1px solid #2a2a4e; border-radius: 16px; padding: 32px; margin-bottom: 28px; }}
        .section-title {{ font-size: 1.1rem; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 20px; }}
        .news-list {{ list-style: none; }}
        .news-list li {{ padding: 12px 0; border-bottom: 1px solid #2a2a4e; color: #a8b2d8; font-size: 0.92rem; line-height: 1.5; }}
        .news-list li:last-child {{ border-bottom: none; }}
        .news-list li::before {{ content: "→ "; color: #e94560; font-weight: bold; }}
        .ai-resume h3 {{ font-size: 1.05rem; font-weight: 700; color: #ccd6f6; margin: 20px 0 8px; }}
        .ai-resume h3:first-child {{ margin-top: 0; }}
        .ai-resume p {{ color: #a8b2d8; line-height: 1.7; font-size: 0.95rem; margin-bottom: 12px; }}
        .ai-resume ul {{ margin-left: 20px; color: #a8b2d8; }}
        .ai-resume li {{ margin-bottom: 6px; line-height: 1.6; font-size: 0.93rem; }}
        .footer {{ text-align: center; padding: 32px; color: #4a4a6a; font-size: 0.8rem; border-top: 1px solid #1a1a2e; }}
        .footer a {{ color: #e94560; text-decoration: none; }}
    </style>
</head>
<body>
    <div class="header">
        <div class="badge">🤖 Généré par IA</div>
        <h1>Veille <span>Tech</span></h1>
        <div class="date">📅 {date_str} — {heure_str}</div>
    </div>
    <div class="container">
        <div class="section" style="border-left: 4px solid #e94560;">
            <div class="section-title" style="color: #e94560;">🧠 Analyse IA du jour</div>
            <div class="ai-resume">{resume}</div>
        </div>
        {html_sources}
    </div>
    <div class="footer">
        Généré automatiquement par votre Agent de Veille Tech •
        Propulsé par <a href="https://groq.com">Groq</a> + LLaMA 3 •
        {heure_str}
    </div>
</body>
</html>"""
    return html


# ──────────────────────────────────────────────────────────
# 📧  ÉTAPE 4 : Envoyer par email
# ──────────────────────────────────────────────────────────

def envoyer_email(html_content):
    print("\n📧 Envoi de l'email...")
    date_str = datetime.now().strftime("%d/%m/%Y")
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🤖 Veille Tech — {date_str}"
    msg["From"]    = GMAIL_ADDRESS
    msg["To"]      = DESTINATAIRE
    msg.attach(MIMEText(html_content, "html", "utf-8"))
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(GMAIL_ADDRESS, GMAIL_APP_PASS)
            smtp.sendmail(GMAIL_ADDRESS, DESTINATAIRE, msg.as_string())
        print(f"  ✅ Email envoyé à {DESTINATAIRE}")
        return True
    except Exception as e:
        print(f"  ❌ Erreur envoi email : {e}")
        return False


# ──────────────────────────────────────────────────────────
# 🚀  MAIN
# ──────────────────────────────────────────────────────────

def main():
    print("=" * 55)
    print("  🤖 AGENT DE VEILLE TECHNOLOGIQUE")
    print(f"  {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}")
    print("=" * 55)

    news = collecter_toutes_news()
    resume = resumer_avec_groq(news)

    print("\n🎨 Génération de la page HTML...")
    html = generer_html(resume, news)

    nom_fichier = f"veille_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    with open(nom_fichier, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✅ Fichier sauvegardé : {nom_fichier}")

    envoyer_email(html)

    print("\n✅ Agent terminé avec succès !")
    print("=" * 55)


if __name__ == "__main__":
    main()