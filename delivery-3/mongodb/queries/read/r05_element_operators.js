// Requirement: D3-QR-5
// Category: element query operators
// Title: Festivals hosting bands and selling typed food
// Description: $exists finds festivals where at least one performing artist has a formationYear (that is, a band); $type checks that a foodType string is present in some product.
// Evidence to collect: delivery-3/report/figures/r05_element_operators.png (MongoDB Compass / Atlas / mongosh)
// Query as typed in mongosh (copy into the report):
/*
db.festivals.find(
  {
    "stages.performances.artists.formationYear": { $exists: true },
    "stands.products.foodType": { $type: "string" }
  },
  { _id: 0, name: 1, location: 1 }
)
*/
printjson(db.festivals.find(
  {
    "stages.performances.artists.formationYear": { $exists: true },
    "stands.products.foodType": { $type: "string" }
  },
  { _id: 0, name: 1, location: 1 }
).toArray());
