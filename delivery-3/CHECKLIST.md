# Delivery 3: evidence checklist

Nothing in this list has been collected yet. Text outputs in `build/` are local test results, **not** screenshots of the tools.

## Work to complete

- [ ] Confirm the document structure (`mongodb/schema.md`) and the 5+ entities
- [ ] Rebuild from the final delivery-1 data: `mongo-transform`, `mongo-seed`, `mongo-check`
- [ ] If Atlas is required: import `build/delivery-3/mongo-seed/festivals.json` into Atlas (not done by the scaffold)
- [ ] Run the queries in Compass / Atlas / mongosh and take the screenshots; then `mongo-seed` again
- [ ] Web static: replace demo content, take desktop and mobile screenshots
- [ ] Web auth: create the users table on https://sqliteonline.com/ with `web-auth/db/users.sql`, export `db/users.db`
- [ ] Web auth: try the client-side validation by hand and take screenshots (success, failure)
- [ ] Report: at most 30 pages after adding all screenshots

## Deliverables (zip)

- [ ] MongoDB dump: `python scripts/eicta.py mongo-dump` -> `build/delivery-3/mongo-dump/euphoric_events/`
- [ ] One folder per web task: `web-static/`, `web-auth/` (`node_modules` excluded by `package`)
- [ ] Report PDF (<= 30 pages)
- [ ] Folder of high-resolution images
- [ ] `python scripts/eicta.py package 3` shows no MISSING item

## Figures expected by the report (20)

Save each file in `report/figures/` with exactly this name: the report includes it automatically.

| Done | File | Caption | Chapter |
|---|---|---|---|
| [ ] | `mongo-structure.png` | Containment hierarchy of the festivals collection. | 01-document-structure.tex |
| [ ] | `w01_insert_festival.png` | Result of the query "Insert a new festival document". | 02-queries.tex |
| [ ] | `w02_update_stage_capacity.png` | Result of the query "Increase capacity of the Chalet Stage". | 02-queries.tex |
| [ ] | `w03_update_merchandise_prices.png` | Result of the query "Discount all merchandise by 10\%". | 02-queries.tex |
| [ ] | `w04_push_product.png` | Result of the query "Add a product to a stand". | 02-queries.tex |
| [ ] | `w05_delete_festival.png` | Result of the query "Delete the demo festival". | 02-queries.tex |
| [ ] | `r01_projection_logical_or.png` | Result of the query "Festivals in Milano or Roma". | 02-queries.tex |
| [ ] | `r02_projection_logical_and_nor.png` | Result of the query "Festivals sponsored by Blue Bank outside the south". | 02-queries.tex |
| [ ] | `r03_limit_sort_comparison_capacity.png` | Result of the query "First five festivals with a big stage". | 02-queries.tex |
| [ ] | `r04_limit_sort_comparison_dates.png` | Result of the query "Last three early-summer festivals by name". | 02-queries.tex |
| [ ] | `r05_element_operators.png` | Result of the query "Festivals hosting bands and selling typed food". | 02-queries.tex |
| [ ] | `r06_group_festivals_per_city.png` | Result of the query "Festivals per city". | 02-queries.tex |
| [ ] | `r07_unwind_group_capacity.png` | Result of the query "Total stage capacity per festival". | 02-queries.tex |
| [ ] | `r08_unwind_group_filter_genres.png` | Result of the query "Genres with at least 10 performances". | 02-queries.tex |
| [ ] | `r09_array_conditions_separately.png` | Result of the query "Festivals with a Main Stage and some small stage". | 02-queries.tex |
| [ ] | `r10_array_conditions_elemmatch.png` | Result of the query "Festivals whose Main Stage is small". | 02-queries.tex |
| [ ] | `web-static-desktop.png` | Promotional page, desktop view. | 03-web-static.tex |
| [ ] | `web-static-mobile.png` | Promotional page, mobile view. | 03-web-static.tex |
| [ ] | `web-auth-signup.png` | Successful sign-in with welcome message. | 04-web-auth.tex |
| [ ] | `web-auth-login-error.png` | Failed log-in attempt handled by the server. | 04-web-auth.tex |
