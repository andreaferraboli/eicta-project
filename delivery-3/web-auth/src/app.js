const path = require("node:path");
const express = require("express");
const { openDatabase } = require("./db");
const { validateSignup, validateLogin } = require("./validation");
const { hashPassword, verifyPassword } = require("./passwords");

function createApp({ dbFile }) {
  const db = openDatabase(dbFile);
  const app = express();

  app.use(express.json({ limit: "10kb" }));
  app.use(express.urlencoded({ extended: false, limit: "10kb" }));
  app.use(express.static(path.join(__dirname, "..", "public")));

  // Sign-in (registration)
  app.post("/api/signup", (req, res) => {
    const { data, errors } = validateSignup(req.body || {});
    if (Object.keys(errors).length) {
      return res.status(400).json({ ok: false, message: "Please fix the highlighted fields.", errors });
    }
    if (db.findUserByEmail(data.email)) {
      return res.status(409).json({ ok: false, message: "An account with this email already exists.",
                                    errors: { email: "Email already registered." } });
    }
    try {
      db.createUser({ ...data, password: hashPassword(data.password) });
    } catch (err) {
      if (String(err.message).includes("UNIQUE")) { // race between check and insert
        return res.status(409).json({ ok: false, message: "An account with this email already exists." });
      }
      throw err;
    }
    return res.status(201).json({ ok: true, message: `Welcome, ${data.name} ${data.surname}! Your account has been created.` });
  });

  // Log-in
  app.post("/api/login", (req, res) => {
    const { data, errors } = validateLogin(req.body || {});
    if (Object.keys(errors).length) {
      return res.status(400).json({ ok: false, message: "Please fix the highlighted fields.", errors });
    }
    const user = db.findUserByEmail(data.email);
    if (!user || !verifyPassword(data.password, user.password)) {
      // Same message for unknown email and wrong password: do not reveal which accounts exist.
      return res.status(401).json({ ok: false, message: "Invalid email or password." });
    }
    return res.json({ ok: true, message: `Welcome back, ${user.name} ${user.surname}!` });
  });

  // Malformed JSON and unexpected errors
  app.use((err, req, res, next) => {
    if (err.type === "entity.parse.failed") {
      return res.status(400).json({ ok: false, message: "Malformed request." });
    }
    console.error(err);
    return res.status(500).json({ ok: false, message: "Unexpected server error." });
  });

  app.locals.db = db;
  return app;
}

module.exports = { createApp };
