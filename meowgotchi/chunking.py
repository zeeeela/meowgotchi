import PyPDF2
import os
from meowgotchi.paths import PAPER_PATH


def chunk_text(folder=PAPER_PATH, chunk_size=500, overlap=50):
    # Implementation for chunking text from a folder of PDF files
    for filename in os.listdir(folder):

        if filename.endswith(".pdf"):
            pdf = PyPDF2.PdfReader(os.path.join(folder, filename))
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                text += page_text
            # Now chunk the text
            chunks_temp = []
            for i in range(0, len(text), chunk_size - overlap):
                chunks_temp.append(text[i:i + chunk_size])
            yield filename, chunks_temp
   

if __name__ == "__main__":
    #Test the chunking function
    folder = PAPER_PATH
    chunks = list(chunk_text(folder))
    for filename, chunks_temp in chunks:
        print(f"{filename} has {len(chunks_temp)} chunks.")

    print(len(chunks))
        
    