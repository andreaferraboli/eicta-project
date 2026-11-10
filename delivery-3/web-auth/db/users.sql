-- Single user table for the sign-in / log-in web task.
-- Paste this into https://sqliteonline.com/ (SQLite engine), run it, then
-- File > Export (Save as .db) and place the file at delivery-3/web-auth/db/users.db.
-- If no users.db is present, the server creates one locally from this same file.

CREATE TABLE IF NOT EXISTS users (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    email    TEXT NOT NULL UNIQUE COLLATE NOCASE,
    password TEXT NOT NULL,  -- scrypt hash "scrypt$<salt>$<hash>" (see README: the PDF allows plain text, we hash)
    name     TEXT NOT NULL,
    surname  TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
