-- Requirement: D1-Q-J (delivery 1, task 5j)
-- Combination: j. WHERE, GROUP BY, HAVING, 2 JOINs
-- Title: Stands selling the most food and drinks
-- Description: Joins stands with the items sold and with the product catalogue, keeps food and drink items and returns the stands with at least 2 such items sold.
-- Evidence to collect: delivery-1/report/figures/q10_where_groupby_having_2joins.png (screenshot of the result in SQLite Online / MySQL Workbench)
-- Local text output (not a screenshot): build/delivery-1/query-results/q10_where_groupby_having_2joins.txt
SELECT st.Name, st.Sponsor, COUNT(*)
FROM Stand st
JOIN PurchaseItem pi ON pi.StandName = st.Name
JOIN Product p ON p.Name = pi.ProductName
WHERE p.Category IN ('food', 'drink')
GROUP BY st.Name, st.Sponsor
HAVING COUNT(*) >= 2;
