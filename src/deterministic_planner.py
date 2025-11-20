"""
deterministic_planner.py

A tiny, purely deterministic planner that turns a natural language goal
into a normalized, JSON-like execution plan.

- No randomness
- No LLM calls
- Same input → same output
"""

import argparse
import json
from dataclasses import dataclass, asdict
from typing import Any, Dict, List


@dataclass
class Step:
    id: int
    action: str
    params: Dict[str, Any]


@dataclass
class Plan:
    goal: str
    original_request: str
    steps: List[Step]
    constraints: Dict[str, Any]


def normalize_goal(request: str) -> str:
    """
    Very simple, rule-based goal normalization.
    This is intentionally naive and deterministic.
    """
    text = request.lower()

    if "paper" in text or "journal" in text or "research" in text:
        if "summar" in text:
            return "find_papers_and_summarize"
        return "find_papers"
    if "compare" in text or "vs" in text:
        return "compare_sources"
    if "report" in text and "generate" in text:
        return "generate_report"
    if "news" in text:
        return "fetch_news"
    # default fallback
    return "generic_information_task"


def build_steps(goal: str, request: str) -> List[Step]:
    """
    Build an ordered list of steps based on the normalized goal.
    Each branch is deterministic and static.
    """
    steps: List[Step] = []

    if goal == "find_papers_and_summarize":
        steps.append(
            Step(
                id=1,
                action="search",
                params={
                    "source": "scholar_like",
                    "query": request,
                    "top_k": 3,
                },
            )
        )
        steps.append(
            Step(
                id=2,
                action="extract",
                params={
                    "fields": ["title", "year", "abstract"],
                },
            )
        )
        steps.append(
            Step(
                id=3,
                action="summarize",
                params={
                    "style": "concise",
                    "max_words": 300,
                },
            )
        )
    elif goal == "find_papers":
        steps.append(
            Step(
                id=1,
                action="search",
                params={
                    "source": "scholar_like",
                    "query": request,
                    "top_k": 5,
                },
            )
        )
    elif goal == "compare_sources":
        steps.append(
            Step(
                id=1,
                action="identify_entities",
                params={
                    "from_request": True,
                    "max_entities": 4,
                },
            )
        )
        steps.append(
            Step(
                id=2,
                action="fetch_facts",
                params={
                    "per_entity_top_k": 3,
                },
            )
        )
        steps.append(
            Step(
                id=3,
                action="compare",
                params={
                    "dimensions": ["pros", "cons", "risks"],
                },
            )
        )
    elif goal == "generate_report":
        steps.append(
            Step(
                id=1,
                action="gather_context",
                params={
                    "source": "mixed",
                    "query": request,
                },
            )
        )
        steps.append(
            Step(
                id=2,
                action="outline",
                params={
                    "sections": ["introduction", "body", "conclusion"],
                },
            )
        )
        steps.append(
            Step(
                id=3,
                action="write",
                params={
                    "format": "markdown",
                    "target_audience": "general",
                },
            )
        )
    elif goal == "fetch_news":
        steps.append(
            Step(
                id=1,
                action="search",
                params={
                    "source": "news_api",
                    "query": request,
                    "top_k": 5,
                },
            )
        )
        steps.append(
            Step(
                id=2,
                action="summarize",
                params={
                    "style": "bullet_points",
                    "max_items": 5,
                },
            )
        )
    else:
        # generic fallback pipeline
        steps.append(
            Step(
                id=1,
                action="search",
                params={
                    "source": "web",
                    "query": request,
                    "top_k": 3,
                },
            )
        )
        steps.append(
            Step(
                id=2,
                action="summarize",
                params={
                    "style": "short",
                    "max_words": 200,
                },
            )
        )

    return steps


def build_plan(request: str) -> Plan:
    """
    Deterministic end-to-end plan builder.
    """
    goal = normalize_goal(request)
    steps = build_steps(goal, request)
    constraints: Dict[str, Any] = {
        "max_latency_ms": 8000,
        "must_be_reproducible": True,
    }
    return Plan(
        goal=goal,
        original_request=request,
        steps=steps,
        constraints=constraints,
    )


def plan_to_dict(plan: Plan) -> Dict[str, Any]:
    # Convert dataclasses to pure dict structure for JSON dumping
    data = asdict(plan)
    return data


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Deterministic planner PoC"
    )
    parser.add_argument(
        "--goal",
        type=str,
        required=True,
        help="User goal / task description in natural language.",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON output.",
    )
    args = parser.parse_args()

    plan = build_plan(args.goal)
    as_dict = plan_to_dict(plan)
    if args.pretty:
        print(json.dumps(as_dict, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(as_dict, ensure_ascii=False))


if __name__ == "__main__":
    main()
