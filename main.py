from fastapi import FastAPI, HTTPException

from langchain.agents import create_agent
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.tools.retriever import create_retriever_tool
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings


import os

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PERSIST_DIRECTORY = "./chroma_db"

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


print("Chargement de la base vectorielle depuis le disque...")
vectorstore = dict()
    
    # Vérification si le dossier principal existe
if os.path.exists(PERSIST_DIRECTORY):
    # Parcourt dynamiquement tous les sous-dossiers de "politique" (ex: politique1, politique2...)
    for nom_politique in os.listdir(PERSIST_DIRECTORY):
        dossier_politique = os.path.join(PERSIST_DIRECTORY, nom_politique)
        
        # On s'assure que c'est bien un dossier
        if os.path.isdir(dossier_politique):
            print(f"\n--- Chargement de la base vectorielle pour : {nom_politique} ---")
            persist_dir = os.path.join(PERSIST_DIRECTORY, nom_politique)
            
            if os.path.exists(persist_dir) and os.listdir(persist_dir):
                print(f"Chargement de la base Chroma existante pour {nom_politique}...")
                vectorstore[nom_politique] = Chroma(
                    persist_directory=persist_dir,
                    embedding_function=embeddings
                )
            else:
                print(f"Aucune base Chroma trouvée pour {nom_politique}.")

#Retriever pour l'agent

retriever = {nom_politique: vectorstore[nom_politique].as_retriever(search_kwargs={"k": 3}) for nom_politique in vectorstore}

pdf_tool = [create_retriever_tool(
    retriever[nom_politique],
    name="search_pdf_document"+nom_politique,
    description="Search and extract relevant information from the uploaded PDF document.",
) for nom_politique in retriever]
tools = pdf_tool


agent = create_agent(
    model="google_genai:gemini-3.1-flash-lite",
    tools=tools,
    system_prompt="You are a helpful assistant. " \
    "Tu dois baser ta réponse sur les réponses des outils qui te sont fournis." \
    "Pour chaque question, utilise tout les outils et concatènela réponse de chaque outil en précisant le nom du politique correspondant.",
)







app = FastAPI(
    title="API Agent",
    description="API to retrieve/refresh data and predict from stored model.",
    version="1.0.0"
)





@app.get("/ask")
def ask_agent(question: str):
    try:
        # L'agent décide tout seul d'appeler l'outil PDF si la question le nécessite
        result = agent.invoke(
            {"messages": [{"role": "user", "content": question}]}
        )
        last_message = result["messages"][-1]
        response_content = getattr(last_message, "content", str(last_message))
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "question": question,
        "response": response_content
    }