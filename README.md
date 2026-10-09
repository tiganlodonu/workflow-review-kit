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

## Request a free public report

[Open a review request](https://github.com/tiganlodonu/workflow-review-kit/issues/new?template=review.yml) and supply a public GitHub repository URL. The trial supports one to three workflow files under `.github/workflows`, up to 50 KB each. There is no required payment.

Reports appear at `reports/request-N.md`, where N is your issue number. The local worker checks requests about every 15 minutes and attempts at most one new report per check. It depends on the owner's computer being awake and on free public services being available. There is no guaranteed delivery time. Failed requests may be retried; this is an experimental service.

All requests and reports are public. Do not submit private code, secrets, personal information, or confidential material. Only public source is read; the repository's code and workflows are never executed. These are automated heuristic reports, not professional security audits. No customer demand or income has been established.

## Optional tips after delivery

If a report was useful, you may optionally send **native USDC on Base mainnet (chain ID 8453)** to:

`0x2aD2E6505dCD890048830E6E9203e5245dc6e842`

Supported USDC contract: `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` ([Circle's official list](https://developers.circle.com/stablecoins/usdc-contract-addresses)). Other tokens and networks are not tracked by this trial. The sender pays any applicable network fee. Tips are voluntary and do not purchase a security audit or a delivery guarantee.

After delivery, you may edit your request to include the optional transaction hash, sender public address, and exact USDC amount. These fields are public. Never include a seed phrase or private key. The tracker waits for a finalized receipt, checks the matching transfer, and counts each transaction/log only once. Unrelated wallet deposits are not attributed to this project.

## Operation and ownership

Created with assistance from an AI agent. Funds go directly to the owner's wallet. The runner has only its public receiving address; it cannot sign transactions or spend from the wallet. Automatic reinvestment is disabled. A future spending ceiling of 25% of verified tips is tracked, but no spending integration exists.

The free Base public RPC is rate-limited and is not recommended by Base for production systems. This remains a trial; errors delay delivery and payment verification, with no paid fallback. [Base network documentation](https://docs.base.org/get-started/connect-to-base).
