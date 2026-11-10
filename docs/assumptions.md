# Assunzioni

**Stato: bozza da revisionare dal gruppo.** Ogni assunzione interpreta il testo senza contraddirlo (vincolo del PDF 1, pag. 1). Le assunzioni del modello vanno riportate nel capitolo "Text analysis" del report (in inglese).

## Modello dati (consegna 1)

| ID | Assunzione | Motivo | Dove pesa |
|---|---|---|---|
| A-01 | Il nome del festival è unico e fa da chiave (ogni edizione ha un nome distinto, es. "Aurora Fest 2026"). | Il testo non dà un identificatore; la nota a vieta ID artificiali se un attributo può essere chiave. | `Festival.Name` PK |
| A-02 | Il codice dello stage è unico tra tutti i festival. | "identification code" indica un identificatore. | `Stage.Code` PK |
| A-03 | ID artificiali solo per Ticket e Purchase. | Nessun attributo del testo li identifica (tipo, prezzo, data, metodo di pagamento si ripetono). `PerformanceID` non è artificiale: il testo dice "a unique identifier". | `TicketID`, `PurchaseID` |
| A-04 | Stage name dell'artista, nome dello stand, nome del prodotto ed email della persona sono unici. | Sono gli unici attributi candidati chiave nel testo. | PK |
| A-05 | "Multiple stages" = almeno 2 stage per festival. | Lettura letterale di "multiple". | cardinalità (2,N); `checks.sql` |
| A-06 | Artist ISA {Musician, Band} totale ed esclusiva. | "artists, which may be solo musicians or bands": nessun altro tipo, un artista non è entrambi. | ER, `Artist.ArtistType` |
| A-07 | Una band ha almeno 2 musicisti (relazione Member of tra Musician e Band); un musicista può appartenere a 0..N band. | "bands (i.e., at least two musicians)". Il testo non vieta l'appartenenza a più band. | `BandMember`; `checks.sql` |
| A-08 | Product ISA {Food, Drink, Merchandise} totale ed esclusiva. | "either of the three aforementioned products". | ER |
| A-09 | "Can sell either of the three products" = ogni stand può vendere prodotti di una qualsiasi categoria (N:M Sells). Uno stand vende almeno un prodotto. | Lettura meno restrittiva che non contraddice il testo; alternativa: uno stand vende una sola categoria (vedi source-discrepancies D-05). | `Sells` |
| A-10 | Food e Drink hanno ExpirationDate; solo Food ha Type. | Testo esplicito. Tradotto collassando le figlie nel padre con vincoli CHECK. | `Product` |
| A-11 | Un acquisto (Purchase) è un evento con data e metodo di pagamento, fatto da una persona, che contiene biglietti e/o articoli. Ogni biglietto appartiene a un solo acquisto. | "Whenever a purchase happens, the system should store the date and the payment method used" vale per biglietti e articoli. | `Purchase`, `Ticket.PurchaseID`, `PurchaseItem` |
| A-12 | Un articolo è acquistato presso uno stand che lo vende (relazione ternaria Buys item: Purchase, Stand, Product). Nessuna quantità. | Il testo non parla di quantità: non viene aggiunta. | `PurchaseItem` con FK verso `Sells` |
| A-13 | Il periodo di validità del biglietto è rappresentato da ValidFrom e ValidTo, dentro le date del festival. | "a validity period". | `Ticket` |
| A-14 | Un biglietto vale per un solo festival. | Implicito in "To enter a festival, people must buy tickets". | `Ticket.FestivalName` |
| A-15 | Le performance si svolgono dentro le date del festival del loro stage; gli acquisti di articoli avvengono durante il festival. | "purchase shop items during the festival". | `checks.sql` |
| A-16 | Genere della performance e genere principale dell'artista sono attributi indipendenti (possono differire). | Il testo li definisce separatamente. | query Neo4j r05 |

## Dati

| ID | Assunzione |
|---|---|
| A-20 | I dati in `delivery-1/data/demo/` sono un **fallback dimostrativo** deterministico, non dati Mockaroo. La consegna richiede Mockaroo. |
| A-21 | Il generatore demo dà a ogni performance 2 o 3 artisti e a ogni stand 3 prodotti, così le consegne 2 e 3 possono riusare gli stessi dati senza array con meno di 2 elementi. |

## Consegna 2

| ID | Assunzione |
|---|---|
| A-30 | Le ISA diventano label multiple sullo stesso nodo (`:Artist:Musician`, `:Product:Food`). |
| A-31 | Purchase resta un nodo (non una relazione) per coerenza con l'entità del modello ER; l'acquisto di un articolo è la relazione `INCLUDES_ITEM {standName}`. |
| A-32 | BPMN Store&Store e processo Euphoric Events: assunzioni in `delivery-2/bpmn/assumptions.md`. |

## Consegna 3

| ID | Assunzione |
|---|---|
| A-40 | Collection unica `festivals`: un documento per festival con stage, performance, artisti, stand e prodotti incorporati (6 entità). Persone, biglietti e acquisti restano fuori: non servono al minimo di 5 entità e moltiplicherebbero i documenti. |
| A-41 | Gli artisti sono incorporati (copiati) in ogni performance: duplicazione accettata, tipica del modello documentale. |
| A-42 | Database locale in Docker invece di MongoDB Atlas (il PDF indica Atlas come strumento). Il dump `mongodump` ha lo stesso formato. Se il docente richiede Atlas, importare il seed in Atlas. |
| A-43 | Web auth: le password sono salvate con hash scrypt anche se il PDF permette il testo in chiaro; il login accetta anche righe inserite a mano in chiaro su SQLite Online. |
