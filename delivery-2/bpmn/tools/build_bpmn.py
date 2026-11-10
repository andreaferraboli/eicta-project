"""Generates the INITIAL DRAFT of the two BPMN diagrams with full layout (BPMN DI).

The generated .bpmn files are meant to be opened and refined in https://demo.bpmn.io/.
Once you edit them there, do NOT run this script again: it refuses to overwrite
existing files unless --force is given.

    python delivery-2/bpmn/tools/build_bpmn.py [--force]

Stdlib only.
"""

import sys
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parents[1]

SIZES = {"task": (100, 80), "userTask": (100, 80), "sendTask": (100, 80), "receiveTask": (100, 80),
         "serviceTask": (100, 80), "subProcess": (100, 80),
         "startEvent": (36, 36), "endEvent": (36, 36), "intermediateCatchEvent": (36, 36),
         "exclusiveGateway": (50, 50), "eventBasedGateway": (50, 50), "parallelGateway": (50, 50),
         "dataStoreReference": (50, 50)}
COL_W, X0, ROW_OFF = 135, 260, 62


class Diagram:
    def __init__(self, def_id):
        self.def_id = def_id
        self.pools = []      # dicts: id, name, y, lanes [(id, name, height)], process or None (collapsed)
        self.nodes = {}      # id -> dict(type, name, pool, lane, col, row, event, attrs)
        self.flows = []      # (id, src, tgt, name, route)
        self.messages = []   # (id, src, tgt, name)
        self.data = []       # (task, store, "in"|"out")

    def pool(self, pid, name, y, lanes=None, height=None):
        lanes = lanes or []
        h = height or sum(l[2] for l in lanes)
        self.pools.append({"id": pid, "name": name, "y": y, "lanes": lanes, "height": h,
                           "process": None if not lanes else f"Process_{pid}"})

    def node(self, nid, ntype, name, pool, lane, col, row=0, event=None, **attrs):
        self.nodes[nid] = {"type": ntype, "name": name, "pool": pool, "lane": lane, "col": col,
                           "row": row, "event": event, "attrs": attrs}

    def seq(self, src, tgt, name="", route=None):
        self.flows.append((f"Flow_{src}_{tgt}", src, tgt, name, route))

    def msg(self, src, tgt, name=""):
        self.messages.append((f"Msg_{src}_{tgt}", src, tgt, name))

    # ----------------------------------------------------------------- geometry
    def lane_box(self, pool_id, lane_id):
        p = next(p for p in self.pools if p["id"] == pool_id)
        y = p["y"]
        for lid, _, h in p["lanes"]:
            if lid == lane_id:
                return y, h
            y += h
        raise KeyError(lane_id)

    def width(self):
        return X0 + (max(n["col"] for n in self.nodes.values()) + 1) * COL_W - 120

    def bounds(self, nid):
        n = self.nodes[nid]
        w, h = SIZES[n["type"]]
        ly, lh = self.lane_box(n["pool"], n["lane"])
        cx = X0 + n["col"] * COL_W
        cy = ly + lh / 2 + n["row"] * ROW_OFF
        return cx - w / 2, cy - h / 2, w, h

    def anchor(self, nid, side):
        x, y, w, h = self.bounds(nid)
        return {"left": (x, y + h / 2), "right": (x + w, y + h / 2),
                "top": (x + w / 2, y), "bottom": (x + w / 2, y + h)}[side]

    def seq_waypoints(self, src, tgt, route):
        sx, sy = self.anchor(src, "right")
        tx, ty = self.anchor(tgt, "left")
        if route == "up-left":  # leave from the top, enter the target from its left side
            ax, ay = self.anchor(src, "top")
            return [(ax, ay), (ax, ty), (tx, ty)]
        if route in ("below", "above"):
            side = "bottom" if route == "below" else "top"
            (ax, ay), (bx, by) = self.anchor(src, side), self.anchor(tgt, side)
            ly, lh = self.lane_box(self.nodes[src]["pool"], self.nodes[src]["lane"])
            y = (ly + lh - 14) if route == "below" else (ly + 14)
            return [(ax, ay), (ax, y), (bx, y), (bx, by)]
        if abs(sy - ty) < 1:
            return [(sx, sy), (tx, ty)]
        if self.nodes[src]["type"].endswith("Gateway"):
            # leave the gateway from its top/bottom corner, then go right
            ax, ay = self.anchor(src, "top" if ty < sy else "bottom")
            return [(ax, ay), (ax, ty), (tx, ty)]
        if self.nodes[tgt]["type"].endswith("Gateway"):
            bx, by = self.anchor(tgt, "top" if sy < ty else "bottom")
            return [(sx, sy), (bx, sy), (bx, by)]
        mx = (sx + tx) / 2
        return [(sx, sy), (mx, sy), (mx, ty), (tx, ty)]

    def pool_box(self, pid):
        p = next(p for p in self.pools if p["id"] == pid)
        return p["y"], p["height"]

    def msg_waypoints(self, src, tgt):
        def target_is_pool(t):
            return t not in self.nodes
        s_pool = self.nodes[src]["pool"]
        t_pool = tgt if target_is_pool(tgt) else self.nodes[tgt]["pool"]
        sy0, _ = self.pool_box(s_pool)
        ty0, _ = self.pool_box(t_pool)
        down = ty0 > sy0
        sx, sy = self.anchor(src, "bottom" if down else "top")
        if target_is_pool(tgt):
            py, ph = self.pool_box(tgt)
            return [(sx, sy), (sx, py if down else py + ph)]
        tx, ty = self.anchor(tgt, "top" if down else "bottom")
        if abs(sx - tx) < 1:
            return [(sx, sy), (tx, ty)]
        s_top, s_h = self.pool_box(s_pool)
        my = (s_top + s_h + ty0) / 2 if down else (ty0 + self.pool_box(t_pool)[1] + s_top) / 2
        return [(sx, sy), (sx, my), (tx, my), (tx, ty)]

    # ----------------------------------------------------------------- XML
    def xml(self):
        out = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" '
               'xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" '
               'xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" '
               'xmlns:di="http://www.omg.org/spec/DD/20100524/DI" '
               f'id="{self.def_id}" targetNamespace="http://bpmn.io/schema/bpmn" '
               'exporter="build_bpmn.py (draft)" exporterVersion="1.0">']
        out.append('  <bpmn:collaboration id="Collaboration_1">')
        for p in self.pools:
            ref = f' processRef="{p["process"]}"' if p["process"] else ""
            out.append(f'    <bpmn:participant id="{p["id"]}" name="{escape(p["name"])}"{ref} />')
        for mid, s, t, name in self.messages:
            out.append(f'    <bpmn:messageFlow id="{mid}" name="{escape(name)}" sourceRef="{s}" targetRef="{t}" />')
        out.append('  </bpmn:collaboration>')

        incoming, outgoing = {}, {}
        for fid, s, t, *_ in self.flows:
            outgoing.setdefault(s, []).append(fid)
            incoming.setdefault(t, []).append(fid)
        for p in self.pools:
            if not p["process"]:
                continue
            out.append(f'  <bpmn:process id="{p["process"]}" isExecutable="false">')
            out.append('    <bpmn:laneSet id="LaneSet_%s">' % p["id"])
            for lid, lname, _ in p["lanes"]:
                out.append(f'      <bpmn:lane id="{lid}" name="{escape(lname)}">')
                for nid, n in self.nodes.items():
                    if n["lane"] == lid and n["type"] != "dataStoreReference":
                        out.append(f'        <bpmn:flowNodeRef>{nid}</bpmn:flowNodeRef>')
                out.append('      </bpmn:lane>')
            out.append('    </bpmn:laneSet>')
            for nid, n in self.nodes.items():
                if n["pool"] != p["id"]:
                    continue
                if n["type"] == "dataStoreReference":
                    out.append(f'    <bpmn:dataStoreReference id="{nid}" name="{escape(n["name"])}" />')
                    continue
                extra = "".join(f' {k}="{escape(str(v))}"' for k, v in n["attrs"].items() if not k.startswith("_"))
                out.append(f'    <bpmn:{n["type"]} id="{nid}" name="{escape(n["name"])}"{extra}>')
                for f in incoming.get(nid, []):
                    out.append(f'      <bpmn:incoming>{f}</bpmn:incoming>')
                for f in outgoing.get(nid, []):
                    out.append(f'      <bpmn:outgoing>{f}</bpmn:outgoing>')
                for task, store, direction in self.data:
                    if task != nid:
                        continue
                    if direction == "in":
                        out.append(f'      <bpmn:property id="Property_{nid}_{store}" name="__targetRef_placeholder" />')
                        out.append(f'      <bpmn:dataInputAssociation id="DataIn_{nid}_{store}">')
                        out.append(f'        <bpmn:sourceRef>{store}</bpmn:sourceRef>')
                        out.append(f'        <bpmn:targetRef>Property_{nid}_{store}</bpmn:targetRef>')
                        out.append('      </bpmn:dataInputAssociation>')
                    else:
                        out.append(f'      <bpmn:dataOutputAssociation id="DataOut_{nid}_{store}">')
                        out.append(f'        <bpmn:targetRef>{store}</bpmn:targetRef>')
                        out.append('      </bpmn:dataOutputAssociation>')
                if n["event"] == "message":
                    out.append(f'      <bpmn:messageEventDefinition id="MED_{nid}" />')
                elif n["event"] == "timer":
                    out.append(f'      <bpmn:timerEventDefinition id="TED_{nid}">')
                    out.append(f'        <bpmn:timeDuration xsi:type="bpmn:tFormalExpression" '
                               f'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">{n["attrs"].get("_duration", "")}</bpmn:timeDuration>'
                               if n["attrs"].get("_duration") else "")
                    out.append('      </bpmn:timerEventDefinition>')
                out.append(f'    </bpmn:{n["type"]}>')
            for fid, s, t, name, _ in self.flows:
                if self.nodes[s]["pool"] == p["id"]:
                    out.append(f'    <bpmn:sequenceFlow id="{fid}" name="{escape(name)}" sourceRef="{s}" targetRef="{t}" />')
            out.append('  </bpmn:process>')

        # ---- DI
        out.append('  <bpmndi:BPMNDiagram id="BPMNDiagram_1">')
        out.append('    <bpmndi:BPMNPlane id="BPMNPlane_1" bpmnElement="Collaboration_1">')
        width = self.width()
        for p in self.pools:
            out.append(f'      <bpmndi:BPMNShape id="{p["id"]}_di" bpmnElement="{p["id"]}" isHorizontal="true">')
            out.append(f'        <dc:Bounds x="160" y="{p["y"]}" width="{width}" height="{p["height"]}" />')
            out.append('      </bpmndi:BPMNShape>')
            y = p["y"]
            for lid, _, h in p["lanes"]:
                out.append(f'      <bpmndi:BPMNShape id="{lid}_di" bpmnElement="{lid}" isHorizontal="true">')
                out.append(f'        <dc:Bounds x="190" y="{y}" width="{width - 30}" height="{h}" />')
                out.append('      </bpmndi:BPMNShape>')
                y += h
        for nid, n in self.nodes.items():
            x, y, w, h = self.bounds(nid)
            marker = ' isMarkerVisible="true"' if n["type"] == "exclusiveGateway" else ""
            expanded = ' isExpanded="false"' if n["type"] == "subProcess" else ""
            out.append(f'      <bpmndi:BPMNShape id="{nid}_di" bpmnElement="{nid}"{marker}{expanded}>')
            out.append(f'        <dc:Bounds x="{x:.0f}" y="{y:.0f}" width="{w}" height="{h}" />')
            if n["type"] in ("startEvent", "endEvent", "intermediateCatchEvent", "exclusiveGateway",
                             "eventBasedGateway", "dataStoreReference") and n["name"]:
                out.append('        <bpmndi:BPMNLabel>')
                out.append(f'          <dc:Bounds x="{x + w / 2 - 50:.0f}" y="{y + h + 4:.0f}" width="100" height="27" />')
                out.append('        </bpmndi:BPMNLabel>')
            out.append('      </bpmndi:BPMNShape>')
        for fid, s, t, name, route in self.flows:
            pts = self.seq_waypoints(s, t, route)
            out.append(f'      <bpmndi:BPMNEdge id="{fid}_di" bpmnElement="{fid}">')
            out += [f'        <di:waypoint x="{x:.0f}" y="{y:.0f}" />' for x, y in pts]
            if name:
                lx, ly = pts[0] if len(pts) == 2 else pts[1]
                out.append('        <bpmndi:BPMNLabel>')
                out.append(f'          <dc:Bounds x="{lx + 4:.0f}" y="{ly - 20:.0f}" width="60" height="14" />')
                out.append('        </bpmndi:BPMNLabel>')
            out.append('      </bpmndi:BPMNEdge>')
        for mid, s, t, name in self.messages:
            pts = self.msg_waypoints(s, t)
            out.append(f'      <bpmndi:BPMNEdge id="{mid}_di" bpmnElement="{mid}">')
            out += [f'        <di:waypoint x="{x:.0f}" y="{y:.0f}" />' for x, y in pts]
            out.append('      </bpmndi:BPMNEdge>')
        for task, store, direction in self.data:
            aid = f"DataIn_{task}_{store}" if direction == "in" else f"DataOut_{task}_{store}"
            a = self.anchor(store, "top") if direction == "in" else self.anchor(task, "bottom")
            b = self.anchor(task, "bottom") if direction == "in" else self.anchor(store, "top")
            out.append(f'      <bpmndi:BPMNEdge id="{aid}_di" bpmnElement="{aid}">')
            out.append(f'        <di:waypoint x="{a[0]:.0f}" y="{a[1]:.0f}" />')
            out.append(f'        <di:waypoint x="{b[0]:.0f}" y="{b[1]:.0f}" />')
            out.append('      </bpmndi:BPMNEdge>')
        out.append('    </bpmndi:BPMNPlane>')
        out.append('  </bpmndi:BPMNDiagram>')
        out.append('</bpmn:definitions>')
        return "\n".join(line for line in out if line) + "\n"


def store_and_store():
    d = Diagram("Definitions_StoreAndStore")
    d.pool("Pool_Customer", "Customer", 80, [("Lane_Customer", "Customer", 270)])
    d.pool("Pool_Store", "Store&Store", 390, [("Lane_CS", "Customer Service", 240),
                                               ("Lane_IM", "Inventory Management", 240),
                                               ("Lane_LG", "Logistics", 150)])
    d.pool("Pool_Supplier", "External Supplier", 1060, height=70)
    C, S = "Pool_Customer", "Pool_Store"
    # Customer
    d.node("c_start", "startEvent", "Products needed", C, "Lane_Customer", 0)
    d.node("c_ask", "sendTask", "Ask for available products", C, "Lane_Customer", 1)
    d.node("c_recvlist", "receiveTask", "Receive product list", C, "Lane_Customer", 3)
    d.node("c_prepare", "userTask", "Prepare order", C, "Lane_Customer", 4)
    d.node("c_send", "sendTask", "Send order", C, "Lane_Customer", 5)
    d.node("c_evgw", "eventBasedGateway", "", C, "Lane_Customer", 6)
    d.node("c_oos", "intermediateCatchEvent", "Out-of-stock notice", C, "Lane_Customer", 9, -1, event="message")
    d.node("c_update", "sendTask", "Update and send shopping list", C, "Lane_Customer", 10, -1)
    d.node("c_ready", "intermediateCatchEvent", "Order ready notice", C, "Lane_Customer", 14, 1, event="message")
    d.node("c_recvship", "receiveTask", "Receive order", C, "Lane_Customer", 15, 1)
    d.node("c_gw", "exclusiveGateway", "Defective items?", C, "Lane_Customer", 16, 1)
    d.node("c_return", "sendTask", "Return items", C, "Lane_Customer", 17, 1)
    d.node("c_end_ret", "endEvent", "Items returned", C, "Lane_Customer", 18, 1)
    d.node("c_end_ok", "endEvent", "Order kept", C, "Lane_Customer", 17, -1)
    d.seq("c_start", "c_ask"); d.seq("c_ask", "c_recvlist"); d.seq("c_recvlist", "c_prepare")
    d.seq("c_prepare", "c_send"); d.seq("c_send", "c_evgw")
    d.seq("c_evgw", "c_oos"); d.seq("c_oos", "c_update"); d.seq("c_update", "c_evgw", route="above")
    d.seq("c_evgw", "c_ready"); d.seq("c_ready", "c_recvship"); d.seq("c_recvship", "c_gw")
    d.seq("c_gw", "c_return", "yes"); d.seq("c_return", "c_end_ret"); d.seq("c_gw", "c_end_ok", "no")
    # Store&Store
    d.node("s_start", "startEvent", "Product request received", S, "Lane_CS", 1, event="message")
    d.node("s_fwd", "task", "Forward request to inventory management", S, "Lane_CS", 2)
    d.node("s_retrieve", "task", "Retrieve list of available products", S, "Lane_IM", 3)
    d.node("s_sendlist", "sendTask", "Send product list", S, "Lane_CS", 4)
    d.node("s_recvorder", "receiveTask", "Receive order", S, "Lane_CS", 5)
    d.node("s_merge1", "exclusiveGateway", "", S, "Lane_IM", 6)
    d.node("s_check", "task", "Check availability of next product", S, "Lane_IM", 7)
    d.node("s_avail", "exclusiveGateway", "Product available?", S, "Lane_IM", 8)
    d.node("s_notify", "sendTask", "Notify customer: product not in stock", S, "Lane_CS", 9)
    d.node("s_recvupd", "receiveTask", "Receive updated shopping list", S, "Lane_CS", 10)
    d.node("s_low", "exclusiveGateway", "Fewer than 10 items left?", S, "Lane_IM", 9, 0)
    d.node("s_supplier", "sendTask", "Place order to external supplier", S, "Lane_IM", 10, -1)
    d.node("s_merge2", "exclusiveGateway", "", S, "Lane_IM", 11)
    d.node("s_pack", "task", "Package product", S, "Lane_IM", 12)
    d.node("s_all", "exclusiveGateway", "All products packaged?", S, "Lane_IM", 13)
    d.node("s_ready", "sendTask", "Notify customer: order ready for shipping", S, "Lane_CS", 14)
    d.node("s_ship", "task", "Send order to customer", S, "Lane_LG", 15)
    d.node("s_evgw", "eventBasedGateway", "", S, "Lane_CS", 16)
    d.node("s_ret", "intermediateCatchEvent", "Returned items received", S, "Lane_CS", 17, -1, event="message")
    d.node("s_report", "task", "Write report for returned items", S, "Lane_CS", 18, -1)
    d.node("s_end_ret", "endEvent", "Process terminated (report written)", S, "Lane_CS", 19, -1)
    d.node("s_week", "intermediateCatchEvent", "One week elapsed", S, "Lane_CS", 17, 1, event="timer", _duration="P7D")
    d.node("s_record", "task", "Record order", S, "Lane_CS", 18, 1)
    d.node("s_end_ok", "endEvent", "Process terminated (order recorded)", S, "Lane_CS", 19, 1)
    for a, b in [("s_start", "s_fwd"), ("s_fwd", "s_retrieve"), ("s_retrieve", "s_sendlist"),
                 ("s_sendlist", "s_recvorder"), ("s_recvorder", "s_merge1"), ("s_merge1", "s_check"),
                 ("s_check", "s_avail"), ("s_notify", "s_recvupd"),
                 ("s_supplier", "s_merge2"), ("s_merge2", "s_pack"), ("s_pack", "s_all"),
                 ("s_ready", "s_ship"), ("s_ship", "s_evgw"), ("s_evgw", "s_ret"), ("s_ret", "s_report"),
                 ("s_report", "s_end_ret"), ("s_evgw", "s_week"), ("s_week", "s_record"), ("s_record", "s_end_ok")]:
        d.seq(a, b)
    d.seq("s_avail", "s_notify", "no")
    d.seq("s_avail", "s_low", "yes")
    d.seq("s_recvupd", "s_merge1", route="above")
    d.seq("s_low", "s_supplier", "yes")
    d.seq("s_low", "s_merge2", "no")
    d.seq("s_all", "s_merge1", "no", route="below")
    d.seq("s_all", "s_ready", "yes")
    # Message flows
    d.msg("c_ask", "s_start", "product request")
    d.msg("s_sendlist", "c_recvlist", "product list")
    d.msg("c_send", "s_recvorder", "order")
    d.msg("s_notify", "c_oos", "out-of-stock notification")
    d.msg("c_update", "s_recvupd", "updated shopping list")
    d.msg("s_ready", "c_ready", "order ready")
    d.msg("s_ship", "c_recvship", "shipment")
    d.msg("c_return", "s_ret", "returned items")
    d.msg("s_supplier", "Pool_Supplier", "supply order")
    return d


def euphoric_events():
    d = Diagram("Definitions_EuphoricBooking")
    d.pool("Pool_Artist", "Artist (management)", 80, [("Lane_Artist", "Artist", 270)])
    d.pool("Pool_EE", "Euphoric Events", 390, [("Lane_Booking", "Booking Office", 240),
                                                ("Lane_PM", "Program Manager", 180),
                                                ("Lane_DB", "Festival RDBMS (delivery 1)", 170)])
    A, E = "Pool_Artist", "Pool_EE"
    # Artist
    d.node("a_start", "startEvent", "Booking proposal received", A, "Lane_Artist", 4, event="message")
    d.node("a_eval", "task", "Evaluate proposal", A, "Lane_Artist", 5)
    d.node("a_gw", "exclusiveGateway", "Accept?", A, "Lane_Artist", 6)
    d.node("a_accept", "sendTask", "Send acceptance", A, "Lane_Artist", 7, -1)
    d.node("a_decline", "sendTask", "Send decline", A, "Lane_Artist", 8, 1)
    d.node("a_end_no", "endEvent", "Proposal declined", A, "Lane_Artist", 9, 1)
    d.node("a_contract", "receiveTask", "Receive contract", A, "Lane_Artist", 11, -1)
    d.node("a_sign", "sendTask", "Sign and return contract", A, "Lane_Artist", 12, -1)
    d.node("a_end", "endEvent", "Contract signed", A, "Lane_Artist", 13, -1)
    d.seq("a_start", "a_eval"); d.seq("a_eval", "a_gw")
    d.seq("a_gw", "a_accept", "yes"); d.seq("a_gw", "a_decline", "no"); d.seq("a_decline", "a_end_no")
    d.seq("a_accept", "a_contract"); d.seq("a_contract", "a_sign"); d.seq("a_sign", "a_end")
    # Euphoric Events
    d.node("e_start", "startEvent", "Line-up planning opens", E, "Lane_Booking", 0, event="timer", _duration="")
    d.node("e_query", "serviceTask", "Query stages and free time slots", E, "Lane_DB", 1)
    d.node("e_shortlist", "userTask", "Shortlist artists", E, "Lane_PM", 2)
    d.node("e_merge", "exclusiveGateway", "", E, "Lane_Booking", 3)
    d.node("e_propose", "sendTask", "Send booking proposal to next artist", E, "Lane_Booking", 4)
    d.node("e_evgw", "eventBasedGateway", "", E, "Lane_Booking", 5)
    d.node("e_accept", "intermediateCatchEvent", "Acceptance received", E, "Lane_Booking", 6, -1, event="message")
    d.node("e_decline", "intermediateCatchEvent", "Decline received", E, "Lane_Booking", 6.75, 1, event="message")
    d.node("e_timeout", "intermediateCatchEvent", "5 days without answer", E, "Lane_Booking", 6, 0, event="timer", _duration="P5D")
    d.node("e_more", "exclusiveGateway", "Other shortlisted artists?", E, "Lane_Booking", 7.6, 1)
    d.node("e_fail", "endEvent", "No artist booked", E, "Lane_Booking", 8.5, 1)
    d.node("e_register", "serviceTask", "Register performance in DB", E, "Lane_DB", 7)
    d.node("e_schedule", "userTask", "Assign stage and time slot", E, "Lane_PM", 9)
    d.node("e_update", "serviceTask", "Update performance schedule", E, "Lane_DB", 10)
    d.node("e_contract", "sendTask", "Send contract", E, "Lane_Booking", 11)
    d.node("e_signed", "intermediateCatchEvent", "Signed contract received", E, "Lane_Booking", 12, event="message")
    d.node("e_publish", "subProcess", "Publish line-up update", E, "Lane_Booking", 13)
    d.node("e_end", "endEvent", "Artist booked", E, "Lane_Booking", 14)
    d.node("e_db", "dataStoreReference", "Euphoric Events DB", E, "Lane_DB", 4, 0)
    d.seq("e_shortlist", "e_merge", route="up-left")
    for a, b in [("e_start", "e_query"), ("e_query", "e_shortlist"),
                 ("e_merge", "e_propose"), ("e_propose", "e_evgw"), ("e_evgw", "e_accept"), ("e_evgw", "e_decline"),
                 ("e_evgw", "e_timeout"), ("e_decline", "e_more"), ("e_timeout", "e_more"),
                 ("e_accept", "e_register"), ("e_register", "e_schedule"), ("e_schedule", "e_update"),
                 ("e_update", "e_contract"), ("e_contract", "e_signed"), ("e_signed", "e_publish"), ("e_publish", "e_end")]:
        d.seq(a, b)
    d.seq("e_more", "e_merge", "yes", route="below")
    d.seq("e_more", "e_fail", "no")
    d.data += [("e_query", "e_db", "in"), ("e_register", "e_db", "out"), ("e_update", "e_db", "out")]
    d.msg("e_propose", "a_start", "booking proposal")
    d.msg("a_accept", "e_accept", "acceptance")
    d.msg("a_decline", "e_decline", "decline")
    d.msg("e_contract", "a_contract", "contract")
    d.msg("a_sign", "e_signed", "signed contract")
    return d


def main():
    force = "--force" in sys.argv
    for name, build in (("store-and-store.bpmn", store_and_store), ("euphoric-events-artist-booking.bpmn", euphoric_events)):
        target = OUT / name
        if target.exists() and not force:
            print(f"skip {name}: already exists (edit it in bpmn.io, or use --force to regenerate and LOSE edits)")
            continue
        target.write_text(build().xml(), encoding="utf-8")
        print(f"wrote {target}")


if __name__ == "__main__":
    main()
