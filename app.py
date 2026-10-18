import streamlit as st
import requests

# Titre de l'application
st.title("💬 Chatbot FastAPI")

# URL de ton API FastAPI
FASTAPI_URL = "http://localhost:8000/ask"

# Initialisation de l'historique de discussion
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage des messages de l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Entrée utilisateur (input du chat)
if prompt := st.chat_input("Posez votre question..."):
    # 1. Ajouter et afficher le message de l'utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # 2. Requête vers la route GET /ask de FastAPI
    with st.chat_message("assistant"):
        with st.spinner("Réflexion en cours..."):
            try:
                response = requests.get(FASTAPI_URL, params={"question": prompt})
                
                if response.status_code == 200:
                    data = response.json()
                    # On récupère la réponse (adapte la clé "response" selon ton retour d'API)
                    bot_response = data.get("response", data)
                    print(bot_response)
                    bot_response=bot_response[0]["text"]
                else:
                    bot_response = f"Erreur {response.status_code}: Impossible de contacter l'API."
            except Exception as e:
                bot_response = f"Erreur de connexion : {e}"

            # Afficher et sauvegarder la réponse de l'assistant
            st.write(bot_response)
            st.session_state.messages.append({"role": "assistant", "content": bot_response})