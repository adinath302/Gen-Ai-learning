# Prompt templates (CineSage Ai Project)

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model

load_dotenv()

model = init_chat_model (
    model="gemini-3.6-flash",
   model_provider="google_genai",
)

prompt = ChatPromptTemplate.from_messages(
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
)


para = input("Give your paragraph : ")

Final_Prompt = prompt.invoke(
    {"paragraph":para}
)

response = model.invoke(Final_Prompt)

print(response.text)