-- Requirement: D1-Q-I (delivery 1, task 5i)
-- Combination: i. WHERE, GROUP BY, HAVING, 1 JOIN
-- Title: Large bands formed before 2000
-- Description: Joins bands with their members, keeps bands formed before 2000 and returns those with at least 3 members.
-- Evidence to collect: delivery-1/report/figures/q09_where_groupby_having_1join.png (screenshot of the result in SQLite Online / MySQL Workbench)
-- Local text output (not a screenshot): build/delivery-1/query-results/q09_where_groupby_having_1join.txt
SELECT b.StageName, b.FormationYear, COUNT(*)
FROM Band b
JOIN BandMember m ON m.BandName = b.StageName
WHERE b.FormationYear < 2000
GROUP BY b.StageName, b.FormationYear
HAVING COUNT(*) >= 3;
