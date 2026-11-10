// Requirement: D3-QR-2
// Category: projections + logical query operators (2/2)
// Title: Festivals sponsored by Blue Bank outside the south
// Description: Combines $and and $nor: festivals with at least one stand sponsored by Blue Bank that are not in Napoli, Bari or Palermo. Projects name, location and stand names.
// Evidence to collect: delivery-3/report/figures/r02_projection_logical_and_nor.png (MongoDB Compass / Atlas / mongosh)
// Query as typed in mongosh (copy into the report):
/*
db.festivals.find(
  { $and: [
      { "stands.sponsor": "Blue Bank" },
      { $nor: [{ location: "Napoli" }, { location: "Bari" }, { location: "Palermo" }] }
  ] },
  { _id: 0, name: 1, location: 1, "stands.name": 1, "stands.sponsor": 1 }
)
*/
printjson(db.festivals.find(
  { $and: [
      { "stands.sponsor": "Blue Bank" },
      { $nor: [{ location: "Napoli" }, { location: "Bari" }, { location: "Palermo" }] }
  ] },
  { _id: 0, name: 1, location: 1, "stands.name": 1, "stands.sponsor": 1 }
).toArray());
