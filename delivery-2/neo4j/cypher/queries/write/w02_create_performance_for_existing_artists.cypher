// Requirement: D2-QW-2
// Category: CREATE
// Title: Schedule a performance with existing artists
// Description: Creates a performance on the new Ice Dome stage and links two existing artists to it.
// Evidence to collect: delivery-2/report/figures/w02_create_performance_for_existing_artists.png (Neo4j Browser, graph or table view)
MATCH (s:Stage {code: 'STW01A'})
MATCH (a:Artist) WITH s, a ORDER BY a.stageName LIMIT 2
WITH s, collect(a) AS artists
CREATE (p:Performance {performanceId: 9001, title: 'Winter Opening', genre: 'electronic',
                       startTime: localdatetime('2026-12-10T21:00'), endTime: localdatetime('2026-12-10T22:30')})-[:HELD_AT]->(s)
FOREACH (a IN artists | CREATE (a)-[:PERFORMS_IN]->(p))
RETURN p.title AS performance, [a IN artists | a.stageName] AS artists;
