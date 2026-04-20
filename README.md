# [*] Assistant Support IT RAG (Mistral + FAISS) — Secteur Service Desk

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Mistral AI](https://img.shields.io/badge/LLM-Mistral%20API-orange.svg)](https://mistral.ai/)
[![FAISS](https://img.shields.io/badge/Vector%20DB-FAISS-green.svg)](https://github.com/facebookresearch/faiss)

## Resume Executif
Ce projet deploye un systeme complet de **RAG (Retrieval-Augmented Generation)** pour automatiser le support IT niveau 1. A partir d'une base de **50 tickets historiques** et **5 guides techniques**, l'assistant repond aux problemes utilisateurs (VPN, Active Directory, impression, ecran bleu) en produisant des solutions structurees, sourcees et exploitables. L'utilisation de **FAISS** pour la recherche vectorielle et de l'**API Mistral** (modele `mistral-small-latest`) garantit des reponses rapides (<5 secondes) et tracables, sans installation locale de LLM.

---

## Problematique Business
Les equipes support IT recoivent quotidiennement des dizaines de tickets redondants (reinitialisation VPN, compte verrouille, lenteur reseau). L'enjeu est triple :
1. **Automatisation des resolutions** : fournir une reponse immediate pour les problemes courants.
2. **Qualite et tracabilite** : citer systematiquement les sources (tickets historiques, documentation) pour justifier la solution.
3. **Reduction du temps de resolution** : passer de 30 minutes a moins de 5 minutes par incident de niveau 1.

---


**Donnees :**  
- 50 tickets CSV (5 categories : VPN, AD, imprimantes, reseau, BSOD)  
- 5 guides Markdown (procedures detaillees)

---

## Resultats & Demonstration

| Etape | Metrique | Valeur |
|-------|----------|--------|
| Vectorisation (FAISS) | Taille base | 80 chunks |
| Recherche | Temps moyen | < 100 ms |
| Generation (Mistral) | Temps moyen | 2-3 s |
| **Reponse complete** | **Latence** | **~3 s** |
| Pertinence | Score similarite | 0.68 – 0.85 |

**Exemple de reponse generee (probleme VPN) :**  
- Diagnostic : cache corrompu ou version instable  
- Etapes : nettoyage cache → reinstallation → desactivation antivirus  
- Sources : Ticket TK01002 (score 0.68), Ticket TK01009 (score 0.68)  

**Plus-value demontree :**  
- Reponse personnalisee (pas de copier-coller)  
- Combinaison de plusieurs tickets pour enrichir la solution  
- Escalade vers support avance si besoin  

---

## Stack Technique & Competences

- **Langage** : Python 3.8+  
- **Orchestration RAG** : LangChain, importlib dynamique  
- **Base vectorielle** : FAISS (faiss-cpu) – evite les DLL Windows problematiques  
- **Embeddings** : HuggingFace (all-MiniLM-L6-v2) – gratuit, local  
- **LLM** : Mistral API (mistral-small-latest) – cloud, pas d'infra locale  
- **Interface** : Streamlit (web app simple)  
- **Gestion des secrets** : python-dotenv  

**Competences cles mises en oeuvre :**  
- Ingenierie des prompts (system / user prompts)  
- Decoupage intelligent (chunking)  
- Gestion des limites de contexte (troncature)  
- Integration d'API REST (Mistral)  
- Deploiement local et reproductible  

---

## Prochaines Etapes & Limites

- **Ameliorations possibles** :  
  - Ajouter plus de tickets (500+) pour couvrir davantage de cas  
  - Integrer un feedback utilisateur pour affiner les reponses  
  - Passer aux embeddings Mistral (API) pour une stack homogene  
  - Deployer via Docker (docker-compose.yml fourni)  

- **Limites actuelles** :  
  - Base de connaissances reduite (50 tickets)  
  - Dependance a une connexion internet pour l'API Mistral  
  - Pas d'historique persistant des conversations  

---

## Installation et Utilisation

```bash
# Cloner le projet
git clone https://github.com/votre-nom/rag-it-support.git
cd rag-it-support

# Creer un environnement virtuel
python -m venv .venv
source .venv/bin/activate   # ou .venv\Scripts\activate sous Windows

# Installer les dependances
pip install -r requirements.txt

# Configurer la cle Mistral
echo "MISTRAL_API_KEY=votre_cle" > .env
echo "MISTRAL_MODEL=mistral-small-latest" >> .env

# Generer les donnees et la base vectorielle
python 1_generate_data.py
python 2_ingest_vectorize.py

# Tester le moteur RAG
python 3_rag_engine.py

# Lancer l'interface web
streamlit run 4_streamlit_app.py