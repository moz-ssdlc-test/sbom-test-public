# Intentionally-vulnerable test fixtures

Files under this directory contain deliberate security flaws used to verify
that the SSDLC code-scanning workflows (`semgrep`, `zizmor`) surface findings
correctly. They are **not** intended to be built, deployed, or imported.

| File | Planted issues |
|---|---|
| `app.py`    | hardcoded AWS keys, SQL injection, command injection (`shell=True`), `eval()`, MD5 password hash, `debug=True` |
| `server.js` | hardcoded GitHub/Stripe tokens, reflected XSS, command injection via `exec`, `eval()`, MD5 session token |

If you remove findings here, expect downstream PR checks to start passing.
