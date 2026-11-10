-- Requirement: D1-Q-B (delivery 1, task 5b)
-- Combination: b. WHERE, LIMIT, LIKE
-- Title: Cheapest vegetarian or vegan food items
-- Description: Selects food products whose type starts with 'veg' (vegetarian, vegan) using LIKE, and returns only the first five by price with LIMIT. ORDER BY is added only to make LIMIT deterministic.
-- Evidence to collect: delivery-1/report/figures/q02_where_limit_like.png (screenshot of the result in SQLite Online / MySQL Workbench)
-- Local text output (not a screenshot): build/delivery-1/query-results/q02_where_limit_like.txt
SELECT Name, Price, FoodType
FROM Product
WHERE Category = 'food' AND FoodType LIKE 'veg%'
ORDER BY Price
LIMIT 5;
