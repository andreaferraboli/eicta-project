// Requirement: D2-QR-8
// Category: 3+ nodes in MATCH + conditions + multiple WITH (2/2)
// Title: Ticket revenue per festival
// Description: Revenue from regular and VIP tickets per festival; a second WITH derives the average ticket price and keeps festivals above 100 of revenue.
// Evidence to collect: delivery-2/report/figures/r08_match3_cond_multiwith_ticket_revenue.png (Neo4j Browser, graph or table view)
MATCH (pe:Person)-[:MADE]->(pu:Purchase)-[:INCLUDES]->(t:Ticket)-[:VALID_FOR]->(f:Festival)
WHERE t.type IN ['regular', 'VIP']
WITH f, sum(t.price) AS revenue, count(t) AS tickets, count(DISTINCT pe) AS buyers
WITH f, revenue, tickets, buyers, round(revenue / tickets, 2) AS avgTicketPrice
WHERE revenue > 100
RETURN f.name AS festival, tickets, buyers, revenue, avgTicketPrice
ORDER BY revenue DESC;
