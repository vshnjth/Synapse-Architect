# 🧠 Synapse-Architect — Development Log

> Tracking every decision made with GitHub Copilot (Agent Mode) to demonstrate **Meaningful Copilot Use** for the Agents League Creative Apps prize.

---

## Session 1: Project Scaffolding & Architecture

**Date:** 2025-01-XX
**Mode:** GitHub Copilot Agent Mode (Chat)

### Decisions Made

#### 1. Tech Stack Selection
- **Streamlit** chosen for rapid prototyping of interactive web UIs — ideal for a hackathon demo.
- **OpenAI GPT-4o-mini** chosen as the LLM backend for cost-efficiency and JSON mode support.
- **Mermaid.js** for flowchart rendering — embeddable in HTML, widely supported, no extra server needed.
- **python-dotenv** for secure API key management.

#### 2. Architecture: `brain_logic.py` (Engine) + `app.py` (UI)
- **Separation of concerns:** All LLM interaction, NCERT data, and validation logic lives in `brain_logic.py`.
  The UI layer (`app.py`) only handles rendering and user interaction.
- This makes the agent logic **testable independently** of the UI.

#### 3. NCERT Grounding Strategy
- A static `NCERT_REFERENCE` dictionary was embedded directly in `brain_logic.py` containing:
  - Receptor types, neuron types, signal pathway components, brain regions, signal transmission concepts.
  - Explicit NCERT chapter references (Class 10 Ch.7, Class 11 Ch.21, Class 12 Ch.4).
- This dictionary is serialized into the **system prompt** so the LLM is constrained to NCERT-accurate terminology.
- The agent is instructed to cross-check every step against this data.

#### 4. Prompt Engineering
- **System prompt** enforces:
  - Exactly 5 steps from receptor → cortex.
  - Valid JSON output with `response_format: json_object`.
  - Mermaid.js `graph TD` syntax.
  - NCERT accuracy notes as a dedicated output field.
  - Temperature set to 0.3 for deterministic, factual responses.

#### 5. Validation Layer
- `validate_response()` checks:
  - Presence of all required keys.
  - Exactly 5 steps returned.
  - Mermaid syntax starts with `graph TD`.
- Provides structured error/warning reports to the UI.

#### 6. UI/UX: "Neuro-Lab" Dark Theme
- Custom CSS with:
  - `#0a0a0a` deep black background, `#1a1a2e` card backgrounds.
  - `#39FF14` neon green as the primary accent (text-shadow glow effects).
  - JetBrains Mono monospace font for a "lab terminal" aesthetic.
  - Animated step cards with left neon border and hover effects.
  - Mermaid chart rendered with matching dark theme variables.
- `.streamlit/config.toml` sets the base Streamlit theme to match.

#### 7. Mermaid Rendering
- Used `streamlit.components.v1.html()` to embed a full HTML page with Mermaid.js CDN.
- Custom Mermaid theme variables match the Neuro-Lab palette.

### Files Created
| File | Purpose |
|------|---------|
| `requirements.txt` | Python dependencies |
| `.streamlit/config.toml` | Streamlit dark theme config |
| `brain_logic.py` | Neuro-reasoning engine (LLM + NCERT + validation) |
| `app.py` | Streamlit UI with Neuro-Lab styling |
| `DEV_LOG.md` | This decision log |

### Copilot Contributions
- **100% of scaffolding** generated via Copilot Agent Mode.
- Copilot designed the NCERT reference data structure, prompt engineering strategy,
  validation logic, Mermaid rendering pipeline, and full CSS theme.
- Every architectural decision was made collaboratively in a single agent session.

---

*Next session: Testing with real stimuli, refining Mermaid output, adding error handling edge cases.*
