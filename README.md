# CSE 132A Homework 3 — 3NF and BCNF

Version: 2.0.0

## Overview

In this homework, you will be given the functional dependencies, and compute the 3NF and BCNF decompositions.



## Submission

Only submit the `decompose.py` in gradescope. The `decompose.py` has the following functions:

- `solve_3nf(relation_name, attributes, functional_dependencies)` → returns a list of relations (each a list of attributes)
- `solve_bcnf(relation_name, attributes, functional_dependencies)` → returns a list of relations (each a list of attributes)

Inputs to both functions:
- relation_name: like `"R"`
- attributes: a list like `["A","B","C"]`
- functional_dependencies: a list of dicts like:
  - `{"left": ["A", "B"], "right": ["C"]}` (right side has exactly one attribute)

Each relation is just a list of attributes. No need to name relations (`R1`, `R2`, ...). The program will print:
```json
{ "3nf": [...], "bcnf": [...] }
```

## How to test

Each test is a single JSON file under `tests/`.

Example:
```bash
python3 decompose.py tests/test_00_chain_abc.json
```

## Input format

Each test JSON looks like this:
```json
{
  "relationName": "R",
  "attributes": ["A", "B", "C"],
  "functionalDependencies": [
    { "left": ["A"], "right": ["B"] },
    { "left": ["B"], "right": ["C"] }
  ]
}
```

## Output format

Print a JSON object with two keys, `"3nf"` and `"bcnf"`, where each value is a list of relations (each relation is a list of attribute names).

Example output:
```json
{
  "3nf":  [["A","B"], ["B","C"]],
  "bcnf": [["A","B"], ["B","C"]]
}
```
