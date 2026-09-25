#!/usr/bin/env python3
"""Ontology Forge helpers.

  split  - cut data/tickets.md into batch files for parallel extraction agents
  vocab  - write ontology/vocab.json (the controlled vocabularies + canonical ids)
  merge  - merge agent batch outputs, enforce the schema, write ontology.json + report
"""
import argparse
import collections
import json
import random
import re
import sys
from pathlib import Path

ENTITY_TYPES = {
    "System": "system", "Component": "component", "Interface": "interface", "Initiative": "initiative",
    "Release": "release", "External Dependency": "dependency", "Failure Mode": "failure",
    "Business Impact": "impact", "Role": "role", "Process": "process",
}
C, S, I, IN, R, D, F, B, RO, P = ("Component", "System", "Interface", "Initiative", "Release",
                                  "External Dependency", "Failure Mode", "Business Impact", "Role", "Process")
# predicate: (allowed subject types, allowed object types)
RELATIONS = {
    "PART_OF": ({C}, {S}),
    "DEPENDS_ON": ({C, S}, {C, S, D}),
    "EXPOSES": ({C}, {I}),
    "EXHIBITS": ({C, I, R}, {F}),
    "TRIGGERED_BY": ({F}, {I, C, D}),
    "CAUSES": ({F}, {B}),
    "CHANGES": ({IN}, {C, I}),
    "SUPERSEDES": ({C, I}, {C, I}),
    "DELIVERED_IN": ({IN, C, I}, {R}),
    "MITIGATED_BY": ({F}, {P, IN, I}),
    "CONCERNED_WITH": ({RO}, {B, S}),
    "PERFORMS": ({RO}, {P}),
    "GOVERNED_BY": ({IN, I}, {P}),
}
VOCAB = {
    "Failure Mode": ["Crash / Unhandled Exception", "Hang / Stuck State", "Data Loss / Corruption",
                     "Incorrect Behavior", "Config Not Honored", "Performance Degradation", "Resource Leak",
                     "Security Vulnerability", "Flaky Test", "Build / CI Failure", "Packaging / Release Defect",
                     "Compatibility / Upgrade Break", "Documentation Gap", "API Usability Gap",
                     "Missing Observability"],
    "Business Impact": ["Data Durability Risk", "Availability / Outage Risk", "Security & Compliance Exposure",
                        "Upgrade / Migration Friction", "Operational Burden", "Developer Productivity Loss",
                        "User Confusion / Adoption Barrier", "Performance / Cost"],
    "Role": ["End User / App Developer", "Operator / SRE", "Contributor", "Newcomer Contributor",
             "Committer / Reviewer", "Release Manager", "Security Reporter", "Vendor / Integrator"],
    "Process": ["KIP (Design Proposal) Process", "Release & Backport", "CI / Testing", "Deprecation Lifecycle",
                "Vulnerability Response", "Contributor Onboarding", "Triage", "Platform Migration"],
}
SYSTEMS = {"broker": "Broker", "controller": "Controller", "clients": "Clients", "streams": "Streams",
           "connect": "Connect", "mirrormaker": "MirrorMaker", "tooling": "Tooling", "build-ci": "Build & CI",
           "documentation": "Documentation", "security": "Security"}
CONF_RANK = {"low": 0, "medium": 1, "high": 2}


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def vocab_ids():
    return {f"{ENTITY_TYPES[t]}:{slug(v)}": (t, v) for t, vals in VOCAB.items() for v in vals}


def sections(path):
    text = Path(path).read_text()
    return re.split(r"\n(?=## KAFKA-)", text)[1:]


def cmd_split(args):
    secs = sections(args.tickets)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    # Pilot: the same 40 tickets the schema was designed from (1 per 1/40th slice, seed 40).
    random.seed(40)
    n = len(secs)
    pilot = [secs[random.randrange(int(i * n / 40), int((i + 1) * n / 40))] for i in range(40)]
    (out / "pilot.md").write_text("\n".join(pilot))
    size = -(-n // args.batches)
    for b in range(args.batches):
        chunk = secs[b * size:(b + 1) * size]
        (out / f"batch_{b + 1:02d}.md").write_text("\n".join(chunk))
        print(f"batch_{b + 1:02d}.md: {len(chunk)} tickets, ≈{sum(map(len, chunk)) // 4:,} tokens")
    print(f"pilot.md: 40 tickets")


def cmd_vocab(args):
    data = {
        "entity_types": {t: f"{p}:<kebab-case-name>" for t, p in ENTITY_TYPES.items()},
        "relations": {k: {"subject": sorted(s), "object": sorted(o)} for k, (s, o) in RELATIONS.items()},
        "controlled_vocabulary_ids": {i: f"{t}: {v}" for i, (t, v) in vocab_ids().items()},
    }
    Path(args.out).write_text(json.dumps(data, indent=2))
    print(f"wrote {args.out}")


def cmd_merge(args):
    created = {}
    for line in open(args.raw):
        r = json.loads(line)
        created[r["key"]] = r["created"][:10]
    vids = vocab_ids()
    entities, rels, pending = {}, {}, {}
    problems = collections.defaultdict(list)
    batch_keys_seen = set()
    raw_counts = collections.Counter()

    for bf in sorted(Path(args.batches).glob(args.pattern)):
        src_md = Path(args.batch_md_dir) / (bf.stem + ".md")
        allowed = set(re.findall(r"^## (KAFKA-\d+)", src_md.read_text(), re.M)) if src_md.exists() else set(created)
        batch_keys_seen |= allowed
        data = json.loads(bf.read_text())
        raw_counts["entities"] += len(data.get("entities", []))
        raw_counts["relationships"] += len(data.get("relationships", []))

        def check_evidence(ev, where):
            # Normalize bare numbers ("13270" -> "KAFKA-13270"); still checked against the batch below.
            ev = [f"KAFKA-{k}" if str(k).isdigit() else k for k in ev or []]
            bad = [k for k in ev if k not in allowed]
            if bad:
                problems["evidence not in the agent's batch (possible hallucination)"].append(f"{bf.name} {where}: {bad}")
            return [k for k in ev if k in allowed]

        for e in data.get("entities", []):
            t, eid = e.get("type"), e.get("id", "")
            if t not in ENTITY_TYPES:
                problems["unknown entity type"].append(f"{bf.name} {eid}: {t}")
                continue
            if not eid.startswith(ENTITY_TYPES[t] + ":"):
                eid = f"{ENTITY_TYPES[t]}:{slug(e.get('name', eid))}"
            if t in VOCAB and eid not in vids and not e.get("proposed"):
                problems["controlled-vocabulary value not in seed list (and not marked proposed)"].append(
                    f"{bf.name} {eid}")
            ev = check_evidence(e.get("evidence"), eid)
            if not ev and t not in VOCAB and eid not in entities:
                # Held back: kept only if a relationship with valid evidence references it (see below).
                pending.setdefault(eid, e | {"type": t})
                continue
            cur = entities.setdefault(eid, {"id": eid, "type": t, "name": e.get("name") or eid,
                                             "aliases": set(), "attributes": {}, "evidence": set(),
                                             "proposed": bool(e.get("proposed"))})
            if t in VOCAB and eid in vids:
                cur["name"] = vids[eid][1]
            cur["aliases"] |= {a for a in e.get("aliases") or [] if a and a != cur["name"]}
            if e.get("name") and e["name"] != cur["name"]:
                cur["aliases"].add(e["name"])
            cur["attributes"].update(e.get("attributes") or {})
            cur["evidence"] |= set(ev)

        for r in data.get("relationships", []):
            key = (r.get("subject"), r.get("predicate"), r.get("object"))
            ev = check_evidence(r.get("evidence"), "->".join(map(str, key)))
            if not ev:
                problems["relationship with no valid evidence (dropped)"].append(f"{bf.name} {key}")
                continue
            cur = rels.setdefault(key, {"subject": key[0], "predicate": key[1], "object": key[2],
                                        "attributes": {}, "evidence": set(), "confidence": "low"})
            cur["attributes"].update(r.get("attributes") or {})
            cur["evidence"] |= set(ev)
            c = r.get("confidence", "medium")
            if CONF_RANK.get(c, 1) > CONF_RANK[cur["confidence"]]:
                cur["confidence"] = c

    # Evidence-less entities survive only if an evidenced relationship uses them; they inherit its evidence.
    for key, r in rels.items():
        for eid in (key[0], key[2]):
            if eid in pending and eid not in entities:
                e = pending[eid]
                entities[eid] = {"id": eid, "type": e["type"], "name": e.get("name") or eid,
                                 "aliases": set(e.get("aliases") or []), "attributes": dict(e.get("attributes") or {}),
                                 "evidence": set(), "proposed": bool(e.get("proposed"))}
            if eid in entities and eid in pending:
                entities[eid]["evidence"] |= r["evidence"]
    for eid in pending:
        if eid not in entities:
            problems["entity with no evidence and no evidenced relationship (dropped)"].append(eid)

    # Canonical nodes (controlled vocabularies + the fixed System list) always exist when referenced.
    canonical = dict(vids, **{f"system:{k}": ("System", v) for k, v in SYSTEMS.items()})
    for key in rels:
        for eid in (key[0], key[2]):
            if eid in canonical and eid not in entities:
                t, v = canonical[eid]
                entities[eid] = {"id": eid, "type": t, "name": v, "aliases": set(), "attributes": {},
                                 "evidence": set(), "proposed": False}

    # Schema enforcement on relationships (flagged, kept for the critic to review).
    for key, r in rels.items():
        s, p, o = key
        issues = []
        if p not in RELATIONS:
            issues.append("unknown predicate")
        elif s not in entities or o not in entities:
            issues.append("dangling reference")
        else:
            st, ot = entities[s]["type"], entities[o]["type"]
            dom, rng = RELATIONS[p]
            if st not in dom or ot not in rng:
                issues.append(f"domain/range: {st} -{p}-> {ot}")
        if issues:
            r["schema_violation"] = "; ".join(issues)
            problems["relationship violates schema (flagged for critic)"].append(f"{s} -{p}-> {o}: {issues[0]}")
        # vocab entities gain evidence through their relationships
        for eid in (s, o):
            if eid in entities and entities[eid]["type"] in VOCAB:
                entities[eid]["evidence"] |= r["evidence"]

    # first/last seen come from ticket dates, never from the agent.
    for e in entities.values():
        dates = sorted(created[k] for k in e["evidence"])
        e["first_seen"], e["last_seen"] = (dates[0], dates[-1]) if dates else (None, None)
        e["aliases"], e["evidence"] = sorted(e["aliases"]), sorted(e["evidence"])
    for r in rels.values():
        r["evidence"] = sorted(r["evidence"])

    cited = {k for x in list(entities.values()) + list(rels.values()) for k in x["evidence"]}
    ent_list = sorted(entities.values(), key=lambda e: (e["type"], e["id"]))
    rel_list = sorted(rels.values(), key=lambda r: (r["predicate"], r["subject"], r["object"]))
    out = {"schema_version": "1.0", "entities": ent_list, "relationships": rel_list}
    Path(args.out).write_text(json.dumps(out, indent=1, ensure_ascii=False))

    by_type = collections.Counter(e["type"] for e in ent_list)
    by_pred = collections.Counter(r["predicate"] for r in rel_list)
    violations = sum(1 for r in rel_list if "schema_violation" in r)
    coverage = len(cited & batch_keys_seen) / max(1, len(batch_keys_seen))
    lines = [f"# Merge report: `{Path(args.out).name}`", "",
             f"- Agent output: {raw_counts['entities']} entity mentions, {raw_counts['relationships']} relationship mentions",
             f"- After merge: **{len(ent_list)} entities**, **{len(rel_list)} relationships**",
             f"- Ticket coverage: **{coverage:.0%}** of {len(batch_keys_seen)} tickets cited as evidence",
             f"- Schema violations flagged: **{violations}** ({violations / max(1, len(rel_list)):.0%} of relationships)",
             f"- Confidence: " + ", ".join(f"{c} {n}" for c, n in collections.Counter(r['confidence'] for r in rel_list).most_common()),
             "", "## Entities by type", "", "| Type | Count |", "|---|---|"]
    lines += [f"| {t} | {by_type[t]} |" for t in ENTITY_TYPES if by_type[t]]
    lines += ["", "## Relationships by predicate", "", "| Predicate | Count |", "|---|---|"]
    lines += [f"| {p} | {by_pred[p]} |" for p in RELATIONS if by_pred[p]]
    lines += ["", "## Problems found", ""]
    if not problems:
        lines.append("None.")
    for k, v in problems.items():
        lines += [f"### {k} ({len(v)})", ""] + [f"- {x}" for x in v[:25]]
        if len(v) > 25:
            lines.append(f"- …and {len(v) - 25} more")
        lines.append("")
    Path(args.report).write_text("\n".join(lines) + "\n")
    print("\n".join(lines[:9]))
    for k, v in problems.items():
        print(f"  {k}: {len(v)}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("split")
    s.add_argument("--tickets", default="data/tickets.md")
    s.add_argument("--out", default="data/batches")
    s.add_argument("--batches", type=int, default=8)
    v = sub.add_parser("vocab")
    v.add_argument("--out", default="ontology/vocab.json")
    m = sub.add_parser("merge")
    m.add_argument("--batches", default="ontology/batches")
    m.add_argument("--pattern", default="[bg]*.json")  # batch_*.json + gapfill.json (pilot excluded)
    m.add_argument("--batch-md-dir", default="data/batches")
    m.add_argument("--raw", default="data/raw/kafka_issues.jsonl")
    m.add_argument("--out", default="ontology/ontology.json")
    m.add_argument("--report", default="ontology/merge_report.md")
    args = ap.parse_args()
    {"split": cmd_split, "vocab": cmd_vocab, "merge": cmd_merge}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
