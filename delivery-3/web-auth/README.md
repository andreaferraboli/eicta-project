# Web task 2: sign-in and log-in (Node.js + Express + SQLite)

Two forms (sign-in = registration, log-in) that submit to an Express server, which queries an SQLite database with a single `users` table.

**Requirements:** Node.js >= 22.13 (uses the built-in `node:sqlite` module, so no native package has to be compiled). Only dependency: `express` (pinned, `package-lock.json` included).

## Run

```
cd delivery-3/web-auth
npm install
npm start          # http://127.0.0.1:3000
npm test           # 10 end-to-end tests on a temporary database
```

Environment variables (optional): `WEB_AUTH_PORT` (default 3000), `WEB_AUTH_DB` (default `db/users.db`).

## SQLite Online step (required by the PDF, to do by hand)

1. Open https://sqliteonline.com/ and select SQLite.
2. Paste and run [`db/users.sql`](db/users.sql).
3. Optionally insert a test user (a plain-text password works, see below).
4. Export the database as a `.db` file and save it as `db/users.db`.
5. `npm start`: the server uses that file. `CREATE TABLE IF NOT EXISTS` leaves it intact.

If `db/users.db` does not exist, the server creates it locally from the same SQL. This is a convenience for testing, **not** the SQLite Online step.

## Logic (for the report)

| Step | Sign-in (`POST /api/signup`) | Log-in (`POST /api/login`) |
|---|---|---|
| Client validation (`public/app.js`) | name and surname letters only (max 50), valid email, password 8 to 128 chars | valid email, non-empty password |
| Server validation (`src/validation.js`) | same rules, re-checked; email trimmed and lower-cased | same |
| Query | `SELECT ... WHERE email = ?`, then `INSERT ... VALUES (?, ?, ?, ?)` (prepared statements) | `SELECT ... WHERE email = ?` |
| Failure | 400 invalid fields (per-field messages), 409 email already registered | 400 invalid fields, 401 "Invalid email or password." (same message for unknown email and wrong password) |
| Success | 201 "Welcome, Name Surname! Your account has been created." | 200 "Welcome back, Name Surname!" |

**Password storage.** The PDF allows plain-text passwords. We store a salted scrypt hash (`scrypt$salt$hash`, Node built-in crypto), which keeps the requested behaviour. Rows typed by hand in SQLite Online with a plain-text password are still accepted at log-in.

**Uniqueness.** `email` is `UNIQUE COLLATE NOCASE`; the server checks before inserting and also handles the UNIQUE error.

## Tests (`test/auth.test.js`)

valid sign-in, duplicate email (case-insensitive), hashed storage, valid log-in, wrong password, unknown email, invalid sign-in fields, missing log-in fields, SQL injection attempt treated as data, malformed JSON. The browser-side validation is not covered by automated tests: check it by hand and take screenshots.
