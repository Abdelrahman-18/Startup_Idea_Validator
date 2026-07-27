"""
AI Startup Validator — Streamlit frontend
Business Analysis + SWOT + Investment Readiness, powered by RAG over an
uploaded PDF, using a free Hugging Face Inference API model.

All RAG/chain/model logic lives in core/ — this file is UI only.

Layout: chat is the primary surface (always visible, ChatGPT-style),
with the three analysis chains living as a secondary panel underneath.
See the accompanying explanation for what changed and why.
"""

import os
import tempfile

import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage

from core.llm import load_chat_model as _load_chat_model, load_embeddings as _load_embeddings, DEFAULT_MODEL, EMBEDDING_MODEL
from core.rag import build_vectorstore, retrieve_context
from core.chains import (
    business_prompt, swot_prompt, investment_prompt,
    business_parser, swot_parser, investment_parser,
    RETRIEVAL_QUERIES, run_chain, generate_chat_answer,
)

load_dotenv()

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

st.set_page_config(page_title="AI Startup Validator", page_icon="🚀", layout="wide")


def get_hf_token() -> str:
    """Secrets (deployed) take priority over .env (local dev)."""
    try:
        if "HUGGINGFACEHUB_API_TOKEN" in st.secrets:
            return st.secrets["HUGGINGFACEHUB_API_TOKEN"]
    except st.errors.StreamlitSecretNotFoundError:
        pass
    return os.getenv("HUGGINGFACEHUB_API_TOKEN", "")


# ---------------------------------------------------------------------------
# Theme — dark, minimal, AI-dashboard styling
# ---------------------------------------------------------------------------

THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg: #090C14;
    --bg-elevated: #0F1420;
    --card: #141926;
    --card-hover: #181E2E;
    --border: #232A3D;
    --accent: #6366F1;
    --accent-hover: #4F46E5;
    --accent-soft: rgba(99, 102, 241, 0.13);
    --gold: #F0B429;
    --gold-soft: rgba(240, 180, 41, 0.13);
    --text: #EDF0F7;
    --text-secondary: #8891A7;
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse 900px 500px at 50% -10%, rgba(99,102,241,0.10), transparent),
        var(--bg);
    color: var(--text);
}

/* Hide default Streamlit chrome so this reads as a product, not a demo */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }

/* Center the app in a comfortable reading column */
.block-container {
    max-width: 880px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--bg-elevated);
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] .stButton button {
    width: 100%;
}

/* Headings use Sora for a distinct, less generic display voice */
h1, h2, h3 {
    color: var(--text) !important;
    font-family: 'Sora', 'Inter', sans-serif;
    letter-spacing: -0.02em;
    font-weight: 700;
}
p, span, label { color: var(--text); }

/* Buttons */
.stButton button, .stDownloadButton button {
    background: var(--accent);
    color: #ffffff;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    padding: 0.5rem 1.1rem;
    transition: background 0.15s ease, transform 0.1s ease;
}
.stButton button:hover, .stDownloadButton button:hover {
    background: var(--accent-hover);
    color: #ffffff;
    transform: translateY(-1px);
}
.stButton button:disabled {
    background: var(--border);
    color: var(--text-secondary);
    transform: none;
}

/* Text input / file uploader */
.stTextInput input {
    background: var(--bg);
    color: var(--text);
    border: 1px solid var(--border);
    border-radius: 8px;
}
section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
    background: var(--bg);
    border: 1px dashed var(--border);
    border-radius: 10px;
}

/* Tabs -> pill style */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    border-bottom: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 8px 8px 0 0;
    color: var(--text-secondary);
    padding: 8px 18px;
}
.stTabs [aria-selected="true"] {
    background: var(--card);
    color: var(--text) !important;
    border-bottom: 2px solid var(--accent);
}

/* Chat bubbles — user and assistant get distinct tinting */
[data-testid="stChatMessage"] {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 6px 8px;
    margin-bottom: 10px;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background: var(--accent-soft);
    border-color: rgba(99, 102, 241, 0.35);
}

/* Chat input dock */
[data-testid="stChatInput"] {
    background: transparent;
}
[data-testid="stChatInput"] textarea {
    background: var(--card);
    color: var(--text);
    border: 1px solid var(--border);
    border-radius: 12px;
}

/* Custom card component */
.av-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 10px;
    transition: background 0.15s ease;
}
.av-card:hover { background: var(--card-hover); }
.av-card .av-label {
    color: var(--text-secondary);
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin-bottom: 3px;
}
.av-card .av-value {
    color: var(--text);
    font-size: 0.92rem;
    font-weight: 500;
    font-family: 'JetBrains Mono', monospace;
    word-break: break-word;
}

/* Status badge */
.av-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 500;
}
.av-badge.ready { background: var(--accent-soft); color: #A5A8FF; border: 1px solid rgba(99,102,241,0.4); }
.av-badge.idle { background: rgba(136,145,167,0.12); color: var(--text-secondary); border: 1px solid var(--border); }

/* Empty state hero */
.av-hero {
    text-align: center;
    padding: 72px 24px 36px 24px;
}
.av-hero h1 {
    font-size: 2.3rem;
    margin-bottom: 10px;
    background: linear-gradient(135deg, #F1F3FF 20%, #9498FF 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    display: inline-block;
}
.av-hero p { color: var(--text-secondary); font-size: 1.04rem; }
.av-hero-badges {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-top: 24px;
    flex-wrap: wrap;
}

/* Score card (Investment Readiness) — gold accent, sets it apart from chat */
.av-score-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px 22px;
    margin: 10px 0 16px 0;
}
.av-score-top { display: flex; align-items: baseline; justify-content: space-between; }
.av-score-value { font-family: 'Sora', sans-serif; font-size: 2.4rem; font-weight: 700; color: var(--gold); }
.av-score-max { color: var(--text-secondary); font-size: 1rem; margin-left: 4px; }
.av-score-track {
    width: 100%;
    height: 8px;
    background: var(--gold-soft);
    border-radius: 999px;
    margin-top: 12px;
    overflow: hidden;
}
.av-score-fill {
    height: 100%;
    background: linear-gradient(90deg, #F0B429, #FFD873);
    border-radius: 999px;
}

/* Divider */
hr { border-color: var(--border); }
</style>
"""

st.markdown(THEME_CSS, unsafe_allow_html=True)


def render_card(label: str, value: str) -> None:
    st.markdown(
        f"""<div class="av-card">
                <div class="av-label">{label}</div>
                <div class="av-value">{value}</div>
            </div>""",
        unsafe_allow_html=True,
    )


def render_badge(text: str, state: str = "idle") -> str:
    dot = "●"
    return f'<span class="av-badge {state}">{dot} {text}</span>'


def render_score_card(score: int, explanation: str) -> None:
    pct = max(0, min(100, score))
    st.markdown(
        f"""<div class="av-score-card">
                <div class="av-score-top">
                    <div><span class="av-score-value">{score}</span><span class="av-score-max">/100</span></div>
                </div>
                <div class="av-score-track"><div class="av-score-fill" style="width:{pct}%;"></div></div>
                <p style="margin-top:14px; color:var(--text); font-size:0.95rem;">{explanation}</p>
            </div>""",
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Cached resources (loaded once per app process, not once per user click)
# ---------------------------------------------------------------------------

@st.cache_resource(show_spinner=False)
def load_chat_model(hf_token: str, model_id: str):
    return _load_chat_model(hf_token, model_id)


@st.cache_resource(show_spinner=False)
def load_embeddings():
    return _load_embeddings()


# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------

defaults = {
    "vectorstore": None,
    "retriever": None,
    "pdf_name": None,
    "n_chunks": None,
    "business_result": None,
    "swot_result": None,
    "investment_result": None,
    "chat_history": [],  # list[HumanMessage | AIMessage]
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------------------------------------------------------------------------
# Sidebar — upload + config + status
# ---------------------------------------------------------------------------

with st.sidebar:
    st.markdown("### 🚀 Startup Validator")
    st.caption("RAG-powered document analysis")
    st.divider()

    hf_token = get_hf_token()
    if not hf_token:
        st.error("No Hugging Face token found. Add `HUGGINGFACEHUB_API_TOKEN` to .env (local) or Secrets (deployed).")

    model_id = st.text_input("Model", value=DEFAULT_MODEL, label_visibility="visible")

    uploaded_file = st.file_uploader("Upload document (PDF)", type=["pdf"])

    build_clicked = st.button("Build Knowledge Base", type="primary", disabled=not (uploaded_file and hf_token))

    st.divider()
    st.markdown("**Status**")

    if st.session_state.retriever is not None:
        st.markdown(render_badge("Knowledge base ready", "ready"), unsafe_allow_html=True)
        render_card("Current document", st.session_state.pdf_name)
        render_card("Chunks indexed", str(st.session_state.n_chunks))
    else:
        st.markdown(render_badge("Waiting for document", "idle"), unsafe_allow_html=True)

    render_card("Embedding model", EMBEDDING_MODEL)
    render_card("Chat model", model_id)

# ---------------------------------------------------------------------------
# Build knowledge base
# ---------------------------------------------------------------------------

if build_clicked and uploaded_file and hf_token:
    with st.spinner("Reading PDF, chunking, and embedding..."):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            pdf_path = tmp.name

        embeddings = load_embeddings()
        vectorstore, n_pages, n_chunks = build_vectorstore(pdf_path, embeddings)

        st.session_state.vectorstore = vectorstore
        st.session_state.retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
        st.session_state.pdf_name = uploaded_file.name
        st.session_state.n_chunks = n_chunks
        # Reset previous analysis + chat when a new document is loaded
        st.session_state.business_result = None
        st.session_state.swot_result = None
        st.session_state.investment_result = None
        st.session_state.chat_history = []

        os.unlink(pdf_path)

    st.toast(f"Indexed {n_pages} page(s) into {n_chunks} chunk(s).", icon="✅")

# ---------------------------------------------------------------------------
# Main area
# ---------------------------------------------------------------------------

if st.session_state.retriever is None:
    # ---- Empty state ----
    st.markdown(
        """
        <div class="av-hero">
            <h1>🚀 AI Startup Validator</h1>
            <p>Upload a startup pitch deck or business plan to begin.</p>
            <div class="av-hero-badges">
                <span class="av-badge idle">✓ Pitch decks</span>
                <span class="av-badge idle">✓ Business plans</span>
                <span class="av-badge idle">✓ Startup documents</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

chat_model = load_chat_model(hf_token, model_id)

# ---- Header ----
header_col1, header_col2 = st.columns([3, 1])
with header_col1:
    st.markdown("## 💬 Ask about your document")
    st.caption(f"Chatting with **{st.session_state.pdf_name}** — analysis tools are below.")
with header_col2:
    st.markdown(render_badge("Knowledge base ready", "ready"), unsafe_allow_html=True)

# ---- Conversation (primary surface) ----
# Rendered in normal page flow (no fixed-height scroll box) so the newest
# exchange always lands right above the chat input, at the bottom of the
# page — a fixed-height box was hiding the latest message at its top edge
# on every rerun, which is the opposite of what we want here.
if not st.session_state.chat_history:
    st.caption("No messages yet — ask a question below to get started.")
for msg in st.session_state.chat_history:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.write(msg.content)

# ---- Chat input (Streamlit docks this to the bottom of the viewport
#      automatically wherever it's called — this is the closest native
#      equivalent to a fixed ChatGPT-style composer) ----
question = st.chat_input("Ask something about the document...")
if question:
    st.session_state.chat_history.append(HumanMessage(content=question))
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                answer = generate_chat_answer(
                    chat_model,
                    st.session_state.retriever,
                    question,
                    st.session_state.chat_history[:-1],  # exclude the question just added
                )
                st.write(answer)
            except Exception as e:
                answer = None
                st.error(f"Couldn't get a response: {e}")

    if answer is not None:
        st.session_state.chat_history.append(AIMessage(content=answer))

st.divider()

# ---- Analysis tools (secondary panel, below the chat) ----
st.markdown("### 📊 Analysis")

tab_business, tab_swot, tab_investment = st.tabs(
    ["📋 Business Analysis", "⚖️ SWOT", "💰 Investment Readiness"]
)

# --- Business ---
with tab_business:
    if st.button("Run Business Analysis"):
        with st.spinner("Analyzing..."):
            context, _ = retrieve_context(st.session_state.retriever, RETRIEVAL_QUERIES["business"])
            try:
                st.session_state.business_result = run_chain(chat_model, business_prompt, business_parser, context)
            except RuntimeError as e:
                st.error(str(e))

    result = st.session_state.business_result
    if result:
        st.subheader(result.startup_name)
        st.write(result.summary)
        col1, col2 = st.columns(2)
        with col1:
            render_card("Industry", result.industry)
            render_card("Target Customers", result.target_customers)
            render_card("Problem", result.problem)
            render_card("Solution", result.solution)
        with col2:
            render_card("Value Proposition", result.unique_value_proposition)
            render_card("Business Model", result.business_model)
            render_card("Revenue Model", result.revenue_model)

# --- SWOT ---
with tab_swot:
    if st.button("Run SWOT Analysis"):
        with st.spinner("Analyzing..."):
            context, _ = retrieve_context(st.session_state.retriever, RETRIEVAL_QUERIES["swot"])
            try:
                st.session_state.swot_result = run_chain(chat_model, swot_prompt, swot_parser, context)
            except RuntimeError as e:
                st.error(str(e))

    result = st.session_state.swot_result
    if result:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**✅ Strengths**")
            for item in result.strengths:
                st.markdown(f"- {item}")
            st.markdown("**🌱 Opportunities**")
            for item in result.opportunities:
                st.markdown(f"- {item}")
        with col2:
            st.markdown("**⚠️ Weaknesses**")
            for item in result.weaknesses:
                st.markdown(f"- {item}")
            st.markdown("**🚨 Threats**")
            for item in result.threats:
                st.markdown(f"- {item}")

# --- Investment ---
with tab_investment:
    if st.button("Run Investment Readiness"):
        with st.spinner("Analyzing..."):
            context, _ = retrieve_context(st.session_state.retriever, RETRIEVAL_QUERIES["investment"])
            try:
                st.session_state.investment_result = run_chain(chat_model, investment_prompt, investment_parser, context)
            except RuntimeError as e:
                st.error(str(e))

    result = st.session_state.investment_result
    if result:
        render_score_card(result.investment_score, result.explanation)
        col1, col2 = st.columns(2)
        with col1:
            render_card("Scalability", result.scalability)
            render_card("Innovation", result.innovation)
        with col2:
            render_card("Team", result.team_assessment)
            render_card("Product", result.product_assessment)
        st.markdown("**Key Risks:**")
        for risk in result.key_risks:
            st.markdown(f"- {risk}")
