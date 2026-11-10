-- Requirement: D1-Q-E (delivery 1, task 5e)
-- Combination: e. WHERE, GROUP BY
-- Title: Tickets per type for festivals from July 2026
-- Description: Keeps only the tickets valid from 1 July 2026 onward and counts them per ticket type.
-- Evidence to collect: delivery-1/report/figures/q05_where_groupby.png (screenshot of the result in SQLite Online / MySQL Workbench)
-- Local text output (not a screenshot): build/delivery-1/query-results/q05_where_groupby.txt
SELECT Type, COUNT(*)
FROM Ticket
WHERE ValidFrom >= '2026-07-01'
GROUP BY Type;
