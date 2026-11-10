#!/usr/bin/env python3
"""EICTA project helper: one portable entry point for every delivery.

Stdlib only (Python >= 3.10). All paths are relative to the project root and
every external command is called with an argument list, so paths containing
spaces work on Windows, Linux and macOS.

    python scripts/eicta.py --help
    python scripts/eicta.py <command> --help

Destructive commands (reset, *-restore) ask for confirmation. Pass --yes only
when you really mean it.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"
D1, D2, D3 = ROOT / "delivery-1", ROOT / "delivery-2", ROOT / "delivery-3"

SQL_DB = BUILD / "delivery-1" / "euphoric_events.db"
SQL_DUMP = BUILD / "delivery-1" / "euphoric_events_dump.sql"
SQL_SOURCE = BUILD / "delivery-1" / "data-source.txt"
SQL_RESULTS = BUILD / "delivery-1" / "query-results"
NEO4J_IMPORT = BUILD / "delivery-2" / "neo4j-import"
NEO4J_DUMP = BUILD / "delivery-2" / "neo4j-dump"
NEO4J_RESULTS = BUILD / "delivery-2" / "query-results"
MONGO_SEED = BUILD / "delivery-3" / "mongo-seed"
MONGO_DUMP = BUILD / "delivery-3" / "mongo-dump"
MONGO_RESULTS = BUILD / "delivery-3" / "query-results"

TABLE_ORDER = ["Festival", "Stage", "Artist", "Musician", "Band", "BandMember", "Performance",
               "PerformanceArtist", "Stand", "Product", "Sells", "Person", "Purchase", "Ticket", "PurchaseItem"]
MIN_TUPLES = 25          # delivery 1, task 4
MIN_NODES_PER_TYPE = 10  # delivery 2
MIN_DOCUMENTS = 10       # delivery 3
MIN_ARRAY_ELEMENTS = 2   # delivery 3

MONGO_DB, MONGO_COLLECTION = "euphoric_events", "festivals"


class Fail(Exception):
    pass


def log(msg: str) -> None:
    print(msg, flush=True)


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT))
    except ValueError:
        return str(p)


def confirm(question: str, assume_yes: bool) -> None:
    if assume_yes:
        return
    answer = input(f"{question} Type 'yes' to continue: ").strip().lower()
    if answer != "yes":
        raise Fail("aborted by user")


DEFAULTS = {  # local-only placeholders, same defaults as docker-compose.yml
    "NEO4J_PASSWORD": "eicta-local-dev",
    "MONGO_ROOT_USERNAME": "eicta",
    "MONGO_ROOT_PASSWORD": "eicta-local-dev",
}


def load_env() -> dict[str, str]:
    """Defaults, overridden by an optional .env (same file docker compose reads), then by the environment."""
    values = dict(DEFAULTS)
    env_file = ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                values[key.strip()] = value.strip()
    values.update({k: os.environ[k] for k in DEFAULTS if k in os.environ})
    return values


def run(cmd: list[str], *, check: bool = True, capture: bool = False, input_text: str | None = None) -> subprocess.CompletedProcess:
    proc = subprocess.run(cmd, cwd=ROOT, text=True, encoding="utf-8", errors="replace",
                          capture_output=capture, input=input_text)
    if check and proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or "").strip() if capture else ""
        raise Fail(f"command failed ({proc.returncode}): {' '.join(cmd)}\n{detail}")
    return proc


def compose(*args: str, capture: bool = False, check: bool = True, input_text: str | None = None) -> subprocess.CompletedProcess:
    if not shutil.which("docker"):
        raise Fail("docker not found in PATH")
    return run(["docker", "compose", "--project-directory", str(ROOT), "-f", str(ROOT / "docker-compose.yml"), *args],
               capture=capture, check=check, input_text=input_text)


# --------------------------------------------------------------------------- setup

def cmd_setup(args) -> None:
    log(".env found (overrides defaults)" if (ROOT / ".env").exists()
        else "no .env: using local-only defaults (see README, Configuration)")
    for d in (SQL_RESULTS, NEO4J_IMPORT, NEO4J_DUMP, NEO4J_RESULTS, MONGO_SEED, MONGO_DUMP, MONGO_RESULTS):
        d.mkdir(parents=True, exist_ok=True)
    log("build/ directories ready")
    for tool in ("docker", "node", "npm", "sqlite3", "latexmk", "pdflatex"):
        log(f"  {tool:9} {'found' if shutil.which(tool) else 'NOT FOUND'}")


# --------------------------------------------------------------------------- delivery 1: SQL

def seed_files(source: str) -> list[Path]:
    if source == "demo":
        seed = D1 / "data" / "demo" / "seed_demo.sql"
        if not seed.exists():
            run([sys.executable, str(D1 / "data" / "generate_demo_data.py"), str(seed)])
        return [seed]
    folder = D1 / "data" / "mockaroo"
    files = []
    for table in TABLE_ORDER:
        f = folder / f"{table}.sql"
        if not f.exists():
            raise Fail(f"missing Mockaroo export {rel(f)} (see delivery-1/mockaroo/README.md)")
        files.append(f)
    return files


def connect(db: Path = SQL_DB) -> sqlite3.Connection:
    if not db.exists():
        raise Fail(f"{rel(db)} not found: run 'python scripts/eicta.py sql-build' first")
    con = sqlite3.connect(db)
    con.execute("PRAGMA foreign_keys = ON")
    return con


def cmd_sql_build(args) -> None:
    SQL_DB.parent.mkdir(parents=True, exist_ok=True)
    if SQL_DB.exists():
        SQL_DB.unlink()  # build artefact, regenerated from versioned sources
    con = sqlite3.connect(SQL_DB)
    con.execute("PRAGMA foreign_keys = ON")
    con.executescript((D1 / "sql" / "schema.sql").read_text(encoding="utf-8"))
    for f in seed_files(args.source):
        con.executescript(f.read_text(encoding="utf-8"))
    con.commit()
    con.close()
    SQL_SOURCE.write_text(args.source + "\n", encoding="utf-8")  # read by "package" to flag demo data
    log(f"built {rel(SQL_DB)} from schema.sql + {args.source} data")
    if args.source == "demo":
        log("NOTE: demo data is a local fallback, not Mockaroo evidence")


def cmd_sql_check(args) -> None:
    con = connect()
    problems = []
    fk = con.execute("PRAGMA foreign_key_check").fetchall()
    log(f"  foreign_key_check: {len(fk)} violations")
    if fk:
        problems.append("foreign keys")
    for table in TABLE_ORDER:
        n = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        ok = n >= MIN_TUPLES
        log(f"  {table:18} {n:5} tuples  {'OK' if ok else f'< {MIN_TUPLES}'}")
        if not ok:
            problems.append(f"{table} has {n} tuples")
    for stmt in split_sql((D1 / "sql" / "checks.sql").read_text(encoding="utf-8")):
        name, violations = con.execute(stmt).fetchone()
        log(f"  {name:32} {violations} violations")
        if violations:
            problems.append(name)
    con.close()
    if problems:
        raise Fail("SQL checks failed: " + ", ".join(problems))
    log("SQL checks passed")


def split_sql(text: str) -> list[str]:
    lines = [l for l in text.splitlines() if not l.strip().startswith("--")]
    return [s.strip() for s in "\n".join(lines).split(";") if s.strip()]


def format_table(cols: list[str], rows: list[tuple]) -> str:
    cells = [[str(c) for c in cols]] + [["NULL" if v is None else str(v) for v in r] for r in rows]
    widths = [max(len(row[i]) for row in cells) for i in range(len(cols))]
    out = [" | ".join(c.ljust(w) for c, w in zip(cells[0], widths)),
           "-+-".join("-" * w for w in widths)]
    out += [" | ".join(c.ljust(w) for c, w in zip(r, widths)) for r in cells[1:]]
    return "\n".join(out)


def cmd_sql_queries(args) -> None:
    con = connect()
    SQL_RESULTS.mkdir(parents=True, exist_ok=True)
    empty = []
    for qf in sorted((D1 / "sql" / "queries").glob("q*.sql")):
        sql = qf.read_text(encoding="utf-8")
        cur = con.execute("\n".join(l for l in sql.splitlines() if not l.startswith("--")))
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description]
        header = ("-- LOCAL TEXT OUTPUT generated by scripts/eicta.py sql-queries.\n"
                  "-- Not a screenshot: the report needs a screenshot from the actual tool.\n"
                  f"-- Query: {rel(qf)}\n-- Rows: {len(rows)}\n\n")
        (SQL_RESULTS / f"{qf.stem}.txt").write_text(header + format_table(cols, rows) + "\n", encoding="utf-8")
        log(f"  {qf.stem:34} {len(rows):4} rows")
        if not rows:
            empty.append(qf.stem)
    con.close()
    log(f"results in {rel(SQL_RESULTS)}")
    if empty:
        raise Fail("queries with no output tuple (PDF asks for at least one): " + ", ".join(empty))


def cmd_sql_dump(args) -> None:
    con = connect()
    SQL_DUMP.write_text("\n".join(con.iterdump()) + "\n", encoding="utf-8")
    con.close()
    # Prove that the dump is self-contained: restore it into a fresh in-memory DB and compare counts.
    restored = sqlite3.connect(":memory:")
    restored.executescript(SQL_DUMP.read_text(encoding="utf-8"))
    src = connect()
    for table in TABLE_ORDER:
        a = src.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        b = restored.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        if a != b:
            raise Fail(f"dump mismatch on {table}: {a} vs {b}")
    log(f"wrote {rel(SQL_DUMP)} (schema + data, restore verified in memory)")
    log(f"the .db file itself is also self-contained: {rel(SQL_DB)}")


# --------------------------------------------------------------------------- delivery 2: Neo4j

def cmd_export_csv(args) -> None:
    """Export the SQL tables as CSV for LOAD CSV (one file per table, plus a merged artist file)."""
    con = connect()
    NEO4J_IMPORT.mkdir(parents=True, exist_ok=True)
    queries = {t: f"SELECT * FROM {t}" for t in TABLE_ORDER}
    queries["ArtistFull"] = ("SELECT a.StageName, a.Country, a.MainGenre, a.ArtistType, m.FullName, m.Nationality, "
                             "m.MainInstrument, b.FormationYear FROM Artist a "
                             "LEFT JOIN Musician m ON m.StageName = a.StageName "
                             "LEFT JOIN Band b ON b.StageName = a.StageName")
    for name, q in queries.items():
        cur = con.execute(q)
        with open(NEO4J_IMPORT / f"{name.lower()}.csv", "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow([d[0] for d in cur.description])
            w.writerows(cur.fetchall())
    con.close()
    log(f"exported {len(queries)} CSV files to {rel(NEO4J_IMPORT)}")


def cypher(env: dict, file_in_container: str | None = None, query: str | None = None, capture: bool = True) -> str:
    cmd = ["exec", "-T", "neo4j", "cypher-shell", "-u", "neo4j", "-p", env["NEO4J_PASSWORD"], "--format", "plain"]
    if file_in_container:
        cmd += ["-f", file_in_container]
    proc = compose(*cmd, capture=capture, input_text=query)
    return proc.stdout if capture else ""


def cmd_neo4j_load(args) -> None:
    env = load_env()
    if not (NEO4J_IMPORT / "festival.csv").exists():
        cmd_export_csv(args)
    log("clearing graph and loading CSV")
    cypher(env, "/cypher/99_cleanup.cypher")
    cypher(env, "/cypher/00_constraints.cypher")
    cypher(env, "/cypher/01_import.cypher")
    log("graph loaded")


def cmd_neo4j_check(args) -> None:
    env = load_env()
    out = cypher(env, "/cypher/checks.cypher")
    problems = []
    for line in out.splitlines():
        parts = [p.strip().strip('"') for p in line.split(",")]
        if len(parts) == 3 and parts[2].lstrip("-").isdigit():
            kind, name, value = parts[0], parts[1], int(parts[2])
            ok = value >= MIN_NODES_PER_TYPE if kind == "count" else value == 0
            log(f"  {kind:10} {name:34} {value:5}  {'OK' if ok else 'FAIL'}")
            if not ok:
                problems.append(name)
    # Coherence with delivery 1: node counts equal SQL table counts.
    con = connect()
    sql_counts = {"Festival": "Festival", "Stage": "Stage", "Performance": "Performance", "Artist": "Artist",
                  "Musician": "Musician", "Band": "Band", "Stand": "Stand", "Product": "Product",
                  "Person": "Person", "Purchase": "Purchase", "Ticket": "Ticket"}
    for label, table in sql_counts.items():
        n_sql = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        n_graph = int(cypher(env, query=f"MATCH (n:{label}) RETURN count(n);").splitlines()[-1])
        ok = n_sql == n_graph
        log(f"  coherence  {label:34} sql={n_sql} graph={n_graph}  {'OK' if ok else 'FAIL'}")
        if not ok:
            problems.append(f"coherence {label}")
    con.close()
    if problems:
        raise Fail("Neo4j checks failed: " + ", ".join(problems))
    log("Neo4j checks passed")


def cmd_neo4j_queries(args) -> None:
    env = load_env()
    NEO4J_RESULTS.mkdir(parents=True, exist_ok=True)
    qdir = D2 / "neo4j" / "cypher" / "queries"
    for kind in ("read", "write"):  # reads first, on the pristine seed
        for qf in sorted((qdir / kind).glob("*.cypher")):
            out = cypher(env, f"/cypher/queries/{kind}/{qf.name}")
            rows = max(len(out.strip().splitlines()) - 1, 0)
            (NEO4J_RESULTS / f"{qf.stem}.txt").write_text(
                "-- LOCAL TEXT OUTPUT from cypher-shell, not a Neo4j Browser screenshot.\n"
                f"-- Query: {rel(qf)}\n\n" + out, encoding="utf-8")
            log(f"  {kind:5} {qf.stem:40} {rows:4} rows")
    log("write queries modified the graph: run 'neo4j-load' to restore the seed")


def neo4j_volume_cmd(env: dict, *admin_args: str) -> None:
    compose("stop", "neo4j")
    try:
        compose("run", "--rm", "--no-deps", "neo4j", "neo4j-admin", "database", *admin_args)
    finally:
        compose("up", "-d", "--wait", "neo4j")


def cmd_neo4j_dump(args) -> None:
    env = load_env()
    NEO4J_DUMP.mkdir(parents=True, exist_ok=True)
    neo4j_volume_cmd(env, "dump", "neo4j", "--to-path=/backups", "--overwrite-destination=true")
    log(f"dump written to {rel(NEO4J_DUMP / 'neo4j.dump')}")


def cmd_neo4j_restore(args) -> None:
    env = load_env()
    if not (NEO4J_DUMP / "neo4j.dump").exists():
        raise Fail(f"no dump at {rel(NEO4J_DUMP / 'neo4j.dump')}")
    confirm("This OVERWRITES the current Neo4j database with the dump.", args.yes)
    neo4j_volume_cmd(env, "load", "neo4j", "--from-path=/backups", "--overwrite-destination=true")
    log("Neo4j database restored from dump")


# --------------------------------------------------------------------------- delivery 3: MongoDB

def ext_date(value: str) -> dict:
    """Extended JSON date understood by mongoimport."""
    text = value if "T" in value or " " in value else value + " 00:00"
    return {"$date": dt.datetime.fromisoformat(text.replace(" ", "T")).strftime("%Y-%m-%dT%H:%M:%SZ")}


def cmd_mongo_transform(args) -> None:
    """Reshape the delivery-1 SQL data into one collection of festival documents."""
    con = connect()
    con.row_factory = sqlite3.Row
    artists = {}
    for r in con.execute("SELECT a.*, m.FullName, m.Nationality, m.MainInstrument, b.FormationYear FROM Artist a "
                         "LEFT JOIN Musician m ON m.StageName = a.StageName LEFT JOIN Band b ON b.StageName = a.StageName"):
        doc = {"stageName": r["StageName"], "country": r["Country"], "mainGenre": r["MainGenre"], "type": r["ArtistType"]}
        if r["ArtistType"] == "musician":
            doc.update(fullName=r["FullName"], nationality=r["Nationality"], mainInstrument=r["MainInstrument"])
        else:
            doc["formationYear"] = r["FormationYear"]
        artists[r["StageName"]] = doc
    docs = []
    for f in con.execute("SELECT * FROM Festival ORDER BY StartDate"):
        stages = []
        for s in con.execute("SELECT * FROM Stage WHERE FestivalName = ? ORDER BY Code", (f["Name"],)):
            perfs = []
            for p in con.execute("SELECT * FROM Performance WHERE StageCode = ? ORDER BY StartTime", (s["Code"],)):
                names = [r[0] for r in con.execute(
                    "SELECT ArtistStageName FROM PerformanceArtist WHERE PerformanceID = ? ORDER BY 1", (p["PerformanceID"],))]
                perfs.append({"performanceId": p["PerformanceID"], "title": p["Title"], "genre": p["Genre"],
                              "startTime": ext_date(p["StartTime"]), "endTime": ext_date(p["EndTime"]),
                              "artists": [artists[n] for n in names]})
            stages.append({"code": s["Code"], "name": s["Name"], "maxCapacity": s["MaxCapacity"],
                           "locationDescription": s["LocationDescription"], "performances": perfs})
        stands = []
        for st in con.execute("SELECT * FROM Stand WHERE FestivalName = ? ORDER BY Name", (f["Name"],)):
            products = []
            for pr in con.execute("SELECT p.* FROM Product p JOIN Sells s ON s.ProductName = p.Name "
                                  "WHERE s.StandName = ? ORDER BY p.Name", (st["Name"],)):
                prod = {"name": pr["Name"], "price": float(pr["Price"]), "category": pr["Category"]}
                if pr["ExpirationDate"]:
                    prod["expirationDate"] = ext_date(pr["ExpirationDate"])
                if pr["FoodType"]:
                    prod["foodType"] = pr["FoodType"]
                products.append(prod)
            stands.append({"name": st["Name"], "sponsor": st["Sponsor"], "products": products})
        docs.append({"_id": f["Name"], "name": f["Name"], "location": f["Location"],
                     "startDate": ext_date(f["StartDate"]), "endDate": ext_date(f["EndDate"]),
                     "stages": stages, "stands": stands})
    con.close()
    short = [path for d in docs for path in short_arrays(d, d["_id"])]
    if short:
        raise Fail("arrays with fewer than 2 elements (not allowed in delivery 3): " + "; ".join(short[:5]))
    MONGO_SEED.mkdir(parents=True, exist_ok=True)
    out = MONGO_SEED / f"{MONGO_COLLECTION}.json"
    out.write_text(json.dumps(docs, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    log(f"wrote {len(docs)} documents to {rel(out)}")


def short_arrays(node, path: str) -> list[str]:
    found = []
    if isinstance(node, dict):
        for k, v in node.items():
            found += short_arrays(v, f"{path}.{k}")
    elif isinstance(node, list):
        if len(node) < MIN_ARRAY_ELEMENTS:
            found.append(f"{path} has {len(node)} element(s)")
        for i, v in enumerate(node):
            found += short_arrays(v, f"{path}[{i}]")
    return found


def mongosh(env: dict, script: str | None = None, eval_js: str | None = None) -> str:
    cmd = ["exec", "-T", "mongo", "mongosh", "--quiet", "-u", env["MONGO_ROOT_USERNAME"], "-p", env["MONGO_ROOT_PASSWORD"],
           "--authenticationDatabase", "admin", MONGO_DB]
    if eval_js:
        cmd += ["--eval", eval_js]
    if script:
        cmd.append(script)
    return compose(*cmd, capture=True).stdout


def cmd_mongo_seed(args) -> None:
    env = load_env()
    if not (MONGO_SEED / f"{MONGO_COLLECTION}.json").exists():
        cmd_mongo_transform(args)
    compose("exec", "-T", "mongo", "mongoimport", "--quiet", "-u", env["MONGO_ROOT_USERNAME"], "-p", env["MONGO_ROOT_PASSWORD"],
            "--authenticationDatabase", "admin", "--db", MONGO_DB, "--collection", MONGO_COLLECTION,
            "--drop", "--jsonArray", "--file", f"/seed/{MONGO_COLLECTION}.json")
    log(f"seeded {MONGO_DB}.{MONGO_COLLECTION} (collection dropped and reloaded)")


def cmd_mongo_check(args) -> None:
    env = load_env()
    out = mongosh(env, "/scripts/checks.js")
    log(out.rstrip())
    if "CHECKS FAILED" in out or "CHECKS PASSED" not in out:
        raise Fail("MongoDB checks failed")


def cmd_mongo_queries(args) -> None:
    env = load_env()
    MONGO_RESULTS.mkdir(parents=True, exist_ok=True)
    qdir = D3 / "mongodb" / "queries"
    for kind in ("read", "write"):
        for qf in sorted((qdir / kind).glob("*.js")):
            out = mongosh(env, f"/scripts/queries/{kind}/{qf.name}")
            (MONGO_RESULTS / f"{qf.stem}.txt").write_text(
                "-- LOCAL TEXT OUTPUT from mongosh, not a Compass/Atlas screenshot.\n"
                f"-- Query: {rel(qf)}\n\n" + out, encoding="utf-8")
            log(f"  {kind:5} {qf.stem:40} {len(out.splitlines()):4} output lines")
    log(mongosh(env, "/scripts/elemmatch-demo.js").rstrip())
    log("write queries modified the collection: run 'mongo-seed' to restore the seed")


def cmd_mongo_dump(args) -> None:
    env = load_env()
    MONGO_DUMP.mkdir(parents=True, exist_ok=True)
    compose("exec", "-T", "mongo", "mongodump", "--quiet", "-u", env["MONGO_ROOT_USERNAME"], "-p", env["MONGO_ROOT_PASSWORD"],
            "--authenticationDatabase", "admin", "--db", MONGO_DB, "--out", "/dump")
    log(f"dump written to {rel(MONGO_DUMP / MONGO_DB)}")


def cmd_mongo_restore(args) -> None:
    env = load_env()
    if not (MONGO_DUMP / MONGO_DB).exists():
        raise Fail(f"no dump at {rel(MONGO_DUMP / MONGO_DB)}")
    confirm(f"This DROPS {MONGO_DB} collections and restores them from the dump.", args.yes)
    compose("exec", "-T", "mongo", "mongorestore", "--quiet", "-u", env["MONGO_ROOT_USERNAME"], "-p", env["MONGO_ROOT_PASSWORD"],
            "--authenticationDatabase", "admin", "--drop", "--nsInclude", f"{MONGO_DB}.*", "/dump")
    log("MongoDB restored from dump")


# --------------------------------------------------------------------------- services

def cmd_up(args) -> None:
    for d in (NEO4J_IMPORT, NEO4J_DUMP, MONGO_SEED, MONGO_DUMP):
        d.mkdir(parents=True, exist_ok=True)
    load_env()
    compose("up", "-d", "--wait")
    compose("ps")


def cmd_down(args) -> None:
    compose("down")  # keeps volumes


def cmd_status(args) -> None:
    compose("ps")


def cmd_reset(args) -> None:
    confirm("This DELETES the Neo4j and MongoDB Docker volumes (all graph and document data).", args.yes)
    compose("down", "--volumes")
    log("containers and volumes removed; run 'up' and the load/seed commands to start again")


# --------------------------------------------------------------------------- reports and packaging

def cmd_report(args) -> None:
    if not shutil.which("latexmk"):
        raise Fail("latexmk not found: compile the report on Overleaf (see report/README.md)")
    for n in args.delivery:
        rdir = ROOT / f"delivery-{n}" / "report"
        outdir = BUILD / f"delivery-{n}" / "report"
        outdir.mkdir(parents=True, exist_ok=True)
        proc = subprocess.run(["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error",
                               f"-outdir={outdir}", "main.tex"], cwd=rdir, capture_output=True, text=True,
                              encoding="utf-8", errors="replace")
        if proc.returncode != 0:
            raise Fail(f"latexmk failed for delivery {n}, see {rel(outdir / 'main.log')}\n{proc.stdout[-1500:]}")
        log(f"compiled {rel(outdir / 'main.pdf')}")


PACKAGES = {
    "1": [("dump", SQL_DB), ("dump", SQL_DUMP), ("report", BUILD / "delivery-1" / "report" / "main.pdf"),
          ("images", D1 / "report" / "figures")],
    "2": [("dump", NEO4J_DUMP / "neo4j.dump"), ("report", BUILD / "delivery-2" / "report" / "main.pdf"),
          ("images", D2 / "report" / "figures")],
    "3": [("dump", MONGO_DUMP / MONGO_DB), ("web-static", D3 / "web-static"), ("web-auth", D3 / "web-auth"),
          ("report", BUILD / "delivery-3" / "report" / "main.pdf"), ("images", D3 / "report" / "figures")],
}
SKIP_IN_ZIP = {"node_modules", ".env", "__pycache__", ".gitkeep"}


def cmd_package(args) -> None:
    n = args.delivery
    out = BUILD / f"delivery-{n}" / f"delivery-{n}.zip"
    out.parent.mkdir(parents=True, exist_ok=True)
    missing = []
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for folder, src in PACKAGES[n]:
            if not src.exists():
                missing.append(rel(src))
                continue
            files = [src] if src.is_file() else [p for p in src.rglob("*") if p.is_file()]
            for f in files:
                if any(part in SKIP_IN_ZIP for part in f.parts) or f.suffix == ".db" and "web-auth" in f.parts:
                    continue
                arc = Path(folder) / (f.name if src.is_file() else f.relative_to(src))
                zf.write(f, arc.as_posix())
    log(f"wrote {rel(out)}")
    # Content checks: an existing file is not enough.
    figures = ROOT / f"delivery-{n}" / "report" / "figures"
    images = [p for p in figures.glob("*") if p.is_file() and p.name not in SKIP_IN_ZIP]
    if not images:
        missing.append(f"{rel(figures)} contains no image")
    todos = sum(p.read_text(encoding="utf-8").count("\\todo{")
                for p in (ROOT / f"delivery-{n}" / "report").rglob("*.tex"))
    if todos:
        missing.append(f"report still has {todos} TODO placeholders")
    source = SQL_SOURCE.read_text(encoding="utf-8").strip() if SQL_SOURCE.exists() else "unknown"
    if source != "mockaroo":
        missing.append(f"data built from '{source}' data, not Mockaroo (rebuild: sql-build --source mockaroo)")
    if missing:
        log("NOT READY TO SUBMIT:")
        for m in missing:
            log(f"  - {m}")
    else:
        log("no missing item detected (still review CHECKLIST.md by hand)")
    log("Check the evidence checklist before submitting: delivery-%s/CHECKLIST.md" % n)
    if missing:
        raise Fail(f"{rel(out)} written but NOT ready to submit")


# --------------------------------------------------------------------------- CLI

def main() -> int:
    parser = argparse.ArgumentParser(prog="eicta", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    def add(name, func, help_text, yes=False):
        p = sub.add_parser(name, help=help_text)
        p.set_defaults(func=func)
        if yes:
            p.add_argument("--yes", action="store_true", help="skip the confirmation prompt")
        return p

    add("setup", cmd_setup, "create the build/ folders and report which tools are installed")
    p = add("sql-build", cmd_sql_build, "build build/delivery-1/euphoric_events.db from schema + data")
    p.add_argument("--source", choices=["demo", "mockaroo"], default="demo",
                   help="demo = deterministic fallback; mockaroo = delivery-1/data/mockaroo/<Table>.sql exports")
    add("sql-check", cmd_sql_check, "check FKs, >= 25 tuples per table and the constraints in checks.sql")
    add("sql-queries", cmd_sql_queries, "run the 10 queries and save text outputs")
    add("sql-dump", cmd_sql_dump, "write a self-contained .sql dump and verify it restores")
    add("export-csv", cmd_export_csv, "export SQL tables to CSV for Neo4j")
    add("up", cmd_up, "start Neo4j and MongoDB (docker compose up -d --wait)")
    add("down", cmd_down, "stop the containers (volumes are kept)")
    add("status", cmd_status, "show container status")
    add("reset", cmd_reset, "DELETE containers and volumes", yes=True)
    add("neo4j-load", cmd_neo4j_load, "clear the graph, create constraints and import the CSV")
    add("neo4j-check", cmd_neo4j_check, "check node minimums, ISA labels and coherence with SQL")
    add("neo4j-queries", cmd_neo4j_queries, "run read then write Cypher queries, save outputs")
    add("neo4j-dump", cmd_neo4j_dump, "neo4j-admin database dump (stops Neo4j briefly)")
    add("neo4j-restore", cmd_neo4j_restore, "neo4j-admin database load from the dump", yes=True)
    add("mongo-transform", cmd_mongo_transform, "reshape SQL data into festival documents (JSON)")
    add("mongo-seed", cmd_mongo_seed, "drop and reload the collection from the JSON seed")
    add("mongo-check", cmd_mongo_check, "check document/array minimums and no empty arrays")
    add("mongo-queries", cmd_mongo_queries, "run read then write queries and the $elemMatch demo")
    add("mongo-dump", cmd_mongo_dump, "mongodump of the project database")
    add("mongo-restore", cmd_mongo_restore, "mongorestore --drop from the dump", yes=True)
    p = add("report", cmd_report, "compile LaTeX reports with latexmk")
    p.add_argument("delivery", nargs="*", default=["1", "2", "3"], choices=["1", "2", "3"])
    p = add("package", cmd_package, "build the submission ZIP and list what is missing")
    p.add_argument("delivery", choices=["1", "2", "3"])

    args = parser.parse_args()
    try:
        args.func(args)
    except Fail as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    except subprocess.CalledProcessError as exc:
        print(f"ERROR: command failed: {exc.cmd}\n{(exc.stdout or b'').decode(errors='replace')[-2000:]}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
