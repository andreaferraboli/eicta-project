// Requirement: D3-QR-6
// Category: group operator
// Title: Festivals per city
// Description: Groups the festivals by location, counting them and taking the earliest start date.
// Evidence to collect: delivery-3/report/figures/r06_group_festivals_per_city.png (MongoDB Compass / Atlas / mongosh)
// Query as typed in mongosh (copy into the report):
/*
db.festivals.aggregate([
  { $group: { _id: "$location", festivals: { $sum: 1 }, firstStart: { $min: "$startDate" } } },
  { $sort: { _id: 1 } }
])
*/
printjson(db.festivals.aggregate([
  { $group: { _id: "$location", festivals: { $sum: 1 }, firstStart: { $min: "$startDate" } } },
  { $sort: { _id: 1 } }
]).toArray());
