// Password hashing with Node's built-in scrypt. The PDF allows plain-text passwords;
// hashing is a deliberate extra that does not change the requested behaviour.
const crypto = require("node:crypto");

const KEY_LENGTH = 32;

function hashPassword(password) {
  const salt = crypto.randomBytes(16).toString("hex");
  const hash = crypto.scryptSync(password, salt, KEY_LENGTH).toString("hex");
  return `scrypt$${salt}$${hash}`;
}

function verifyPassword(password, stored) {
  const [scheme, salt, hash] = String(stored).split("$");
  if (scheme !== "scrypt" || !salt || !hash) {
    // Rows typed by hand in SQLite Online may hold plain-text passwords (allowed by the PDF).
    const a = Buffer.from(String(password));
    const b = Buffer.from(String(stored));
    return a.length === b.length && crypto.timingSafeEqual(a, b);
  }
  const expected = Buffer.from(hash, "hex");
  const actual = crypto.scryptSync(password, salt, expected.length);
  return crypto.timingSafeEqual(actual, expected);
}

module.exports = { hashPassword, verifyPassword };
