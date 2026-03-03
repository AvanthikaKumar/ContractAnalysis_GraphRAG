from PyPDF2 import PdfReader
 
 
def extract_text_from_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""
 
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
 
    return text
 
 
def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100):
    chunks = []
    start = 0
 
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
 
    return chunks