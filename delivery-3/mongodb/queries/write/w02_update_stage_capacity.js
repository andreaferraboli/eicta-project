// Requirement: D3-QW-2
// Category: update
// Title: Increase capacity of the Chalet Stage
// Description: Uses an array filter to update only the stage with code STW01B inside the new festival.
// Evidence to collect: delivery-3/report/figures/w02_update_stage_capacity.png (MongoDB Compass / Atlas / mongosh)
// Query as typed in mongosh (copy into the report):
/*
printjson(db.festivals.updateOne(
  { _id: "Demo Winter Fest 2026" },
  { $set: { "stages.$[s].maxCapacity": 1200 } },
  { arrayFilters: [{ "s.code": "STW01B" }] }
));
*/
printjson(db.festivals.updateOne(
  { _id: "Demo Winter Fest 2026" },
  { $set: { "stages.$[s].maxCapacity": 1200 } },
  { arrayFilters: [{ "s.code": "STW01B" }] }
));
