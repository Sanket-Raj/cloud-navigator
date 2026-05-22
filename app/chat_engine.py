import os
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from app.intent_parser import parse_intent
from app.migration_planner import generate_runbook
from app.cost_estimator import estimate_cost
from app.risk_scorer import score_risk

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "mistral")
CHROMA_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_data")

def load_rag_chain():
    embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=OLLAMA_HOST)
    vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    llm = Ollama(model=MODEL_NAME, base_url=OLLAMA_HOST, temperature=0.2)
    prompt_template = """You are CloudNavigator, a multi-cloud migration expert.
Use the following pieces of context to answer the user's question.
If you don't know the answer, just say you don't know.

Context:
{context}

Question: {question}
Answer:"""
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    return RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, chain_type_kwargs={"prompt": PROMPT})

def process_query(message: str) -> dict:
    intent = parse_intent(message)
    qa_chain = load_rag_chain()
    rag_reply = qa_chain.invoke(message)["result"]
    runbook = None
    if intent["source"] and intent["target"]:
        runbook = generate_runbook(intent["source"], intent["target"], intent["service"])
    cost = estimate_cost(intent["source"], intent["target"], intent["service"])
    risk = score_risk(intent["source"], intent["target"], intent["service"])
    return {
        "reply": rag_reply,
        "runbook": runbook,
        "cost_comparison": cost,
        "risk_score": risk
    }
