import os
from PyPDF2 import PdfReader
from src.vector_store import upload_document
from src.graph_builder import build_graph_from_chunk
 
 
def extract_text_from_pdf(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    text = ""
 
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
 
    return text
 
 
def chunk_text(text: str, chunk_size: int = 2000, overlap: int = 200):
    chunks = []
    start = 0
    text_length = len(text)
 
    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
 
    return chunks
 
 
def ingest_contracts(contracts_path: str):
    print("Starting ingestion...\n")
 
    for file_name in os.listdir(contracts_path):
        if not file_name.endswith(".pdf"):
            continue
 
        file_path = os.path.join(contracts_path, file_name)
        print(f"Ingesting {file_name}...")
 
        # Extract full document text
        full_text = extract_text_from_pdf(file_path)
 
        # Create chunks for vector search
        chunks = chunk_text(full_text)
 
        print(f"Total chunks generated: {len(chunks)}")
 
        # Upload each chunk to Azure AI Search
        for i, chunk in enumerate(chunks):
            print(f"Uploading chunk {i + 1}/{len(chunks)}")
            upload_document(chunk)
 
        # Build graph ONCE per document
        print("Building knowledge graph...")
        build_graph_from_chunk(full_text)
 
        print(f"Finished processing {file_name}\n")
 
    print("Ingestion complete.")