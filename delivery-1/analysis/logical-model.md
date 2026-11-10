# Logical model (DRAFT)

> Derived from the draft ER model. Notation: <u>underlined</u> = primary key, *italic* = foreign key (target in brackets). Same content as `sql/schema.sql`.

| Table | Attributes | Primary key | Foreign keys | From |
|---|---|---|---|---|
| Festival | <u>Name</u>, Location, StartDate, EndDate | Name | - | entity |
| Stage | <u>Code</u>, Name, MaxCapacity, LocationDescription, *FestivalName* | Code | FestivalName -> Festival(Name) | entity + Divided into (1,1 side) |
| Performance | <u>PerformanceID</u>, Title, Genre, StartTime, EndTime, *StageCode* | PerformanceID | StageCode -> Stage(Code) | entity + Held at |
| Artist | <u>StageName</u>, Country, MainGenre, ArtistType | StageName | - | ISA parent |
| Musician | <u>*StageName*</u>, FullName, Nationality, MainInstrument | StageName | StageName -> Artist(StageName) | ISA child |
| Band | <u>*StageName*</u>, FormationYear | StageName | StageName -> Artist(StageName) | ISA child |
| BandMember | <u>*BandName*</u>, <u>*MusicianName*</u> | (BandName, MusicianName) | BandName -> Band, MusicianName -> Musician | Member of (N:M) |
| PerformanceArtist | <u>*PerformanceID*</u>, <u>*ArtistStageName*</u> | (PerformanceID, ArtistStageName) | -> Performance, -> Artist | Given by (N:M) |
| Stand | <u>Name</u>, Sponsor, *FestivalName* | Name | FestivalName -> Festival(Name) | entity + Hosts |
| Product | <u>Name</u>, Price, Category, ExpirationDate, FoodType | Name | - | ISA collapsed into parent |
| Sells | <u>*StandName*</u>, <u>*ProductName*</u> | (StandName, ProductName) | -> Stand, -> Product | Sells (N:M) |
| Person | <u>Email</u>, FullName, Phone | Email | - | entity |
| Purchase | <u>PurchaseID</u>, PurchaseDate, PaymentMethod, *PersonEmail* | PurchaseID | PersonEmail -> Person(Email) | entity + Makes |
| Ticket | <u>TicketID</u>, Type, Price, ValidFrom, ValidTo, *FestivalName*, *PurchaseID* | TicketID | -> Festival, -> Purchase | entity + Valid for + Includes |
| PurchaseItem | <u>*PurchaseID*</u>, <u>*StandName*</u>, <u>*ProductName*</u> | all three | PurchaseID -> Purchase; (StandName, ProductName) -> Sells | Buys item (ternary) |

## Translation choices

- **1:N relationships** become a foreign key on the (1,1) side (Stage, Performance, Stand, Purchase, Ticket).
- **N:M relationships** become bridge tables (BandMember, PerformanceArtist, Sells).
- **Ternary Buys item** becomes PurchaseItem; its FK to Sells guarantees that the stand actually sells the product.
- **ISA Artist**: parent and child tables, so that Musician can be referenced by BandMember. `ArtistType` makes the total/exclusive constraint checkable.
- **ISA Product**: collapsed into the parent, because Merchandise has no attributes and Food/Drink share ExpirationDate. CHECK constraints enforce: ExpirationDate present only for food and drink, FoodType present only for food.
- **Composite attribute ValidityPeriod** is split into ValidFrom and ValidTo.
- All FKs use `ON UPDATE CASCADE ON DELETE CASCADE` (review: a stricter `RESTRICT` may be preferred for Person/Purchase).
