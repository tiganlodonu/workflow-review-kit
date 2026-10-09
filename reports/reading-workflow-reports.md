# How to read a Workflow Review Kit report

This experimental trial produces automated text-based review hints for public GitHub Actions workflows. A report is a starting point for inspection, not a security audit, proof of exploitability, or approval to merge changes.

## Request scope and privacy

Use the project's [review request form](https://github.com/tiganlodonu/workflow-review-kit/issues/new?template=review.yml) and provide a public repository URL. The documented trial scope is one to three files under `.github/workflows`, up to 50 KB each. The current form asks for a repository URL, not a workflow-path selector; do not assume it selects particular files or covers every workflow in a larger repository. Check the delivered report's actual coverage.

Requests and reports are public. Do not submit credentials, private code, personal information, logs containing secrets, or confidential settings. The trial reads public source; it does not execute submitted repository code or workflows. Delivery is experimental and has no guaranteed turnaround.

Worker reports use `reports/request-N.md`, with N matching the request issue. This guide does not replace or modify those reports.

## Interpreting common hints

| Hint | What it means | What to inspect before changing anything |
| --- | --- | --- |
| `MUTABLE_ACTION` | An external action reference was not recognized as a full commit SHA. | Identify the authentic upstream revision, maintenance status, and runtime compatibility. Pinning a malicious or obsolete revision does not make it safe. |
| `MUTABLE_IMAGE` | A container action reference was not recognized as SHA-256 digest-pinned. | Verify the intended image and digest through a trusted source. Plan future updates. |
| `PERMISSIONS_REVIEW` | No permissions key was recognized by the text heuristic. | Inspect effective repository/organization defaults and every job. Absence of a recognized key does not prove write access. |
| `WRITE_ALL` | A broad write-all declaration was recognized. | Identify the capabilities each job needs; reduce permissions without blindly breaking publishing or deployment. |
| `TARGET_TRIGGER_REVIEW` | Text referencing pull_request_target was recognized. | Confirm it is an actual trigger. Trace untrusted checkout refs, scripts, inputs, artifacts, secrets, and token privileges. The trigger alone is not a vulnerability. |
| `EVENT_INPUT_REVIEW` | A selected event-input expression was recognized. | Determine whether untrusted text becomes executable shell code. Passing it through an environment variable can be safer, but quoting and downstream use still matter. |

## No hints does not mean secure

The checker is not a YAML parser. It can miss quoted keys, unusual formatting, multiline expressions, and data flow. YAML-like text in a script can cause false positives. A permissions declaration in one place does not establish least privilege in every job. Local actions, reusable workflows, dependency code, runner configuration, and repository settings require separate examination.

A report covering selected files is not a repository-wide assessment. Unit tests of heuristic examples, even when passing, do not establish real-world detection accuracy or workflow compatibility.

## A practical verification checklist

1. **Confirm coverage:** record the repository, files, and revision actually reviewed. A branch URL can change; preserve commit-addressed evidence where possible.
2. **Read the context:** inspect the complete job and related local/reusable actions, not just the matched line.
3. **Separate evidence from inference:** note what is observed, what remains unknown, and what would establish impact.
4. **Choose a minimal change:** verify upstream commit mappings or image digests. Do not copy an invented pin or remove permissions without understanding the job.
5. **Validate in an authorized environment:** review the diff and run appropriate tests/CI before merge. This guide does not authorize execution or resource spending.
6. **Record residual risk:** list unreviewed settings, dependencies, workflows, and compatibility questions.

Useful maintainer notes can be as simple as:

```text
Source commit and workflow path:
Reported rule and line:
Context inspected:
Confirmed observation:
Unknowns / reason this may be a false positive:
Proposed change:
Validation actually performed and result:
Remaining limitations:
```

Do not label unperformed validation as passed. A candidate patch is not a tested fix.

## Sources and boundaries

Trial scope and request behavior were checked against the project's public [README](https://github.com/tiganlodonu/workflow-review-kit/blob/main/README.md) and [issue form](https://github.com/tiganlodonu/workflow-review-kit/blob/main/.github/ISSUE_TEMPLATE/review.yml). These are mutable references; consult the current project documentation if behavior changes. No customer data, request-specific findings, financial claims, or delivery commitments are included in this guide.
