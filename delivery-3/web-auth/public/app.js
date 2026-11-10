// Client-side validation and form submission (fetch + JSON) to the Express server.
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
const NAME_RE = /^[\p{L}][\p{L}' -]{0,49}$/u;

const rules = {
  name: (v) => NAME_RE.test(v.trim()) || "Enter your name (letters only, max 50).",
  surname: (v) => NAME_RE.test(v.trim()) || "Enter your surname (letters only, max 50).",
  email: (v) => EMAIL_RE.test(v.trim()) || "Enter a valid email address.",
  password: (v, form) => form.id === "signup-form"
    ? (v.length >= 8 && v.length <= 128) || "Password must be 8 to 128 characters."
    : v.length > 0 || "Enter your password.",
};

const message = document.getElementById("message");

function showMessage(text, ok) {
  message.textContent = text;
  message.className = ok ? "ok" : "error";
}

function showFieldErrors(form, errors) {
  form.querySelectorAll("input").forEach((input) => {
    const error = errors[input.name] || "";
    input.classList.toggle("invalid", Boolean(error));
    form.querySelector(`.field-error[data-for="${input.name}"]`).textContent = error;
  });
}

function validate(form) {
  const errors = {};
  form.querySelectorAll("input").forEach((input) => {
    const result = rules[input.name](input.value, form);
    if (result !== true) errors[input.name] = result;
  });
  return errors;
}

async function submit(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const errors = validate(form);
  showFieldErrors(form, errors);
  if (Object.keys(errors).length) {
    showMessage("Please fix the highlighted fields.", false);
    return;
  }
  const body = Object.fromEntries(new FormData(form));
  try {
    const res = await fetch(form.action, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const data = await res.json();
    showFieldErrors(form, data.errors || {});
    showMessage(data.message, data.ok);
    if (data.ok) form.reset();
  } catch {
    showMessage("Cannot reach the server. Is it running?", false);
  }
}

document.getElementById("signup-form").addEventListener("submit", submit);
document.getElementById("login-form").addEventListener("submit", submit);
