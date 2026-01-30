import streamlit as st
import asyncio
from agents import Agent, Runner, function_tool
from upstash_vector import Index
from dotenv import load_dotenv

load_dotenv()
index = Index.from_env()

# --- L'OUTIL (Directement ici pour éviter l'erreur) ---
@function_tool
def consulter_dossier(recherche: str) -> str:
    """Recherche des infos sur Alioune DIOP (nom, parcours, McDo, BOA)."""
    res = index.query(data=recherche, top_k=6, include_metadata=True)
    if not res:
        return "Aucune info trouvée."
    return "\n\n".join([f"Source: {r.metadata.get('title')}\n{r.data}" for r in res])

# --- CONFIGURATION STREAMLIT ---
st.set_page_config(page_title="Alioune AI", page_icon="🎓")
st.title("🎓 Alioune AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrée utilisateur
if prompt := st.chat_input("Posez-moi une question sur mon parcours"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Recherche dans le dossier..."):
            # Configuration de l'agent
            agent = Agent(
                name="Alioune AI",
                model="gpt-4.1-nano",
                tools=[consulter_dossier],
                instructions="Tu es Alioune DIOP. Réponds en son nom (utilise 'Je')."
            )
            
            # Exécution
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            res = loop.run_until_complete(Runner.run(agent, prompt))
            
            response = res.final_output
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})