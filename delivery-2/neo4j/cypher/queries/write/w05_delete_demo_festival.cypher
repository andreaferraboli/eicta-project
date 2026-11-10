// Requirement: D2-QW-5
// Category: DELETE
// Title: Delete the demo winter festival
// Description: Deletes the festival created by w01 with its stages and the performance created by w02 (DETACH DELETE removes the relationships too).
// Evidence to collect: delivery-2/report/figures/w05_delete_demo_festival.png (Neo4j Browser, graph or table view)
MATCH (f:Festival {name: 'Demo Winter Fest 2026'})<-[:PART_OF]-(s:Stage)
OPTIONAL MATCH (p:Performance)-[:HELD_AT]->(s)
WITH f, collect(DISTINCT s) AS stages, collect(DISTINCT p) AS performances
FOREACH (n IN performances | DETACH DELETE n)
FOREACH (n IN stages | DETACH DELETE n)
DETACH DELETE f
RETURN size(stages) AS deletedStages, size(performances) AS deletedPerformances;
