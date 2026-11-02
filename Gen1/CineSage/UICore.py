
import os
from pathlib import Path
from typing import List, Optional

import streamlit as st
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser


# Load environment variables
APP_DIR = Path(__file__).resolve().parent
PROJECT_DIR = APP_DIR.parent
ENV_PATH = PROJECT_DIR / ".env"

load_dotenv(ENV_PATH, override=True)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()


# Streamlit configuration
st.set_page_config(
    page_title="CineSage AI",
    page_icon="🎬",
    layout="centered"
)


# Pydantic Schema
class Movie(BaseModel):

    title: str = Field(description="Movie title")

    release_year: Optional[int] = Field(
        default=None,
        description="Movie release year"
    )

    genre: List[str] = Field(default_factory=list)

    director: Optional[str] = None

    cast: List[str] = Field(default_factory=list)

    rating: Optional[float] = None

    summary: str = Field(
        description="Quick movie summary in 2-3 sentences"
    )


# Gemini Model
@st.cache_resource
def get_model(api_key):

    return init_chat_model(
        model="gemini-3.6-flash",
        model_provider="google_genai",
        google_api_key=api_key
    )


# Pydantic Output Parser
parser = PydanticOutputParser(
    pydantic_object=Movie
)


# System Prompt
system_prompt = """
You are an intelligent movie information extraction assistant.

Extract the following information from the user's paragraph:

1. Movie title
2. Release year
3. Genre
4. Director
5. Cast
6. Rating
7. Quick summary

IMPORTANT RULES:

- Extract information only from the provided paragraph.
- Never invent facts.
- Do not use external knowledge.
- If release year, director, or rating is unavailable, return null.
- If genre or cast is unavailable, return an empty list.
- Correct obvious spelling and grammatical mistakes.
- Generate a clear summary in 2-3 sentences.
- Do not assume character names from actor names.

Return the result according to these formatting instructions:

{format_instructions}
"""


# Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        (
            "human",
            "Extract movie information from this paragraph:\n\n{paragraph}"
        )
    ]
)


# Streamlit Styling
st.markdown(
    """
    <style>
        .stApp {
            background: #0b0d12;
        }

        .main .block-container {
            max-width: 850px;
            padding-top: 2.5rem;
        }

        .cine-title {
            font-size: 2rem;
            font-weight: 700;
            color: #f4f5f7;
        }

        .cine-subtitle {
            color: #9ba3b4;
            font-size: 0.9rem;
            margin-bottom: 1.5rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# Application Heading
st.markdown(
    '<div class="cine-title">🎬 CineSage AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="cine-subtitle">Movie Information Extraction</div>',
    unsafe_allow_html=True
)


# User Input
with st.container(border=True):

    paragraph = st.text_area(
        "Movie Paragraph",
        placeholder="Paste your movie description here...",
        height=230
    )

    analyze = st.button(
        "Generate JSON",
        type="primary",
        use_container_width=True
    )


# Generate Structured JSON
if analyze:

    if not paragraph.strip():

        st.warning("Please enter a movie paragraph.")

    elif not ENV_PATH.is_file():

        st.error(f".env file not found: {ENV_PATH}")

    elif not GOOGLE_API_KEY:

        st.error("GOOGLE_API_KEY was not found.")

    else:

        try:

            with st.spinner("Extracting movie information..."):

                model = get_model(GOOGLE_API_KEY)

                # Connect prompt, model and parser
                chain = prompt | model | parser

                # Invoke the chain
                movie = chain.invoke(
                    {
                        "paragraph": paragraph.strip(),
                        "format_instructions":
                            parser.get_format_instructions()
                    }
                )

                # Convert Pydantic object into JSON
                json_output = movie.model_dump_json(
                    indent=2
                )

            # Display JSON
            st.subheader("Generated JSON")

            st.code(
                json_output,
                language="json"
            )

        except Exception as error:

            st.error(
                f"Error: {type(error).__name__}: {error}"
            )
