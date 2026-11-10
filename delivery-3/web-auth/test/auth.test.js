// End-to-end tests against a real server on a random port and a temporary SQLite file.
// Run: npm test
const { test, before, after } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { createApp } = require("../src/app");

let server, base, tmpDir;

before(async () => {
  tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "web-auth test "));  // space on purpose
  const app = createApp({ dbFile: path.join(tmpDir, "users.db") });
  await new Promise((resolve) => { server = app.listen(0, "127.0.0.1", resolve); });
  base = `http://127.0.0.1:${server.address().port}`;
  server.on("close", () => app.locals.db.close());
});

after(async () => {
  await new Promise((resolve) => server.close(resolve));
  fs.rmSync(tmpDir, { recursive: true, force: true });
});

const post = async (url, body, raw = false) => {
  const res = await fetch(base + url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: raw ? body : JSON.stringify(body),
  });
  return { status: res.status, body: await res.json() };
};

const valid = { name: "Giulia", surname: "Rossi", email: "Giulia.Rossi@example.com", password: "festival2026" };

test("valid sign-in creates the user and welcomes them", async () => {
  const r = await post("/api/signup", valid);
  assert.equal(r.status, 201);
  assert.equal(r.body.ok, true);
  assert.match(r.body.message, /Welcome, Giulia Rossi/);
});

test("duplicate email is rejected (case-insensitive)", async () => {
  const r = await post("/api/signup", { ...valid, email: "giulia.rossi@EXAMPLE.com" });
  assert.equal(r.status, 409);
  assert.equal(r.body.ok, false);
});

test("password is stored hashed, not in plain text", async () => {
  const db = new (require("node:sqlite").DatabaseSync)(path.join(tmpDir, "users.db"));
  const row = db.prepare("SELECT password FROM users WHERE email = ?").get("giulia.rossi@example.com");
  db.close();
  assert.match(row.password, /^scrypt\$/);
  assert.ok(!row.password.includes(valid.password));
});

test("log-in with correct credentials welcomes the user", async () => {
  const r = await post("/api/login", { email: valid.email, password: valid.password });
  assert.equal(r.status, 200);
  assert.match(r.body.message, /Welcome back, Giulia Rossi/);
});

test("log-in with wrong password fails with a generic message", async () => {
  const r = await post("/api/login", { email: valid.email, password: "wrong-password" });
  assert.equal(r.status, 401);
  assert.equal(r.body.message, "Invalid email or password.");
});

test("log-in with unknown email fails with the same message", async () => {
  const r = await post("/api/login", { email: "nobody@example.com", password: "whatever123" });
  assert.equal(r.status, 401);
  assert.equal(r.body.message, "Invalid email or password.");
});

test("invalid sign-in input is rejected field by field", async () => {
  const r = await post("/api/signup", { name: "", surname: "R0ssi", email: "not-an-email", password: "short" });
  assert.equal(r.status, 400);
  assert.deepEqual(Object.keys(r.body.errors).sort(), ["email", "name", "password", "surname"]);
});

test("missing log-in fields are rejected", async () => {
  const r = await post("/api/login", {});
  assert.equal(r.status, 400);
  assert.ok(r.body.errors.email && r.body.errors.password);
});

test("SQL injection attempt in email is treated as data", async () => {
  // Payload without spaces so that it passes validation and reaches the parameterized query.
  const r = await post("/api/login", { email: "x'OR'1'='1'--@x.com", password: "x'OR'1'='1" });
  assert.equal(r.status, 401);
});

test("malformed JSON returns 400", async () => {
  const r = await post("/api/login", "{not json", true);
  assert.equal(r.status, 400);
});
