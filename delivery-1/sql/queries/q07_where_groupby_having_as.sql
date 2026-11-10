-- Requirement: D1-Q-G (delivery 1, task 5g)
-- Combination: g. WHERE, GROUP BY, HAVING, AS
-- Title: Popular payment methods from June 2026
-- Description: Considers purchases made from 1 June 2026, groups them by payment method and keeps the methods used more than 5 times.
-- Evidence to collect: delivery-1/report/figures/q07_where_groupby_having_as.png (screenshot of the result in SQLite Online / MySQL Workbench)
-- Local text output (not a screenshot): build/delivery-1/query-results/q07_where_groupby_having_as.txt
SELECT PaymentMethod, COUNT(*) AS NumPurchases
FROM Purchase
WHERE PurchaseDate >= '2026-06-01'
GROUP BY PaymentMethod
HAVING COUNT(*) > 5;
