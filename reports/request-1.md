# Automated workflow review

Repository: https://github.com/Conway-Research/automaton

Reviewed commit: `d8f816881fd24b6f5e3d616e59edec387a447667`

Method: heuristic text scanning. Repository code and workflows were not executed. This is not a security audit or a guarantee of safety.

## Source files

- [.github/workflows/ci.yml](https://raw.githubusercontent.com/Conway-Research/automaton/d8f816881fd24b6f5e3d616e59edec387a447667/.github/workflows/ci.yml)

- [.github/workflows/release.yml](https://raw.githubusercontent.com/Conway-Research/automaton/d8f816881fd24b6f5e3d616e59edec387a447667/.github/workflows/release.yml)

## Review hints

- **PERMISSIONS_REVIEW** — `.github/workflows/ci.yml:1`: No permissions key recognized. Inspect effective repository/org defaults and declare least privilege. This does not prove write access.

- **MUTABLE_ACTION** — `.github/workflows/ci.yml:10`: External action is not recognized as pinned to a full commit SHA. Verify the intended upstream commit before pinning.

- **MUTABLE_ACTION** — `.github/workflows/ci.yml:11`: External action is not recognized as pinned to a full commit SHA. Verify the intended upstream commit before pinning.

- **MUTABLE_ACTION** — `.github/workflows/ci.yml:14`: External action is not recognized as pinned to a full commit SHA. Verify the intended upstream commit before pinning.

- **MUTABLE_ACTION** — `.github/workflows/ci.yml:40`: External action is not recognized as pinned to a full commit SHA. Verify the intended upstream commit before pinning.

- **MUTABLE_ACTION** — `.github/workflows/ci.yml:41`: External action is not recognized as pinned to a full commit SHA. Verify the intended upstream commit before pinning.

- **MUTABLE_ACTION** — `.github/workflows/ci.yml:44`: External action is not recognized as pinned to a full commit SHA. Verify the intended upstream commit before pinning.

- **PERMISSIONS_REVIEW** — `.github/workflows/release.yml:1`: No permissions key recognized. Inspect effective repository/org defaults and declare least privilege. This does not prove write access.

- **MUTABLE_ACTION** — `.github/workflows/release.yml:9`: External action is not recognized as pinned to a full commit SHA. Verify the intended upstream commit before pinning.

- **MUTABLE_ACTION** — `.github/workflows/release.yml:10`: External action is not recognized as pinned to a full commit SHA. Verify the intended upstream commit before pinning.

- **MUTABLE_ACTION** — `.github/workflows/release.yml:13`: External action is not recognized as pinned to a full commit SHA. Verify the intended upstream commit before pinning.

## Limits

Only up to three YAML workflow files are scanned. This scanner does not parse YAML, inspect repository settings, validate action code, prove exploits, apply patches, or run CI. Every hint requires contextual review. False positives and missed issues are possible.

## Optional support

This trial is free. Optional tip instructions are on the project README. You do not need to pay to receive this report.