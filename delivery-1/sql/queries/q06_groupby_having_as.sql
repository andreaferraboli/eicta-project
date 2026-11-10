-- Requirement: D1-Q-F (delivery 1, task 5f)
-- Combination: f. GROUP BY, HAVING, AS
-- Title: Most programmed genres
-- Description: Counts performances per genre and keeps only the genres with at least 10 performances.
-- Evidence to collect: delivery-1/report/figures/q06_groupby_having_as.png (screenshot of the result in SQLite Online / MySQL Workbench)
-- Local text output (not a screenshot): build/delivery-1/query-results/q06_groupby_having_as.txt
SELECT Genre, COUNT(*) AS NumPerformances
FROM Performance
GROUP BY Genre
HAVING COUNT(*) >= 10;
