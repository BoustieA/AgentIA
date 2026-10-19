from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
import os

load_dotenv()


ROOT_DIR = "politique"        # Dossier principal contenant les sous-dossiers
CHROMA_ROOT = "./chroma_db"   # Dossier racine pour stocker les bases vectorielles
# Vérification si le dossier principal existe
if os.path.exists(ROOT_DIR):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Initialisation des embeddings partagés (locaux et gratuits)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    vectorstores_par_politique = {}
    # Parcourt dynamiquement tous les sous-dossiers de "politique" (ex: politique1, politique2...)
    for nom_politique in os.listdir(ROOT_DIR):
        dossier_politique = os.path.join(ROOT_DIR, nom_politique)
        
        # On s'assure que c'est bien un dossier
        if os.path.isdir(dossier_politique):
            persist_dir = os.path.join(CHROMA_ROOT, nom_politique)
            
            print(f"\n--- Traitement pour : {nom_politique} ---")
            
            # 1. Chargement ou création de la base vectorielle pour ce politique
            if os.path.exists(persist_dir) and os.listdir(persist_dir):
                print(f"Chargement de la base Chroma existante pour {nom_politique}...")
                vectorstore = Chroma(
                    persist_directory=persist_dir,
                    embedding_function=embeddings
                )
            else:
                print(f"Création de la base Chroma à partir des PDF de {nom_politique}...")
                # Chargement récursif des PDF de ce sous-dossier (et ses éventuels sous-dossiers)
                loader = DirectoryLoader(
                    dossier_politique, 
                    glob="**/*.pdf", 
                    loader_cls=PyPDFLoader
                )
                docs = loader.load()
                
                if docs:
                    splits = text_splitter.split_documents(docs)
                    vectorstore = Chroma.from_documents(
                        documents=splits,
                        embedding=embeddings,
                        persist_directory=persist_dir
                    )
                    print(f"{len(docs)} documents indexés pour {nom_politique}.")
                else:
                    print(f"Aucun PDF trouvé dans le dossier de {nom_politique}.")
                    continue
            
            # Stockage de la base vectorielle prête à l'emploi dans un dictionnaire
            vectorstores_par_politique[nom_politique] = vectorstore
else:
    print(f"Le dossier racine '{ROOT_DIR}' est introuvable.")