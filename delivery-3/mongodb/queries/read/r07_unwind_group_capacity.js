// Requirement: D3-QR-7
// Category: unwind + group by
// Title: Total stage capacity per festival
// Description: Unwinds the stages array and groups by festival, counting stages and summing their capacity.
// Evidence to collect: delivery-3/report/figures/r07_unwind_group_capacity.png (MongoDB Compass / Atlas / mongosh)
// Query as typed in mongosh (copy into the report):
/*
db.festivals.aggregate([
  { $unwind: "$stages" },
  { $group: { _id: "$name", stages: { $sum: 1 }, totalCapacity: { $sum: "$stages.maxCapacity" } } },
  { $sort: { totalCapacity: -1 } }
])
*/
printjson(db.festivals.aggregate([
  { $unwind: "$stages" },
  { $group: { _id: "$name", stages: { $sum: 1 }, totalCapacity: { $sum: "$stages.maxCapacity" } } },
  { $sort: { totalCapacity: -1 } }
]).toArray());
