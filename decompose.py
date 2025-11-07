#!/usr/bin/env python3
"""
Starter code for CSE 132A HW3.

Students must implement:
  * infer_fds_from_sample
  * minimal_cover
  * synthesize_3nf
  * decompose_bcnf

Use the provided helper functions to keep the CLI contract and output format.
"""
import argparse
import json
import sys
from pathlib import Path
from typing import List, Tuple


# DO NOT CHANGE THIS VERSION.
# The version is only used if there is any update from the Github repo.
# You will get an error / warning message in Gradescope 
# telling you to update your code to the latest version.
ASSIGNMENT_VERSION = (1, 0, 0) # v1.0.0

# ---------------------------------------------------------------------------
# CLI helpers
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments for the decomposition tool.
    
    Returns:
        argparse.Namespace: Parsed arguments containing:
            - input (str): Path to input JSON file
            - to (str): Target normal form, either "3nf" or "bcnf"
            - output (str or None): Optional output JSON path
            - pretty (bool): Whether to pretty-print JSON output
    """
    parser = argparse.ArgumentParser(description="3NF / BCNF decomposition tool")
    parser.add_argument("--input", required=True, help="Path to input JSON file")
    parser.add_argument("--to", required=True, choices=["3nf", "bcnf"], help="Target normal form")
    parser.add_argument("--output", default=None, help="Optional output JSON path")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Input parsing
# ---------------------------------------------------------------------------

def parse_fd_json(fd_json: List[dict]) -> List[Tuple[frozenset, frozenset]]:
    """
    Convert JSON list of functional dependencies into internal frozenset representation.
    
    Args:
        fd_json (List[dict]): List of FD dictionaries, each with 'left' and 'right' keys.
                                   Example: [{"left": ["A"], "right": ["B"]}, ...]
    
    Returns:
        List[Tuple[frozenset, frozenset]]: List of FD tuples where each tuple contains:
            - First element: frozenset of LHS attributes
            - Second element: frozenset of RHS attributes
    
    Raises:
        ValueError: If any FD is missing 'left' or 'right', or if they are empty.
    """
    fds: List[Tuple[frozenset, frozenset]] = []
    for idx, fd in enumerate(fd_json):
        if "left" not in fd or "right" not in fd:
            raise ValueError(f"FD at index {idx} must contain 'left' and 'right'.")
        left = tuple(fd["left"])
        right = tuple(fd["right"])
        if not left or not right:
            raise ValueError(f"FD at index {idx} must have non-empty left/right sides.")
        fds.append((frozenset(left), frozenset(right)))
    return fds


# ---------------------------------------------------------------------------
# TODO: functions for students to implement. Do not change the function signatures unless explicitly instructed to do so.
# ---------------------------------------------------------------------------

def infer_fds_from_sample(attributes: List[str], sample_rows: List[dict]) -> List[Tuple[frozenset, frozenset]]:
    """
    TODO: Infer functional dependencies from sample data.
    
    This function discovers FDs by examining sample rows. An FD X → Y holds if:
    1. Whenever two rows agree on all attributes in X, they also agree on Y
    2. The attribute set X appears in at least 2 rows (support ≥ 2)
    
    Args:
        attributes (List[str]): List of all attribute names in the relation.
                                 Example: ["A", "B", "C"]
        sample_rows (List[dict]): List of sample data rows as dictionaries.
                                       Example: [{"A": "a1", "B": "b1", "C": "c1"}, ...]
    
    Returns:
        List[Tuple[frozenset, frozenset]]: List of inferred FDs as (LHS, RHS) tuples.
            - Each LHS is a frozenset of attribute names
            - Each RHS is a frozenset of attribute names
            - Note: RHS may contain multiple attributes initially, but will be
              reduced to singletons in the minimal_cover step.
    
    Example:
        attributes = ["A", "B", "C"]
        sample_rows = [{"A": "a1", "B": "b1", "C": "c1"},
                       {"A": "a1", "B": "b1", "C": "c1"}]
        Returns: [(frozenset({"A"}), frozenset({"B"})),
                  (frozenset({"A"}), frozenset({"C"})), ...]
    """
    raise NotImplementedError("infer_fds_from_sample must be implemented by the student.")


def minimal_cover(fds: List[Tuple[frozenset, frozenset]]) -> List[Tuple[frozenset, frozenset]]:
    """
    TODO: Compute a minimal (canonical) cover for the given functional dependencies.
    
    A minimal cover is a simplified set of FDs that is equivalent to the original set
    but has no redundancy. The algorithm should:
    1. Split all FDs so each has a singleton RHS (right side has exactly one attribute)
    2. Minimize the LHS by removing redundant attributes from each FD's left side
    3. Remove redundant FDs that can be inferred from other FDs
    
    Args:
        fds (List[Tuple[frozenset, frozenset]]): Input functional dependencies.
            Each tuple is (LHS, RHS) where both are frozensets of attribute names.
            Example: [(frozenset({"A"}), frozenset({"B", "C"})), ...]
    
    Returns:
        List[Tuple[frozenset, frozenset]]: Minimal cover of FDs where:
            - Each RHS is a singleton frozenset (contains exactly one attribute)
            - No LHS has redundant attributes
            - No FD is redundant (cannot be inferred from others)
            Example: [(frozenset({"A"}), frozenset({"B"})),
                      (frozenset({"A"}), frozenset({"C"})), ...]
    
    Note:
        Use closure computation to test if an attribute or FD is redundant.
    """
    raise NotImplementedError("minimal_cover must be implemented by the student.")


def synthesize_3nf(attributes: List[str], minimal_fds: List[Tuple[frozenset, frozenset]]) -> List[List[str]]:
    """
    TODO: Implement the 3NF synthesis algorithm.
    
    The 3NF synthesis algorithm creates relations in Third Normal Form using these steps:
    1. Start with a minimal cover of FDs
    2. Group FDs by their left-hand side (LHS)
    3. For each group with the same LHS X, create a relation R = X ∪ {all RHS attributes}
    4. If no relation contains a candidate key for the original relation, add a relation
       containing a candidate key
    5. Remove any relation that is a proper subset of another relation
    
    Args:
        attributes (List[str]): All attribute names in the original relation.
                                 Example: ["A", "B", "C", "D"]
        minimal_fds (List[Tuple[frozenset, frozenset]]): Minimal cover of FDs.
            Each tuple is (LHS, RHS) where RHS must be a singleton.
            Example: [(frozenset({"A"}), frozenset({"B"})),
                      (frozenset({"A"}), frozenset({"C"})), ...]
    
    Returns:
        List[List[str]]: List of relations, where each relation is a list of attribute names.
            Example: [["A", "B", "C"], ["C", "D"]]
            Note: The order of attributes within each relation doesn't matter as
            they will be sorted during output normalization.
    
    Example:
        Input: attributes=["A","B","C"], minimal_fds=[({"A"},{"B"}), ({"B"},{"C"})]
        Output: [["A","B"], ["B","C"]]
    """
    raise NotImplementedError("synthesize_3nf must be implemented by the student.")


def decompose_bcnf(attributes: List[str], minimal_fds: List[Tuple[frozenset, frozenset]]) -> List[List[str]]:
    """
    TODO: Implement the BCNF decomposition algorithm.
    
    The BCNF decomposition algorithm decomposes a relation into Boyce-Codd Normal Form:
    1. Start with the original relation R containing all attributes
    2. While there exists a relation Ri that violates BCNF:
       a. Find an FD X → Y where X is not a superkey of Ri
       b. Decompose Ri into two relations:
          - R1 = X ∪ Y
          - R2 = Ri - Y (remove Y, keep X and other attributes)
       c. Replace Ri with R1 and R2
    3. Continue until all relations are in BCNF
    
    A relation is in BCNF if for every non-trivial FD X → Y that holds in the relation,
    X is a superkey of that relation.
    
    Args:
        attributes (List[str]): All attribute names in the original relation.
                                 Example: ["A", "B", "C", "D"]
        minimal_fds (List[Tuple[frozenset, frozenset]]): Minimal cover of FDs.
            Each tuple is (LHS, RHS) where RHS is typically a singleton.
            Example: [(frozenset({"A"}), frozenset({"B"})),
                      (frozenset({"C"}), frozenset({"D"})), ...]
    
    Returns:
        List[List[str]]: List of relations in BCNF, where each relation is a list
            of attribute names.
            Example: [["A", "B"], ["A", "C"], ["C", "D"]]
            Note: The order of attributes within each relation doesn't matter as
            they will be sorted during output normalization.
    
    Example:
        Input: attributes=["A","B","C"], minimal_fds=[({"A","B"},{"C"}), ({"C"},{"B"})]
        Output might be: [["A","B"], ["B","C"]] (depends on decomposition order)
    
    Note:
        BCNF decomposition may not preserve all functional dependencies (not
        dependency-preserving), but it always preserves lossless join.
    """
    raise NotImplementedError("decompose_bcnf must be implemented by the student.")


# ---------------------------------------------------------------------------
# Output validation helpers
# ---------------------------------------------------------------------------

def _ensure_attribute_subset(attrs: List[str], universe: List[str], context: str) -> List[str]:
    """
    Validate and normalize a set of attributes against the universal schema.
    
    Helper function to ensure all attributes are valid members of the original schema
    and to return them in sorted order.
    
    Args:
        attrs (List[str]): Attributes to validate.
                            Example: ["B", "A", "C"]
        universe (List[str]): All valid attribute names in the original relation.
                               Example: ["A", "B", "C", "D"]
        context (str): Description of where this validation is happening (for error messages).
                       Example: "Relation #1" or "FD #2 (LHS)"
    
    Returns:
        List[str]: Sorted list of validated attributes.
                   Example: ["A", "B", "C"]
    
    Raises:
        AssertionError: If attrs is empty or contains attributes not in universe.
    """
    allowed = set(universe)
    normalized = sorted(attrs)
    if not normalized:
        raise AssertionError(f"{context}: relation must contain at least one attribute")
    for attr in normalized:
        if attr not in allowed:
            raise AssertionError(f"{context}: attribute '{attr}' not in original schema {universe}")
    return normalized


def normalize_relations(relations: List[List[str]], attributes: List[str]) -> List[List[str]]:
    """
    Validate and normalize relations returned by decomposition algorithms.
    
    This function ensures that:
    - All relations are properly formatted (lists of strings, not dicts)
    - All attributes in each relation are valid
    - No duplicate relations exist
    - Relations are sorted for consistent output
    
    Args:
        relations (List[List[str]]): List of relations to validate.
            Each relation should be a list of attribute names.
            Example: [["A", "B"], ["B", "C"], ["C", "D"]]
        attributes (List[str]): All valid attribute names from the original relation.
                                 Example: ["A", "B", "C", "D"]
    
    Returns:
        List[List[str]]: Validated and normalized relations where:
            - Each relation's attributes are sorted alphabetically
            - Relations are sorted by concatenated attribute names
            Example: [["A", "B"], ["B", "C"], ["C", "D"]]
    
    Raises:
        AssertionError: If relations is None, contains invalid formats, has duplicate
                        relations, or contains invalid attributes.
    """
    if relations is None:
        raise AssertionError("Expected a list of relations, got None")
    normalized: List[List[str]] = []
    seen = set()
    for idx, rel in enumerate(relations):
        if isinstance(rel, dict):
            raise AssertionError(f"Relation #{idx} should be a list of attribute names, not a dict")
        normalized_attrs = _ensure_attribute_subset(rel, attributes, f"Relation #{idx}")
        key = tuple(normalized_attrs)
        if key in seen:
            raise AssertionError(f"Duplicate relation detected: {normalized_attrs}")
        seen.add(key)
        normalized.append(normalized_attrs)
    normalized.sort(key=lambda xs: "".join(xs))
    return normalized


def normalize_fds_for_output(fds: List[Tuple[frozenset, frozenset]], attributes: List[str]) -> List[Tuple[List[str], List[str]]]:
    """
    Validate and normalize functional dependencies for output.
    
    This function ensures that:
    - All FDs have valid attributes from the original schema
    - Each FD has a singleton RHS (exactly one attribute on the right side)
    - Attributes are sorted within each FD
    
    Args:
        fds (List[Tuple[frozenset, frozenset]]): Functional dependencies to validate.
            Each FD is a tuple of (LHS, RHS) where both are frozensets of attribute names.
            Example: [(frozenset({"A"}), frozenset({"B"})), (frozenset({"B"}), frozenset({"C"}))]
        attributes (List[str]): All valid attribute names from the original relation.
                                 Example: ["A", "B", "C", "D"]
    
    Returns:
        List[Tuple[List[str], List[str]]]: Validated and normalized FDs where:
            - Each LHS and RHS are sorted lists of attributes
            - Each RHS contains exactly one attribute
            Example: [([("A"], ["B"]), (["B"], ["C"])]
    
    Raises:
        AssertionError: If any FD has invalid attributes, empty sides, or non-singleton RHS.
    """
    normalized = []
    for idx, (lhs, rhs) in enumerate(fds):
        lhs_norm = _ensure_attribute_subset(lhs, attributes, f"FD #{idx} (LHS)")
        rhs_norm = _ensure_attribute_subset(rhs, attributes, f"FD #{idx} (RHS)")
        if len(rhs_norm) != 1:
            raise AssertionError(f"FD #{idx} must have singleton RHS after minimal cover, got {rhs_norm}")
        normalized.append((lhs_norm, rhs_norm))
    return normalized


def build_output_payload(relations: List[List[str]], fds: List[Tuple[List[str], List[str]]]) -> dict:
    """
    Build the final JSON output payload from normalized relations and FDs.
    
    This function constructs the output dictionary in the required format with:
    - Named relations (R1, R2, R3, ...)
    - Inferred functional dependencies
    
    Args:
        relations (List[List[str]]): Normalized relations from the decomposition.
            Each relation is a sorted list of attribute names.
            Example: [["A", "B"], ["B", "C"], ["C", "D"]]
        fds (List[Tuple[List[str], List[str]]]): Normalized functional dependencies.
            Each FD is a tuple of (LHS, RHS) where both are sorted lists.
            Example: [(["A"], ["B"]), (["B"], ["C"])]
    
    Returns:
        dict: JSON-serializable dictionary with structure:
            {
                "relations": [
                    {"name": "R1", "attributes": ["A", "B"]},
                    {"name": "R2", "attributes": ["B", "C"]},
                    ...
                ],
                "inferredFDs": [
                    {"left": ["A"], "right": ["B"]},
                    {"left": ["B"], "right": ["C"]},
                    ...
                ]
            }
    
    Raises:
        AssertionError: If the constructed payload doesn't meet the output requirements
                        (e.g., unsorted attributes, non-singleton RHS).
    """
    payload = {
        "relations": [
            {"name": f"R{i+1}", "attributes": rel}
            for i, rel in enumerate(relations)
        ],
        "inferredFDs": [
            {"left": lhs, "right": rhs}
            for lhs, rhs in fds
        ],
    }
    # Assertions to guarantee the schema is correct.
    assert isinstance(payload["relations"], list), "relations must be a list"
    for rel in payload["relations"]:
        assert isinstance(rel, dict), "Each relation must be a dict"
        assert "attributes" in rel, "Missing 'attributes' key in relation"
        assert rel["attributes"] == sorted(rel["attributes"]), "Attributes must be sorted"
    assert isinstance(payload["inferredFDs"], list), "inferredFDs must be a list"
    for fd in payload["inferredFDs"]:
        assert set(fd.keys()) == {"left", "right"}, "Each FD must have 'left' and 'right'"
        assert fd["left"] == sorted(fd["left"]), "FD LHS must be sorted"
        assert fd["right"] == sorted(fd["right"]), "FD RHS must be sorted"
        assert len(fd["right"]) == 1, "FD RHS must be singleton"
    return payload


# ---------------------------------------------------------------------------
# Main entrypoint
# ---------------------------------------------------------------------------

def main() -> None:
    """
    Main entry point for the decomposition tool.
    
    This function orchestrates the entire decomposition process:
    1. Parse command-line arguments
    2. Load and validate input JSON file
    3. Parse or infer functional dependencies
    4. Compute minimal cover of FDs
    5. Perform 3NF synthesis or BCNF decomposition
    6. Validate and normalize the output
    7. Write results to stdout or output file
    
    The function handles both cases:
    - Explicit FDs provided in the input JSON
    - FDs inferred from sample data when not provided
    
    Raises:
        FileNotFoundError: If the input file doesn't exist
        ValueError: If input is missing required fields (attributes, FDs/sample data)
        NotImplementedError: If student hasn't implemented required functions
        AssertionError: If output validation fails
    """
    args = parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    with input_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    relation_name = data.get("relationName", "R")
    attributes = data.get("attributes", [])
    fd_json = data.get("functionalDependencies") or []
    sample_rows = data.get("sample_data") or []

    if not attributes:
        raise ValueError("Input must include a non-empty list of attributes.")

    fds = parse_fd_json(fd_json)
    if not fds:
        if not sample_rows:
            raise ValueError("Either functionalDependencies or sample_data must be provided.")
        print("# No FDs supplied. You must implement infer_fds_from_sample().", file=sys.stderr)
        fds = infer_fds_from_sample(attributes, sample_rows)

    print("# Computing a minimal cover...", file=sys.stderr)
    minimal = minimal_cover(fds)

    print(f"# Decomposing relation {relation_name} to {args.to.upper()}...", file=sys.stderr)
    if args.to == "3nf":
        raw_relations = synthesize_3nf(attributes, minimal)
    else:
        raw_relations = decompose_bcnf(attributes, minimal)

    normalized_relations = normalize_relations(raw_relations, attributes)
    normalized_fds = normalize_fds_for_output(minimal, attributes)
    payload = build_output_payload(normalized_relations, normalized_fds)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as out_file:
            json.dump(payload, out_file, ensure_ascii=False, indent=2 if args.pretty else None)
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2 if args.pretty else None))


if __name__ == "__main__":
    main()
