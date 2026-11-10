// Requirement: D2-QR-10
// Category: shortest path
// Title: Shortest connection between two artists
// Description: Picks the first musician and the last band by stage name and computes the shortest path between them through performances and band memberships.
// Evidence to collect: delivery-2/report/figures/r10_shortest_path_between_artists.png (Neo4j Browser, graph or table view)
MATCH (a:Musician) WITH a ORDER BY a.stageName LIMIT 1
MATCH (b:Band) WITH a, b ORDER BY b.stageName DESC LIMIT 1
MATCH path = shortestPath((a)-[:PERFORMS_IN|MEMBER_OF*..12]-(b))
RETURN a.stageName AS fromArtist, b.stageName AS toArtist, length(path) AS hops,
       [n IN nodes(path) | coalesce(n.stageName, n.title)] AS via;
