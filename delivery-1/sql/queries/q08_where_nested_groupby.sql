-- Requirement: D1-Q-H (delivery 1, task 5h)
-- Combination: h. WHERE, Nested Query, GROUP BY
-- Title: Performances on above-average stages
-- Description: The nested query computes the average stage capacity; the WHERE keeps performances held on stages above that average; GROUP BY counts them per stage.
-- Evidence to collect: delivery-1/report/figures/q08_where_nested_groupby.png (screenshot of the result in SQLite Online / MySQL Workbench)
-- Local text output (not a screenshot): build/delivery-1/query-results/q08_where_nested_groupby.txt
SELECT StageCode, COUNT(*)
FROM Performance
WHERE StageCode IN (SELECT Code
                    FROM Stage
                    WHERE MaxCapacity > (SELECT AVG(MaxCapacity) FROM Stage))
GROUP BY StageCode;
