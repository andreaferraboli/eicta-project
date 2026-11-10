// Requirement: D3-QW-5
// Category: delete
// Title: Delete the demo festival
// Description: Deletes the document inserted by w01.
// Evidence to collect: delivery-3/report/figures/w05_delete_festival.png (MongoDB Compass / Atlas / mongosh)
// Query as typed in mongosh (copy into the report):
/*
printjson(db.festivals.deleteOne({ _id: "Demo Winter Fest 2026" }));
*/
printjson(db.festivals.deleteOne({ _id: "Demo Winter Fest 2026" }));
