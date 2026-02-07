"""
Synapse-Architect: Neuro-Reasoning Engine
Traces neural signal pathways from stimulus to cortex in 5 logical steps,
generates Mermaid.js flowcharts, and cross-checks against NCERT biology standards.
"""

import json
import re
import streamlit as st
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# --- GitHub Models API setup ---
GITHUB_MODELS_ENDPOINT = "https://models.inference.ai.azure.com"

client = ChatCompletionsClient(
    endpoint=GITHUB_MODELS_ENDPOINT,
    credential=AzureKeyCredential(st.secrets["GITHUB_TOKEN"]),
)

NCERT_REFERENCE = {
    "receptor_types": {
        "nociceptors": "Pain receptors in skin/tissue detecting harmful stimuli",
        "thermoreceptors": "Detect temperature changes (hot/cold)",
        "photoreceptors": "Rods and cones in retina detecting light",
        "mechanoreceptors": "Detect pressure, touch, vibration",
        "chemoreceptors": "Detect chemical stimuli (taste, smell)",
        "proprioceptors": "Detect body position and movement",
    },
    "neuron_types": {
        "sensory_neuron": "Afferent neuron carrying signals from receptor to CNS",
        "motor_neuron": "Efferent neuron carrying signals from CNS to effector",
        "interneuron": "Relay neuron within CNS connecting sensory and motor neurons",
    },
    "signal_pathway_components": [
        "Receptor/Sense Organ",
        "Sensory (Afferent) Neuron",
        "Spinal Cord / Brain Stem (CNS Relay)",
        "Interneuron / Relay Neuron",
        "Brain Region (Processing Center)",
    ],
    "key_brain_regions": {
        "somatosensory_cortex": "Processes touch, pain, temperature (parietal lobe)",
        "motor_cortex": "Initiates voluntary movement (frontal lobe)",
        "visual_cortex": "Processes visual information (occipital lobe)",
        "auditory_cortex": "Processes sound (temporal lobe)",
        "cerebellum": "Coordinates balance and fine motor control",
        "hypothalamus": "Regulates temperature, hunger, thirst",
        "medulla_oblongata": "Controls involuntary functions (breathing, heart rate)",
    },
    "signal_transmission": {
        "synapse": "Junction between two neurons; signal crosses via neurotransmitters",
        "neurotransmitters": "Chemical messengers (e.g., acetylcholine, dopamine)",
        "action_potential": "Electrical impulse traveling along the axon",
        "reflex_arc": "Rapid involuntary response pathway bypassing the brain",
    },
    "ncert_chapters": [
        "Class 10 Ch.7: Control and Coordination",
        "Class 11 Ch.21: Neural Control and Coordination",
        "Class 12 Ch.4: Human Neural System (reference)",
    ],
}


def get_ncert_context() -> str:
    """Serialize the NCERT reference data into an LLM-friendly string."""
    lines = ["=== NCERT BIOLOGY REFERENCE DATA ==="]

    lines.append("\n## Receptor Types:")
    for key, val in NCERT_REFERENCE["receptor_types"].items():
        lines.append(f"  - {key}: {val}")

    lines.append("\n## Neuron Types:")
    for key, val in NCERT_REFERENCE["neuron_types"].items():
        lines.append(f"  - {key}: {val}")

    lines.append("\n## Standard Signal Pathway Components (5-step model):")
    for i, comp in enumerate(NCERT_REFERENCE["signal_pathway_components"], 1):
        lines.append(f"  Step {i}: {comp}")

    lines.append("\n## Key Brain Regions:")
    for key, val in NCERT_REFERENCE["key_brain_regions"].items():
        lines.append(f"  - {key}: {val}")

    lines.append("\n## Signal Transmission Concepts:")
    for key, val in NCERT_REFERENCE["signal_transmission"].items():
        lines.append(f"  - {key}: {val}")

    lines.append("\n## NCERT Chapter References:")
    for ch in NCERT_REFERENCE["ncert_chapters"]:
        lines.append(f"  - {ch}")

    return "\n".join(lines)


SYSTEM_PROMPT = f"""You are Synapse-Architect, a neuroscience reasoning agent for students.

Your task: Given a stimulus, trace the complete neural signal pathway in EXACTLY 5 logical steps,
from the receptor to the brain's processing center.

{get_ncert_context()}

You MUST respond with valid JSON only — no markdown, no explanation outside the JSON.
Do NOT wrap the JSON in ```json``` code fences. Output raw JSON only.

JSON schema:
{{
  "stimulus": "<the input stimulus>",
  "steps": [
    {{
      "step_number": 1,
      "title": "<short title>",
      "description": "<detailed NCERT-aligned explanation, 2-3 sentences>",
      "structure": "<anatomical structure involved>",
      "ncert_reference": "<relevant NCERT chapter/concept>"
    }},
    ... (exactly 5 steps)
  ],
  "mermaid_flowchart": "<valid Mermaid.js flowchart string using graph TD>",
  "ncert_accuracy_notes": "<paragraph explaining how each step aligns with NCERT standards>",
  "reflex_arc_note": "<if applicable, explain the reflex arc shortcut>"
}}

Rules:
1. Always start at the receptor and end at the brain processing center.
2. Each step must reference real anatomical structures.
3. The Mermaid flowchart must use graph TD syntax with descriptive node labels.
4. Wrap node labels in quotes if they contain special characters.
5. Cross-check every step against the NCERT reference data provided.
6. Be educational — this is for students preparing for exams.
"""


def _extract_json(text: str) -> dict:
    """Parse JSON from the LLM response, handling markdown fences if present."""
    # Try direct parse first
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Strip markdown ```json ... ``` fences if the model wrapped them
    match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if match:
        return json.loads(match.group(1).strip())

    raise ValueError("Could not parse JSON from model response")


def trace_neural_pathway(stimulus: str) -> dict:
    """
    Main agent function: takes a stimulus string and returns
    a structured neural pathway trace with 5 steps, a Mermaid chart,
    and NCERT grounding notes.
    """
    response = client.complete(
        model="gpt-4o",
        messages=[
            SystemMessage(content=SYSTEM_PROMPT),
            UserMessage(
                content=(
                    f"Trace the complete neural signal pathway for this stimulus: "
                    f"'{stimulus}'. Provide exactly 5 steps from receptor to brain, "
                    f"a Mermaid.js flowchart, and NCERT accuracy cross-check."
                )
            ),
        ],
        temperature=0.3,
        max_tokens=2000,
    )

    raw = response.choices[0].message.content
    result = _extract_json(raw)
    return result


def validate_response(result: dict) -> dict:
    """
    Validates the LLM response structure and returns a validation report.
    """
    report = {"valid": True, "errors": [], "warnings": []}

    # Check required keys
    required_keys = [
        "stimulus",
        "steps",
        "mermaid_flowchart",
        "ncert_accuracy_notes",
    ]
    for key in required_keys:
        if key not in result:
            report["valid"] = False
            report["errors"].append(f"Missing required key: '{key}'")

    # Check steps count
    steps = result.get("steps", [])
    if len(steps) != 5:
        report["valid"] = False
        report["errors"].append(f"Expected 5 steps, got {len(steps)}")

    # Check each step structure
    step_keys = [
        "step_number",
        "title",
        "description",
        "structure",
        "ncert_reference",
    ]
    for i, step in enumerate(steps):
        for key in step_keys:
            if key not in step:
                report["warnings"].append(
                    f"Step {i + 1} missing key: '{key}'"
                )

    # Check Mermaid syntax starts correctly
    mermaid = result.get("mermaid_flowchart", "")
    if not mermaid.strip().startswith("graph TD"):
        report["warnings"].append(
            "Mermaid flowchart may not use 'graph TD' syntax"
        )

    return report


def extract_mermaid_chart(result: dict) -> str:
    """Extract and sanitize the Mermaid flowchart from the result."""
    mermaid = result.get("mermaid_flowchart", "graph TD\n  A[No data] --> B[Error]")
    # Clean up any escaped newlines
    mermaid = mermaid.replace("\\n", "\n")
    return mermaid
