import os
import uuid
from dotenv import load_dotenv
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from azure.core.credentials import AzureKeyCredential
from src.llm_utils import generate_embedding
 
load_dotenv()
 
# Initialize Azure AI Search client
search_client = SearchClient(
    endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
    index_name=os.getenv("AZURE_SEARCH_INDEX"),
    credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_KEY"))
)
 
 
def upload_document(content: str):
    """
    Uploads a single chunk with its embedding to Azure AI Search.
    """
    embedding = generate_embedding(content)
 
    document = {
        "id": str(uuid.uuid4()),
        "content": content,
        "embedding": embedding   # Must match index field name
    }
 
    search_client.upload_documents(documents=[document])
 
 
def search_documents(query: str, top_k: int = 3):
    """
    Performs vector similarity search using the new SDK syntax.
    """
    query_embedding = generate_embedding(query)
 
    vector_query = VectorizedQuery(
        vector=query_embedding,
        k_nearest_neighbors=top_k,
        fields="embedding"   # Must match index field
    )
 
    results = search_client.search(
        search_text=None,
        vector_queries=[vector_query]
    )
 
    documents = []
 
    for result in results:
        documents.append({
            "content": result["content"]
        })
 
    return documents