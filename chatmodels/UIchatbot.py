from dotenv import load_dotenv

load_dotenv()

import streamlit as st
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Mood Bot", page_icon="🎭", layout="centered")

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Mono:wght@400;500&display=swap');

/* ── global reset ── */
html, body, [class*="css"] {
    font-family: 'DM Mono', monospace;
    background-color: #0d0d0d;
    color: #e8e8e8;
}

/* hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* ── app container ── */
.block-container {
    max-width: 720px;
    padding: 2rem 1.5rem 6rem;
}

/* ── title ── */
.title-block {
    text-align: center;
    margin-bottom: 2.5rem;
}
.title-block h1 {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    letter-spacing: -1px;
    margin: 0;
    line-height: 1;
}
.title-block p {
    font-size: 0.78rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    opacity: 0.45;
    margin-top: 0.4rem;
}

/* mode colours */
.mode-angry  { color: #ff4444; }
.mode-funny  { color: #f5c542; }
.mode-sad    { color: #6db4ff; }
.mode-default{ color: #e8e8e8; }

/* ── mode selector cards ── */
.mode-cards {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
}

/* ── chat bubble wrappers ── */
.chat-row {
    display: flex;
    margin-bottom: 1rem;
    gap: 0.75rem;
    align-items: flex-end;
}
.chat-row.user  { flex-direction: row-reverse; }
.chat-row.bot   { flex-direction: row; }

.avatar {
    width: 34px;
    height: 34px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
    border: 1px solid #2a2a2a;
}
.avatar.user-av { background: #1e1e1e; }
.avatar.bot-av  { background: #1a1a1a; }

.bubble {
    max-width: 75%;
    padding: 0.65rem 1rem;
    border-radius: 12px;
    font-size: 0.87rem;
    line-height: 1.55;
    word-break: break-word;
}
.bubble.user-bubble {
    background: #1f1f1f;
    border: 1px solid #2e2e2e;
    border-bottom-right-radius: 3px;
    color: #d4d4d4;
}
.bubble.bot-bubble {
    border-bottom-left-radius: 3px;
}

/* mode-tinted bot bubbles */
.bubble.bot-angry  { background:#2a0a0a; border:1px solid #5a1010; color:#ffaaaa; }
.bubble.bot-funny  { background:#2a2200; border:1px solid #5a4800; color:#ffe680; }
.bubble.bot-sad    { background:#08142a; border:1px solid #143060; color:#aaccff; }

/* ── divider ── */
.divider {
    border: none;
    border-top: 1px solid #1e1e1e;
    margin: 1.5rem 0;
}

/* ── status badge ── */
.status-badge {
    display: inline-block;
    font-size: 0.68rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.2rem 0.65rem;
    border-radius: 999px;
    margin-bottom: 1.2rem;
}
.badge-angry { background:#3a0808; color:#ff6666; border:1px solid #6a1010; }
.badge-funny { background:#3a2e00; color:#f5c542; border:1px solid #6a5200; }
.badge-sad   { background:#071526; color:#6db4ff; border:1px solid #0e2d55; }

/* ── streamlit button overrides ── */
div.stButton > button {
    font-family: 'DM Mono', monospace;
    font-size: 0.82rem;
    letter-spacing: 0.06em;
    border-radius: 8px;
    border: 1px solid #2e2e2e;
    background: #161616;
    color: #c8c8c8;
    padding: 0.5rem 1.1rem;
    transition: all 0.18s ease;
    width: 100%;
}
div.stButton > button:hover {
    border-color: #555;
    color: #fff;
    background: #202020;
}

/* active mode button highlight */
div[data-testid="stButton"].angry-active button  { border-color:#ff4444; color:#ff4444; }
div[data-testid="stButton"].funny-active button   { border-color:#f5c542; color:#f5c542; }
div[data-testid="stButton"].sad-active button     { border-color:#6db4ff; color:#6db4ff; }

/* ── input ── */
div[data-testid="stChatInput"] textarea {
    font-family: 'DM Mono', monospace;
    font-size: 0.85rem;
    background: #141414;
    border: 1px solid #2a2a2a;
    color: #e0e0e0;
    border-radius: 10px;
}
div[data-testid="stChatInput"] textarea:focus {
    border-color: #3a3a3a;
    box-shadow: none;
}

/* scrollable chat area */
.chat-container {
    max-height: 58vh;
    overflow-y: auto;
    padding-right: 4px;
}
.chat-container::-webkit-scrollbar { width: 4px; }
.chat-container::-webkit-scrollbar-track { background: transparent; }
.chat-container::-webkit-scrollbar-thumb { background: #2a2a2a; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ── Session state init ────────────────────────────────────────────────────────
if "mode" not in st.session_state:
    st.session_state.mode = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "lc_messages" not in st.session_state:
    st.session_state.lc_messages = []

# ── Mode config ───────────────────────────────────────────────────────────────
MODE_CONFIG = {
    "angry": {
        "label": "😠  Angry",
        "system": "You are an angry AI agent. You respond aggressively and impatiently.",
        "badge_class": "badge-angry",
        "bubble_class": "bot-angry",
        "title_class": "mode-angry",
        "emoji": "😠",
        "description": "AGGRESSIVE & IMPATIENT",
    },
    "funny": {
        "label": "😂  Funny",
        "system": "You are a very funny AI agent. You respond with humor and jokes.",
        "badge_class": "badge-funny",
        "bubble_class": "bot-funny",
        "title_class": "mode-funny",
        "emoji": "😂",
        "description": "JOKES & HUMOR",
    },
    "sad": {
        "label": "😢  Sad",
        "system": "You are a very sad AI agent. You respond in a depressed and emotional tone.",
        "badge_class": "badge-sad",
        "bubble_class": "bot-sad",
        "title_class": "mode-sad",
        "emoji": "😢",
        "description": "DEPRESSED & EMOTIONAL",
    },
}

# ── Header ────────────────────────────────────────────────────────────────────
mode_class = "mode-default"
if st.session_state.mode:
    mode_class = MODE_CONFIG[st.session_state.mode]["title_class"]

st.markdown(f"""
<div class="title-block">
    <h1 class="{mode_class}">MOOD BOT</h1>
    <p>pick a personality · start chatting</p>
</div>
""", unsafe_allow_html=True)

# ── Mode selector ─────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)

for col, key in zip([col1, col2, col3], ["angry", "funny", "sad"]):
    with col:
        if st.button(MODE_CONFIG[key]["label"], key=f"btn_{key}"):
            st.session_state.mode = key
            sys_msg = MODE_CONFIG[key]["system"]
            st.session_state.lc_messages = [SystemMessage(content=sys_msg)]
            st.session_state.messages = []
            st.rerun()

# ── Active mode badge ─────────────────────────────────────────────────────────
if st.session_state.mode:
    cfg = MODE_CONFIG[st.session_state.mode]
    st.markdown(f"""
    <div style="text-align:center;margin:0.6rem 0 1.4rem;">
        <span class="status-badge {cfg['badge_class']}">
            {cfg['emoji']}  {cfg['description']}  ·  active
        </span>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Chat history ──────────────────────────────────────────────────────────────
if st.session_state.messages:
    chat_html = '<div class="chat-container">'
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            chat_html += f"""
            <div class="chat-row user">
                <div class="avatar user-av">🧑</div>
                <div class="bubble user-bubble">{msg["content"]}</div>
            </div>"""
        else:
            bubble_cls = ""
            if st.session_state.mode:
                bubble_cls = MODE_CONFIG[st.session_state.mode]["bubble_class"]
            emoji = MODE_CONFIG[st.session_state.mode]["emoji"] if st.session_state.mode else "🤖"
            chat_html += f"""
            <div class="chat-row bot">
                <div class="avatar bot-av">{emoji}</div>
                <div class="bubble bot-bubble {bubble_cls}">{msg["content"]}</div>
            </div>"""
    chat_html += "</div>"
    st.markdown(chat_html, unsafe_allow_html=True)
elif st.session_state.mode:
    cfg = MODE_CONFIG[st.session_state.mode]
    st.markdown(f"""
    <div style="text-align:center;opacity:0.3;padding:2rem 0;font-size:0.8rem;letter-spacing:0.1em;">
        {cfg['emoji']}  say something to get started
    </div>""", unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="text-align:center;opacity:0.25;padding:2.5rem 0;font-size:0.8rem;letter-spacing:0.1em;">
        select a mood above to begin
    </div>""", unsafe_allow_html=True)

# ── Chat input ────────────────────────────────────────────────────────────────
prompt = st.chat_input(
    "type your message…",
    disabled=(st.session_state.mode is None),
)

if prompt:
    # add user message to display history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.lc_messages.append(HumanMessage(content=prompt))

    # call model
    model = ChatMistralAI(model="mistral-small-2506", temperature=0.9)
    response = model.invoke(st.session_state.lc_messages)

    # store bot reply
    st.session_state.lc_messages.append(AIMessage(content=response.content))
    st.session_state.messages.append({"role": "assistant", "content": response.content})

    st.rerun()