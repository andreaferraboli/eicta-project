# Text analysis (DRAFT)

> **Status: draft to be reviewed by the group.** It matches `diagrams/er-model.drawio` and `sql/schema.sql`. Assumption IDs (A-xx) refer to `docs/assumptions.md`. Copy the final version into `report/chapters/02-text-analysis.tex`.

## Entities

| Entity | Attributes (identifier underlined in the diagram) | Source in the text | Notes |
|---|---|---|---|
| Festival | **Name**, Location, StartDate, EndDate | "characterized by a name, a location, a start date, and an end date" | A-01 |
| Stage | **Code**, Name, MaxCapacity, LocationDescription | "an identification code, a name, a maximum capacity, and a description about its location" | A-02 |
| Performance | **PerformanceID**, Title, Genre, StartTime, EndTime | "a unique identifier, a title, a genre, and start/end times" | not artificial (A-03) |
| Artist | **StageName**, Country, MainGenre | "stage name, country, and main musical genre" | ISA parent (A-06) |
| Musician | FullName, Nationality, MainInstrument | "musicians should provide their full name, nationality and main instrument" | ISA child |
| Band | FormationYear | "bands must register their formation year" | ISA child |
| Stand | **Name**, Sponsor | "Each stand has a name, a sponsor" | A-04 |
| Product | **Name**, Price | "described by a name and a price" | ISA parent (A-08) |
| Food | ExpirationDate, Type | "food and drinks have an expiration date, and only food items have a type" | ISA child |
| Drink | ExpirationDate | same | ISA child |
| Merchandise | (none) | "merchandise" | ISA child |
| Ticket | **TicketID** (artificial), Type, Price, ValidityPeriod (ValidFrom, ValidTo) | "a type, a price, and a validity period" | A-03, A-13 |
| Person | **Email**, FullName, Phone | "full name, e-mail address, and phone number" | A-04 |
| Purchase | **PurchaseID** (artificial), Date, PaymentMethod | "the system should store the date and the payment method used" | A-11 |

## Relationships

Cardinalities are written as (min,max) on the side of the entity they refer to. Sample reading direction: *a Person makes (0,N) Purchases; a Purchase is made by (1,1) Person*.

| Relationship | Entities | Cardinalities | Source / assumption |
|---|---|---|---|
| Divided into | Festival - Stage | Festival (2,N), Stage (1,1) | "divided into multiple stages" (A-05) |
| Held at | Performance - Stage | Performance (1,1), Stage (0,N) | "At each stage, different musical performances can be held" |
| Given by | Performance - Artist | Performance (1,N), Artist (0,N) | "given by one or more artists" |
| Member of | Musician - Band | Musician (0,N), Band (2,N) | "bands (i.e., at least two musicians)" (A-07) |
| Hosts | Festival - Stand | Festival (0,N), Stand (1,1) | "festivals can host several stands" |
| Sells | Stand - Product | Stand (1,N), Product (0,N) | "can sell either of the three aforementioned products" (A-09) |
| Makes | Person - Purchase | Person (0,N), Purchase (1,1) | "A person can buy multiple tickets [...] purchase shop items" |
| Includes | Purchase - Ticket | Purchase (0,N), Ticket (1,1) | A-11 |
| Valid for | Ticket - Festival | Ticket (1,1), Festival (0,N) | "To enter a festival, people must buy tickets" (A-14) |
| Buys item (ternary) | Purchase - Stand - Product | (0,N) each | "purchase shop items during the festival" (A-12) |

## ISA hierarchies

| Parent | Children | Type | Translation |
|---|---|---|---|
| Artist | Musician, Band | total, exclusive (t, e) | parent + child tables, discriminator `ArtistType` |
| Product | Food, Drink, Merchandise | total, exclusive (t, e) | children collapsed into the parent with `Category` and CHECK constraints |

## Constraints not expressible in the ER diagram

- A band has at least two musicians (checked by `sql/checks.sql`).
- Performances happen within the dates of their festival; shop items are bought during the festival (A-15).
- A ticket's validity period is within the festival dates (A-13).
- An item bought at a stand must be sold by that stand (composite FK `PurchaseItem -> Sells`).
