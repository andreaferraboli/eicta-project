# Discrepanze e ambiguità delle fonti

Fonte primaria: i tre PDF 2025/26. I PDF 2024/25 (in `reference/2024-25/`) descrivono un altro problema e non sono requisiti.

| ID | Dove | Osservazione | Decisione |
|---|---|---|---|
| D-01 | Tutti i PDF | Le date (9 ottobre, 23 ottobre, 20 novembre, 9 dicembre) non riportano l'anno. | Riportate come informazioni dei documenti; verificare su WeBeep. |
| D-02 | PDF 1, pag. 1 | 2025/26 chiede ER, modello logico e SQL; il PDF 2024/25 chiedeva anche un "Relational Model" separato. | Si segue 2025/26: un capitolo per il modello logico, con PK/FK di tutte le tabelle. |
| D-03 | PDF 1, pag. 2 | Strumenti ammessi: SQLite Online o MySQL. Il PDF 2 parla di "MySQL/SQLite Database". | Scelto SQLite: il dump richiesto è il file `.db`. Se il gruppo preferisce MySQL serve adattare `schema.sql` e usare "Self-Contained Dump". |
| D-04 | PDF 1, pag. 2 | Il report della consegna 1 richiede introduzione e analisi del testo; i PDF 2 e 3 elencano solo prima pagina, indice, un capitolo per richiesta e didascalie. | Template 2 e 3 senza capitolo introduzione obbligatorio (presente come facoltativo e breve). |
| D-05 | PDF 1, pag. 1 | "can sell either of the three aforementioned products" può significare "una categoria a scelta" oppure "uno qualsiasi dei tre tipi". | Interpretazione N:M senza restrizioni (A-09). Da confermare col docente o in sede di revisione. |
| D-06 | PDF 1, pag. 1 | "A person can buy multiple tickets, and they can also purchase shop items": non è chiaro se biglietti e articoli condividano lo stesso acquisto. | Entità Purchase unica (A-11). |
| D-07 | PDF 1, pag. 2 | Le combinazioni di query elencano solo alcune clausole; non è detto se clausole aggiuntive (ORDER BY) siano ammesse. | ORDER BY usato solo in q02 per rendere LIMIT deterministico; nessun AS nelle combinazioni che non lo elencano. |
| D-08 | PDF 2, pag. 1 | "be coherent with your ER diagram" mentre la guida importa CSV tabellari. | Ogni tabella ponte N:M diventa una relazione; ogni entità un nodo; controllo automatico dei conteggi SQL vs grafo. |
| D-09 | PDF 2, pag. 2 | Strumenti: "Neo4j Online tool or Desktop Installer". | Usato Neo4j Community 5.26 in Docker; dump con `neo4j-admin database dump`, importabile in Desktop 5.x. Verificare la versione richiesta per il dump. |
| D-10 | PDF 3, pag. 2 | Strumento indicato: MongoDB Atlas. | Istanza locale Docker per i test (A-42). Nessuna risorsa cloud creata. |
| D-11 | PDF 3, pag. 2 | "Passwords can be in plain text without having to hash them". | Hash scrypt (permesso, non vietato) e compatibilità con righe in chiaro (A-43). |
| D-12 | PDF 3, pag. 2 | "sign-in form" è usato nel senso di registrazione ("signing and logging in"). | Form "Sign in" = registrazione, "Log in" = accesso. |
| D-13 | PDF 3, pag. 1 | 2025/26: una sola collection, 10 documenti, 2 elementi per array. 2024/25: 10 documenti per entità e 20 incorporati. | Seguito 2025/26. |
| D-14 | PDF 2 | 2025/26: almeno 8 entità con una ISA e query con path variabile; 2024/25: 5 entità, 3 query MATCH semplici, nessun path variabile. | Seguito 2025/26. |
| D-15 | PDF 2024/25 n. 2 | L'intestazione dice "EICTA 2023/24" ma il file è 2024_2025. | Irrilevante (solo riferimento). |
| D-16 | Template | I template Word e LaTeX sono link SharePoint e non sono nel repository. | Template LaTeX provvisorio dichiarato (requisito D1-DEL-9 "bloccato"): sostituire con quello ufficiale appena scaricato. |
| D-17 | Tutti i PDF | Controllo testo nascosto (font < 5 pt) eseguito sui PDF EICTA: nessun testo nascosto trovato. | Nessuna azione. |
