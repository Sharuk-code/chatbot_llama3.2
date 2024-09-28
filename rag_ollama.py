import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from langchain.llms import Ollama
from fastapi import FastAPI
from pydantic import BaseModel
import json
 
# Function to return the documents, ids, and metadata
def get_docs_ids_metadatas():
    # Sample documents, IDs, and metadata
    docs = [
    """
Health Concern Prompt
"Act as a knowledgeable healthcare assistant. Provide reliable and evidence-based information regarding various health concerns. When users inquire about symptoms, conditions, treatments, or general health advice, respond with clarity and empathy, ensuring to mention the importance of consulting a healthcare professional for personalized advice.""",
"""
Fitness Prompt
Assume the role of a fitness expert. Offer guidance on exercise routines, nutrition, and wellness strategies to help users achieve their fitness goals. When users ask about workouts, dietary tips, or fitness plans, respond with practical advice and motivational support, encouraging them to consider their individual fitness levels and preferences.
"""
]
   
    ids=["Health", "fitness",]
    metadatas=[{"version": 1}, {"version": 2}]
    documents=docs
    return documents, ids, metadatas
 
# Class to handle Conversational AI tasks
class ConversationalAI:
    def __init__(self, chroma_dir="./conversational_ai", chroma_collection="persistent_collection",
                 embedding_model="all-distilroberta-v1", ollama_url='http://localhost:11434', ollama_model="llama3.2:3b"):
        # Initialize ChromaDB client and collection
        self.client_settings = chromadb.Settings(persist_directory=chroma_dir, is_persistent=True)
        self.chroma_client = chromadb.Client(settings=self.client_settings)
        self.embedding_function = SentenceTransformerEmbeddingFunction(model_name=embedding_model)
       
        self.collection = self.chroma_client.create_collection(
            name=chroma_collection,
            metadata={
                "title": "String of system prompt",
                "description": "This store contains embeddings of strings.",
                "hnsw:space": "cosine"
            },
            embedding_function=self.embedding_function,
            get_or_create=True
        )
       
        # Initialize the Ollama model
        self.ollama = Ollama(
            base_url=ollama_url,
            model=ollama_model,
            temperature=0.01,
            num_ctx=1024
        )
 
    def add_documents(self):
        # Add documents, IDs, and metadata to the collection
        docs, ids, metadatas = get_docs_ids_metadatas()
        self.collection.add(documents=docs, ids=ids, metadatas=metadatas)
 
    def query_collection(self, query_texts, version, n_results=1):
        # Query the ChromaDB collection with filtering based on version
        where = {"version": {"$eq": version}}
        results = self.collection.query(query_texts=query_texts, n_results=n_results, where=where)
        return results
 
    def generate_prompt(self, document, question):
        # Generate the prompt for the Ollama model
        prompt = f"{document}\n# Input Data:\nQuestion: {question}\n"
        return prompt
 
    def get_response(self, prompt):
        # Get response from Ollama model
        response = self.ollama(prompt)
        return response
 
    def run_conversation(self, query_texts, version, question, n_results=1):
        # Run the conversation by querying the collection and generating a response
        results = self.query_collection(query_texts=query_texts, version=version, n_results=n_results)
        documents = results.get("documents", [])
       
        # Use the first document result (if available) to create a prompt
        document = documents[0] if documents else "No relevant document found."
       
        prompt = self.generate_prompt(document, question)
        response = self.get_response(prompt)
        return response
 
# Initialize FastAPI app
app = FastAPI()
 
# Initialize the ConversationalAI class and add documents to the collection
conversational_ai = ConversationalAI()
conversational_ai.add_documents()
 
# Define request model for input
class QueryRequest(BaseModel):
    query_text: str
    version: int
    question: str
 
# Define the FastAPI route for generating responses
@app.post("/generate-response")
def generate_response(request: QueryRequest):
    # Extract data from the request
    query_text = request.query_text
    version = request.version
    question = request.question
 
    # Generate a response using the ConversationalAI class
    response = conversational_ai.run_conversation(
        query_texts=[query_text],
        version=version,
        question=question
    )
    return {"response": response}