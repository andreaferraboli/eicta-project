// Requirement: D2-QR-3
// Category: 2 nodes in MATCH + conditions + aggregation, no WITH (1/2)
// Title: Rock and metal performances per stage
// Description: Counts, for each stage, the performances of genre rock or metal.
// Evidence to collect: delivery-2/report/figures/r03_match2_cond_agg_genre_per_stage.png (Neo4j Browser, graph or table view)
MATCH (p:Performance)-[:HELD_AT]->(s:Stage)
WHERE p.genre IN ['rock', 'metal']
RETURN s.code AS stage, s.name AS stageName, count(p) AS performances
ORDER BY performances DESC, stage;
