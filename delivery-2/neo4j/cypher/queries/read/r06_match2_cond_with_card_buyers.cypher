// Requirement: D2-QR-6
// Category: 2 nodes in MATCH + conditions + one WITH (2/2)
// Title: People paying electronically more than once
// Description: People with at least 2 purchases paid with a method other than cash.
// Evidence to collect: delivery-2/report/figures/r06_match2_cond_with_card_buyers.png (Neo4j Browser, graph or table view)
MATCH (pe:Person)-[:MADE]->(pu:Purchase)
WHERE pu.paymentMethod <> 'cash'
WITH pe, count(pu) AS electronicPurchases
WHERE electronicPurchases >= 2
RETURN pe.fullName AS person, pe.email AS email, electronicPurchases
ORDER BY person;
