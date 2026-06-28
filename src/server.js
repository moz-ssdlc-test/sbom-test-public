// Intentionally vulnerable sample for Semgrep / scanner integration testing.
// DO NOT DEPLOY. Every issue below is planted to verify scanner findings flow.

const express = require("express");
const { exec } = require("child_process");
const crypto = require("crypto");
const app = express();

// A04: Cryptographic Failures — hardcoded token committed to source.
const GITHUB_PAT = "ghp_AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA";
const STRIPE_KEY = "sk_live_AAAAAAAAAAAAAAAAAAAAAAAA";

// A05: Injection — reflected XSS via unescaped template literal.
app.get("/hello", (req, res) => {
  const name = req.query.name || "world";
  res.send(`<h1>Hello, ${name}!</h1>`);
});

// A05: Injection — command injection via child_process.exec with user input.
app.get("/dns", (req, res) => {
  const host = req.query.host;
  exec("nslookup " + host, (err, stdout) => {
    if (err) return res.status(500).send(err.message);
    res.send(stdout);
  });
});

// A05: Injection — eval() of user input.
app.get("/eval", (req, res) => {
  res.send(String(eval(req.query.code || "1+1")));
});

// A04: Cryptographic Failures — MD5 for session token.
function makeSessionToken(userId) {
  return crypto.createHash("md5").update(String(userId)).digest("hex");
}

app.listen(3000, "0.0.0.0", () => console.log("listening"));
