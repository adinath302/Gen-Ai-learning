
import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate


# --------------------------------------------------
# Load environment variables from Gen1/.env
# --------------------------------------------------

APP_DIR = Path(__file__).resolve().parent
PROJECT_DIR = APP_DIR.parent
ENV_PATH = PROJECT_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH, override=True)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()


# --------------------------------------------------
# Streamlit configuration
# --------------------------------------------------

st.set_page_config(
    page_title="CineSage AI",
    page_icon="🎬",
    layout="centered",
)


# --------------------------------------------------
# Initialize Gemini model
# --------------------------------------------------

@st.cache_resource
def get_model(api_key):
    return init_chat_model(
        model="gemini-3.6-flash",
        model_provider="google_genai",
        google_api_key=api_key,
    )


# --------------------------------------------------
# System prompt
# --------------------------------------------------

system_prompt = """
You are an intelligent information extraction assistant.

Your task is to analyze the paragraph provided by the user
and extract its most useful and relevant movie information.

Complete two tasks:
1. Extract useful information from the paragraph.
2. Generate a quick summary of the paragraph.

### INFORMATION TO EXTRACT

Identify the following information whenever available:

1. Movie title
2. Release year
3. Director
4. Writers
5. Cast members
6. Genres
7. Plot or story
8. Main characters
9. Setting or location
10. Central conflict
11. Main themes
12. Music composer or soundtrack
13. Visual style
14. Ratings and rating platforms
15. Critical and audience reception
16. Other interesting facts

### QUICK SUMMARY

- Write 2–3 sentences.
- Use simple and understandable language.
- Include the most important information.
- Avoid unnecessary details.

### IMPORTANT INSTRUCTIONS

- Extract information only from the provided paragraph.
- Never invent facts or use external knowledge.
- If information is unavailable, write
  "Not mentioned in the paragraph."
- Correct obvious spelling and grammatical mistakes.
- Do not repeat the same information unnecessarily.
- Keep the extracted information clear and organized.
- Distinguish explicitly mentioned information from
  reasonable interpretations.
- Do not assume an actor's name is the character's name.

### OUTPUT FORMAT

Return the answer using exactly these sections:

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


# --------------------------------------------------
# Create prompt template
# --------------------------------------------------

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        (
            "human",
            "Extract movie information from this paragraph:\n\n{paragraph}",
        ),
    ]
)


# --------------------------------------------------
# Custom CSS
# --------------------------------------------------

st.markdown(
    """
    <style>
        .stApp {
            background: #0b0d12;
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        .main .block-container {
            max-width: 850px;
            padding-top: 3rem;
            padding-bottom: 3rem;
        }

       /* Main application heading */
.cine-title {
    font-size: 2rem;
    font-weight: 700;
    letter-spacing: -0.8px;
    color: #f4f5f7;
    margin-bottom: 0.2rem;
}

/* Subtitle */
.cine-subtitle {
    color: #9ba3b4;
    font-size: 0.9rem;
    margin-bottom: 1.5rem;
}

/* Extracted information headings */
.stMarkdown h1 {
    font-size: 1.5rem;
}

.stMarkdown h2 {
    font-size: 1.2rem;
}

.stMarkdown h3 {
    font-size: 1.05rem;
}

/* Paragraph and list text */
.stMarkdown p,
.stMarkdown li {
    font-size: 0.95rem;
    line-height: 1.7;
}

        div[data-testid="stTextArea"] textarea {
            background: #141923;
            color: #f4f5f7;
            border: 1px solid #30394a;
            border-radius: 12px;
        }

        div[data-testid="stButton"] button {
            min-height: 3rem;
            border-radius: 10px;
            font-weight: 650;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: #111620;
            border: 1px solid #283142;
            border-radius: 14px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Application heading
# --------------------------------------------------

st.markdown(
    '<div class="cine-title">🎬 CineSage AI</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="cine-subtitle">'
    'Movie information extraction and quick summaries'
    '</div>',
    unsafe_allow_html=True,
)


# --------------------------------------------------
# User input
# --------------------------------------------------

with st.container(border=True):

    paragraph = st.text_area(
        "Movie paragraph",
        placeholder="Paste a movie description or paragraph here...",
        height=230,
    )

    analyze_clicked = st.button(
        "Analyze movie",
        type="primary",
        use_container_width=True,
    )



# --------------------------------------------------
# Analyze movie paragraph
# --------------------------------------------------

if analyze_clicked:

    if not paragraph.strip():
        st.warning("Please enter a paragraph before analyzing.")

    elif not ENV_PATH.is_file():
        st.error(f".env file not found: {ENV_PATH}")

    elif not GOOGLE_API_KEY:
        st.error(f"GOOGLE_API_KEY was not found in {ENV_PATH}")

    else:

        try:
            with st.spinner("Analyzing the paragraph..."):

                model = get_model(GOOGLE_API_KEY)

                final_prompt = prompt.invoke(
                    {
                        "paragraph": paragraph.strip()
                    }
                )

                response = model.invoke(final_prompt)

                # Extract generated text
                content = response.content

                if isinstance(content, str):
                    result = content

                elif isinstance(content, list):
                    text_parts = []

                    for block in content:
                        if isinstance(block, dict):
                            if block.get("type") == "text":
                                text_parts.append(
                                    block.get("text", "")
                                )

                        elif isinstance(block, str):
                            text_parts.append(block)

                    result = "\n\n".join(text_parts)

                else:
                    result = str(content)

            # Display result
            if result.strip():
                st.markdown("### Movie Analysis")
                st.markdown(result)
            else:
                st.error("The model returned an empty response.")

        except Exception as error:
            st.error(
                f"Analysis failed: {type(error).__name__}: {error}"
            )
