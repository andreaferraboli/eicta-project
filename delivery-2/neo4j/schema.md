# Neo4j graph: nodes, relationships, properties (DRAFT)

> Diagram: `diagrams/graph-schema.drawio`. Built from the delivery-1 data by `scripts/eicta.py export-csv` + `cypher/01_import.cypher`. Requirement: at least 8 entities including one ISA hierarchy, at least 10 instances per node type.

## Node types

ISA hierarchies are modelled as **extra labels on the same node** (A-30): an artist node has labels `Artist` and exactly one of `Musician` / `Band`; a product node has `Product` and exactly one of `Food` / `Drink` / `Merchandise`.

| Label | Property | Type | Description | Instances (demo data) |
|---|---|---|---|---|
| Festival | name (unique) | String | festival name | 25 |
| | location | String | city | |
| | startDate, endDate | Date | festival dates | |
| Stage | code (unique) | String | identification code | 50 |
| | name | String | stage name | |
| | maxCapacity | Integer | maximum number of people | |
| | locationDescription | String | where the stage is in the festival | |
| Performance | performanceId (unique) | Integer | unique identifier | 100 |
| | title, genre | String | | |
| | startTime, endTime | LocalDateTime | | |
| Artist | stageName (unique) | String | stage name | 55 |
| | country, mainGenre | String | | |
| Musician (+Artist) | fullName, nationality, mainInstrument | String | musician-only properties | 30 |
| Band (+Artist) | formationYear | Integer | band-only property | 25 |
| Stand | name (unique), sponsor | String | | 50 |
| Product | name (unique) | String | | 36 |
| | price | Float | | |
| Food (+Product) | expirationDate: Date, foodType: String | | | 12 |
| Drink (+Product) | expirationDate: Date | | | 12 |
| Merchandise (+Product) | (none) | | | 12 |
| Person | email (unique), fullName, phone | String | buyer | 40 |
| Purchase | purchaseId (unique): Integer, date: Date, paymentMethod: String | | purchase event (A-31) | 80 |
| Ticket | ticketId (unique): Integer, type: String, price: Float, validFrom/validTo: Date | | | 60 |

Entities used: Festival, Stage, Performance, Artist, Musician, Band, Stand, Product, Food, Drink, Merchandise, Person, Purchase, Ticket (14, of which 2 ISA hierarchies).

## Relationship types

| Type | From -> To | Properties | ER relationship |
|---|---|---|---|
| PART_OF | Stage -> Festival | - | Divided into |
| HELD_AT | Performance -> Stage | - | Held at |
| PERFORMS_IN | Artist -> Performance | - | Given by |
| MEMBER_OF | Musician -> Band | - | Member of |
| LOCATED_AT | Stand -> Festival | - | Hosts |
| SELLS | Stand -> Product | - | Sells |
| MADE | Person -> Purchase | - | Makes |
| INCLUDES | Purchase -> Ticket | - | Includes |
| VALID_FOR | Ticket -> Festival | - | Valid for |
| INCLUDES_ITEM | Purchase -> Product | standName: String | Buys item (ternary: the stand is kept as a property) |

## Constraints

Uniqueness constraints on every identifier (`cypher/00_constraints.cypher`), same keys as the SQL primary keys.

## Checks (`python scripts/eicta.py neo4j-check`)

- at least 10 nodes per label;
- every Artist is exactly one of Musician/Band, every Product exactly one of Food/Drink/Merchandise;
- every band has at least 2 members, every performance at least one artist, no isolated node;
- node counts equal the SQL table counts (coherence with delivery 1).
