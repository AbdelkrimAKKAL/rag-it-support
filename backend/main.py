import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Load environment variables
load_dotenv(".env")

# Initialize FastAPI app
app = FastAPI(title="IT Support RAG Chatbot", description="RAG-based IT support assistant")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Initialize embeddings and vector store (optional)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "backend", "chroma_db")

retriever = None
llm = None

# Try to initialize RAG components
try:
    from langchain_chroma import Chroma
    from langchain_mistralai import MistralAIEmbeddings, ChatMistralAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    
    embeddings = MistralAIEmbeddings(model="mistral-embed", max_retries=5)
    
    # Load the vector store if it exists
    if os.path.exists(DB_DIR):
        try:
            vectorstore = Chroma(
                persist_directory=DB_DIR,
                embedding_function=embeddings,
                collection_name="it_support_collection"
            )
            retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
            print("✅ Vector store loaded successfully")
        except Exception as e:
            print(f"⚠️  Vector store exists but could not be loaded: {e}")
    else:
        print("⚠️  Vector store not found. Run scripts/ingest_data.py first for full RAG functionality.")
    
    # Initialize Mistral LLM
    llm = ChatMistralAI(model="mistral-large-latest", temperature=0.7)
    
    # Define the RAG prompt
    rag_prompt = ChatPromptTemplate.from_template("""
    Tu es un assistant IT support français. Réponds de manière très propre, sans aucun caractère de formatage spécial.

    Règles impératives :
    - N'utilise JAMAIS les caractères suivants : # * - > ` _ [ ] ( )
    - N'utilise JAMAIS de hashtags, ni d'astérisques, ni de tirets.
    - Pour organiser ta réponse, utilise uniquement :
    - Des titres en MAJUSCULES, sur une ligne seule
    - Des numéros (1., 2., 3.) pour les étapes
    - Des sauts de ligne entre les sections
    - Exemple de format attendu :

    PROBLÈME DE CONNEXION
    1. Vérifiez votre connexion internet avec la commande ping 8.8.8.8
    2. Redémarrez le service Cisco AnyConnect
    3. Contactez le support si le problème persiste

    SOLUTION ALTERNATIVE
    Utilisez le VPN web en vous connectant sur portal.company.com

    Contexte : {context}

    Question : {question}

    Réponse (format strict, sans aucun symbole bizarre) :
    """)
    
except Exception as e:
    print(f"⚠️  RAG components not fully initialized: {e}")
    print("   Chatbot will operate in demo mode with hardcoded responses.")

# Demo responses for testing without API key
DEMO_RESPONSES = {
    "vpn": """
Bienvenue! Pour vos problèmes VPN Cisco AnyConnect, voici les solutions courantes:

**Problème: Application qui se ferme brutalement**
1. Désinstaller complètement AnyConnect (Panneau de Configuration > Programmes)
2. Télécharger la version 4.10.07055 depuis le portail IT
3. Installer avec droits administrateur
4. Redémarrer l'ordinateur
5. Relancer AnyConnect

**Problème: 'Secure Gateway is unreachable'**
1. Vérifier la connectivité: `ping 8.8.8.8`
2. Vérifier l'adresse du gateway dans l'interface AnyConnect
3. Contacter IT Infrastructure si le problème persiste

**Support VPN:** vpn-team@company.com
""",
    "active directory": """
Besoin d'aide avec Active Directory? Voici les solutions courantes:

**Erreur: 'Credentials are invalid'**
- Vérifier la disposition clavier AZERTY/QWERTY
- Vérifier que CapsLock n'est pas activé
- Redémarrer l'ordinateur avec connexion réseau active

**Réinitialisation de Mot de Passe**
1. Écran de connexion Windows: Appuyer sur Ctrl + Alt + Suppr
2. Sélectionner "Changer un mot de passe"
3. Entrer l'ancien mot de passe
4. Entrer le nouveau (2x pour confirmation)
5. Attendre 15 secondes pour synchronisation

**Compte Verrouillé**
- Attendre 30 minutes pour déblocage automatique
- OU contacter: ad-support@company.com
""",
    "imprimante": """
Problèmes avec les imprimantes réseau? Voici comment résoudre:

**Imprimantes Disponibles:**
- Bureau principal (RDC): HP OfficeJet Pro 8025 (192.168.1.100)
- Étage 1: Xerox VersaLink C405 (192.168.1.101)
- Étage 2: Ricoh MP C3003 (192.168.1.102)
- Salle réunion: Brother HL-L9310CDW (192.168.1.103)

**Ajouter une Imprimante (Windows):**
1. Paramètres > Appareils > Imprimantes & Scanners
2. Cliquer "Ajouter une imprimante ou un scanner"
3. Entrer l'adresse IP (ex: 192.168.1.100)
4. Windows trouvera le pilote automatiquement

**Imprimante introuvable:**
1. Ping l'adresse IP: `ping 192.168.1.100`
2. Redémarrer l'imprimante (éteindre 30 secondes)

**Support:** it-printers@company.com
""",
    "réseau": """
Problèmes réseau ou de performance? Voici le diagnostic:

**Vérifier votre débit:**
1. Visiter https://www.speedtest.net
2. Cliquer "Go" et attendre
3. Minimum attendu: 10 Mbps download, 5 Mbps upload

**Tester la latence:**
```
ping 8.8.8.8          (Test Internet)
ping dc1.company.local (Test domaine interne)
tracert company.com   (Tracer la route)
```

**Connexion Lente - Solutions:**
1. Redémarrer la box/routeur
2. Rapprocher-vous du point WiFi
3. Utiliser Ethernet si possible (plus stable)
4. Fermer les applications inutiles

**Déconnexions Fréquentes:**
1. Vérifier stabilité WiFi
2. Mettre à jour le pilote de la carte réseau
3. Désactiver la mise en veille réseau

**Support:** network-team@company.com
""",
    "windows": """
Problèmes de stabilité Windows ou écran bleu? Voici comment diagnostiquer:

**Écran Bleu (BSOD) - Diagnostic:**
1. Noter le code d'erreur affiché
2. Chercher en ligne: "[Code d'erreur] Windows 11"

**Vérifier l'Intégrité du Disque:**
1. Invite de Commande (Admin)
2. Taper: `chkdsk C: /F /R`
3. Redémarrer et attendre vérification

**Vérifier la RAM:**
1. Windows Search: "Memory Diagnostic"
2. Cliquer "Restart now and check for problems"
3. L'outil redémarre et teste la mémoire

**Restauration Système:**
1. Paramètres > Système > Protection du système
2. Cliquer "Restauration système"
3. Choisir un point antérieur

**Support:** support@company.com
"""
}

# Define request/response models
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    sources: list = []
    is_demo: bool = False

# Routes
@app.get("/")
async def root():
    html_file = os.path.join(static_dir, "index.html")
    if os.path.exists(html_file):
        return FileResponse(html_file)
    return {"message": "IT Support RAG Chatbot API"}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat endpoint with RAG or demo mode"""
    user_message = request.message.strip().lower()
    
    if not user_message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    try:
        # Try RAG mode if available
        if retriever and llm:
            from langchain_core.output_parsers import StrOutputParser
            
            docs = retriever.invoke(request.message)
            context = "\n".join([doc.page_content for doc in docs])
            
            chain = rag_prompt | llm | StrOutputParser()
            response = chain.invoke({"context": context, "question": request.message})
            sources = [doc.metadata.get("source", "Knowledge Base") for doc in docs if doc.metadata]
            
            return ChatResponse(response=response, sources=sources, is_demo=False)
        
        # Fallback to demo mode
        else:
            # Find best matching demo response
            best_match = "general"
            best_score = 0
            
            for key in DEMO_RESPONSES.keys():
                if key in user_message:
                    best_match = key
                    break
            
            response = DEMO_RESPONSES.get(best_match, """
Bonjour! Je suis votre assistant IT Support en mode démonstration.

Pour une assistance complète avec:
- **VPN** - Problèmes de connexion Cisco AnyConnect
- **Active Directory** - Authentification et mots de passe
- **Imprimantes** - Configuration et dépannage
- **Réseau** - Performance et connectivité
- **Windows** - Stabilité et écrans bleus

Merci de configurer une clé API Mistral valide dans backend/.env pour activer le RAG complet!
""")
            
            return ChatResponse(
                response=response,
                sources=["Demo Mode - No Vector Store"],
                is_demo=True
            )
    
    except Exception as e:
        print(f"Error in chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/api/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "ok",
        "rag_available": retriever is not None,
        "llm_available": llm is not None,
        "demo_mode": retriever is None or llm is None
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

