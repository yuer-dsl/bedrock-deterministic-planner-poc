# Bedrock Deterministic Planner PoC

> A minimal, model-agnostic proof-of-concept showing how a **deterministic planning layer**
> can make AI agents more reproducible and auditable than a purely dynamic,
> LLM-driven planner.

This repo does **not** replace AWS Bedrock Agents.  
It simply demonstrates a contrasting approach:

- Bedrock-style dynamic planning → **flexible but non-deterministic**
- Deterministic planner layer → **less flexible but reproducible and auditable**

The goal is to make the discussion around **enterprise-grade reliability** more concrete.

---

## 🌱 Problem

In many agent frameworks (including cloud-based ones), the typical pattern is:

1. User gives a high-level request
2. LLM-based planner decides the steps, tools, order, parameters
3. Each run may produce a different plan, even with the **same input**
4. This makes:
   - Debugging harder
   - Audit trails weaker
   - Replay / reproduction uncertain
   - Enterprise usage more risky

> Same input, different route → hard to call it “enterprise-grade”.

---

## ✅ What this PoC shows

This PoC focuses on the **planning layer only**.

Given a textual goal like:

> "Find 3 recent papers on deterministic AI agents and summarize the key patterns."

The deterministic planner will always:

- Normalize the intent
- Map it to a fixed pipeline template
- Produce the **same JSON plan** on every run

Example output:

```json
{
  "goal": "find_papers_and_summarize",
  "original_request": "Find 3 recent papers on deterministic AI agents and summarize the key patterns.",
  "steps": [
    {
      "id": 1,
      "action": "search",
      "params": {
        "query": "deterministic AI agents recent papers",
        "top_k": 3
      }
    },
    {
      "id": 2,
      "action": "extract",
      "params": {
        "fields": ["title", "year", "abstract"]
      }
    },
    {
      "id": 3,
      "action": "summarize",
      "params": {
        "style": "concise",
        "max_words": 300
      }
    }
  ],
  "constraints": {
    "max_latency_ms": 8000,
    "must_be_reproducible": true
  }
}

Run it 5 times → same plan.
Run a dynamic LLM planner 5 times → likely different plans.

This is the entire point of the PoC.

📁 Project structure

bedrock-deterministic-planner-poc/
  README.md                 # You are here
  pipeline_schema.json      # JSON schema describing the plan structure
  src/
    deterministic_planner.py    # Small deterministic planner implementation
    reproducibility_test.py     # Script to test determinism vs dynamic planner
    bedrock_agent_stub.py       # Example stub for integrating with Bedrock Agent (optional)

🔧 Installation

git clone https://github.com/<your-account>/bedrock-deterministic-planner-poc.git
cd bedrock-deterministic-planner-poc

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt  # (if you add any dependencies)

For this PoC, the core scripts only use the Python standard library.

▶️ Usage
1. Generate deterministic plans

python -m src.deterministic_planner \
  --goal "Find 3 recent papers on deterministic AI agents and summarize them."

Expected:
You get a JSON plan printed to stdout.
Run it multiple times → it should be identical.

2. Reproducibility test

python -m src.reproducibility_test

This script will:

Call the deterministic planner N times

(Optionally) call a dynamic planner / Bedrock Agent N times

Print a small report showing:

How many unique plans from the deterministic planner

How many unique plans from the dynamic planner

By default, the dynamic planner is stubbed / mocked,
so it can run without any AWS credentials.

You can edit bedrock_agent_stub.py to connect to a real Bedrock Agent
if you want to reproduce the behavior in your environment.

🔍 pipeline_schema.json

We define a simple, explicit schema for plans.
This is not meant to be complete, just illustrative.

Key properties:

goal: normalized string ID for the task type

original_request: original user expression

steps: ordered list

each step:

id: integer

action: string enum (search, extract, call_api, summarize, etc.)

params: free-form object

constraints: additional execution constraints (latency, reproducibility flag, etc.)

The schema itself is in pipeline_schema.json.

🧪 Why this matters

The purpose of this PoC is not to say:

“Dynamic planning is wrong.”

But to ask a simple question:

“If we never have a deterministic, spec-driven planning mode,
can we really call our agent systems enterprise-grade and auditable?”

This repo is a tiny, practical argument for:

reproducibility

specification

explicit constraints

transparent planning

⚠️ Notes

This PoC is model-agnostic.

It does not expose any internal architecture beyond what is visible in the code.

It is intended as a reference and discussion piece,
not as a production-ready framework.

If you find this useful or want to extend it to your own agents,
feel free to fork and adapt.

— Yuer
