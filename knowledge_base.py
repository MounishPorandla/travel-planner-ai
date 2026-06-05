import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os

model = SentenceTransformer('all-MiniLM-L6-v2')

def load_destinations():
    """Read raw contents from destinations.txt"""
    with open("data/destinations.txt", "r") as f:
        content = f.read()

    destinations = content.strip().split("\n\n")
    return destinations

def build_knowledge_base():
    """Convert destinations to vectors and store in FAISS"""

    destinations = load_destinations()

    print(f"Loading {len(destinations)} Destinations...")

    #Convert each destination text to a vector
    embeddings = model.encode(destinations)

    embeddings = np.array(embeddings).astype('float32')

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    print(f"Knowledge base built. {index.ntotal} destinations indexed.")

    return index, destinations

def search_destinations(query, index, destinations, k=2):
    """Find k most relevant destinations for a query"""

    query_vector = model.encode([query])
    query_vector = np.array(query_vector).astype('float32')

    # Search FAISS for k nearest neighbours

    distances, indices = index.search(query_vector, k)

    results = []
    for i in indices[0]:
        if i < len(destinations):
            results.append(destinations[i])

    return results


