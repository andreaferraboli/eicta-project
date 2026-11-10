// Requirement: D2-QW-1
// Category: CREATE
// Title: Create a new festival with two stages
// Description: Creates a new festival and two stages connected to it.
// Evidence to collect: delivery-2/report/figures/w01_create_festival_with_stages.png (Neo4j Browser, graph or table view)
CREATE (f:Festival {name: 'Demo Winter Fest 2026', location: 'Trento',
                     startDate: date('2026-12-10'), endDate: date('2026-12-12')})
CREATE (:Stage {code: 'STW01A', name: 'Ice Dome', maxCapacity: 3000, locationDescription: 'inside the arena'})-[:PART_OF]->(f)
CREATE (:Stage {code: 'STW01B', name: 'Chalet Stage', maxCapacity: 900, locationDescription: 'near the slopes'})-[:PART_OF]->(f)
RETURN f.name AS created, COUNT { (:Stage)-[:PART_OF]->(f) } AS stages;
