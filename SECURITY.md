# Security Policy

## Responsible Disclosure

If you discover a security vulnerability, please **do not** open a public issue. Instead, report it privately by emailing `security@topherbot.dev`.

We will acknowledge receipt within 48 hours and aim to publish a fix within 14 days.

## Supported Versions

We support the latest stable release and the previous one (approximately 12 months of support).

## CI Hardening

* All GitHub Actions are **SHA‑pinned**.
* The repository‑wide default `GITHUB_TOKEN` permission is set to **read‑only**.
* Dependencies are **exactly pinned** in `requirements.txt` and scanned with `bandit` on every CI run.
* No secret values are ever committed; CI accesses secrets only via the GitHub Secrets UI.

---

*This security policy is version‑controlled and lives in the repo.*
