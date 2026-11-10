-- Requirement: D1-Q-A (delivery 1, task 5a)
-- Combination: a. WHERE
-- Title: Large-capacity stages
-- Description: Lists the stages that can host at least 5000 people, with the festival they belong to. The WHERE clause filters on MaxCapacity.
-- Evidence to collect: delivery-1/report/figures/q01_where.png (screenshot of the result in SQLite Online / MySQL Workbench)
-- Local text output (not a screenshot): build/delivery-1/query-results/q01_where.txt
SELECT Code, Name, MaxCapacity, FestivalName
FROM Stage
WHERE MaxCapacity >= 5000;
