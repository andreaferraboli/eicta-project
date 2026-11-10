# MongoDB document structure (DRAFT)

> One collection: `festivals` (database `euphoric_events`). Built from the delivery-1 SQL data by `python scripts/eicta.py mongo-transform`. Requirements: at least 5 entities, one collection, at least 10 documents, at least 2 elements per array of sub-documents, no empty array.

## Containment hierarchy

```
Festival (document)                         entity 1
├── stages: [ Stage ]           >= 2        entity 2
│   └── performances: [ Performance ] >= 2  entity 3
│       └── artists: [ Artist ]       >= 2  entity 4 (ISA: type musician | band)
└── stands: [ Stand ]           >= 2        entity 5
    └── products: [ Product ]   >= 2        entity 6 (ISA: category food | drink | merchandise)
```

## Fields

| Path | Type | Description |
|---|---|---|
| `_id` | String | festival name (same key as SQL) |
| `name` | String | festival name |
| `location` | String | city |
| `startDate`, `endDate` | Date | festival dates |
| `stages` | Array of documents | stages of the festival |
| `stages.code` | String | stage identification code |
| `stages.name` | String | stage name |
| `stages.maxCapacity` | Int | maximum capacity |
| `stages.locationDescription` | String | position within the festival |
| `stages.performances` | Array of documents | performances held at the stage |
| `stages.performances.performanceId` | Int | unique identifier |
| `stages.performances.title`, `.genre` | String | |
| `stages.performances.startTime`, `.endTime` | Date | |
| `stages.performances.artists` | Array of documents | artists giving the performance (copied, A-41) |
| `...artists.stageName`, `.country`, `.mainGenre` | String | common artist fields |
| `...artists.type` | String | `musician` or `band` (ISA discriminator) |
| `...artists.fullName`, `.nationality`, `.mainInstrument` | String | only when `type = musician` |
| `...artists.formationYear` | Int | only when `type = band` |
| `stands` | Array of documents | stands of the festival |
| `stands.name`, `stands.sponsor` | String | |
| `stands.products` | Array of documents | products sold by the stand |
| `stands.products.name` | String | |
| `stands.products.price` | Double | |
| `stands.products.category` | String | `food`, `drink`, `merchandise` |
| `stands.products.expirationDate` | Date | only food and drink (field absent otherwise) |
| `stands.products.foodType` | String | only food (field absent otherwise) |

Optional fields are **absent**, not null, so element operators (`$exists`, `$type`) are meaningful (query r05).

## Embedded counts (demo data, from `mongo-check`)

| Array | Arrays | Elements | Min length |
|---|---|---|---|
| stages | 25 | 50 | 2 |
| stages[].performances | 50 | 100 | 2 |
| stages[].performances[].artists | 100 | 250 | 2 |
| stands | 25 | 50 | 2 |
| stands[].products | 50 | 150 | 3 |

## Separate vs simultaneous conditions

`elemmatch-demo.js` runs r09 (`"stages.name"` + `"stages.maxCapacity"`, may match different stages) and r10 (`$elemMatch`, same stage). On the demo data: 9 vs 7 documents; e.g. *Aurora Fest 2026* has a Main Stage of 5000 and a *different* stage of 800, so it matches r09 only.
