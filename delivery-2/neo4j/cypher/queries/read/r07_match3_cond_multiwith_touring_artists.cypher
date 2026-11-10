// Requirement: D2-QR-7
// Category: 3+ nodes in MATCH + conditions + multiple WITH (1/2)
// Title: Touring artists across summer festivals
// Description: Artists performing at 2 or more distinct festivals starting from June 2026; the second WITH ranks them and keeps the top 5.
// Evidence to collect: delivery-2/report/figures/r07_match3_cond_multiwith_touring_artists.png (Neo4j Browser, graph or table view)
MATCH (a:Artist)-[:PERFORMS_IN]->(p:Performance)-[:HELD_AT]->(s:Stage)-[:PART_OF]->(f:Festival)
WHERE f.startDate >= date('2026-06-01')
WITH a, count(DISTINCT f) AS festivals, collect(DISTINCT f.location) AS cities
WHERE festivals >= 2
WITH a, festivals, cities
ORDER BY festivals DESC, a.stageName
LIMIT 5
RETURN a.stageName AS artist, festivals, cities;
