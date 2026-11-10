const path = require("node:path");
const { createApp } = require("./src/app");

const PORT = Number(process.env.WEB_AUTH_PORT || 3000);
const DB_FILE = process.env.WEB_AUTH_DB || path.join(__dirname, "db", "users.db");

const app = createApp({ dbFile: DB_FILE });
app.listen(PORT, "127.0.0.1", () => {
  console.log(`web-auth listening on http://127.0.0.1:${PORT} (database: ${DB_FILE})`);
});
