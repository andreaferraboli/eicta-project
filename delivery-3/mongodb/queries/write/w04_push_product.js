// Requirement: D3-QW-4
// Category: update
// Title: Add a product to a stand
// Description: Pushes a new food product into the products array of the Demo Hot Drinks stand.
// Evidence to collect: delivery-3/report/figures/w04_push_product.png (MongoDB Compass / Atlas / mongosh)
// Query as typed in mongosh (copy into the report):
/*
printjson(db.festivals.updateOne(
  { _id: "Demo Winter Fest 2026", "stands.name": "Demo Hot Drinks" },
  { $push: { "stands.$.products": { name: "Apple Strudel", price: 4.5, category: "food",
                                     expirationDate: ISODate("2026-12-20T00:00:00Z"), foodType: "vegetarian" } } }
));
*/
printjson(db.festivals.updateOne(
  { _id: "Demo Winter Fest 2026", "stands.name": "Demo Hot Drinks" },
  { $push: { "stands.$.products": { name: "Apple Strudel", price: 4.5, category: "food",
                                     expirationDate: ISODate("2026-12-20T00:00:00Z"), foodType: "vegetarian" } } }
));
