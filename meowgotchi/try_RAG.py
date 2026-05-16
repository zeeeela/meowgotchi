from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import requests
import json
import pickle
import os
from meowgotchi.chunking import chunk_text
from meowgotchi.config import OLLAMA_MODEL_RESEARCH_ASSISTANT, OLLAMA_RESEARCH_ASSISTANT_URL
from meowgotchi.paths import PAPER_PATH

CACHE_FILE = os.path.join(PAPER_PATH, ".rag_cache.pkl")

# Load embedding model once at startup (not on every query)
embed_model = SentenceTransformer('all-MiniLM-L6-v2')


def build_and_cache_index():
    """Build embeddings and FAISS index, save to cache"""
    print("Building embeddings index (this may take a moment)...")
    
    chunks = list(chunk_text(PAPER_PATH))
    all_chunks = []
    for filename, chunks_temp in chunks:
        all_chunks.extend(chunks_temp)
    
    embeddings = embed_model.encode(all_chunks)
    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(np.array(embeddings).astype('float32'))
    
    # Cache everything
    cache_data = {
        'chunks': all_chunks,
        'index': index,
    }
    
    with open(CACHE_FILE, 'wb') as f:
        pickle.dump(cache_data, f)
    
    print(f"Cache saved with {len(all_chunks)} chunks")
    return all_chunks, index


def load_or_build_index():
    """Load cached index or build new one"""
    if os.path.exists(CACHE_FILE):
        print("Loading cached embeddings...")
        with open(CACHE_FILE, 'rb') as f:
            cache_data = pickle.load(f)
        return cache_data['chunks'], cache_data['index']
    else:
        print("No cache found, building new index...")
        return build_and_cache_index()


def main(query):
    """Query the RAG system using cached embeddings"""
    all_chunks, index = load_or_build_index()
    
    query_emb = embed_model.encode([query])[0]
    distances, indices = index.search(np.array([query_emb]).astype('float32'), k=3)
    
    relevant_chunks = [all_chunks[i] for i in indices[0]]
    prompt = f"""Based on: {' '.join(relevant_chunks)}

Question: {query}

IMPORTANT: Answer in exactly 5 sentences or less. Be concise."""
    
    response = requests.post(
        OLLAMA_RESEARCH_ASSISTANT_URL,
        json={
            "model": OLLAMA_MODEL_RESEARCH_ASSISTANT,
            "prompt": prompt,
            "temperature": 0.1,
            "num_predict": 100,
        },
        stream=True,
        timeout=60,
    )
    
    if response.status_code != 200:
        raise RuntimeError(
            f"Ollama request failed ({response.status_code}): {response.text}"
        )
    
    output = []
    for line in response.iter_lines(decode_unicode=True):
        if not line:
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue
        if 'response' in data:
            output.append(data['response'])
    
    return ''.join(output)


if __name__ == "__main__":
    query = "What is the main finding?"
    answer = main(query)
    print(answer)