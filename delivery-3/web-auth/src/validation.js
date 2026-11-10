// Server-side validation. The same rules are checked in the browser (public/app.js),
// but the server never trusts the client.
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
const NAME_RE = /^[\p{L}][\p{L}' -]{0,49}$/u;
const MIN_PASSWORD = 8;
const MAX_PASSWORD = 128;

function clean(value) {
  return typeof value === "string" ? value.trim() : "";
}

function validateSignup(body) {
  const data = {
    email: clean(body.email).toLowerCase(),
    password: typeof body.password === "string" ? body.password : "",
    name: clean(body.name),
    surname: clean(body.surname),
  };
  const errors = {};
  if (!EMAIL_RE.test(data.email) || data.email.length > 254) errors.email = "Enter a valid email address.";
  if (data.password.length < MIN_PASSWORD || data.password.length > MAX_PASSWORD) {
    errors.password = `Password must be ${MIN_PASSWORD} to ${MAX_PASSWORD} characters.`;
  }
  if (!NAME_RE.test(data.name)) errors.name = "Enter your name (letters only, max 50).";
  if (!NAME_RE.test(data.surname)) errors.surname = "Enter your surname (letters only, max 50).";
  return { data, errors };
}

function validateLogin(body) {
  const data = {
    email: clean(body.email).toLowerCase(),
    password: typeof body.password === "string" ? body.password : "",
  };
  const errors = {};
  if (!EMAIL_RE.test(data.email)) errors.email = "Enter a valid email address.";
  if (!data.password) errors.password = "Enter your password.";
  return { data, errors };
}

module.exports = { validateSignup, validateLogin, MIN_PASSWORD };
