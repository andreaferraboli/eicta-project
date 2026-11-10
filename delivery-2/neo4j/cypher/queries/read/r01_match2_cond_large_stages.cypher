// Requirement: D2-QR-1
// Category: 2 nodes in MATCH + conditions (1/2)
// Title: Large stages of summer festivals
// Description: Stages with capacity of at least 5000 that belong to festivals starting in June 2026 or later.
// Evidence to collect: delivery-2/report/figures/r01_match2_cond_large_stages.png (Neo4j Browser, graph or table view)
MATCH (s:Stage)-[:PART_OF]->(f:Festival)
WHERE s.maxCapacity >= 5000 AND f.startDate >= date('2026-06-01')
RETURN f.name AS festival, f.startDate AS start, s.code AS stage, s.name AS stageName, s.maxCapacity AS capacity
ORDER BY start, stage;
