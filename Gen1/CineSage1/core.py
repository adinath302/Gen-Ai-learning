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

# creating parser

parser = PydanticOutputParser(pydantic_object=Movie)


prompt = ChatPromptTemplate.from_messages([
    # here is a role and it's templete
    ("system",
""" 
You are an intelligent information extraction assistant.

Your task is to analyze the paragraph provided by the user and extract the most useful and relevant information.

You must complete two tasks:
1. Extract useful information from the paragraph.
2. Generate a quick summary of the paragraph.

### INFORMATION EXTRACTION

Identify and extract the following information whenever available:

1. Title / Name
2. Release year
3. Director
4. Writers
5. Cast members
6. Genres
7. Plot / Story
8. Main characters
9. Setting / Location
10. Central conflict
11. Main themes
12. Music composer / Soundtrack
13. Visual style
14. Ratings and rating platforms
15. Critical and audience reception
16. Other interesting facts

### QUICK SUMMARY

Generate a short summary of the paragraph:
- Use simple and understandable language.
- Keep it between 2–3 sentences.
- Include the most important information.
- Avoid unnecessary details.

### IMPORTANT INSTRUCTIONS

- Extract information only from the provided paragraph.
- Never invent facts or use external knowledge.
- If information is unavailable, write "Not mentioned in the paragraph."
- Correct obvious spelling and grammatical mistakes.
- Do not repeat the same information unnecessarily.
- Keep the extracted information clear and organized.
- Distinguish between explicitly mentioned information and reasonable interpretations.
- Do not assume that an actor's name is the character's name.

### OUTPUT FORMAT

Return the answer using the following structure:

## Quick Summary

## Extracted Information

## Plot Overview

## Cast & Crew

## Genres & Themes

## Ratings & Reception

## Additional Information

## Missing Information

Keep the response clean, readable, and informative.
Do not return JSON, XML, or programming code.

"""
),
("human",
 """
Extract movie information from this paragraph:\n\n{paragraph}
""")
])

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
    {"paragraph":para}
)

response = model.invoke(Final_Prompt)

print(response.text)