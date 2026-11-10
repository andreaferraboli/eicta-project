// Requirement: D2-QW-4
// Category: UPDATE
// Title: Discount merchandise sold at the earliest festival
// Description: Applies a 20% discount to merchandise sold by stands of the earliest festival.
// Evidence to collect: delivery-2/report/figures/w04_update_merchandise_prices.png (Neo4j Browser, graph or table view)
MATCH (f:Festival) WITH f ORDER BY f.startDate LIMIT 1
MATCH (f)<-[:LOCATED_AT]-(:Stand)-[:SELLS]->(p:Merchandise)
WITH DISTINCT p
SET p.price = round(p.price * 0.8, 2)
RETURN p.name AS product, p.price AS newPrice;
