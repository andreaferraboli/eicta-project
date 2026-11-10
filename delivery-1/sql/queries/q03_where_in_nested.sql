-- Requirement: D1-Q-C (delivery 1, task 5c)
-- Combination: c. WHERE, IN, Nested Query
-- Title: People who bought at least one VIP ticket
-- Description: The inner query finds the purchases containing a VIP ticket; the outer queries keep the people who made one of those purchases.
-- Evidence to collect: delivery-1/report/figures/q03_where_in_nested.png (screenshot of the result in SQLite Online / MySQL Workbench)
-- Local text output (not a screenshot): build/delivery-1/query-results/q03_where_in_nested.txt
SELECT FullName, Email
FROM Person
WHERE Email IN (SELECT PersonEmail
                FROM Purchase
                WHERE PurchaseID IN (SELECT PurchaseID
                                     FROM Ticket
                                     WHERE Type = 'VIP'));
