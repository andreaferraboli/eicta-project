// Requirement: D2-QW-3
// Category: UPDATE
// Title: Increase capacity of small stages
// Description: Raises by 10% the capacity of stages with fewer than 1000 places.
// Evidence to collect: delivery-2/report/figures/w03_update_stage_capacity.png (Neo4j Browser, graph or table view)
MATCH (s:Stage)
WHERE s.maxCapacity < 1000
SET s.maxCapacity = toInteger(s.maxCapacity * 1.1)
RETURN s.code AS stage, s.maxCapacity AS newCapacity
ORDER BY stage;
