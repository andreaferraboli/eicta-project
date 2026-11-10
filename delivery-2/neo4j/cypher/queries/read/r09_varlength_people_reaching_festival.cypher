// Requirement: D2-QR-9
// Category: variable-length path in MATCH + conditions
// Title: People connected to festivals in Milano or Roma
// Description: Follows directed paths of 1 to 3 relationships from a person to a festival (Person-MADE-Purchase-INCLUDES-Ticket-VALID_FOR-Festival) for festivals located in Milano or Roma.
// Evidence to collect: delivery-2/report/figures/r09_varlength_people_reaching_festival.png (Neo4j Browser, graph or table view)
MATCH path = (pe:Person)-[*1..3]->(f:Festival)
WHERE f.location IN ['Milano', 'Roma']
RETURN DISTINCT pe.fullName AS person, f.name AS festival, length(path) AS hops
ORDER BY festival, person;
