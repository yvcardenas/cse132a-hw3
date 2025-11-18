#!/usr/bin/env python3
"""
HW3 (Version 2.0.0) - Super simple 3NF / BCNF task.

You only need to fill in two functions below:
- solve_3nf(...)
- solve_bcnf(...)
We already read the JSON file for you and print the result.
No fancy Python features, just lists and dicts.
"""
import json
import sys
from pathlib import Path

# Keep this version as-is
ASSIGNMENT_VERSION = (2, 0, 0)  # v2.0.0

# Helper Functions
# Make all the functional dependencies into a more usable form
def fds_into_sets(functional_dependencies):
    fds = []
    for fd in functional_dependencies:
        left = set(fd["left"])
        right = fd["right"][0]
        fds.append((left, right))
    return fds

# Compute closure
def compute_closure():
    pass

# Compute minimal cover
def compute_minimal_cover(fds):
    fds = [(set(left), right) for left, right in fds]

    for i, (left, right) in enumerate(list(fds)):
        for attr in list(left):
            test_left = left - {attr}
            if not test_left:
                continue
            if right in compute_closure(test_left, fds):
                left.remove(attr)
        fds[i] = (left, right)
    
    # Remove redundant FDs
    changed = True
    while changed:
        changed = False
        for i in range(len(fds)):
            left, right = fds[i]
            others = [fds[j] for j in range(len(fds)) if j != i]
            if right in compute_closure(left, others):
                fds.pop(i)
                changed = True
                break

    return fds

def project_fds(fds, attributes):
    attrs = set(attributes)
    projected = []
    for left, right in fds:
        if left.issubset(attrs) and right in attrs:
            projected.append((set(left), right))
    return projected

# Is X a superkey for the relation
def is_superkey(X, attributes, fds):
    attrs = set(attributes)
    fds_R = project_fds(fds, attrs)
    return compute_closure(X, fds_R) >= attrs

# Find candidate keys
def find_candidate_key(attrs, fds):
    key = set(attrs)
    for a in list(key):
        test = key - {a}
        if test and is_superkey(test, attrs, fds):
            key = test
    return list(key)

# bcnf recursive decomposition
def bcnf_recursive(attributes, fds):
    attrs = set(attributes)
    fds_R = project_fds(fds, attrs)

    for left, right in fds_R:
        if right not in left and not is_superkey(left, attributes, fds):
            closure_left = compute_closure(left, fds_R)
            R1 = closure_left & attrs
            R2 = attrs - (R1 - left)

            left_ = bcnf_recursive(list(R1), fds)
            right_ = bcnf_recursive(list(R2), fds)
            return left_ + right_
    return [list(attrs)]


def solve_3nf(relation_name, attributes, functional_dependencies):
    """
    TODO: Return the 3NF decomposition.

    Inputs:
      - relation_name: a string like "R"
      - attributes: a list of strings, e.g. ["A", "B", "C"]
      - functional_dependencies: a list of dicts, each like:
            {"left": ["A", "B"], "right": ["C"]}
        The right side always has exactly ONE attribute.

    Return:
      A list of relations. Each relation is a list of attribute names.
      Example: [["A","B"], ["B","C"]]
    """
    # Steps for decomposing into 3NF:
    # 1. Turn JSON FDs into a more usable form (set(left), right)
    fds = fds_into_sets(functional_dependencies)
    # 2. Find a minimal cover of the FDs (remove any redundant FDs/attributes)
    fds_minimal = compute_minimal_cover(fds)
    # 3. Create one relation for each FD in the minimal cover
    relations = []
    for left, right in fds_minimal:
        relation = set(left)
        relation.add(right)
        if relation not in relations:
            relations.append(list(relation))
    # 4. Ensure at least one relation contains a candidate key
    key = find_candidate_key(attributes, fds_minimal)
    contains_key = any(set(key).issubset(set(r)) for r in relations)
    if not contains_key:
        relations.append(set(key))

    final_relations = []
    for i, ri in enumerate(relations):
        redundant = False
        for j, rj in enumerate(relations):
            if i != j and set(ri).issubset(set(rj)):
                redundant = True
                break
            if not redundant:
                final_relations.append(ri)
    # 5. Return the list of relations
    return [sorted(list(r)) for r in final_relations]

def solve_bcnf(relation_name, attributes, functional_dependencies):
    """
    TODO: Return the BCNF decomposition.

    Inputs:
      - relation_name: a string like "R"
      - attributes: a list of strings, e.g. ["A", "B", "C"]
      - functional_dependencies: a list of dicts, each like:
            {"left": ["A", "B"], "right": ["C"]}
        The right side always has exactly ONE attribute.

    Return:
      A list of relations. Each relation is a list of attribute names.
      Example: [["A","B"], ["B","C"]]
    """
    fds = fds_into_sets(functional_dependencies)
    decomposed = bcnf_recursive(attributes, fds)
    return [sorted(list(r)) for r in decomposed]



def _read_input_json(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    relation_name = data.get("relationName", "R")
    attributes = data.get("attributes", [])
    fds = data.get("functionalDependencies", [])
    return relation_name, attributes, fds


def _validate_input(attributes, fds):
    if not attributes:
        raise ValueError("attributes must be a non-empty list")
    for i, fd in enumerate(fds):
        if "left" not in fd or "right" not in fd:
            raise ValueError(f"FD #{i} must have 'left' and 'right'")
        if not fd["left"] or not fd["right"]:
            raise ValueError(f"FD #{i} must have non-empty left and right")
        if len(fd["right"]) != 1:
            raise ValueError(f"FD #{i} right side must have exactly one attribute")
        # Basic attribute name check
        for a in fd["left"] + fd["right"]:
            if a not in attributes:
                raise ValueError(f"FD #{i} contains unknown attribute '{a}'")


def main():
    # Usage: python3 decompose_v2.py path/to/test.json
    if len(sys.argv) != 2:
        print("Usage: python3 decompose_v2.py path/to/test.json")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        sys.exit(1)

    relation_name, attributes, fds = _read_input_json(str(input_path))
    _validate_input(attributes, fds)

    # Students implement both functions
    result = {
        "3nf": solve_3nf(relation_name, attributes, fds),
        "bcnf": solve_bcnf(relation_name, attributes, fds),
    }

    # We just print the result as JSON
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()


