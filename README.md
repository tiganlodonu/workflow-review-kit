# Workflow Review Kit

A dependency-free Python tool that produces review hints for GitHub Actions workflow files. This is an experimental public demo, not a security audit or a guarantee that a workflow is safe.

## Run locally

Requires Python 3.9 or later. No package installation is needed.

```sh
python workflow_triage.py .github/workflows
python workflow_triage.py .github/workflows --json
python -m unittest -v test_workflow_triage.py
```

The tool reads local files only. It does not execute workflows, change repositories, publish fixes, or send data to a server.

Exit codes: 0 means no recognized review hints; 1 means review hints were found; 2 means an input/read error. No hints does not mean secure.

## Review hints

- External action references without a full commit SHA.
- Container actions without a recognized SHA-256 digest.
- Missing recognized permissions declarations or write-all permissions.
- References to pull_request_target.
- Direct expressions referencing selected event input fields.

These are text heuristics, not YAML parsing or exploit verification. Comments, strings, unusual formatting, permissions inheritance, multiline expressions, and dataflow can lead to false positives or missed issues. Every finding requires manual review. Pinning a revision does not prove it is trustworthy or maintained.

## Validation

Nine unit tests passed locally on Windows with Python on 2026-10-09. This covers the tested heuristic examples, not real-world security accuracy or workflow compatibility.

## Project status

Created with assistance from an AI agent. No paid service or checkout is currently available. This repository does not collect money or provide autonomous wallet access. Customer demand has not been established.
