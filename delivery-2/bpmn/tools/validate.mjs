// Validates the .bpmn files with bpmn-moddle (the parser used by bpmn.io) plus structural checks.
// Usage (from this folder): npm install && npm run validate
import { readFileSync, readdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import BpmnModdle from "bpmn-moddle";

const dir = join(dirname(fileURLToPath(import.meta.url)), "..");
const files = readdirSync(dir).filter((f) => f.endsWith(".bpmn"));
const moddle = new BpmnModdle();
let failed = false;

for (const file of files) {
  const problems = [];
  const { rootElement: defs, warnings } = await moddle.fromXML(readFileSync(join(dir, file), "utf8"));
  warnings.forEach((w) => problems.push(`parser: ${w.message}`));

  const collab = defs.rootElements.find((e) => e.$type === "bpmn:Collaboration");
  const processes = defs.rootElements.filter((e) => e.$type === "bpmn:Process");
  const plane = defs.diagrams[0].plane;
  const shapes = new Set(plane.planeElement.map((d) => d.bpmnElement && d.bpmnElement.id));
  const participantOf = new Map();
  collab.participants.forEach((p) => {
    if (!shapes.has(p.id)) problems.push(`participant ${p.id} has no shape`);
    if (p.processRef) participantOf.set(p.processRef.id, p.id);
  });

  let starts = 0, ends = 0, gateways = 0, timers = 0, lanes = 0;
  const elementPool = new Map();
  for (const proc of processes) {
    (proc.laneSets || []).forEach((ls) => ls.lanes.forEach((l) => { lanes++; if (!shapes.has(l.id)) problems.push(`lane ${l.id} has no shape`); }));
    const laned = new Set((proc.laneSets || []).flatMap((ls) => ls.lanes.flatMap((l) => (l.flowNodeRef || []).map((n) => n.id))));
    for (const el of proc.flowElements || []) {
      elementPool.set(el.id, participantOf.get(proc.id));
      if (!shapes.has(el.id)) problems.push(`${el.id} has no DI shape/edge`);
      if (el.$type === "bpmn:SequenceFlow" || el.$type === "bpmn:DataStoreReference") continue;
      if (!laned.has(el.id)) problems.push(`${el.id} is not assigned to a lane`);
      const inc = (el.incoming || []).length, out = (el.outgoing || []).length;
      if (el.$type === "bpmn:StartEvent") starts++;
      if (el.$type === "bpmn:EndEvent") ends++;
      if (el.$type.endsWith("Gateway")) gateways++;
      if ((el.eventDefinitions || []).some((d) => d.$type === "bpmn:TimerEventDefinition")) timers++;
      if (el.$type !== "bpmn:StartEvent" && inc === 0) problems.push(`${el.id} has no incoming sequence flow`);
      if (el.$type !== "bpmn:EndEvent" && out === 0) problems.push(`${el.id} has no outgoing sequence flow`);
      if (el.$type === "bpmn:ExclusiveGateway" && out > 1) {
        (el.outgoing || []).forEach((f) => { if (!f.name) problems.push(`flow ${f.id} out of decision ${el.id} has no label`); });
      }
      if (el.$type === "bpmn:EventBasedGateway") {
        (el.outgoing || []).forEach((f) => {
          if (f.targetRef.$type !== "bpmn:IntermediateCatchEvent" && f.targetRef.$type !== "bpmn:ReceiveTask") {
            problems.push(`event-based gateway ${el.id} must lead to catch events`);
          }
        });
      }
    }
  }
  for (const m of collab.messageFlows || []) {
    if (!shapes.has(m.id)) problems.push(`message flow ${m.id} has no edge`);
    const sp = elementPool.get(m.sourceRef.id) || m.sourceRef.id;
    const tp = elementPool.get(m.targetRef.id) || m.targetRef.id;
    if (sp === tp) problems.push(`message flow ${m.id} stays inside one pool`);
  }

  console.log(`${file}: ${collab.participants.length} pools, ${lanes} lanes, ${(collab.messageFlows || []).length} message flows, ` +
              `${starts} start, ${ends} end, ${gateways} gateways, ${timers} timer events`);
  if (problems.length) {
    failed = true;
    problems.forEach((p) => console.log(`  PROBLEM ${p}`));
  } else {
    console.log("  OK");
  }
}
process.exit(failed ? 1 : 0);
