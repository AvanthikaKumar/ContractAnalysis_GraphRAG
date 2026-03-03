from src.vector_store import search_documents
from src.llm_utils import generate_chat_response
 
 
def rag_agent(user_query: str):
    search_results = search_documents(user_query)
 
    if not search_results:
        return "No relevant documents found."
 
    context = "\n\n".join([doc["content"] for doc in search_results])
 
    prompt = f"""
Use only the following contract context to answer the question.
 
Context:
{context}
 
Question:
{user_query}
"""
 
    response = generate_chat_response(prompt)
    return response