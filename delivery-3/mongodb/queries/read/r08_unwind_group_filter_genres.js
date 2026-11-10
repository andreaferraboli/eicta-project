// Requirement: D3-QR-8
// Category: unwind + group by + filter
// Title: Genres with at least 10 performances
// Description: Unwinds stages and performances, groups by genre counting the performances, then filters ($match after $group) the genres with at least 10.
// Evidence to collect: delivery-3/report/figures/r08_unwind_group_filter_genres.png (MongoDB Compass / Atlas / mongosh)
// Query as typed in mongosh (copy into the report):
/*
db.festivals.aggregate([
  { $unwind: "$stages" },
  { $unwind: "$stages.performances" },
  { $group: { _id: "$stages.performances.genre", performances: { $sum: 1 } } },
  { $match: { performances: { $gte: 10 } } },
  { $sort: { performances: -1 } }
])
*/
printjson(db.festivals.aggregate([
  { $unwind: "$stages" },
  { $unwind: "$stages.performances" },
  { $group: { _id: "$stages.performances.genre", performances: { $sum: 1 } } },
  { $match: { performances: { $gte: 10 } } },
  { $sort: { performances: -1 } }
]).toArray());
