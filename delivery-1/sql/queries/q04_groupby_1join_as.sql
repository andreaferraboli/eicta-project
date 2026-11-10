-- Requirement: D1-Q-D (delivery 1, task 5d)
-- Combination: d. GROUP BY, 1 JOIN, AS
-- Title: Stages and total capacity per festival
-- Description: Joins festivals with their stages and groups by festival, counting the stages and summing their capacity. AS renames tables and computed columns.
-- Evidence to collect: delivery-1/report/figures/q04_groupby_1join_as.png (screenshot of the result in SQLite Online / MySQL Workbench)
-- Local text output (not a screenshot): build/delivery-1/query-results/q04_groupby_1join_as.txt
SELECT f.Name AS Festival, COUNT(s.Code) AS NumStages, SUM(s.MaxCapacity) AS TotalCapacity
FROM Festival AS f
JOIN Stage AS s ON s.FestivalName = f.Name
GROUP BY f.Name;
