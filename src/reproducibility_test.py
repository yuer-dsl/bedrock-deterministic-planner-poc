"""
reproducibility_test.py

Small script to compare:
- How many unique plans the deterministic planner produces
- How many unique plans the mock dynamic planner produces

This is *not* a benchmark, just a small reproducibility illustration.
"""

import json
from typing import Any, Dict, List, Set, Tuple

from .deterministic_planner import build_plan, plan_to_dict
from .bedrock_agent_stub import mock_dynamic_planner


def serialize_plan(plan: Dict[str, Any]) -> str:
    """
    Serialize a plan dict into a canonical JSON string for comparison.
    - sort_keys=True to ignore key ordering differences
    """
    return json.dumps(plan, sort_keys=True, ensure_ascii=False)


def run_deterministic_trials(request: str, n: int) -> Tuple[int, List[Dict[str, Any]]]:
    seen: Set[str] = set()
    plans: List[Dict[str, Any]] = []
    for _ in range(n):
        p = plan_to_dict(build_plan(request))
        s = serialize_plan(p)
        seen.add(s)
        plans.append(p)
    return len(seen), plans


def run_dynamic_trials(request: str, n: int) -> Tuple[int, List[Dict[str, Any]]]:
    seen: Set[str] = set()
    plans: List[Dict[str, Any]] = []
    for _ in range(n):
        p = mock_dynamic_planner(request)
        s = serialize_plan(p)
        seen.add(s)
        plans.append(p)
    return len(seen), plans


def main() -> None:
    request = "Find 3 recent papers on deterministic AI agents and summarize the key patterns."
    trials = 10

    print(f"Testing with request:\n  {request}\n")
    print(f"Number of trials: {trials}\n")

    det_unique, _ = run_deterministic_trials(request, trials)
    dyn_unique, _ = run_dynamic_trials(request, trials)

    print("=== Results ===")
    print(f"Deterministic planner: {det_unique} unique plan(s) over {trials} runs.")
    print(f"Dynamic mock planner:  {dyn_unique} unique plan(s) over {trials} runs.")
    print()
    if det_unique == 1:
        print("✅ Deterministic planner is fully reproducible for this input.")
    else:
        print("⚠️ Deterministic planner produced more than one unique plan (unexpected).")

    if dyn_unique > 1:
        print("✅ Dynamic planner shows non-deterministic behavior (as expected).")
    else:
        print("⚠️ Dynamic planner appears deterministic in this small sample (could be luck).")


if __name__ == "__main__":
    main()
