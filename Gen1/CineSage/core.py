# Prompt templates (CineSage Ai Project)
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
# using pydantic it to create Schema
from pydantic import BaseModel
from typing import List,Optional
# for pydantic parser
from langchain_core.output_parsers import PydanticOutputParser
load_dotenv()

model = init_chat_model (
    model="gemini-3.6-flash",
   model_provider="google_genai",
)


# Schema for Ai -
class Movie(BaseModel):
    title:str
    realease_year:Optional[int]
    genre:List[str]
    director:Optional[str]
    cast:List[str]
    rating:Optional[float]
    summary:str

# creating output parser
parser = PydanticOutputParser(pydantic_object=Movie)

prompt = ChatPromptTemplate.from_messages([
    ('system',"""
Extract movie information from the paragraph
{format_instructions}
"""),
(
    "human","{paragraph}"
)]
)

# Automated file reader
file_path = "c:/Code/Generative Ai/Gen1/CineSage/movie.txt"

# This automatically handles checking if the file exists
if not os.path.exists(file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("Paste your full paragraph here.")
    print(f"Empty file created! Please open '{file_path}', paste your movie description, save it, and run this script again.")
else: 
    print(f"Reading movie data directly from: {file_path} ...")
    with open(file_path, "r", encoding="utf-8") as f:
        para = f.read()


Final_Prompt = prompt.invoke(
    {
        "paragraph":para,
     'format_instructions':parser.get_format_instructions()
     }
)

response = model.invoke(Final_Prompt)

print(response.text)