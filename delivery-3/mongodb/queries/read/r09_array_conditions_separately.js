// Requirement: D3-QR-9
// Category: two conditions evaluated separately on array sub-documents
// Title: Festivals with a Main Stage and some small stage
// Description: Two conditions on the stages array WITHOUT $elemMatch: one stage can be named Main Stage and a DIFFERENT stage can have capacity below 1000.
// Evidence to collect: delivery-3/report/figures/r09_array_conditions_separately.png (MongoDB Compass / Atlas / mongosh)
// Query as typed in mongosh (copy into the report):
/*
db.festivals.find(
  { "stages.name": "Main Stage", "stages.maxCapacity": { $lt: 1000 } },
  { _id: 0, name: 1, "stages.name": 1, "stages.maxCapacity": 1 }
)
*/
printjson(db.festivals.find(
  { "stages.name": "Main Stage", "stages.maxCapacity": { $lt: 1000 } },
  { _id: 0, name: 1, "stages.name": 1, "stages.maxCapacity": 1 }
).toArray());
