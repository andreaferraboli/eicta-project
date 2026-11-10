# Verifica

Eseguita il 2026-10-02 su Windows 11, dalla radice del progetto. Log completi in `build/verification-logs/` (rigenerabili, non versionati). Tutto gira sui **dati demo** del generatore deterministico, non su dati Mockaroo.

Ambiente: Python 3.12.1 (sqlite3 3.43.1), Docker 29.1.5 con Compose v5.0.1, immagini `neo4j:5.26.12-community` e `mongo:7.0.14`, Node.js 22.20.0, MiKTeX pdfTeX 4.19 con latexmk 4.86a, Chrome headless (solo per anteprime).

## Comandi eseguiti

| # | Comando | Esito | Evidenza / output |
|---|---|---|---|
| 00 | `docker compose config --quiet` | OK | configurazione valida |
| 01 | `eicta.py setup` | OK | tutti gli strumenti trovati |
| 02 | `eicta.py sql-build` | OK | DB da `schema.sql` + dati demo |
| 03 | `eicta.py sql-check` | OK | 0 violazioni FK; 15 tabelle tra 25 e 250 tuple (minimo 25); 10 controlli di `checks.sql` a 0 |
| 04 | `eicta.py sql-queries` | OK | 10 query, ognuna con almeno 1 riga (da 2 a 25); output testuali in `build/delivery-1/query-results/` |
| 05 | `eicta.py sql-dump` | OK | dump `.sql` ripristinato in un DB in memoria con conteggi identici |
| 06 | `eicta.py export-csv` | OK | 16 CSV per Neo4j |
| 07 | `eicta.py up` | OK | entrambi i container `healthy` |
| 08 | `eicta.py neo4j-load` | OK | vincoli + import CSV |
| 09 | `eicta.py neo4j-check` | OK | 14 label tra 12 e 100 nodi (minimo 10); 6 controlli ISA/coerenza a 0; conteggi grafo = conteggi SQL per 11 entità |
| 10 | `eicta.py neo4j-queries` | OK | 10 letture (da 1 a 53 righe) e 5 scritture eseguite; shortest path: 3 hop |
| 11 | `eicta.py neo4j-load` | OK | seed ripristinato dopo le scritture |
| 12 | `eicta.py neo4j-dump` | OK | `build/delivery-2/neo4j-dump/neo4j.dump` (circa 148 KB) |
| 13-14 | `neo4j-restore --yes`, poi `neo4j-check` | OK | test manuale prima del ciclo: 12 stage modificati, poi 0 dopo il restore; check superato |
| 15 | `eicta.py mongo-transform` | OK | 25 documenti; nessun array con meno di 2 elementi |
| 16-17 | `mongo-seed`, `mongo-check` | OK | 1 collection, 25 documenti; minimo 2 elementi per array (stages 50, performances 100, artists 250, stands 50, products 150) |
| 18 | `eicta.py mongo-queries` | OK | 10 letture, 5 scritture (insert 1, update 1/20/1, delete 1); demo `$elemMatch`: 9 documenti con condizioni separate, 7 con condizioni simultanee |
| 19-22 | `mongo-seed`, `mongo-dump`, `mongo-restore --yes`, `mongo-check` | OK | test manuale prima del ciclo: 2 documenti cancellati, poi ripristinati (25) |
| 23 | `npm test` (web-auth) | OK | 10/10 test |
| 24 | `npm run validate` (BPMN) | OK | entrambi i file validi per bpmn-moddle e per i controlli strutturali |
| 25 | `eicta.py report 1 2 3` | OK | PDF da 18, 13 e 13 pagine (solo segnaposto) |
| 26-28 | `eicta.py package 1/2/3` | ZIP creato, **uscita 1 voluta** | segnala: nessuna immagine, TODO nel report, dati demo |
| 29 | `scripts/eicta.ps1 sql-check` | OK | wrapper PowerShell |
| 30 | `sh scripts/eicta.sh sql-check` | OK dopo correzione | al primo tentativo prendeva lo stub `python3` del Microsoft Store; ora prova ogni interprete |
| 31 | `echo no \| eicta.py reset` | annullato (uscita 1) | conferma richiesta, volumi intatti |
| extra | copia del progetto in `.../path with spaces/eicta copy` | OK | sql-build/check/queries/dump, mongo-transform, export-csv, report 1, wrapper PowerShell |

## Controlli visivi (non sono evidenze)

- BPMN renderizzati con bpmn-js 17 in Chrome headless: layout leggibile; ritoccati due incroci (message flow sopra un task, fine evento sul percorso di un flusso).
- draw.io (ER e grafo) renderizzati col viewer ufficiale: nessun arco rotto; spostato un self-loop sovrapposto a un'etichetta.
- Pagina statica a 1280px e a 375px (iframe): responsive, menu mobile visibile, countdown attivo.
- Report: frontespizio, indice e capitoli query controllati; i listing mostrano solo il codice delle query.

## Problemi trovati e corretti durante la verifica

- Nodo isolato in Neo4j (un prodotto mai venduto): il generatore ora assegna ogni prodotto ad almeno uno stand.
- Controlli Cypher che non stampavano nulla con zero violazioni (aggregazione con chiavi letterali): riscritti con `COUNT {}`.
- Test SQL injection con payload rifiutato dalla validazione prima del DB: payload cambiato per arrivare davvero alla query parametrizzata.
- Porta 27017 occupata da un MongoDB locale: porta host del container portata a 27018 (il MongoDB locale non è stato toccato).
- `package` non segnalava una cartella figure vuota: ora controlla immagini, TODO e origine dei dati.

## Limiti

- Dati demo, non Mockaroo: tutti i "verificato" riguardano il meccanismo, da rieseguire sui dati finali.
- Nessuno screenshot raccolto. Gli output testuali in `build/` non sostituiscono gli screenshot dei tool.
- MongoDB testato in locale (Docker), non su Atlas. Neo4j testato in Docker, non su Neo4j Desktop o Aura: compatibilità del dump con la versione usata dal docente non verificata.
- La validazione lato client del web-auth non ha test automatici.
- Il passaggio su SQLite Online non è stato eseguito.
- I file Mockaroo in `delivery-1/mockaroo/schemas/` sono checklist, non testati con l'import di Mockaroo.
- Template LaTeX provvisorio: quello ufficiale non è disponibile nel repository.
- Limite di 30 pagine verificato solo sui template con segnaposto.

## Passaggi ancora manuali

Vedi le checklist: [consegna 1](../delivery-1/CHECKLIST.md), [consegna 2](../delivery-2/CHECKLIST.md), [consegna 3](../delivery-3/CHECKLIST.md).
