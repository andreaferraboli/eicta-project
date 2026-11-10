# Mockaroo: generate, export and import the data

**Status: to complete.** Mockaroo has not been used by the scaffold. The data in `data/demo/` is a deterministic fallback for local tests and **is not evidence for task 4** (populate with Mockaroo, at least 25 tuples per table, screenshot of each table).

## Files

`schemas/<Table>.json` lists, for each table, the columns in the order of `sql/schema.sql` with the Mockaroo field type to choose in the UI. They are a checklist for building the schemas by hand in https://www.mockaroo.com/, not files tested against the Mockaroo import.

## Order (parents before children)

Festival, Stage, Artist, Musician, Band, BandMember, Performance, PerformanceArtist, Stand, Product, Sells, Person, Purchase, Ticket, PurchaseItem

## Procedure

1. For each table, create a schema in Mockaroo with the columns of `schemas/<Table>.json`. Set **rows >= 25**.
2. **Foreign keys**: after exporting a parent table as CSV, upload it as a Mockaroo *Dataset* (Datasets > Upload). In the child schema, use the field type **Dataset Column** pointing to the parent key. This keeps FKs valid.
3. **ISA Artist**: generate Artist with a `ArtistType` field (Custom List `musician,band`). Export Artist, then build Musician from the rows with type musician and Band from the rows with type band (Dataset Column + filter, or split the CSV).
4. **Constraints to respect** (checked by `python scripts/eicta.py sql-check`): festival EndDate >= StartDate, at least 2 stages per festival, at least 2 musicians per band, at least one artist per performance, Product: ExpirationDate only for food/drink and FoodType only for food, performances and ticket validity inside festival dates.
5. Export each schema as **SQL** (Format: SQL, table name = the table name, uncheck "include CREATE TABLE"). Save it as `delivery-1/data/mockaroo/<Table>.sql`.
6. Build and check:
   ```
   python scripts/eicta.py sql-build --source mockaroo
   python scripts/eicta.py sql-check
   python scripts/eicta.py sql-queries
   ```
   If a query returns no tuple on the Mockaroo data, adjust the condition (the PDF asks to try to have at least one tuple).
7. Take the screenshots required by task 4 in SQLite Online (or DB Browser for SQLite) with `SELECT * FROM <Table>;` and save them as `report/figures/data_<table>.png`.

Constraints that Mockaroo cannot express easily (bands with >= 2 members, dates inside the festival) can be fixed with a few `UPDATE` statements after import. Document any fix in the report.
