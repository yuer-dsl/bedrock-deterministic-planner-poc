"""
bedrock_agent_stub.py

This file provides:
- a mock "dynamic planner" to simulate non-deterministic behavior
- an optional placeholder for integrating with a real AWS Bedrock Agent

By default, this module does NOT call any external service.
"""

import copy
import random
from typing import Any, Dict, List


def mock_dynamic_planner(request: str) -> Dict[str, Any]:
    """
    Simulate a non-deterministic planner:
    - For the same input, it may produce different orders of steps
    - Or slightly different parameters

    This is only for demonstration purposes.
    """
    base_steps: List[Dict[str, Any]] = [
        {
            "id": 1,
            "action": "search",
            "params": {"source": "web", "query": request, "top_k": 3},
        },
        {
            "id": 2,
            "action": "summarize",
            "params": {"style": "short", "max_words": 200},
        },
        {
            "id": 3,
            "action": "reflect",
            "params": {"check_consistency": True},
        },
    ]

    # Randomly shuffle steps and tweak parameters a bit
    steps = copy.deepcopy(base_steps)
    random.shuffle(steps)

    # Randomly alter a param to show drift
    if random.random() < 0.5:
        for step in steps:
            if step["action"] == "search":
                step["params"]["top_k"] = random.choice([3, 4, 5])
            if step["action"] == "summarize":
                step["params"]["max_words"] = random.choice([150, 200, 250])

    plan: Dict[str, Any] = {
        "goal": "mock_dynamic_plan",
        "original_request": request,
        "steps": steps,
        "constraints": {
            "max_latency_ms": None,
            "must_be_reproducible": False,
        },
    }
    return plan


# ---------------------------------------------------------------------------
# Optional: placeholder for real Bedrock Agent integration
# ---------------------------------------------------------------------------

def bedrock_agent_plan_placeholder(request: str) -> Dict[str, Any]:
    """
    Placeholder function.

    If you want to compare this PoC with a real AWS Bedrock Agent,
    you can implement the call here using boto3 or the official SDK.

    For example (pseudo-code):

    import boto3

    client = boto3.client("bedrock-agent-runtime", region_name="us-east-1")
    response = client.invoke_agent(
        agentId="your-agent-id",
        agentAliasId="your-alias-id",
        sessionId="test-session",
        inputText=request,
    )
    # Then parse response into a plan-like structure.

    This is intentionally left unimplemented in this PoC,
    to keep it model-agnostic and credentials-free.
    """
    raise NotImplementedError("Implement this if you want real Bedrock integration.")
