# 🧠 Synapse-Architect

**Autonomous Neuro-Reasoning Agent for Students**

> Enter a stimulus. Watch the neural signal trace itself — from receptor to cortex — in 5 NCERT-grounded steps with a real-time flowchart.

![Python](https://img.shields.io/badge/Python-3.10+-39FF14?style=flat&logo=python&logoColor=39FF14)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-39FF14?style=flat&logo=streamlit&logoColor=39FF14)

---

## 🚀 Quick Start

1. **Clone & install:**
   ```bash
   git clone <your-repo-url>
   cd synapse-architect
   pip install -r requirements.txt
   ```

2. **Set your API key:**
   ```bash
   echo "OPENAI_API_KEY=sk-your-key-here" > .env
   ```

3. **Run the app:**
   ```bash
   streamlit run app.py
   ```

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🧬 **5-Step Reasoning** | Traces neural signals from receptor → cortex in 5 logical steps |
| 📊 **Live Flowchart** | Real-time Mermaid.js neural circuit visualization |
| ✅ **NCERT Grounded** | Cross-checked against Class 10-12 NCERT Biology |
| 🎨 **Neuro-Lab UI** | Dark-mode interface with neon green accents |

---

## 🏗️ Architecture

```
app.py              → Streamlit UI (Neuro-Lab theme)
brain_logic.py      → LLM agent + NCERT data + validation
.streamlit/config.toml → Theme configuration
```

---

## 📖 Built For

**GitHub Copilot Agents League — Creative Apps Track ($500 Prize)**

See [DEV_LOG.md](DEV_LOG.md) for complete Copilot usage documentation.
