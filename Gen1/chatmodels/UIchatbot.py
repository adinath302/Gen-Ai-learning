
import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import (
    AIMessage,
    SystemMessage,
    HumanMessage
)

load_dotenv()

# ---------------- MODEL SETUP ----------------

@st.cache_resource
def get_model():
    return init_chat_model(
        model="gemini-3.6-flash",
        model_provider="google_genai",
    )

model = get_model()

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Mood AI Chatbot",
    page_icon="🤖",
    layout="centered",
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #101426 0%, #171d35 55%, #101426 100%);
        color: white;
    }

    .block-container {
        max-width: 850px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        text-align: center;
        padding: 25px 10px 20px;
    }

    .hero h1 {
        font-size: 44px;
        font-weight: 800;
        color: white;
        margin-bottom: 8px;
    }

    .hero h1 span {
        background: linear-gradient(90deg, #8b5cf6, #38bdf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero p {
        color: #a5aec7;
        font-size: 16px;
    }

    .mode-heading {
        font-size: 20px;
        font-weight: 700;
        color: white;
        margin-bottom: 5px;
    }

    .mode-description {
        color: #a5aec7;
        font-size: 13px;
        margin-bottom: 15px;
    }

    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.045);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 12px;
        margin-bottom: 12px;
    }

    [data-testid="stChatInput"] {
        border-radius: 16px;
    }

    .stCaption {
        color: #9ca3af;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255, 255, 255, 0.035);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 18px;
    }

    div[data-testid="stRadio"] label {
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

st.markdown("""
<div class="hero">
    <h1>Welcome to <span>Mood AI</span> 🤖</h1>
    <p>One chatbot. Three personalities. Choose your experience.</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ---------------- AI MODES ----------------

modes = {
    "😡 Angry Mode": "You are deeply provoked, furious, or filled with righteous anger AI agent. You respond aggressively and impatiently.",
    
    "😂 Funny Mode": "You are a very funny AI agent. You respond with humor and jokes.",
    
    "😢 Sad Mode": "You are a sad AI agent. You respond in a sad and emotional tone."
}

if st.button("🔄 Reset Chat & Change Mode", use_container_width=True):

    st.session_state.messages = []
    st.session_state.chat_started = False
    st.session_state.chat_ended = False
    st.session_state.active_mode = None

    st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_started" not in st.session_state:
    st.session_state.chat_started = False

if "chat_ended" not in st.session_state:
    st.session_state.chat_ended = False

if "active_mode" not in st.session_state:
    st.session_state.active_mode = None

# Mode selection UI
with st.container(border=True):

    st.markdown(
        '<div class="mode-heading">Choose Your AI Personality</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="mode-description">Select how you want your AI assistant to behave.</div>',
        unsafe_allow_html=True
    )

    choice = st.radio(
        "AI Mode",
        options=list(modes.keys()),
        horizontal=True,
        label_visibility="collapsed",
        disabled=st.session_state.chat_started
    )

    st.caption(modes[choice])

    # Initialize or update the personality
if not st.session_state.chat_started and st.session_state.active_mode != choice:

    st.session_state.active_mode = choice

    st.session_state.messages = [
        SystemMessage(content=modes[choice])
    ]

# Initialize chat history with selected personality
if st.session_state.messages is None:
    st.session_state.messages = [
        SystemMessage(content=modes[choice])
    ]

st.divider()

# ---------------- CHAT HISTORY ----------------

st.subheader("💬 Your Conversation")

for message in st.session_state.messages:

    if isinstance(message, HumanMessage):
        with st.chat_message("user", avatar="👤"):
            st.markdown(message.content)

    elif isinstance(message, AIMessage):
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(message.content)

# ---------------- CHAT INPUT ----------------

prompt = st.chat_input(
    "Type your message here...",
    disabled=st.session_state.chat_ended
)

if prompt:

    # Store user message
    st.session_state.messages.append(
        HumanMessage(content=prompt)
    )

    st.session_state.chat_started = True

    # Exit condition
    if prompt == "0":
        st.session_state.chat_ended = True
        st.rerun()

    # Display user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant", avatar="🤖"):

        with st.spinner("AI is thinking..."):
            try:
                response = model.invoke(
                    st.session_state.messages
                )

                st.markdown(response.text)

                # Save AI response
                st.session_state.messages.append(
                    AIMessage(content=response.text)
                )

            except Exception as e:
                st.error(f"Something went wrong: {e}")

# ---------------- EXIT MESSAGE ----------------

if st.session_state.chat_ended:
    st.warning("👋 Conversation ended. Thanks for chatting!")

