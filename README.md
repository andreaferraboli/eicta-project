# EICTA Project 2025/26: Euphoric Events

Group project in three deliveries on the same domain (music festivals for the Euphoric Events company). This repository is a **working base**: tools and pipelines run, examples are labelled as such, and the parts that the group must still design, review or collect are listed explicitly.

| Delivery | Topic | Instructions | Evidence checklist | Deadline (as written in the PDF) |
|---|---|---|---|---|
| 1 | ER, logical model, SQL | [delivery-1/ASSIGNMENT.md](delivery-1/ASSIGNMENT.md) | [CHECKLIST](delivery-1/CHECKLIST.md) | October 23, 23:59 (group registration by October 9) |
| 2 | Neo4j and BPMN | [delivery-2/ASSIGNMENT.md](delivery-2/ASSIGNMENT.md) | [CHECKLIST](delivery-2/CHECKLIST.md) | November 20, 23:59 |
| 3 | MongoDB and Web | [delivery-3/ASSIGNMENT.md](delivery-3/ASSIGNMENT.md) | [CHECKLIST](delivery-3/CHECKLIST.md) | December 9, 23:59 |

The PDFs do not state the year: check the dates on WeBeep.

## What is what

| Kind | Content |
|---|---|
| **Working infrastructure** | `scripts/eicta.py` (build, checks, queries, dumps, restore, reports, ZIPs), `docker-compose.yml` (Neo4j, MongoDB), LaTeX templates, BPMN validator, web-auth server and tests |
| **Demonstrative examples** (review or replace) | draft ER model and logical model, SQL schema, demo data, all queries, graph schema, both BPMN diagrams, MongoDB structure, static web page content |
| **Project work to complete** | review of the model and assumptions, Mockaroo data, final query descriptions, the Euphoric Events process approval, report text |
| **Evidence still to collect** | every screenshot (Mockaroo tables, query results in the real tools, diagrams, web pages), the SQLite Online step, final dumps built from the final data |

Status of every requirement: [docs/requirements.md](docs/requirements.md) ([CSV](docs/requirements.csv)). What was actually executed: [docs/verification.md](docs/verification.md). Assumptions: [docs/assumptions.md](docs/assumptions.md). Ambiguities in the PDFs: [docs/source-discrepancies.md](docs/source-discrepancies.md).

## Requirements

- Python >= 3.10 (stdlib only, nothing to install)
- Docker with Compose v2 (deliveries 2 and 3)
- Node.js >= 22.13 (web-auth, BPMN validator)
- Optional: a LaTeX distribution with `latexmk` (or use Overleaf)

## Quick start

All commands run from the project root. On Windows PowerShell use `.\scripts\eicta.ps1 <command>`, on Linux/macOS `./scripts/eicta.sh <command>`, or directly `python scripts/eicta.py <command>`.

```
python scripts/eicta.py setup            # build/ folders, tool check

# Delivery 1 (SQLite, no container)
python scripts/eicta.py sql-build        # --source mockaroo once the Mockaroo exports exist
python scripts/eicta.py sql-check
python scripts/eicta.py sql-queries
python scripts/eicta.py sql-dump

# Delivery 2
python scripts/eicta.py up               # Neo4j + MongoDB, waits for healthchecks
python scripts/eicta.py export-csv
python scripts/eicta.py neo4j-load
python scripts/eicta.py neo4j-check
python scripts/eicta.py neo4j-queries    # reads first, then writes; neo4j-load restores the seed
python scripts/eicta.py neo4j-dump

# Delivery 3
python scripts/eicta.py mongo-transform
python scripts/eicta.py mongo-seed
python scripts/eicta.py mongo-check
python scripts/eicta.py mongo-queries    # mongo-seed restores the seed
python scripts/eicta.py mongo-dump
cd delivery-3/web-auth && npm install && npm test

# Reports and submission ZIPs
python scripts/eicta.py report 1 2 3
python scripts/eicta.py package 1        # lists anything still missing
python scripts/eicta.py down             # stop containers, keep data
```

Destructive commands ask for confirmation: `reset` (deletes the Docker volumes), `neo4j-restore`, `mongo-restore`. `sql-build` and `neo4j-load` / `mongo-seed` rebuild derived data from the versioned sources.

## Configuration

Local-only defaults are built in (`docker-compose.yml` and `scripts/eicta.py`): Neo4j user `neo4j` / `eicta-local-dev`, MongoDB `eicta` / `eicta-local-dev`, ports bound to 127.0.0.1 (Neo4j 7474/7687, MongoDB **27018** to avoid clashing with a local MongoDB on 27017). To override, set environment variables or create a `.env` file in the project root (ignored by git):

```
NEO4J_PASSWORD=...
MONGO_ROOT_USERNAME=...
MONGO_ROOT_PASSWORD=...
NEO4J_HTTP_PORT=7474
NEO4J_BOLT_PORT=7687
MONGO_PORT=27018
```

Pinned images: `neo4j:5.26.12-community`, `mongo:7.0.14`.

## Layout

```
docs/                 requirements matrix, assumptions, discrepancies, verification log
scripts/              eicta.py (+ PowerShell and POSIX wrappers)
delivery-1/  analysis/ diagrams/ sql/ (schema, checks, queries) data/ (demo generator, mockaroo/) mockaroo/ report/
delivery-2/  neo4j/ (schema.md, diagrams/, cypher/) bpmn/ (.bpmn, tools/) report/
delivery-3/  mongodb/ (schema.md, queries, checks) web-static/ web-auth/ report/
reference/   previous-year texts (not requirements)
build/       generated: databases, CSV, dumps, outputs, PDFs, ZIPs (ignored by git)
```
