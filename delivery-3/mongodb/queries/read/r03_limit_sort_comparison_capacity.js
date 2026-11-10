// Requirement: D3-QR-3
// Category: limit + sort + comparison query operators (1/2)
// Title: First five festivals with a big stage
// Description: Festivals having at least one stage with capacity >= 5000 ($gte), sorted by start date, first five.
// Evidence to collect: delivery-3/report/figures/r03_limit_sort_comparison_capacity.png (MongoDB Compass / Atlas / mongosh)
// Query as typed in mongosh (copy into the report):
/*
db.festivals.find(
  { "stages.maxCapacity": { $gte: 5000 } },
  { _id: 0, name: 1, startDate: 1 }
).sort({ startDate: 1 }).limit(5)
*/
printjson(db.festivals.find(
  { "stages.maxCapacity": { $gte: 5000 } },
  { _id: 0, name: 1, startDate: 1 }
).sort({ startDate: 1 }).limit(5).toArray());
