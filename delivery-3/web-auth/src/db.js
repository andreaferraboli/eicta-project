// SQLite access through Node's built-in node:sqlite module (Node >= 22.13, no native build needed).
// All statements are prepared with placeholders: user input is never concatenated into SQL.
const fs = require("node:fs");
const path = require("node:path");
const { DatabaseSync } = require("node:sqlite");

const SCHEMA = path.join(__dirname, "..", "db", "users.sql");

function openDatabase(file) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  const db = new DatabaseSync(file);
  db.exec(fs.readFileSync(SCHEMA, "utf8")); // CREATE TABLE IF NOT EXISTS: safe on a SQLite Online export too
  const insertUser = db.prepare("INSERT INTO users (email, password, name, surname) VALUES (?, ?, ?, ?)");
  const findByEmail = db.prepare("SELECT id, email, password, name, surname FROM users WHERE email = ?");
  return {
    createUser: (u) => insertUser.run(u.email, u.password, u.name, u.surname),
    findUserByEmail: (email) => findByEmail.get(email),
    close: () => db.close(),
  };
}

module.exports = { openDatabase };
