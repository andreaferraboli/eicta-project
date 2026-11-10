# Delivery 2: evidence checklist

Nothing in this list has been collected yet. Text outputs in `build/` are local test results, **not** screenshots of the tools.

## Work to complete

- [ ] Choose the final set of entities (>= 8, with at least one ISA) and update `neo4j/schema.md`
- [ ] Rebuild from the final delivery-1 data: `export-csv`, `up`, `neo4j-load`, `neo4j-check`
- [ ] Run the queries in Neo4j Browser (http://127.0.0.1:7474) and take the screenshots
- [ ] Reload the seed after the write queries: `python scripts/eicta.py neo4j-load`
- [ ] Review both BPMN diagrams in https://demo.bpmn.io/, export the images
- [ ] Approve or replace the Euphoric Events process (`bpmn/euphoric-events-process.md`)
- [ ] Report: at most 30 pages after adding all screenshots

## Deliverables (zip)

- [ ] Neo4j dump: `python scripts/eicta.py neo4j-dump` -> `build/delivery-2/neo4j-dump/neo4j.dump`
- [ ] Report PDF (<= 30 pages)
- [ ] Folder of high-resolution images
- [ ] `python scripts/eicta.py package 2` shows no MISSING item

## Figures expected by the report (18)

Save each file in `report/figures/` with exactly this name: the report includes it automatically.

| Done | File | Caption | Chapter |
|---|---|---|---|
| [ ] | `graph-schema.png` | Neo4j schema: node types, relationship types and properties. | 01-graph-schema.tex |
| [ ] | `w01_create_festival_with_stages.png` | Result of the query "Create a new festival with two stages". | 03-queries.tex |
| [ ] | `w02_create_performance_for_existing_artists.png` | Result of the query "Schedule a performance with existing artists". | 03-queries.tex |
| [ ] | `w03_update_stage_capacity.png` | Result of the query "Increase capacity of small stages". | 03-queries.tex |
| [ ] | `w04_update_merchandise_prices.png` | Result of the query "Discount merchandise sold at the earliest festival". | 03-queries.tex |
| [ ] | `w05_delete_demo_festival.png` | Result of the query "Delete the demo winter festival". | 03-queries.tex |
| [ ] | `r01_match2_cond_large_stages.png` | Result of the query "Large stages of summer festivals". | 03-queries.tex |
| [ ] | `r02_match2_cond_band_members.png` | Result of the query "Guitarists and drummers in bands formed before 2000". | 03-queries.tex |
| [ ] | `r03_match2_cond_agg_genre_per_stage.png` | Result of the query "Rock and metal performances per stage". | 03-queries.tex |
| [ ] | `r04_match2_cond_agg_price_per_sponsor.png` | Result of the query "Average food and drink price per sponsor". | 03-queries.tex |
| [ ] | `r05_match2_cond_with_off_genre.png` | Result of the query "Artists often playing outside their main genre". | 03-queries.tex |
| [ ] | `r06_match2_cond_with_card_buyers.png` | Result of the query "People paying electronically more than once". | 03-queries.tex |
| [ ] | `r07_match3_cond_multiwith_touring_artists.png` | Result of the query "Touring artists across summer festivals". | 03-queries.tex |
| [ ] | `r08_match3_cond_multiwith_ticket_revenue.png` | Result of the query "Ticket revenue per festival". | 03-queries.tex |
| [ ] | `r09_varlength_people_reaching_festival.png` | Result of the query "People connected to festivals in Milano or Roma". | 03-queries.tex |
| [ ] | `r10_shortest_path_between_artists.png` | Result of the query "Shortest connection between two artists". | 03-queries.tex |
| [ ] | `bpmn-store-and-store.png` | BPMN diagram of the Store&Store order process. | 04-bpmn-store.tex |
| [ ] | `bpmn-euphoric-events.png` | BPMN diagram of the Euphoric Events artist booking process. | 05-bpmn-euphoric.tex |
