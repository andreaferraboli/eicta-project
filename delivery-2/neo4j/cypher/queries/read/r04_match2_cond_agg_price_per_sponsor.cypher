// Requirement: D2-QR-4
// Category: 2 nodes in MATCH + conditions + aggregation, no WITH (2/2)
// Title: Average food and drink price per sponsor
// Description: For food and drink products, average price and number of products sold by stands, grouped by stand sponsor.
// Evidence to collect: delivery-2/report/figures/r04_match2_cond_agg_price_per_sponsor.png (Neo4j Browser, graph or table view)
MATCH (st:Stand)-[:SELLS]->(p:Product)
WHERE p:Food OR p:Drink
RETURN st.sponsor AS sponsor, round(avg(p.price), 2) AS avgPrice, count(p) AS products
ORDER BY avgPrice DESC;
