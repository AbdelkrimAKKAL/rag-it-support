"""
ÉTAPE 4: INTERFACE UTILISATEUR SIMPLIFIÉE
"""

import streamlit as st
import sys
import os

# Ajoute le répertoire courant pour pouvoir importer 3_rag_engine.py
sys.path.append(os.path.dirname(__file__))

# ============================================================================
# CHARGEMENT DU MOTEUR RAG
# ============================================================================

@st.cache_resource
def load_engine():
    """Charge le moteur RAG depuis 3_rag_engine.py"""
    try:
        # Import direct du fichier 3_rag_engine.py
        import importlib.util
        spec = importlib.util.spec_from_file_location("rag_engine", "3_rag_engine.py")
        rag_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(rag_module)
        return rag_module.RAGEngine()
    except Exception as e:
        st.error(f" Erreur de chargement: {e}")
        st.info("Assurez-vous que `3_rag_engine.py` existe et que toutes les dépendances sont installées.")
        return None

# ============================================================================
# INTERFACE STREAMLIT
# ============================================================================

st.set_page_config(page_title="Support IT RAG", page_icon="🤖")
st.title("🤖 Assistant Support IT - RAG")

# Sidebar
with st.sidebar:
    st.header("⚙️ Options")
    num_sources = st.slider("Nombre de sources", 1, 5, 3)
    st.markdown("---")
    st.subheader("💡 Exemples")
    examples = [
        "VPN ne se connecte plus",
        "Imprimante introuvable",
        "Écran bleu au démarrage"
    ]
    for ex in examples:
        if st.button(ex):
            st.session_state.query = ex

# Zone principale
st.subheader("🔧 Décrivez votre problème")
query = st.text_area("", height=120, key="query", placeholder="Ex: Mon VPN ne fonctionne pas...")

col1, col2 = st.columns(2)
with col1:
    submit = st.button("🚀 Résoudre", type="primary", use_container_width=True)
with col2:
    clear = st.button("🗑️ Effacer", use_container_width=True)

if clear:
    st.session_state.query = ""
    st.rerun()

if submit and query.strip():
    engine = load_engine()
    if engine:
        with st.spinner("Recherche de solutions..."):
            try:
                result = engine.resolve_ticket(query, k=num_sources)
                st.markdown("---")
                st.markdown("### ✅ Réponse")
                st.markdown(result['response'])
                
                st.markdown("---")
                st.markdown("### 📚 Sources")
                for src in result['sources']:
                    if src['type'] == 'ticket':
                        st.markdown(f"- 🎫 Ticket {src['id']} (similarité {src['score']:.1%})")
                    else:
                        st.markdown(f"- 📖 {src['filename']} (similarité {src['score']:.1%})")
            except Exception as e:
                st.error(f"Erreur: {e}")
elif submit and not query.strip():
    st.warning("Veuillez entrer une description.")