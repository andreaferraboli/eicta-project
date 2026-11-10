// Requirement: D3-QW-3
// Category: update
// Title: Discount all merchandise by 10%
// Description: updateMany with the all-positional operator on stands and a filtered positional operator on products, multiplying merchandise prices by 0.9.
// Evidence to collect: delivery-3/report/figures/w03_update_merchandise_prices.png (MongoDB Compass / Atlas / mongosh)
// Query as typed in mongosh (copy into the report):
/*
printjson(db.festivals.updateMany(
  { "stands.products.category": "merchandise" },
  { $mul: { "stands.$[].products.$[p].price": 0.9 } },
  { arrayFilters: [{ "p.category": "merchandise" }] }
));
*/
printjson(db.festivals.updateMany(
  { "stands.products.category": "merchandise" },
  { $mul: { "stands.$[].products.$[p].price": 0.9 } },
  { arrayFilters: [{ "p.category": "merchandise" }] }
));
