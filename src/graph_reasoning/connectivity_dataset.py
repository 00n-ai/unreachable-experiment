"""Matched worlds with targets present in both answer classes (version 3)."""

import hashlib
from .complexity import graph_complexity

VERSION = "controlled-connectivity-v3"


def make_connectivity_example(depth, breadth, replicate, reachable, negated, seed=62471893):
    if depth < 1 or breadth < 1 or replicate < 0:
        raise ValueError("depth/breadth must be positive and replicate nonnegative")
    # Reachability and polarity do not alter the vocabulary or implication rules.
    nonce = f"{VERSION}|{seed}|{depth}|{breadth}|{replicate}"
    def symbol(role, prefix="p"):
        return prefix + hashlib.sha256(f"{nonce}|{role}".encode()).hexdigest()[:12]
    entity = symbol("entity", "e")
    spines = [[symbol(f"component-{c}-spine-{i}") for i in range(depth+1)]
              for c in range(2)]
    predicates, rules = [], []
    for c, spine in enumerate(spines):
        predicates.extend(spine)
        for i in range(depth):
            children = [spine[i+1]]
            for j in range(breadth-1):
                child = symbol(f"component-{c}-leaf-{i}-{j}")
                predicates.append(child)
                children.append(child)
            for child in children:
                rules.append({"type": "implication", "antecedent": spine[i],
                              "consequent": child})
    if len(set(predicates+[entity])) != len(predicates)+1:
        raise ValueError("Symbol collision")
    target = spines[0][-1]
    root = spines[0 if reachable else 1][0]
    fact = {"entity": entity, "predicate": root}
    edges = [{"source": r["antecedent"], "target": r["consequent"], "type": "implies"}
             for r in rules] + [{"source": entity, "target": root, "type": "instance_of"}]
    graph = {"nodes": [{"id": p, "type": "predicate"} for p in predicates]
             + [{"id": entity, "type": "entity"}], "edges": edges}
    context = [f"Every {r['antecedent']} is a {r['consequent']}." for r in rules]
    # Stable sentence slots across the matched reachable/unreachable worlds.
    ordered = [(hashlib.sha256(f"{nonce}|sentence|{i}".encode()).hexdigest(), text)
               for i, text in enumerate(context+[f"{entity} is a {root}."])]
    context = [text for _,text in sorted(ordered)]
    query_text = f"{entity} is {'not ' if negated else ''}a {target}."
    instance = {
        "schema_version": VERSION, "generator": "matched_two_component_spines",
        "instance_id": f"connectivity-d{depth}-b{breadth}-i{replicate}-"
                       f"{'r' if reachable else 'u'}-{'n' if negated else 'p'}-s{seed}",
        "reasoning_depth": depth, "chain_length": depth, "branching_factor": breadth,
        "context_sentences": context, "context": " ".join(context),
        "question": "True or false: " + query_text,
        "query": {"entity": entity, "predicate": target, "negated": negated, "text": query_text},
        "answer": str(reachable != negated), "answer_boolean": reachable != negated,
        "formal_world": {"facts": [fact], "rules": rules}, "gold_graph": graph,
        "gold_proof": {
            "seed_fact": {**fact, "text": f"{entity} is a {root}."},
            "kind": "witness" if reachable else "exhaustion",
            "rule_applications": depth if reachable else 0,
            "steps": [{"step": i+1, "derives": spines[0][i+1],
                       "text": f"{entity} is a {spines[0][i+1]}."}
                      for i in range(depth)] if reachable else [],
        },
        "anonymization": {"version": "opaque-sha256-v1", "model_visible_role_labels": False},
    }
    instance["graph_complexity"] = graph_complexity(graph, entity, target)
    assert instance["graph_complexity"]["target_reachable"] == reachable
    assert target in instance["context"]
    return instance


def balanced_cell(depth, breadth, n=4, seed=62471893, replicate_offset=0):
    if n < 4 or n % 4:
        raise ValueError("samples per cell must be a positive multiple of four")
    return [make_connectivity_example(depth, breadth, rep, reachable, negated, seed)
            for rep in range(replicate_offset, replicate_offset+n//4)
            for reachable in (True, False) for negated in (False, True)]
