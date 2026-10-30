from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

# Load your GOOGLE_API_KEY from the .env file
load_dotenv()

# Set up the free Google Embedding model
embeddings = GoogleGenerativeAIEmbeddings (
    model="models/gemini-embedding-001"
)

texts=[
    "This is Part 1 of our complete Generative AI series, where we focus on the core fundamentals required before moving to advanced topics like RAG and production-level AI systems.",
"Whether you are a beginner or an aspiring AI developer, this ",
"session will help you understand how real AI applications are built from scratch.",
] 

# Generate the embedding vector
vector = embeddings.embed_documents(texts)

# Print the list of numbers (vector) and see its size
print(f"Vector Length: {len(vector)}")
print(f"First few numbers: {vector[:5]}")
