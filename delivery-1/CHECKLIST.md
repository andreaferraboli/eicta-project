# Delivery 1: evidence checklist

Nothing in this list has been collected yet. Text outputs in `build/` are local test results, **not** screenshots of the tools.

## Work to complete

- [ ] Register the group (link in `ASSIGNMENT.md`; date in the PDF: October 9, 23:59)
- [ ] Review the draft ER model (`diagrams/er-model.drawio`) and the assumptions (`docs/assumptions.md`)
- [ ] Review the logical model (`analysis/logical-model.md`) and `sql/schema.sql`
- [ ] Generate the data **with Mockaroo** (`mockaroo/README.md`), save the exports in `data/mockaroo/`
- [ ] `python scripts/eicta.py sql-build --source mockaroo` then `sql-check` (>= 25 tuples per table, all constraints)
- [ ] `python scripts/eicta.py sql-queries`: every query returns at least one tuple on the Mockaroo data
- [ ] Write descriptions in the report chapters, remove every `TODO`
- [ ] Replace the provisional LaTeX template with the official one (or keep and declare it)

## Deliverables (zip)

- [ ] Self-contained dump: `build/delivery-1/euphoric_events.db` (built from Mockaroo data, not demo data)
- [ ] Report PDF with front page, index, introduction, text analysis, one chapter per request, captions
- [ ] Folder of high-resolution images (`report/figures/`)
- [ ] `python scripts/eicta.py package 1` shows no MISSING item

## Figures expected by the report (27)

Save each file in `report/figures/` with exactly this name: the report includes it automatically.

| Done | File | Caption | Chapter |
|---|---|---|---|
| [ ] | `er-model.png` | ER diagram (exported from delivery-1/diagrams/er-model.drawio). | 03-er-model.tex |
| [ ] | `logical-model.png` | Logical model. | 04-logical-model.tex |
| [ ] | `data_festival.png` | Data inserted in table Festival (Mockaroo). | 06-population.tex |
| [ ] | `data_stage.png` | Data inserted in table Stage (Mockaroo). | 06-population.tex |
| [ ] | `data_artist.png` | Data inserted in table Artist (Mockaroo). | 06-population.tex |
| [ ] | `data_musician.png` | Data inserted in table Musician (Mockaroo). | 06-population.tex |
| [ ] | `data_band.png` | Data inserted in table Band (Mockaroo). | 06-population.tex |
| [ ] | `data_bandmember.png` | Data inserted in table BandMember (Mockaroo). | 06-population.tex |
| [ ] | `data_performance.png` | Data inserted in table Performance (Mockaroo). | 06-population.tex |
| [ ] | `data_performanceartist.png` | Data inserted in table PerformanceArtist (Mockaroo). | 06-population.tex |
| [ ] | `data_stand.png` | Data inserted in table Stand (Mockaroo). | 06-population.tex |
| [ ] | `data_product.png` | Data inserted in table Product (Mockaroo). | 06-population.tex |
| [ ] | `data_sells.png` | Data inserted in table Sells (Mockaroo). | 06-population.tex |
| [ ] | `data_person.png` | Data inserted in table Person (Mockaroo). | 06-population.tex |
| [ ] | `data_purchase.png` | Data inserted in table Purchase (Mockaroo). | 06-population.tex |
| [ ] | `data_ticket.png` | Data inserted in table Ticket (Mockaroo). | 06-population.tex |
| [ ] | `data_purchaseitem.png` | Data inserted in table PurchaseItem (Mockaroo). | 06-population.tex |
| [ ] | `q01_where.png` | Result of the query "Large-capacity stages". | 07-queries.tex |
| [ ] | `q02_where_limit_like.png` | Result of the query "Cheapest vegetarian or vegan food items". | 07-queries.tex |
| [ ] | `q03_where_in_nested.png` | Result of the query "People who bought at least one VIP ticket". | 07-queries.tex |
| [ ] | `q04_groupby_1join_as.png` | Result of the query "Stages and total capacity per festival". | 07-queries.tex |
| [ ] | `q05_where_groupby.png` | Result of the query "Tickets per type for festivals from July 2026". | 07-queries.tex |
| [ ] | `q06_groupby_having_as.png` | Result of the query "Most programmed genres". | 07-queries.tex |
| [ ] | `q07_where_groupby_having_as.png` | Result of the query "Popular payment methods from June 2026". | 07-queries.tex |
| [ ] | `q08_where_nested_groupby.png` | Result of the query "Performances on above-average stages". | 07-queries.tex |
| [ ] | `q09_where_groupby_having_1join.png` | Result of the query "Large bands formed before 2000". | 07-queries.tex |
| [ ] | `q10_where_groupby_having_2joins.png` | Result of the query "Stands selling the most food and drinks". | 07-queries.tex |
