import os
from dotenv import load_dotenv
# 🎯 Modern way to call the API without using langchain_community
from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings

load_dotenv()

# Initialize the cloud-based API connection
embedding = HuggingFaceEndpointEmbeddings(
    model="sentence-transformers/all-MiniLM-L6-v2",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
)

texts = [
    "This is Part 1 of our complete Generative AI series, where we focus on the core fundamentals required before moving to advanced topics like RAG and production-level AI systems.",
    "Whether you are a beginner or an aspiring AI developer, this ",
    "session will help you understand how real AI applications are built from scratch.",
]

# Get vectors from the cloud serverless API
vector = embedding.embed_documents(texts)

print("Success! Your cloud vector has been created.")
print(f"Vector dimensions: {(vector)}")
