// Requirement: D3-QR-10
// Category: two conditions evaluated simultaneously on array sub-documents
// Title: Festivals whose Main Stage is small
// Description: Same two conditions with $elemMatch: the SAME stage must be named Main Stage and have capacity below 1000.
// Evidence to collect: delivery-3/report/figures/r10_array_conditions_elemmatch.png (MongoDB Compass / Atlas / mongosh)
// Query as typed in mongosh (copy into the report):
/*
db.festivals.find(
  { stages: { $elemMatch: { name: "Main Stage", maxCapacity: { $lt: 1000 } } } },
  { _id: 0, name: 1, "stages.name": 1, "stages.maxCapacity": 1 }
)
*/
printjson(db.festivals.find(
  { stages: { $elemMatch: { name: "Main Stage", maxCapacity: { $lt: 1000 } } } },
  { _id: 0, name: 1, "stages.name": 1, "stages.maxCapacity": 1 }
).toArray());
