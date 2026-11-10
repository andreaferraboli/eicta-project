// Requirement: D2-QR-5
// Category: 2 nodes in MATCH + conditions + one WITH (1/2)
// Title: Artists often playing outside their main genre
// Description: Counts the performances whose genre differs from the main genre of the artist, keeping artists with at least 2 of them.
// Evidence to collect: delivery-2/report/figures/r05_match2_cond_with_off_genre.png (Neo4j Browser, graph or table view)
MATCH (a:Artist)-[:PERFORMS_IN]->(p:Performance)
WHERE p.genre <> a.mainGenre
WITH a, count(p) AS offGenre
WHERE offGenre >= 2
RETURN a.stageName AS artist, a.mainGenre AS mainGenre, offGenre
ORDER BY offGenre DESC, artist;
