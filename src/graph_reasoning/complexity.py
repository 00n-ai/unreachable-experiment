"""Deterministic structural and query-specific graph complexity metrics."""

from __future__ import annotations

from collections import Counter, deque
from math import log2
from typing import Any, Dict, Mapping


def graph_complexity(graph: Mapping[str, Any], start_entity: str,
                     target_predicate: str) -> Dict[str, Any]:
    node_types = {str(n["id"]): str(n["type"]) for n in graph["nodes"]}
    outgoing = {node: [] for node in node_types}
    incoming = {node: [] for node in node_types}
    for edge in graph["edges"]:
        source, target = str(edge["source"]), str(edge["target"])
        outgoing[source].append(target)
        incoming[target].append(source)
    for values in outgoing.values():
        values.sort()
    for values in incoming.values():
        values.sort()

    distance = {start_entity: 0}
    parents = {start_entity: []}
    queue = deque([start_entity])
    while queue:
        node = queue.popleft()
        for child in outgoing[node]:
            candidate = distance[node] + 1
            if child not in distance:
                distance[child] = candidate
                parents[child] = [node]
                queue.append(child)
            elif candidate == distance[child]:
                parents[child].append(node)
    reachable = set(distance)
    reachable_edge_count = sum(
        str(edge["source"]) in reachable and str(edge["target"]) in reachable
        for edge in graph["edges"]
    )
    reachable_predicates = {n for n in reachable if node_types[n] == "predicate"}
    target_reachable = target_predicate in reachable

    ancestors = set()
    if target_reachable:
        stack = [target_predicate]
        while stack:
            node = stack.pop()
            if node in ancestors:
                continue
            ancestors.add(node)
            stack.extend(p for p in incoming[node] if p in reachable)
    proof_nodes = {n for n in ancestors if node_types[n] == "predicate"}
    distractors = reachable_predicates - proof_nodes
    predicate_out_degrees = [
        len([child for child in outgoing[node] if node_types[child] == "predicate"])
        for node in reachable_predicates
    ]
    level_counts = Counter(distance[n] for n in reachable_predicates)
    branching_nodes = sum(degree > 1 for degree in predicate_out_degrees)
    merge_nodes = sum(
        len([p for p in incoming[node] if p in reachable_predicates]) > 1
        for node in reachable_predicates
    )

    # Count shortest paths only; this remains finite even if a future graph has cycles.
    shortest_path_counts = {start_entity: 1}
    for node, _ in sorted(distance.items(), key=lambda item: item[1]):
        if node == start_entity:
            continue
        shortest_path_counts[node] = sum(
            shortest_path_counts.get(parent, 0) for parent in parents[node]
        )
    entropy = sum(log2(degree) for degree in predicate_out_degrees if degree > 1)
    target_depth = distance.get(target_predicate)
    shortest_proof_node_count = target_depth + 1 if target_depth is not None else None
    proof_density = (
        shortest_proof_node_count / len(reachable)
        if shortest_proof_node_count is not None and reachable else None
    )
    return {
        "node_count": len(node_types),
        "predicate_node_count": sum(t == "predicate" for t in node_types.values()),
        "entity_node_count": sum(t == "entity" for t in node_types.values()),
        "edge_count": len(graph["edges"]),
        "reachable_node_count": len(reachable),
        "reachable_edge_count": reachable_edge_count,
        # Deterministic forward graph search has worst-case O(V + E) work.
        "graph_work_units": len(reachable) + reachable_edge_count,
        "reachable_predicate_count": len(reachable_predicates),
        "max_reachable_depth": max(distance.values()) if distance else 0,
        "mean_branching_factor": (
            sum(predicate_out_degrees) / len(predicate_out_degrees)
            if predicate_out_degrees else 0.0
        ),
        "max_branching_factor": max(predicate_out_degrees, default=0),
        "branching_node_count": branching_nodes,
        "merge_node_count": merge_nodes,
        "convergence_rate": merge_nodes / len(reachable_predicates)
        if reachable_predicates else 0.0,
        "leaf_count": sum(degree == 0 for degree in predicate_out_degrees),
        "max_width": max(level_counts.values(), default=0),
        "target_reachable": target_reachable,
        "target_depth": target_depth,
        "shortest_target_path_count": shortest_path_counts.get(target_predicate, 0),
        "shortest_proof_node_count": shortest_proof_node_count,
        "shortest_proof_edge_count": target_depth,
        "proof_predicate_count": len(proof_nodes),
        "proof_density": proof_density,
        "search_overhead_ratio": (
            1.0 - proof_density if proof_density is not None else None
        ),
        "distractor_node_count": len(distractors),
        "distractor_ratio": (
            len(distractors) / len(reachable_predicates)
            if reachable_predicates else 0.0
        ),
        "branching_entropy_bits": entropy,
    }
