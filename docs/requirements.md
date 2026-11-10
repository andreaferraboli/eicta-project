# Matrice dei requisiti

Fonte primaria: i PDF 2025/26 (`1st/2nd/3rd Project Delivery.pdf`). Le pagine sono quelle dei PDF. Le scadenze sono riportate come scritte nei documenti, senza presumere che siano ancora valide.

Versione tabellare: [requirements.csv](requirements.csv) (stesso contenuto).

**Tipo**: `obbligo` = richiesto dal PDF; `suggerimento` = consiglio del docente ("recommend", "you can"); `info` = informazione organizzativa.

**Stato**: `predisposto` (struttura pronta, contenuto da scrivere) · `dimostrativo` (esempio funzionante, da rivedere o sostituire) · `da completare` (lavoro o evidenza mancante) · `verificato` (eseguito davvero, vedi [verification.md](verification.md)) · `bloccato` (dipende da qualcosa che manca).

`verificato` indica che il meccanismo è stato eseguito con esito positivo **sui dati demo**. Non sostituisce le evidenze richieste (screenshot, dati Mockaroo).

Riepilogo: bloccato 1, da completare 15, dimostrativo 15, predisposto 8, verificato 42 (totale 81).

## Consegna 1: ER e SQL

| ID | Pag. | Tipo | Descrizione | Vincolo | Supporto | Verifica | Stato | Note |
|---|---|---|---|---|---|---|---|---|
| D1-ER-1 | 1 | obbligo | Modello ER del problema con diagramma | non contraddire il testo | delivery-1/diagrams/er-model.drawio; delivery-1/analysis/text-analysis.md | revisione del gruppo contro il testo | **dimostrativo** | bozza da revisionare |
| D1-ER-2 | 1 | obbligo | Assunzioni, ragionamenti e scelte di progetto |  | docs/assumptions.md; delivery-1/analysis/text-analysis.md | revisione | **dimostrativo** | bozza |
| D1-ER-3 | 1 | obbligo | ID artificiali solo se nessun attributo del testo puo essere chiave (nota a) |  | delivery-1/sql/schema.sql (commento iniziale); docs/assumptions.md A-03 | ispezione: solo TicketID, PurchaseID | **predisposto** |  |
| D1-ER-4 | 1 | obbligo | Direzione di lettura di esempio per le cardinalita (nota b) |  | er-model.drawio (frecce nei rombi, nota) | ispezione visiva | **dimostrativo** |  |
| D1-ER-5 | 1 | obbligo | Tipo delle gerarchie ISA sempre indicato (nota c) |  | er-model.drawio: ISA (t, e) su Artist e Product | ispezione visiva | **dimostrativo** |  |
| D1-LM-1 | 1 | obbligo | Modello logico: relazioni, attributi, PK e FK |  | delivery-1/analysis/logical-model.md | coerenza con schema.sql | **dimostrativo** |  |
| D1-SQL-1 | 1 | obbligo | Codice SQL di definizione di ogni tabella, descritto |  | delivery-1/sql/schema.sql | sql-build + sql-check | **verificato** | eseguito su SQLite locale (python sqlite3) |
| D1-SQL-2 | 1 | obbligo | Popolamento con Mockaroo | almeno 25 tuple per tabella | delivery-1/mockaroo/ | sql-build --source mockaroo + sql-check | **da completare** | i dati demo non valgono come evidenza Mockaroo |
| D1-SQL-3 | 1 | obbligo | Screenshot dei dati inseriti per ogni tabella | 1 per tabella (15) | delivery-1/report/figures/ | checklist | **da completare** |  |
| D1-SQL-4 | 1 | obbligo | Controllo quantita: almeno 25 tuple per tabella | >= 25 | scripts/eicta.py sql-check | sql-check | **verificato** | verificato sui dati demo; da rieseguire sui dati Mockaroo |
| D1-Q-A | 1 | obbligo | Query WHERE | >= 1 query, >= 1 tupla in output (suggerito) | delivery-1/sql/queries/q01_where.sql | sql-queries | **verificato** | eseguita su dati demo |
| D1-Q-B | 1 | obbligo | Query WHERE, LIMIT, LIKE |  | q02_where_limit_like.sql | sql-queries | **verificato** | ORDER BY aggiunto per determinismo |
| D1-Q-C | 1 | obbligo | Query WHERE, IN, Nested Query |  | q03_where_in_nested.sql | sql-queries | **verificato** |  |
| D1-Q-D | 1 | obbligo | Query GROUP BY, 1 JOIN, AS |  | q04_groupby_1join_as.sql | sql-queries | **verificato** |  |
| D1-Q-E | 1 | obbligo | Query WHERE, GROUP BY |  | q05_where_groupby.sql | sql-queries | **verificato** |  |
| D1-Q-F | 1 | obbligo | Query GROUP BY, HAVING, AS |  | q06_groupby_having_as.sql | sql-queries | **verificato** |  |
| D1-Q-G | 1 | obbligo | Query WHERE, GROUP BY, HAVING, AS |  | q07_where_groupby_having_as.sql | sql-queries | **verificato** |  |
| D1-Q-H | 1 | obbligo | Query WHERE, Nested Query, GROUP BY |  | q08_where_nested_groupby.sql | sql-queries | **verificato** |  |
| D1-Q-I | 1 | obbligo | Query WHERE, GROUP BY, HAVING, 1 JOIN |  | q09_where_groupby_having_1join.sql | sql-queries | **verificato** |  |
| D1-Q-J | 2 | obbligo | Query WHERE, GROUP BY, HAVING, 2 JOINs |  | q10_where_groupby_having_2joins.sql | sql-queries | **verificato** |  |
| D1-Q-DOC | 2 | obbligo | Per ogni query: titolo, SQL, descrizione, screenshot del risultato |  | intestazione di ogni q*.sql; report chapter queries | checklist | **da completare** | mancano gli screenshot reali |
| D1-DEL-1 | 2 | obbligo | Registrazione del gruppo | scadenza nel PDF: 9 ottobre 23:59 | link in delivery-1/ASSIGNMENT.md | manuale | **da completare** | data riportata dal PDF, validita non verificata |
| D1-DEL-2 | 2 | info | Consegna su WeBeep, sezione Assignments, cartella zippata | scadenza nel PDF: 23 ottobre 23:59 | scripts/eicta.py package 1 | package | **da completare** |  |
| D1-DEL-3 | 2 | obbligo | Dump self-contained (schema + dati); per SQLite il file .db |  | build/delivery-1/euphoric_events.db; euphoric_events_dump.sql | sql-dump (restore in memoria) | **verificato** | verificato su dati demo |
| D1-DEL-4 | 2 | obbligo | Report PDF: prima pagina con titolo, numero gruppo, membri, anno accademico |  | delivery-1/report/main.tex | compilazione LaTeX | **predisposto** | segnaposto TODO |
| D1-DEL-5 | 2 | obbligo | Report: indice, capitolo introduzione con il testo della consegna |  | delivery-1/report/chapters/01-introduction.tex | compilazione | **predisposto** |  |
| D1-DEL-6 | 3 | obbligo | Report: capitolo analisi del testo (entita, relazioni, attributi, assunzioni) |  | chapters/02-text-analysis.tex | compilazione | **predisposto** |  |
| D1-DEL-7 | 3 | obbligo | Report: un capitolo per ogni richiesta; didascalia per ogni figura |  | chapters/03..06 | compilazione | **predisposto** |  |
| D1-DEL-8 | 3 | obbligo | Cartella con immagini ad alta risoluzione, una per figura |  | delivery-1/report/figures/ | checklist | **da completare** |  |
| D1-DEL-9 | 3 | suggerimento | Usare i template forniti (Word o LaTeX); Overleaf consigliato |  | template provvisorio in delivery-1/report/ |  | **bloccato** | template ufficiale non presente nel repo: sostituire |

## Consegna 2: Neo4j e BPMN

| ID | Pag. | Tipo | Descrizione | Vincolo | Supporto | Verifica | Stato | Note |
|---|---|---|---|---|---|---|---|---|
| D2-NEO-1 | 1 | obbligo | Database Neo4j da almeno 8 entita del modello ER, inclusa almeno una gerarchia ISA | >= 8 entita, >= 1 ISA | delivery-2/neo4j/schema.md; cypher/01_import.cypher | neo4j-check | **verificato** | 14 tipi di nodo, 2 ISA come label |
| D2-NEO-2 | 1 | obbligo | Nodi collegati e coerenti con il diagramma ER |  | neo4j-check (isolated_nodes, coerenza conteggi SQL) | neo4j-check | **verificato** |  |
| D2-NEO-3 | 1 | suggerimento | Riutilizzo dei dati SQL tramite CSV e guida di import |  | scripts/eicta.py export-csv; neo4j-load | neo4j-load | **verificato** |  |
| D2-NEO-4 | 1 | obbligo | Almeno 10 istanze per tipo di nodo | >= 10 | cypher/checks.cypher | neo4j-check | **verificato** |  |
| D2-NEO-5 | 1 | obbligo | Rappresentazione schematica di nodi, relazioni e proprieta (draw.io suggerito) |  | delivery-2/neo4j/diagrams/graph-schema.drawio | ispezione visiva | **dimostrativo** |  |
| D2-NEO-6 | 1 | obbligo | Dizionario attributi e tipi di nodi e relazioni, assunzioni aggiuntive |  | delivery-2/neo4j/schema.md | revisione | **dimostrativo** |  |
| D2-QW | 1 | obbligo | 5 query create/update/delete, almeno una per tipo | 5 totali, >= 1 per tipo | cypher/queries/write/w01..w05 | neo4j-queries | **verificato** | 2 create, 2 update, 1 delete |
| D2-QR-A | 1 | obbligo | 2 query: >= 2 nodi nel MATCH + condizioni | 2 | read/r01, r02 | neo4j-queries | **verificato** |  |
| D2-QR-B | 1 | obbligo | 2 query: >= 2 nodi + condizioni + aggregazione senza WITH | 2 | read/r03, r04 | neo4j-queries | **verificato** |  |
| D2-QR-C | 1 | obbligo | 2 query: >= 2 nodi + condizioni + un WITH | 2 | read/r05, r06 | neo4j-queries | **verificato** |  |
| D2-QR-D | 1 | obbligo | 2 query: >= 3 nodi + condizioni + piu WITH | 2 | read/r07, r08 | neo4j-queries | **verificato** |  |
| D2-QR-E | 1 | obbligo | 1 query con path a lunghezza variabile + condizioni | 1 | read/r09 | neo4j-queries | **verificato** |  |
| D2-QR-F | 1 | obbligo | 1 query di shortest path | 1 | read/r10 | neo4j-queries | **verificato** |  |
| D2-Q-DOC | 1 | obbligo | Per ogni query: titolo, descrizione breve, screenshot (grafo o tabella) |  | intestazioni .cypher; report | checklist | **da completare** | screenshot da Neo4j Browser |
| D2-BPMN-1 | 1 | obbligo | Diagramma BPMN del processo Store&Store, con eventuali assunzioni |  | delivery-2/bpmn/store-and-store.bpmn; bpmn/assumptions.md | validate.mjs (bpmn-moddle) + render bpmn-js | **dimostrativo** | bozza da revisionare in bpmn.io |
| D2-BPMN-2 | 2 | obbligo | Processo Euphoric Events: testo + diagramma |  | euphoric-events-artist-booking.bpmn; bpmn/euphoric-events-process.md | validate.mjs | **dimostrativo** | processo proposto, da approvare dal gruppo |
| D2-BPMN-3 | 2 | obbligo | Processo Euphoric: almeno un attore esterno | >= 1 | pool Artist (management) | validate.mjs (2 pool) | **dimostrativo** |  |
| D2-BPMN-4 | 2 | obbligo | Processo Euphoric: RDBMS della prima consegna con artefatti e swim lane dedicata |  | lane Festival RDBMS + data store | ispezione + validate | **dimostrativo** |  |
| D2-BPMN-5 | 2 | obbligo | Processo Euphoric: almeno 10 passi prima della terminazione | >= 10 | percorso di successo: 14 elementi | conteggio manuale sul diagramma | **dimostrativo** |  |
| D2-DEL-1 | 2 | info | Consegna su WeBeep, cartella zippata | scadenza nel PDF: 20 novembre 23:59 | scripts/eicta.py package 2 | package | **da completare** |  |
| D2-DEL-2 | 2 | obbligo | Dump del database Neo4j |  | scripts/eicta.py neo4j-dump / neo4j-restore | dump + restore eseguiti | **verificato** | su dati demo |
| D2-DEL-3 | 2 | obbligo | Report PDF di al massimo 30 pagine: prima pagina, indice, un capitolo per richiesta, didascalie | <= 30 pagine | delivery-2/report/ | compilazione + conteggio pagine | **predisposto** |  |
| D2-DEL-4 | 3 | obbligo | Cartella di immagini ad alta risoluzione, una per figura |  | delivery-2/report/figures/ | checklist | **da completare** |  |

## Consegna 3: MongoDB e Web

| ID | Pag. | Tipo | Descrizione | Vincolo | Supporto | Verifica | Stato | Note |
|---|---|---|---|---|---|---|---|---|
| D3-MDB-1 | 1 | obbligo | Database MongoDB da almeno 5 entita del modello ER | >= 5 | delivery-3/mongodb/schema.md (6 entita) | revisione | **dimostrativo** |  |
| D3-MDB-2 | 1 | obbligo | Una sola collection | = 1 | mongodb/checks.js | mongo-check | **verificato** |  |
| D3-MDB-3 | 1 | obbligo | Struttura dei documenti e gerarchia di contenimento descritte |  | delivery-3/mongodb/schema.md | revisione | **dimostrativo** |  |
| D3-MDB-4 | 1 | obbligo | Almeno 10 documenti nella collection | >= 10 | checks.js | mongo-check | **verificato** | 25 documenti |
| D3-MDB-5 | 1 | obbligo | Almeno due elementi per ogni array di sotto-documenti, nessun array vuoto | >= 2, nessun [] | checks.js; transform in scripts/eicta.py | mongo-check + controllo in mongo-transform | **verificato** |  |
| D3-MDB-6 | 1 | suggerimento | Riuso dei dati della prima consegna rimodellati |  | scripts/eicta.py mongo-transform | mongo-transform | **verificato** |  |
| D3-QW | 1 | obbligo | 5 query create/update/delete, almeno una per tipo | 5, >= 1 per tipo | mongodb/queries/write/w01..w05 | mongo-queries | **verificato** | 1 insert, 3 update, 1 delete |
| D3-QR-A | 1 | obbligo | 2 query con proiezioni e operatori logici | 2 | read/r01, r02 | mongo-queries | **verificato** |  |
| D3-QR-B | 1 | obbligo | 2 query con limit, sort e operatori di confronto | 2 | read/r03, r04 | mongo-queries | **verificato** |  |
| D3-QR-C | 1 | obbligo | 1 query con operatori element | 1 | read/r05 | mongo-queries | **verificato** |  |
| D3-QR-D | 1 | obbligo | 1 query con l'operatore group | 1 | read/r06 | mongo-queries | **verificato** |  |
| D3-QR-E | 1 | obbligo | 1 query con unwind e group by | 1 | read/r07 | mongo-queries | **verificato** |  |
| D3-QR-F | 1 | obbligo | 1 query con unwind, group by e filtro successivo | 1 | read/r08 | mongo-queries | **verificato** |  |
| D3-QR-G | 1 | obbligo | 1 query con due condizioni valutate separatamente sui sotto-documenti di un array | 1 | read/r09; elemmatch-demo.js | mongo-queries (9 documenti) | **verificato** |  |
| D3-QR-H | 1 | obbligo | 1 query con due condizioni valutate simultaneamente ($elemMatch) | 1 | read/r10; elemmatch-demo.js | mongo-queries (7 documenti, 2 di differenza) | **verificato** |  |
| D3-Q-DOC | 1 | obbligo | Per ogni query: titolo, descrizione breve, screenshot |  | intestazioni .js; report | checklist | **da completare** |  |
| D3-WEB-1 | 1 | obbligo | Pagina promozionale statica di un festival (HTML, CSS, JS opzionale, non solo HTML puro) | nessuna interazione con server | delivery-3/web-static/ | apertura nel browser (headless Chrome) | **dimostrativo** | contenuti fittizi |
| D3-WEB-2 | 1 | obbligo | Report: descrizione contenuti, struttura e stile della pagina, screenshot |  | web-static/README.md; report chapter | checklist | **da completare** |  |
| D3-WEB-3 | 2 | obbligo | Pagina con form di log-in e sign-in verso server Node.js + Express che interroga SQLite |  | delivery-3/web-auth/ | npm test | **verificato** | 10 test passati |
| D3-WEB-4 | 2 | obbligo | DB SQLite creato con sqliteonline.com, una tabella utenti (email unica, password, nome, cognome) |  | web-auth/db/users.sql | manuale su sqliteonline.com | **da completare** | SQL pronto; passaggio su SQLite Online non eseguito |
| D3-WEB-5 | 2 | obbligo | Messaggio di benvenuto in caso di successo |  | src/app.js; public/app.js | npm test | **verificato** |  |
| D3-WEB-6 | 2 | obbligo | Validazione lato client; il server gestisce tentativi falliti |  | public/app.js; src/validation.js | npm test (server); client da provare a mano | **verificato** | lato client non coperto da test automatici |
| D3-WEB-7 | 2 | obbligo | Report: descrizione della logica di sign-in e log-in |  | web-auth/README.md; report chapter | checklist | **da completare** |  |
| D3-DEL-1 | 2 | info | Consegna su WeBeep, cartella zippata | scadenza nel PDF: 9 dicembre 23:59 | scripts/eicta.py package 3 | package | **da completare** |  |
| D3-DEL-2 | 2 | obbligo | Dump del database MongoDB |  | scripts/eicta.py mongo-dump / mongo-restore | dump + restore eseguiti | **verificato** | su istanza locale Docker, non Atlas |
| D3-DEL-3 | 2 | obbligo | Una cartella per ogni Web Task con il codice sorgente | 2 cartelle | web-static/, web-auth/ | package 3 | **predisposto** |  |
| D3-DEL-4 | 2 | obbligo | Report PDF di al massimo 30 pagine; List of Figures/Tables facoltative | <= 30 pagine | delivery-3/report/ | compilazione + conteggio pagine | **predisposto** |  |
| D3-DEL-5 | 3 | obbligo | Cartella di immagini ad alta risoluzione, una per figura |  | delivery-3/report/figures/ | checklist | **da completare** |  |
