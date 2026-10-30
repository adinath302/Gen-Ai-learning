# from dotenv import load_dotenv

# load_dotenv()

# from langchain_groq import ChatGroq

# model = ChatGroq(
#    model = "openai/gpt-oss-120b",
    
# )

# response = model.invoke("What is philosophy ?")

# print(response.content);


from dotenv import load_dotenv

load_dotenv()

from langchain_mistralai import ChatMistralAI

model = ChatMistralAI(
   model = "mistral-small-2506",   
)

response = model.invoke("What is philosophy ?")

print(response.content);