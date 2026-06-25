import streamlit as st
import time
import sys
import os
from pipeline import run_research_pipeline 

# ── page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MASP — Research Assistant",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

/* ── reset & base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: #3D1534 !important;
    font-family: 'Space Grotesk', sans-serif;
    color: #FFF4EB;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 20%, #4a1d42 0%, #3D1534 40%, #2a0e24 100%) !important;
}

/* hide streamlit chrome */
#MainMenu, footer, header, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"] { display: none !important; }

/* ── main container ── */
.block-container {
    padding: 3rem 4rem 4rem 4rem !important;
    max-width: 900px !important;
    margin: 0 auto !important;
}

/* ── wordmark / header ── */
.masp-wordmark {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.35em;
    color: #A6BCC9;
    text-transform: uppercase;
    margin-bottom: 0.25rem;
}

.masp-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.6rem;
    font-weight: 700;
    color: #FFF4EB;
    line-height: 1.05;
    margin-bottom: 0.4rem;
    letter-spacing: -0.02em;
}

.masp-title span {
    color: #F6E0B6;
}

.masp-subtitle {
    font-size: 0.9rem;
    color: #A6BCC9;
    font-weight: 400;
    margin-bottom: 2.5rem;
    letter-spacing: 0.01em;
}

/* ── divider ── */
.rule {
    height: 1px;
    background: linear-gradient(90deg, #3E4B8E 0%, #F6E0B6 40%, #3E4B8E 100%);
    margin: 1.8rem 0;
    opacity: 0.5;
}

/* ── section label ── */
.section-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.3em;
    color: #A6BCC9;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}

/* ── text area / input ── */
[data-testid="stTextArea"] textarea {
    background: rgba(62, 75, 142, 0.15) !important;
    border: 1px solid rgba(166, 188, 201, 0.25) !important;
    border-radius: 6px !important;
    color: #FFF4EB !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 1rem 1.1rem !important;
    resize: none !important;
    transition: border-color 0.2s ease;
}

[data-testid="stTextArea"] textarea:focus {
    border-color: #F6E0B6 !important;
    box-shadow: 0 0 0 2px rgba(246, 224, 182, 0.1) !important;
    outline: none !important;
}

[data-testid="stTextArea"] textarea::placeholder {
    color: rgba(166, 188, 201, 0.5) !important;
}

[data-testid="stTextArea"] label {
    display: none !important;
}

/* ── slider ── */
[data-testid="stSlider"] {
    padding: 0 !important;
}

[data-testid="stSlider"] label {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.6rem !important;
    letter-spacing: 0.25em !important;
    color: #A6BCC9 !important;
    text-transform: uppercase !important;
}

[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {
    background: #F6E0B6 !important;
    border-color: #F6E0B6 !important;
}

[data-testid="stSlider"] [data-baseweb="slider"] [data-testid="stTickBarMin"],
[data-testid="stSlider"] [data-baseweb="slider"] [data-testid="stTickBarMax"] {
    color: #A6BCC9 !important;
    font-size: 0.7rem !important;
}

/* ── button ── */
[data-testid="stButton"] button {
    background: #F6E0B6 !important;
    color: #3D1534 !important;
    border: none !important;
    border-radius: 5px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.7rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    padding: 0.75rem 2rem !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
}

[data-testid="stButton"] button:hover {
    background: #FFF4EB !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 24px rgba(246, 224, 182, 0.2) !important;
}

[data-testid="stButton"] button:active {
    transform: translateY(0) !important;
}

/* ── pipeline tracker ── */
.pipeline-wrap {
    margin: 1.5rem 0;
}

.pipeline-node {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    margin-bottom: 0;
}

.node-track {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex-shrink: 0;
}

.node-dot {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    border: 2px solid rgba(166, 188, 201, 0.3);
    background: rgba(62, 75, 142, 0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.4s ease;
    position: relative;
}

.node-dot.idle {
    border-color: rgba(166, 188, 201, 0.3);
    background: rgba(62, 75, 142, 0.2);
}

.node-dot.running {
    border-color: #F6E0B6;
    background: rgba(246, 224, 182, 0.1);
    animation: pulse 1.2s ease-in-out infinite;
}

.node-dot.done {
    border-color: #A6BCC9;
    background: rgba(166, 188, 201, 0.15);
}

.node-dot.error {
    border-color: #c77;
    background: rgba(200, 100, 100, 0.1);
}

.node-inner {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: rgba(166, 188, 201, 0.3);
    transition: background 0.4s ease;
}

.node-dot.running .node-inner { background: #F6E0B6; }
.node-dot.done .node-inner    { background: #A6BCC9; }
.node-dot.error .node-inner   { background: #c77; }

.node-connector {
    width: 1px;
    height: 36px;
    background: repeating-linear-gradient(
        to bottom,
        rgba(166, 188, 201, 0.25) 0px,
        rgba(166, 188, 201, 0.25) 4px,
        transparent 4px,
        transparent 8px
    );
    margin: 3px 0;
}

.node-content {
    padding-top: 2px;
    padding-bottom: 1.5rem;
}

.node-tag {
    font-family: 'Space Mono', monospace;
    font-size: 0.55rem;
    letter-spacing: 0.3em;
    color: #A6BCC9;
    text-transform: uppercase;
    margin-bottom: 0.15rem;
}

.node-name {
    font-size: 0.95rem;
    font-weight: 600;
    color: #FFF4EB;
    margin-bottom: 0.15rem;
}

.node-name.running { color: #F6E0B6; }
.node-name.done    { color: #A6BCC9; }

.node-desc {
    font-size: 0.78rem;
    color: rgba(166, 188, 201, 0.6);
    font-weight: 400;
}

.node-status {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.15em;
    margin-top: 0.3rem;
}

.status-running { color: #F6E0B6; }
.status-done    { color: #A6BCC9; }
.status-error   { color: #c77; }

@keyframes pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(246, 224, 182, 0.3); }
    50%       { box-shadow: 0 0 0 8px rgba(246, 224, 182, 0); }
}

/* ── output card ── */
.output-card {
    background: rgba(62, 75, 142, 0.12);
    border: 1px solid rgba(166, 188, 201, 0.2);
    border-left: 3px solid #F6E0B6;
    border-radius: 6px;
    padding: 1.5rem 1.6rem;
    margin-top: 0.5rem;
}

.output-card p {
    font-size: 0.92rem;
    line-height: 1.75;
    color: #FFF4EB;
    margin-bottom: 0.8rem;
}

.output-card p:last-child { margin-bottom: 0; }

.output-card h1, .output-card h2, .output-card h3 {
    color: #F6E0B6;
    font-weight: 600;
    margin: 1rem 0 0.5rem;
    font-size: 1rem;
}

.output-card ul, .output-card ol {
    padding-left: 1.2rem;
    color: #FFF4EB;
    font-size: 0.92rem;
    line-height: 1.75;
}

.output-card code {
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    background: rgba(62, 75, 142, 0.3);
    padding: 0.1rem 0.3rem;
    border-radius: 3px;
    color: #A6BCC9;
}

/* ── error box ── */
.error-card {
    background: rgba(180, 60, 60, 0.08);
    border: 1px solid rgba(200, 100, 100, 0.3);
    border-left: 3px solid #c77;
    border-radius: 6px;
    padding: 1rem 1.2rem;
    margin-top: 0.5rem;
}

.error-card p {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: rgba(200, 140, 140, 0.9);
    line-height: 1.6;
}

/* ── meta row ── */
.meta-row {
    display: flex;
    gap: 2rem;
    margin-top: 1.2rem;
    padding-top: 1rem;
    border-top: 1px solid rgba(166, 188, 201, 0.1);
}

.meta-item {
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
}

.meta-key {
    font-family: 'Space Mono', monospace;
    font-size: 0.55rem;
    letter-spacing: 0.25em;
    color: rgba(166, 188, 201, 0.5);
    text-transform: uppercase;
}

.meta-val {
    font-size: 0.82rem;
    font-weight: 600;
    color: #F6E0B6;
}

/* ── select box ── */
[data-testid="stSelectbox"] label {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.6rem !important;
    letter-spacing: 0.25em !important;
    color: #A6BCC9 !important;
    text-transform: uppercase !important;
}

[data-testid="stSelectbox"] [data-baseweb="select"] {
    background: rgba(62, 75, 142, 0.15) !important;
}

[data-testid="stSelectbox"] [data-baseweb="select"] > div {
    background: rgba(62, 75, 142, 0.15) !important;
    border-color: rgba(166, 188, 201, 0.25) !important;
    color: #FFF4EB !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

/* ── checkbox ── */
[data-testid="stCheckbox"] label {
    color: #A6BCC9 !important;
    font-size: 0.82rem !important;
}

[data-testid="stCheckbox"] [data-baseweb="checkbox"] [data-baseweb="checkbox"] {
    background: #F6E0B6 !important;
}

/* ── expander ── */
[data-testid="stExpander"] {
    border: 1px solid rgba(166, 188, 201, 0.15) !important;
    border-radius: 6px !important;
    background: rgba(62, 75, 142, 0.08) !important;
}

[data-testid="stExpander"] summary {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.2em !important;
    color: #A6BCC9 !important;
    text-transform: uppercase !important;
}

/* ── columns gap ── */
[data-testid="stHorizontalBlock"] { gap: 1rem !important; }

/* ── copy button area ── */
.copy-hint {
    font-family: 'Space Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.2em;
    color: rgba(166, 188, 201, 0.4);
    text-align: right;
    margin-top: 0.5rem;
    text-transform: uppercase;
}

/* scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(166, 188, 201, 0.2); border-radius: 2px; }
</style>
""", unsafe_allow_html=True)


# ── helpers ───────────────────────────────────────────────────────────────────
def pipeline_node_html(tag, name, desc, state="idle", status_text=""):
    state_cls = state
    name_cls  = "running" if state == "running" else ("done" if state == "done" else "")
    status_html = ""
    if status_text:
        scls = f"status-{state}" if state in ("running","done","error") else ""
        status_html = f'<div class="node-status {scls}">{status_text}</div>'
    return f"""
    <div class="node-track">
        <div class="node-dot {state_cls}"><div class="node-inner"></div></div>
        <div class="node-connector"></div>
    </div>
    <div class="node-content">
        <div class="node-tag">{tag}</div>
        <div class="node-name {name_cls}">{name}</div>
        <div class="node-desc">{desc}</div>
        {status_html}
    </div>
    """

def render_pipeline(states):
    nodes = [
        ("agent / 01", "Search Agent",  "Tavily API — real-time retrieval across sources"),
        ("agent / 02", "Reader Agent",  "BeautifulSoup — scrapes and extracts page content"),
        ("chain / 03", "Writer Chain",  "Synthesises findings into structured prose"),
        ("chain / 04", "Critic Chain",  "Evaluates, refines and scores the output"),
    ]
    html = '<div class="pipeline-wrap">'
    for i, (tag, name, desc) in enumerate(nodes):
        state = states[i]
        status_map = {
            "idle":    "",
            "running": "running...",
            "done":    "complete",
            "error":   "failed",
        }
        html += f'<div class="pipeline-node">{pipeline_node_html(tag, name, desc, state, status_map[state])}</div>'
    html += "</div>"
    return html


# ── session state init ─────────────────────────────────────────────────────────
if "output"        not in st.session_state: st.session_state.output        = None
if "error"         not in st.session_state: st.session_state.error         = None
if "running"       not in st.session_state: st.session_state.running       = False
if "node_states"   not in st.session_state: st.session_state.node_states   = ["idle","idle","idle","idle"]
if "elapsed"       not in st.session_state: st.session_state.elapsed       = None
if "topic_used"    not in st.session_state: st.session_state.topic_used    = ""


# ── header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="masp-wordmark">Multi-Agent System Pipeline</div>', unsafe_allow_html=True)
st.markdown('<h1 class="masp-title">Research <span>Assistant</span></h1>', unsafe_allow_html=True)
st.markdown('<p class="masp-subtitle">Tavily search · BeautifulSoup scraping · LangChain writer + critic</p>', unsafe_allow_html=True)
st.markdown('<div class="rule"></div>', unsafe_allow_html=True)


# ── input section ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Research Topic</div>', unsafe_allow_html=True)

topic = st.text_area(
    label="topic",
    placeholder="Enter a topic, question, or research prompt...",
    height=110,
    key="topic_input",
)

col1, col2 = st.columns([1, 1])
with col1:
    depth = st.selectbox(
        "SEARCH DEPTH",
        ["Standard", "Deep", "Exhaustive"],
        index=0,
    )
with col2:
    max_sources = st.slider("MAX SOURCES", min_value=3, max_value=15, value=7, step=1)

st.markdown("<br>", unsafe_allow_html=True)

with st.expander("ADVANCED OPTIONS"):
    col_a, col_b = st.columns(2)
    with col_a:
        include_critic = st.checkbox("Run critic chain", value=True)
    with col_b:
        verbose_mode = st.checkbox("Verbose pipeline logs", value=False)

st.markdown("<br>", unsafe_allow_html=True)
run_clicked = st.button("RUN PIPELINE")

st.markdown('<div class="rule"></div>', unsafe_allow_html=True)


# ── pipeline status ───────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Pipeline Status</div>', unsafe_allow_html=True)
pipeline_placeholder = st.empty()

# render initial / current pipeline state
def render_current_pipeline():
    pipeline_placeholder.markdown(
        render_pipeline(st.session_state.node_states),
        unsafe_allow_html=True,
    )

render_current_pipeline()


# ── run logic ─────────────────────────────────────────────────────────────────
if run_clicked and topic.strip():
    # reset
    st.session_state.output      = None
    st.session_state.error       = None
    st.session_state.elapsed     = None
    st.session_state.topic_used  = topic.strip()
    st.session_state.node_states = ["idle","idle","idle","idle"]

    # add pipeline.py's directory to path
    pipeline_dir = os.path.dirname(os.path.abspath(__file__))
    if pipeline_dir not in sys.path:
        sys.path.insert(0, pipeline_dir)

    start = time.time()
    try:
        from pipeline import run_research_pipeline  # adjust if entry point differs

        def update_node(idx, state):
            st.session_state.node_states[idx] = state
            pipeline_placeholder.markdown(
                render_pipeline(st.session_state.node_states),
                unsafe_allow_html=True,
            )

        update_node(0, "running")
        time.sleep(0.3)

        # call your pipeline — expects (topic, depth, max_sources) or similar
        # adjust arguments to match your actual pipeline signature
        try:
            result = run_research_pipeline(
                topic=topic.strip(),
                depth=depth.lower(),
                max_sources=max_sources,
                include_critic=include_critic,
                verbose=verbose_mode,
            )
        except TypeError:
            # fallback: try just the topic
            result = run_research_pipeline(topic.strip())

        update_node(0, "done")
        update_node(1, "running")
        time.sleep(0.2)
        update_node(1, "done")
        update_node(2, "running")
        time.sleep(0.2)
        update_node(2, "done")

        if include_critic:
            update_node(3, "running")
            time.sleep(0.2)
            update_node(3, "done")
        else:
            update_node(3, "idle")

        st.session_state.output  = result
        st.session_state.elapsed = round(time.time() - start, 1)

    except ImportError as e:
        st.session_state.error = f"ImportError: {e}\n\nMake sure pipeline.py is in the same directory and run_pipeline() is exported."
        st.session_state.node_states = ["error","idle","idle","idle"]
        render_current_pipeline()

    except Exception as e:
        st.session_state.error = str(e)
        # mark whichever node was running as error
        ns = st.session_state.node_states
        for i, s in enumerate(ns):
            if s == "running":
                ns[i] = "error"
        render_current_pipeline()

elif run_clicked and not topic.strip():
    st.markdown(
        '<p style="font-family:\'Space Mono\',monospace;font-size:0.7rem;'
        'color:rgba(166,188,201,0.7);letter-spacing:0.1em;margin-top:0.5rem;">'
        'Enter a research topic before running.</p>',
        unsafe_allow_html=True,
    )


# ── output section ────────────────────────────────────────────────────────────
if st.session_state.output or st.session_state.error:
    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Output</div>', unsafe_allow_html=True)

if st.session_state.output:
    output_text = st.session_state.output
    if not isinstance(output_text, str):
        output_text = str(output_text)

    import re
    # convert markdown-ish to html for display
    lines = output_text.split("\n")
    html_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("### "):
            html_lines.append(f"<h3>{stripped[4:]}</h3>")
        elif stripped.startswith("## "):
            html_lines.append(f"<h2>{stripped[3:]}</h2>")
        elif stripped.startswith("# "):
            html_lines.append(f"<h1>{stripped[2:]}</h1>")
        elif stripped.startswith("- ") or stripped.startswith("* "):
            html_lines.append(f"<li>{stripped[2:]}</li>")
        elif stripped == "":
            html_lines.append("")
        else:
            # bold
            line_html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", stripped)
            # inline code
            line_html = re.sub(r"`(.+?)`", r"<code>\1</code>", line_html)
            html_lines.append(f"<p>{line_html}</p>")

    output_html = "\n".join(html_lines)

    st.markdown(f'<div class="output-card">{output_html}</div>', unsafe_allow_html=True)

    if st.session_state.elapsed:
        topic_display = st.session_state.topic_used[:48] + "..." \
            if len(st.session_state.topic_used) > 48 else st.session_state.topic_used
        st.markdown(f"""
        <div class="meta-row">
            <div class="meta-item">
                <div class="meta-key">Topic</div>
                <div class="meta-val">{topic_display}</div>
            </div>
            <div class="meta-item">
                <div class="meta-key">Elapsed</div>
                <div class="meta-val">{st.session_state.elapsed}s</div>
            </div>
            <div class="meta-item">
                <div class="meta-key">Depth</div>
                <div class="meta-val">{depth}</div>
            </div>
            <div class="meta-item">
                <div class="meta-key">Sources</div>
                <div class="meta-val">{max_sources}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="copy-hint">Select text above to copy</div>', unsafe_allow_html=True)

if st.session_state.error:
    st.markdown(
        f'<div class="error-card"><p>{st.session_state.error}</p></div>',
        unsafe_allow_html=True,
    )