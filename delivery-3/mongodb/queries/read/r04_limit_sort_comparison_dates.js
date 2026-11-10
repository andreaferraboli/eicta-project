// Requirement: D3-QR-4
// Category: limit + sort + comparison query operators (2/2)
// Title: Last three early-summer festivals by name
// Description: Festivals starting before 1 August 2026 ($lt) and not in Torino ($ne), sorted by name descending, first three.
// Evidence to collect: delivery-3/report/figures/r04_limit_sort_comparison_dates.png (MongoDB Compass / Atlas / mongosh)
// Query as typed in mongosh (copy into the report):
/*
db.festivals.find(
  { startDate: { $lt: ISODate("2026-08-01T00:00:00Z") }, location: { $ne: "Torino" } },
  { _id: 0, name: 1, location: 1, startDate: 1 }
).sort({ name: -1 }).limit(3)
*/
printjson(db.festivals.find(
  { startDate: { $lt: ISODate("2026-08-01T00:00:00Z") }, location: { $ne: "Torino" } },
  { _id: 0, name: 1, location: 1, startDate: 1 }
).sort({ name: -1 }).limit(3).toArray());
