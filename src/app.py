"""
Intentionally vulnerable sample for Semgrep / scanner integration testing.

DO NOT DEPLOY. Every issue below is planted to verify scanner findings flow.
Expected Semgrep rules (from p/owasp-top-ten + p/secrets + p/security-audit):
  - python.lang.security.audit.dangerous-subprocess-use
  - python.flask.security.injection.tainted-sql-string
  - python.lang.security.audit.md5-used-as-password
  - generic.secrets.security.detected-aws-access-key-id
  - python.lang.security.audit.exec-detected
"""
import hashlib
import subprocess
import sqlite3
from flask import Flask, request

app = Flask(__name__)

# A04: Cryptographic Failures — hardcoded secret committed to source.
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"


@app.route("/lookup")
def lookup():
    # A05: Injection — string-concatenated SQL with user input.
    user_id = request.args.get("id", "")
    conn = sqlite3.connect("app.db")
    cur = conn.cursor()
    cur.execute("SELECT name, email FROM users WHERE id = '" + user_id + "'")
    return str(cur.fetchone())


@app.route("/ping")
def ping():
    # A05: Injection — shell=True with user-controlled host.
    host = request.args.get("host", "127.0.0.1")
    out = subprocess.check_output("ping -c 1 " + host, shell=True)
    return out


@app.route("/calc")
def calc():
    # A05: Injection — eval() on user input.
    expr = request.args.get("expr", "1+1")
    return str(eval(expr))


def hash_password(pw: str) -> str:
    # A04: Cryptographic Failures — MD5 for password storage.
    return hashlib.md5(pw.encode()).hexdigest()


if __name__ == "__main__":
    # A05 / A02: Debug mode enabled in a code path that could be deployed.
    app.run(host="0.0.0.0", port=5000, debug=True)
