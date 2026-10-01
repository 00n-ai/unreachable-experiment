"""Versioned prompt builders for the three experimental conditions."""

from __future__ import annotations

import json
from typing import Any, Dict, List, Mapping


PROMPT_VERSION = "experiment1-text-answer-last-v3"

SYSTEM_PROMPT = """You solve synthetic deductive reasoning problems.
Treat every predicate and entity name as an arbitrary symbol. Use only the
facts, implication rules, or graph supplied in this request. Do not use outside
knowledge. Follow the requested plain-text response structure exactly. Do not
use JSON, Markdown, code fences, or text outside the structure."""

ANSWER_SCHEMA = """Return plain text in exactly this structure:
STEP 1: first derived proposition
STEP 2: second derived proposition
ANSWER: True
END

Include one STEP line per derived proposition, numbered consecutively from 1.
After all STEP lines, write ANSWER followed by either True or False. If no
derivation is needed, begin with the ANSWER line. Do not include commentary,
confidence, alternatives, or unstated facts."""

GRAPH_SCHEMA = """Return plain text in exactly this structure:
NODE | symbol | entity
NODE | symbol | predicate
EDGE | source_symbol | instance_of | target_symbol
EDGE | source_symbol | implies | target_symbol
END

Emit one NODE line per node and one EDGE line per edge. Node types must be
entity or predicate. Edge types must be instance_of or implies. Include every
fact and implication exactly once. Do not infer transitive edges or answer the
question in this phase."""


def _user(content: str) -> List[Dict[str, str]]:
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": content},
    ]


def condition_a(instance: Mapping[str, Any]) -> List[Dict[str, str]]:
    """Natural-language-only baseline."""
    return _user(
        "Condition: Natural Language Only\n\n"
        "World:\n"
        + str(instance["context"])
        + "\n\nQuestion:\n"
        + str(instance["question"])
        + "\n\n"
        + ANSWER_SCHEMA
    )


def condition_a_branching(instance: Mapping[str, Any]) -> List[Dict[str, str]]:
    """Natural-language branching baseline with witness/exhaustion parity."""
    return _user(
        "Condition: Natural Language Branching World\n\n"
        "World:\n"
        + str(instance["context"])
        + "\n\nQuestion:\n"
        + str(instance["question"])
        + "\n\nDetermine whether the query predicate is reachable from the entity "
          "through the stated implications. If it is reachable, return exactly "
          "one contiguous entity-level proof path and omit all distractor branches. "
          "If it is unreachable, return no STEP lines. Account for query negation "
          "when selecting the Boolean answer.\n\n"
        + ANSWER_SCHEMA
    )


def condition_b_build_graph(instance: Mapping[str, Any]) -> List[Dict[str, str]]:
    """First Model-Built-Graph call: externalize the natural-language world."""
    return _user(
        "Condition: Model-Built Graph — Graph Construction Phase\n\n"
        "World:\n"
        + str(instance["context"])
        + "\n\nQuestion (provided for parity; do not answer it yet):\n"
        + str(instance["question"])
        + "\n\n"
        + GRAPH_SCHEMA
    )


def condition_b_answer(
    instance: Mapping[str, Any], constructed_graph: Mapping[str, Any]
) -> List[Dict[str, str]]:
    """Second Model-Built-Graph call: answer using only constructed state."""
    return _user(
        "Condition: Model-Built Graph — Graph Reasoning Phase\n\n"
        "Use only this model-constructed graph:\n"
        + json.dumps(constructed_graph, sort_keys=True, separators=(",", ":"))
        + "\n\nQuestion:\n"
        + str(instance["question"])
        + "\n\n"
        + ANSWER_SCHEMA
    )


def condition_c(instance: Mapping[str, Any]) -> List[Dict[str, str]]:
    """Gold-graph condition; intentionally excludes natural-language context."""
    return _user(
        "Condition: Gold Graph\n\n"
        "Use only this benchmark-derived graph:\n"
        + json.dumps(instance["gold_graph"], sort_keys=True, separators=(",", ":"))
        + "\n\nQuestion:\n"
        + str(instance["question"])
        + "\n\n"
        + ANSWER_SCHEMA
    )
