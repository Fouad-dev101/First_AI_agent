# 🤖 Agent de Veille Technologique

Un agent Python autonome qui tourne chaque matin, scrape les dernières news tech sur internet, les résume en français grâce à l'IA (Groq + LLaMA 3), génère une belle page HTML et l'envoie par email automatiquement.

---

## ✨ Fonctionnalités

- 🕷️ **Scraping automatique** de 3 sources tech (Hacker News, Le Monde Informatique, Dev.to)
- 🧠 **Résumé IA** en français via Groq (LLaMA 3.3 70B)
- 🎨 **Newsletter HTML** dark-mode avec une section par source
- 📧 **Envoi automatique** par email via Gmail
- ⏰ **Tourne tout seul** chaque matin (Windows Scheduler ou PythonAnywhere)

---

## 📸 Aperçu

```
===================================================
  🤖 AGENT DE VEILLE TECHNOLOGIQUE
  23/04/2026 à 07:00:00
===================================================
🕷️  Scraping des sources...
  ✅ Hacker News : 8 titres récupérés
  ✅ Le Monde Informatique : 5 titres récupérés
  ✅ Dev.to Trending : 6 titres récupérés
🤖 Résumé par IA (Groq)...
  ✅ Résumé généré avec succès
🎨 Génération de la page HTML...
  ✅ Fichier sauvegardé : veille_20260423_0700.html
📧 Envoi de l'email...
  ✅ Email envoyé à toi@gmail.com
✅ Agent terminé avec succès !
===================================================
```

---

## 🛠️ Installation

### 1. Cloner le repo

```bash
git clone https://github.com/ton-username/agent-veille-tech.git
cd agent-veille-tech
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Configurer les variables d'environnement

Crée un fichier `.env` à la racine du projet :

```env
GROQ_API_KEY=gsk_ta_cle_groq_ici
GMAIL_ADDRESS=toi@gmail.com
GMAIL_APP_PASS=xxxx xxxx xxxx xxxx
DESTINATAIRE=toi@gmail.com
```

> ⚠️ Ne partage jamais ce fichier — il est ignoré par Git grâce au `.gitignore`

---

## 🔑 Obtenir les clés

### Clé Groq (gratuite)
1. Va sur [console.groq.com](https://console.groq.com)
2. Crée un compte gratuit
3. Clique **API Keys** → **Create API Key**

### App Password Gmail
1. Va sur [myaccount.google.com/security](https://myaccount.google.com/security)
2. Active la **validation en 2 étapes**
3. Cherche **"Mots de passe des applications"**
4. Génère un mot de passe pour "Mail"

---

## 🚀 Lancer l'agent

```bash
python agent_veille.py
```

---

## ⏰ Automatisation

### Sur Windows (tourne chaque matin à 7h)

```cmd
schtasks /create /tn "VeilleTech" /tr "py C:\chemin\vers\agent_veille.py" /sc daily /st 07:00
```

### Sur PythonAnywhere (gratuit, 24h/24)
1. Upload `agent_veille.py` et `.env` sur PythonAnywhere
2. Dans **Tasks**, ajoute une tâche à 07:00 :
```
python /home/TONUSERNAME/agent_veille.py
```

---

## 📁 Structure du projet

```
agent-veille-tech/
├── agent_veille.py      # Le script principal
├── requirements.txt     # Les dépendances Python
├── .env                 # Tes clés secrètes (jamais sur GitHub)
├── .gitignore           # Ignore le .env
└── README.md            # Ce fichier
```

---

## 🧰 Technologies utilisées

| Outil | Rôle |
|---|---|
| `requests` | Télécharger les pages web |
| `BeautifulSoup` | Parser le HTML et extraire les titres |
| `Groq API` | Résumer les news avec LLaMA 3 |
| `smtplib` | Envoyer l'email via Gmail |
| `python-dotenv` | Gérer les variables secrètes |

---

## 🐛 Problèmes courants

| Problème | Solution |
|---|---|
| `pip not recognized` | Utiliser `py -m pip install` |
| Erreur Gmail auth | Vérifier l'App Password (pas le vrai mdp) |
| Modèle Groq déprécié | Changer pour `llama-3.3-70b-versatile` |
| Aucun titre récupéré | Le sélecteur CSS du site a changé |

---

## 📄 Licence

MIT — libre d'utilisation et de modification.

---

*Projet réalisé dans le cadre d'une formation Full Stack — ISTA Maroc 🇲🇦*
