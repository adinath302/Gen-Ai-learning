from dotenv import load_dotenv

load_dotenv()

from langchain.chat_models import init_chat_model

model = init_chat_model(
   model = "gemini-3.6-flash",
   temperature = 0.9,
    model_provider="google_genai",
)

response = model.invoke("write a poem on ai?")

print(response.content)