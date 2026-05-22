import os
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
CHROMA_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_data")
DOCS_DIR = "knowledge/docs"

def ingest():
    loader = DirectoryLoader(DOCS_DIR, glob="*.txt", loader_cls=TextLoader)
    docs = loader.load()
    if not docs:
        print("No documents found in knowledge/docs/. Creating a sample doc.")
        # Create a sample document if none exist
        sample_doc = "knowledge/docs/aws_to_azure.txt"
        with open(sample_doc, "w") as f:
            f.write("Migrating from AWS to Azure involves re-architecting IAM roles to Azure AD. Map EC2 to VMs, S3 to Blob Storage.")
        loader = DirectoryLoader(DOCS_DIR, glob="*.txt", loader_cls=TextLoader)
        docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(docs)

    embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=OLLAMA_HOST)
    Chroma.from_documents(chunks, embeddings, persist_directory=CHROMA_PATH)
    print(f"Ingested {len(chunks)} chunks into ChromaDB at {CHROMA_PATH}")

if __name__ == "__main__":
    ingest()
