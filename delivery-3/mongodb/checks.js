// Quantitative checks for delivery 3 (run: python scripts/eicta.py mongo-check).
// - only one collection in the project database
// - at least 10 documents
// - every array has at least 2 elements (so no empty array)
const MIN_DOCUMENTS = 10;
const MIN_ARRAY_ELEMENTS = 2;
const problems = [];

const collections = db.getCollectionNames().filter((c) => !c.startsWith("system."));
print(`collections: ${JSON.stringify(collections)}`);
if (collections.length !== 1) problems.push(`expected exactly 1 collection, found ${collections.length}`);

const n = db.festivals.countDocuments();
print(`documents in festivals: ${n}`);
if (n < MIN_DOCUMENTS) problems.push(`only ${n} documents (< ${MIN_DOCUMENTS})`);

const arrayStats = {};
function walk(node, path, id) {
  if (Array.isArray(node)) {
    const key = path.replace(/\[\d+\]/g, "[]");
    const s = (arrayStats[key] = arrayStats[key] || { arrays: 0, elements: 0, min: Infinity });
    s.arrays += 1;
    s.elements += node.length;
    s.min = Math.min(s.min, node.length);
    if (node.length < MIN_ARRAY_ELEMENTS) problems.push(`${id}: ${path} has ${node.length} element(s)`);
    node.forEach((v, i) => walk(v, `${path}[${i}]`, id));
  } else if (node && typeof node === "object" && !(node instanceof Date) && !(node instanceof ObjectId)) {
    for (const [k, v] of Object.entries(node)) walk(v, path ? `${path}.${k}` : k, id);
  }
}
db.festivals.find().forEach((doc) => walk(doc, "", doc._id));

print("embedded arrays (arrays / total elements / min length):");
for (const [path, s] of Object.entries(arrayStats)) {
  print(`  ${path.padEnd(32)} ${String(s.arrays).padStart(4)} / ${String(s.elements).padStart(5)} / ${s.min}`);
}
if (problems.length) {
  print("CHECKS FAILED");
  problems.slice(0, 20).forEach((p) => print(`  - ${p}`));
} else {
  print("CHECKS PASSED");
}
