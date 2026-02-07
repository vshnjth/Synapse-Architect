"""
Synapse-Architect: Neuro-Lab UI
A Streamlit-based web app for tracing neural signal pathways.
"""

import streamlit as st
import streamlit.components.v1 as components
from brain_logic import (
    trace_neural_pathway,
    validate_response,
    extract_mermaid_chart,
    NCERT_REFERENCE,
)

# ─── Page Config ───
st.set_page_config(
    page_title="Synapse-Architect | Neuro-Lab",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS: Neuro-Lab Dark Mode + Neon Green ───
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600;700&display=swap');

    :root {
        --neon-green: #39FF14;
        --dark-bg: #0a0a0a;
        --card-bg: #1a1a2e;
        --card-border: #39FF1440;
        --text-primary: #e0e0e0;
        --text-dim: #888888;
    }

    .stApp {
        background-color: var(--dark-bg);
        font-family: 'JetBrains Mono', monospace;
    }

    /* Header */
    .neuro-header {
        text-align: center;
        padding: 2rem 0 1rem 0;
        border-bottom: 2px solid var(--neon-green);
        margin-bottom: 2rem;
    }
    .neuro-header h1 {
        color: var(--neon-green);
        font-size: 2.8rem;
        font-weight: 700;
        text-shadow: 0 0 20px #39FF1480, 0 0 40px #39FF1440;
        margin-bottom: 0.3rem;
        letter-spacing: 2px;
    }
    .neuro-header p {
        color: var(--text-dim);
        font-size: 1rem;
    }

    /* Step Cards */
    .step-card {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.75rem 0;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .step-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 4px; height: 100%;
        background: var(--neon-green);
        border-radius: 4px 0 0 4px;
    }
    .step-card:hover {
        border-color: var(--neon-green);
        box-shadow: 0 0 15px #39FF1420;
        transform: translateY(-2px);
    }
    .step-number {
        display: inline-block;
        background: var(--neon-green);
        color: #0a0a0a;
        font-weight: 700;
        width: 32px; height: 32px;
        line-height: 32px;
        text-align: center;
        border-radius: 50%;
        margin-right: 0.75rem;
        font-size: 0.9rem;
    }
    .step-title {
        color: var(--neon-green);
        font-size: 1.15rem;
        font-weight: 600;
        display: inline;
    }
    .step-desc {
        color: var(--text-primary);
        margin-top: 0.75rem;
        line-height: 1.6;
        font-size: 0.92rem;
    }
    .step-meta {
        color: var(--text-dim);
        font-size: 0.8rem;
        margin-top: 0.5rem;
        padding-top: 0.5rem;
        border-top: 1px solid #ffffff10;
    }

    /* Accuracy Badge */
    .accuracy-badge {
        background: linear-gradient(135deg, #1a1a2e, #0a2a0a);
        border: 1px solid var(--neon-green);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .accuracy-badge h3 {
        color: var(--neon-green);
        margin-bottom: 0.75rem;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #0d0d1a;
        border-right: 1px solid var(--card-border);
    }

    /* Input styling */
    .stTextInput input {
        background-color: var(--card-bg) !important;
        border: 1px solid var(--card-border) !important;
        color: var(--neon-green) !important;
        font-family: 'JetBrains Mono', monospace !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
        font-size: 1.05rem !important;
    }
    .stTextInput input:focus {
        border-color: var(--neon-green) !important;
        box-shadow: 0 0 10px #39FF1430 !important;
    }

    /* Button */
    .stButton > button {
        background: linear-gradient(135deg, #39FF14, #20cc0e) !important;
        color: #0a0a0a !important;
        font-weight: 700 !important;
        font-family: 'JetBrains Mono', monospace !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 2rem !important;
        font-size: 1rem !important;
        letter-spacing: 1px !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        box-shadow: 0 0 20px #39FF1460 !important;
        transform: scale(1.02);
    }

    /* Spinner */
    .stSpinner > div {
        border-top-color: var(--neon-green) !important;
    }

    /* Hide default Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""",
    unsafe_allow_html=True,
)


def render_mermaid(mermaid_code: str, height: int = 450):
    """Render a Mermaid.js flowchart using an HTML component."""
    html = f"""
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
        <style>
            body {{
                background-color: #0a0a0a;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
                padding: 1rem;
            }}
            .mermaid {{
                font-family: 'JetBrains Mono', monospace;
            }}
        </style>
    </head>
    <body>
        <pre class="mermaid">
{mermaid_code}
        </pre>
        <script>
            mermaid.initialize({{
                startOnLoad: true,
                theme: 'dark',
                themeVariables: {{
                    primaryColor: '#1a1a2e',
                    primaryTextColor: '#39FF14',
                    primaryBorderColor: '#39FF14',
                    lineColor: '#39FF14',
                    secondaryColor: '#0d0d1a',
                    tertiaryColor: '#1a1a2e',
                    fontFamily: 'JetBrains Mono, monospace',
                    fontSize: '14px',
                    edgeLabelBackground: '#0a0a0a',
                    nodeTextColor: '#e0e0e0'
                }}
            }});
        </script>
    </body>
    </html>
    """
    components.html(html, height=height, scrolling=True)


# ─── Header ───
st.markdown(
    """
<div class="neuro-header">
    <h1>🧠 SYNAPSE-ARCHITECT</h1>
    <p>Autonomous Neuro-Reasoning Agent &nbsp;|&nbsp; NCERT-Grounded &nbsp;|&nbsp; Real-Time Visualization</p>
</div>
""",
    unsafe_allow_html=True,
)

# ─── Sidebar ───
with st.sidebar:
    st.markdown("## ⚡ Control Panel")
    st.markdown("---")

    st.markdown("### 📡 Quick Stimuli")
    example_stimuli = [
        "Stubbing a toe",
        "Touching a hot pan",
        "Seeing a bright flash",
        "Hearing a loud bang",
        "Smelling fresh coffee",
        "Tasting something sour",
        "Stepping on a sharp object",
        "Feeling a cold breeze",
    ]

    selected_example = st.selectbox(
        "Choose a pre-set stimulus:",
        ["— Select —"] + example_stimuli,
    )

    st.markdown("---")
    st.markdown("### 📚 NCERT Reference")
    with st.expander("Receptor Types"):
        for name, desc in NCERT_REFERENCE["receptor_types"].items():
            st.markdown(f"**{name}**: {desc}")

    with st.expander("Brain Regions"):
        for name, desc in NCERT_REFERENCE["key_brain_regions"].items():
            st.markdown(f"**{name}**: {desc}")

    with st.expander("Neuron Types"):
        for name, desc in NCERT_REFERENCE["neuron_types"].items():
            st.markdown(f"**{name}**: {desc}")

    st.markdown("---")
    st.markdown(
        "<p style='color:#555; font-size:0.75rem; text-align:center;'>"
        "Built with 🧬 Synapse-Architect<br>Powered by GitHub Copilot</p>",
        unsafe_allow_html=True,
    )

# ─── Main Input ───
col_input, col_btn = st.columns([4, 1])

with col_input:
    default_val = "" if selected_example == "— Select —" else selected_example
    stimulus = st.text_input(
        "🔬 Enter a stimulus to trace:",
        value=default_val,
        placeholder="e.g., Stubbing a toe, Touching a hot surface...",
        label_visibility="visible",
    )

with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    trace_btn = st.button("⚡ TRACE", use_container_width=True)

# ─── Run Agent ───
if trace_btn and stimulus:
    with st.spinner("🧠 Neural pathway analysis in progress..."):
        try:
            result = trace_neural_pathway(stimulus)
            validation = validate_response(result)

            if not validation["valid"]:
                st.error(
                    "⚠️ Response validation failed: "
                    + "; ".join(validation["errors"])
                )
                st.json(result)
            else:
                # Store in session for persistence
                st.session_state["result"] = result
                st.session_state["validation"] = validation

        except Exception as e:
            st.error(f"❌ Error during neural trace: {str(e)}")
            st.info("💡 Make sure your OPENAI_API_KEY is set in a .env file.")

# ─── Display Results ───
if "result" in st.session_state:
    result = st.session_state["result"]
    validation = st.session_state["validation"]

    st.markdown("---")

    # Tabs for organized output
    tab_pathway, tab_flowchart, tab_accuracy = st.tabs(
        ["🧬 Neural Pathway", "📊 Flowchart", "✅ NCERT Accuracy"]
    )

    with tab_pathway:
        st.markdown(
            f"### Signal Trace: *{result.get('stimulus', stimulus)}*"
        )
        for step in result.get("steps", []):
            st.markdown(
                f"""
            <div class="step-card">
                <span class="step-number">{step.get('step_number', '?')}</span>
                <span class="step-title">{step.get('title', 'Untitled')}</span>
                <div class="step-desc">{step.get('description', '')}</div>
                <div class="step-meta">
                    🏗️ <strong>Structure:</strong> {step.get('structure', 'N/A')}
                    &nbsp;&nbsp;|&nbsp;&nbsp;
                    📖 <strong>NCERT:</strong> {step.get('ncert_reference', 'N/A')}
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        if result.get("reflex_arc_note"):
            st.markdown("---")
            st.info(f"⚡ **Reflex Arc Note:** {result['reflex_arc_note']}")

    with tab_flowchart:
        st.markdown("### 📊 Neural Circuit Flowchart")
        mermaid_code = extract_mermaid_chart(result)
        render_mermaid(mermaid_code, height=500)

        with st.expander("📝 View Mermaid Source Code"):
            st.code(mermaid_code, language="mermaid")

    with tab_accuracy:
        st.markdown(
            f"""
        <div class="accuracy-badge">
            <h3>✅ NCERT Accuracy Cross-Check</h3>
            <p style="color: #e0e0e0; line-height: 1.8;">
                {result.get('ncert_accuracy_notes', 'No accuracy notes generated.')}
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Validation report
        if validation.get("warnings"):
            st.warning("⚠️ Warnings: " + "; ".join(validation["warnings"]))
        else:
            st.success("✅ All validation checks passed!")

        st.markdown("#### 📚 Referenced NCERT Chapters")
        for ch in NCERT_REFERENCE["ncert_chapters"]:
            st.markdown(f"- {ch}")

elif not trace_btn:
    # Landing state
    st.markdown("---")
    cols = st.columns(3)
    features = [
        ("🧬", "5-Step Reasoning", "Traces the neural signal from receptor to cortex in exactly 5 logical, NCERT-aligned steps."),
        ("📊", "Live Flowchart", "Generates a real-time Mermaid.js neural circuit diagram with dark-mode neon styling."),
        ("✅", "NCERT Grounded", "Every pathway is cross-checked against NCERT Class 10-12 biology standards."),
    ]
    for col, (icon, title, desc) in zip(cols, features):
        with col:
            st.markdown(
                f"""
            <div class="step-card" style="text-align:center; padding:2rem;">
                <div style="font-size:2.5rem; margin-bottom:0.75rem;">{icon}</div>
                <div class="step-title" style="display:block; font-size:1.1rem;">{title}</div>
                <div class="step-desc" style="font-size:0.85rem;">{desc}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )
