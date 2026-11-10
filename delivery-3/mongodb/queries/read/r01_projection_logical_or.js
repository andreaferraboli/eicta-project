// Requirement: D3-QR-1
// Category: projections + logical query operators (1/2)
// Title: Festivals in Milano or Roma
// Description: Uses $or to select festivals located in Milano or Roma and a projection to return only name, location and start date.
// Evidence to collect: delivery-3/report/figures/r01_projection_logical_or.png (MongoDB Compass / Atlas / mongosh)
// Query as typed in mongosh (copy into the report):
/*
db.festivals.find(
  { $or: [{ location: "Milano" }, { location: "Roma" }] },
  { _id: 0, name: 1, location: 1, startDate: 1 }
)
*/
printjson(db.festivals.find(
  { $or: [{ location: "Milano" }, { location: "Roma" }] },
  { _id: 0, name: 1, location: 1, startDate: 1 }
).toArray());
