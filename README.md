# IT Support RAG Chatbot

Un assistant IT support moderne basé sur RAG (Retrieval-Augmented Generation) utilisant **Mistral AI**, **Chroma** et **FastAPI**.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Framework-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![Mistral AI](https://img.shields.io/badge/LLM-Mistral%20AI-orange.svg)](https://mistral.ai/)
[![Chroma](https://img.shields.io/badge/Vector%20DB-Chroma-green.svg)](https://www.trychroma.com/)

## 🎯 Objectif business

- Réduire le temps moyen de résolution (MTTR) des incidents IT de 40 % en automatisant les réponses aux questions fréquentes.
- Diminuer la charge des équipes support de niveau 1 de 60 %, leur permettant de se concentrer sur les problèmes complexes.
- Offrir une assistance 24/7 sans augmentation des effectifs, avec une satisfaction utilisateur mesurée via un feedback intégré.
- Capitaliser la connaissance métier sous forme de base vectorielle évolutive, réutilisable pour former de nouveaux techniciens.

👉 **Ces gains opérationnels se traduisent directement par des économies financières pour l'entreprise (coûts évités, productivité accrue, réduction du turnover).**

## 📁 Structure du projet
├── backend/
│ ├── main.py # Serveur FastAPI, endpoints RAG
│ ├── static/ # Frontend (HTML, CSS, JS)
│ ├── chroma_db/ # Base vectorielle (créée par ingestion)
│ └── .env # Variables d'environnement (clé API Mistral)
├── scripts/
│ └── ingest_data.py # Script d'ingestion des documents
├── data/ # Documents sources (.md, .txt)
│ ├── Active_Directory_Guide.md
│ ├── Imprimantes_Guide.md
│ ├── Reseau_Performance.md
│ ├── VPN_Guide.md
│ └── Windows_Stability.md
├── requirements.txt # Dépendances Python
├── docker-compose.yml # Orchestration Docker (optionnel)
└── Dockerfile # Image Docker


## 🚀 Démarrage rapide

### Option 1 : Installation locale

```bash
# 1. Cloner le dépôt
git clone https://github.com/votre-nom/rag-it-support.git
cd rag-it-support

# 2. Créer et activer l'environnement virtuel
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer la clé API Mistral
cp backend/.env.example backend/.env
# Éditer backend/.env et ajouter votre clé : MISTRAL_API_KEY=xxxx

# 5. Ingérer les documents dans la base vectorielle
python scripts/ingest_data.py

# 6. Lancer le serveur backend
cd backend
python main.py

# Option 2 : Docker
docker-compose up --build