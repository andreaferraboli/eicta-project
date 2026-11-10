// Makes the difference between queries r09 and r10 verifiable on the seed data.
//   separately   : { "stages.name": "Main Stage", "stages.maxCapacity": { $lt: 1000 } }
//                  -> each condition may be satisfied by a DIFFERENT element of stages
//   simultaneous : { stages: { $elemMatch: { name: "Main Stage", maxCapacity: { $lt: 1000 } } } }
//                  -> both conditions must hold on the SAME element
const separately = { "stages.name": "Main Stage", "stages.maxCapacity": { $lt: 1000 } };
const together = { stages: { $elemMatch: { name: "Main Stage", maxCapacity: { $lt: 1000 } } } };

const a = db.festivals.find(separately, { _id: 1 }).toArray().map((d) => d._id);
const b = db.festivals.find(together, { _id: 1 }).toArray().map((d) => d._id);
const onlySeparately = a.filter((id) => !b.includes(id));

print(`elemMatch demo: separately=${a.length} simultaneously=${b.length} matched only separately=${onlySeparately.length}`);
onlySeparately.slice(0, 3).forEach((id) => {
  const doc = db.festivals.findOne({ _id: id }, { _id: 0, name: 1, "stages.name": 1, "stages.maxCapacity": 1 });
  print(`  ${doc.name}: ${doc.stages.map((s) => `${s.name} (${s.maxCapacity})`).join(", ")}`);
});
if (onlySeparately.length === 0) {
  print("  WARNING: on this data the two queries return the same documents; adjust the conditions or the data");
}
