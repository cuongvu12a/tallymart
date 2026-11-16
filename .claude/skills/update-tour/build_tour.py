#!/usr/bin/env python3
"""Generate docs/overview/system-tour.html from docs/overview/SYSTEM_TOUR.md.

Standard library only (R-REPO-04: no new dependency). Used by the /update-tour skill.

Two steps:
  units  Write every translatable unit (heading, sentence, table cell, diagram) of the
         Markdown to a JSON file {english: vietnamese_or_null}. Translations already in
         the current HTML are reused, so only new or changed units are null.
  build  Read the Markdown and the completed JSON, and write the HTML.

The JSON file holds Vietnamese, so it MUST stay outside the repo (R-DOC-03): keep it in
a scratch folder. The HTML is the only repo file allowed to hold Vietnamese.
"""
import argparse
import html
import json
import re
import sys
from pathlib import Path

MERMAID_URL = "https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js"

# Diagrams hidden as a whole in Presentation mode, because their shape (step order or
# states) is itself undecided, so stripping the markers would make them look decided.
# Key: "<section anchor>#<n>", n = 1 for the first diagram after that anchor.
INTERNAL_ONLY = {"s4-checkout#1", "s4-checkout#2", "s5#1"}

# Sections hidden as a whole in Presentation mode.
INTERNAL_SECTIONS = {"s0", "s7"}

# A sentence, list item or cell is internal (hidden in Presentation mode) when its
# English text matches this.
INTERNAL_TEXT = re.compile(
    r"Q-\d\d|❓|\bproposed\b|\bProposed\b|\bUndecided\b|[Nn]ot decided|\bis open\b|"
    r"\bare open\b|[Dd]ashed|[Aa]mber|open question|EP-\d\d|derived view|regenerate|"
    r"^Sources:|_pending_|recommendations|\b[Ss]olid\b"
)
# Table columns hidden in Presentation mode (by header text).
INTERNAL_COLUMNS = {"❓", "Q-IDs", "Q-ID"}
# Table rows hidden in Presentation mode when a cell starts with one of these.
INTERNAL_ROW = re.compile(r"^(Proposed|Undecided)\b")

# Labels of the page controls. They are translation units like the Markdown text.
UI_LABELS = ["System tour", "Presentation mode", "Language", "Undecided"]

ANCHOR = re.compile(r'<a id="([^"]+)"></a>')
Q_LINK = re.compile(r"❓?\[(Q-\d\d)\]\(\.\./OPEN_QUESTIONS\.md#(q-\d\d)\)")


# ---------------------------------------------------------------- Markdown parsing

def strip_frontmatter(md):
    if md.startswith("---\n"):
        end = md.index("\n---\n", 4)
        return md[end + 5:]
    return md


def is_block_start(line):
    return (line.startswith(("#", "|", "- ", "```", "<a id=")) or re.match(r"\d+\. ", line))


def parse(md):
    lines = strip_frontmatter(md).split("\n")
    blocks, i = [], 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
        elif line.startswith("```mermaid"):
            j = i + 1
            while not lines[j].startswith("```"):
                j += 1
            blocks.append(("mermaid", "\n".join(lines[i + 1:j]) + "\n"))
            i = j + 1
        elif ANCHOR.fullmatch(line.strip()):
            blocks.append(("anchor", ANCHOR.fullmatch(line.strip()).group(1)))
            i += 1
        elif re.match(r"#{1,6} ", line):
            level = len(line) - len(line.lstrip("#"))
            blocks.append(("h", level, line[level + 1:].strip()))
            i += 1
        elif line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                if not re.fullmatch(r"\|[\s\-:|]+\|", lines[i]):
                    rows.append([c.strip() for c in lines[i].strip()[1:-1].split(" | ")])
                i += 1
            blocks.append(("table", rows))
        elif line.startswith("- ") or re.match(r"\d+\. ", line):
            kind = "ul" if line.startswith("- ") else "ol"
            items = []
            while i < len(lines) and (lines[i].startswith("- ") or re.match(r"\d+\. ", lines[i])
                                      or (lines[i].startswith("  ") and items)):
                if lines[i].startswith("  ") and not re.match(r"\d+\. ", lines[i]):
                    items[-1] += " " + lines[i].strip()
                else:
                    items.append(re.sub(r"^(- |\d+\. )", "", lines[i]))
                i += 1
            blocks.append((kind, items))
        else:
            para = []
            while i < len(lines) and lines[i].strip() and not (para and is_block_start(lines[i])):
                para.append(lines[i].strip())
                i += 1
            blocks.append(("p", " ".join(para)))
    return blocks


def sentences(text):
    """Split prose into sentences. A sentence ends with . ! or ? (optionally closed by **)
    followed by a space and an upper-case letter, *, [, ( or ❓."""
    out, start = [], 0
    for m in re.finditer(r"[.!?](\*\*)?\s+(?=[A-Z*\[(❓`\"])", text):
        out.append(text[start:m.end()].strip())
        start = m.end()
    out.append(text[start:].strip())
    return [s for s in out if s]


def needs_translation(text):
    plain = re.sub(r"\]\([^)]*\)", "]", text)
    plain = re.sub(r"`[^`]*`|<[^>]+>|\b[A-Z]+-\d+\b|Q-\d\d|EP-\d\d", "", plain)
    return re.search(r"[A-Za-z]{3,}", plain) is not None


def units_of(blocks):
    units = []
    for b in blocks:
        if b[0] == "h":
            units.append(b[2])
        elif b[0] == "p":
            units += sentences(b[1])
        elif b[0] in ("ul", "ol"):
            for item in b[1]:
                units += sentences(item)
        elif b[0] == "table":
            for row in b[1]:
                units += [ANCHOR.sub("", c) for c in row]
        elif b[0] == "mermaid":
            units.append(b[1])
    units += UI_LABELS
    seen, out = set(), []
    for u in units:
        if u not in seen and needs_translation(u):
            seen.add(u)
            out.append(u)
    return out


# ---------------------------------------------------------------- inline rendering

def inline(text, in_decisions=False):
    """Render one line of inline Markdown to HTML."""
    anchors = ANCHOR.findall(text)
    text = ANCHOR.sub("", text)
    store = []

    def keep(s):
        store.append(s)
        return f"\x00{len(store) - 1}\x00"

    text = re.sub(r"`([^`]+)`", lambda m: keep(f"<code>{html.escape(m.group(1))}</code>"), text)

    def qlink(m):
        label = m.group(0)[0] == "❓" and "❓" or ""
        qid, anchor = m.group(1), m.group(2)
        if in_decisions:
            return keep(f'<a href="../OPEN_QUESTIONS.md#{anchor}">{label}{qid}</a>')
        return keep(f'<a class="q" href="#d-{anchor}" title="Decision waiting: {qid}">{label}{qid}</a>')

    text = Q_LINK.sub(qlink, text)
    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)",
                  lambda m: keep(f'<a href="{html.escape(m.group(2))}">{inline_simple(m.group(1))}</a>'),
                  text)
    text = inline_simple(text)
    text = re.sub(r"\x00(\d+)\x00", lambda m: store[int(m.group(1))], text)
    text = re.sub(r"\x00(\d+)\x00", lambda m: store[int(m.group(1))], text)
    # A parenthesis that holds a question link is hidden with it in Presentation mode.
    text = re.sub(r'\(([^()]*class="q"[^()]*)\)', r'<span class="qx">(\1)</span>', text)
    text = text.replace("❓", '<span class="qm">❓</span>') if "❓" in text and 'class="q"' not in text else text
    return anchors, text


def inline_simple(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", text)
    return text


# ---------------------------------------------------------------- diagram variants

def strip_markers(label, keep_name=True, colon=True):
    """Remove the parts of a diagram label that carry an open-question marker.

    A label line after the first that holds a marker is a question about the step,
    so it is dropped whole. In the first line, a bracket or a " · " segment that holds
    a marker is dropped. With colon=True, a segment "name: question ❓Q-xx" keeps its
    name. If nothing is left and keep_name is True (a box, a participant or a message
    must keep a name), only the marker itself is removed. Notes use colon=False and
    keep_name=False: a note segment that holds a marker is dropped whole."""
    parts = label.split("<br/>")
    out = []
    for idx, p in enumerate(parts):
        if "❓" not in p:
            out.append(p)
            continue
        if idx > 0:
            continue
        whole = p
        p = re.sub(r"\s*\([^()]*❓[^()]*\)", "", p)
        segs = []
        for s in p.split(" · "):
            if "❓" not in s:
                segs.append(s)
            elif colon and ": " in s and "❓" not in s.rsplit(": ", 1)[0]:
                segs.append(s.rsplit(": ", 1)[0])
        if segs:
            out.append(" · ".join(segs).rstrip(" ?·"))
        elif keep_name:
            out.append(re.sub(r"\s*❓Q-\d\d", "", whole).rstrip(" ?·"))
    return "<br/>".join(o for o in out if o.strip())


def present_flowchart(src):
    lines = src.split("\n")
    node_def = re.compile(r'^\s*(\w+)(\[\(|\(\[|\(\(|\[|\(|\{)(.*?)(\)\]|\]\)|\)\)|\]|\)|\})(:::(\w+))?\s*$')
    drop = set()
    for ln in lines:
        m = node_def.match(ln)
        if m and m.group(6) in ("proposed", "decision"):
            drop.add(m.group(1))
    out, linked = [], set()
    edge_split = re.compile(r"\s*(-->|-\.->|-\.-|---|--x|<-->)(\|[^|]*\|)?\s*")
    for ln in lines:
        m = node_def.match(ln)
        if m:
            if m.group(1) in drop:
                continue
            label = m.group(3)
            quoted = label.startswith('"')
            inner = label.strip('"')
            new = strip_markers(inner)
            label = f'"{new}"' if quoted else new
            out.append((m.group(1), f"{ln[:m.start(3)]}{label}{ln[m.end(3):]}"))
            continue
        s = ln.strip()
        if s and edge_split.search(s) and not s.startswith(("classDef", "subgraph", "end", "flowchart")):
            tokens = edge_split.split(s)
            # tokens: node, arrow, label, node, arrow, label, node ...
            nodes, arrows = tokens[0::3], list(zip(tokens[1::3], tokens[2::3]))
            indent = ln[:len(ln) - len(ln.lstrip())]
            for a, b, (arrow, lab) in zip(nodes, nodes[1:], arrows):
                if a in drop or b in drop or arrow in ("-.->", "-.-"):
                    continue
                lab = lab or ""
                if lab:
                    text = strip_markers(lab[1:-1].strip('"'), keep_name=False)
                    lab = f'|"{text}"|' if text else ""
                linked.update((a, b))
                out.append((None, f"{indent}{a} {arrow}{lab} {b}"))
            continue
        out.append((None, ln))
    # A box left with no arrow at all says nothing in this mode: drop it.
    return "\n".join(ln for node, ln in out if node is None or not linked or node in linked)


def present_sequence(src):
    out = []
    for ln in src.split("\n"):
        s = ln.strip()
        if "-->>" in s:
            continue
        m = re.match(r"(\s*(?:participant|actor) \w+ as )(.*)$", ln)
        if m:
            out.append(m.group(1) + strip_markers(m.group(2)))
            continue
        m = re.match(r"(\s*Note [^:]+: )(.*)$", ln)
        if m:
            text = strip_markers(m.group(2), keep_name=False, colon=False)
            if text.strip():
                out.append(m.group(1) + text)
            continue
        m = re.match(r"(\s*\S+->>\S+: )(.*)$", ln)
        if m:
            out.append(m.group(1) + (strip_markers(m.group(2)) or m.group(2)))
            continue
        m = re.match(r"(\s*(?:alt|else|opt|loop) )(.*)$", ln)
        if m:
            out.append(m.group(1) + (strip_markers(m.group(2)) or m.group(2)))
            continue
        out.append(ln)
    # Drop participants that no message or note uses any more.
    used = set()
    for ln in out:
        m = re.match(r"\s*(\w+)-?->>(\w+):", ln)
        if m:
            used.update(m.groups())
        m = re.match(r"\s*Note (?:over|left of|right of) ([\w,]+):", ln)
        if m:
            used.update(m.group(1).split(","))
    out = [ln for ln in out
           if not (re.match(r"\s*(participant|actor) (\w+) as", ln)
                   and re.match(r"\s*(?:participant|actor) (\w+)", ln).group(1) not in used)]
    # Drop opt/alt/loop blocks left with no message inside.
    changed = True
    while changed:
        changed = False
        for i in range(len(out) - 1):
            if re.match(r"\s*(opt|loop)\b", out[i]) and out[i + 1].strip() == "end":
                del out[i:i + 2]
                changed = True
                break
    return "\n".join(out)


def present(src):
    return present_sequence(src) if src.lstrip().startswith("sequenceDiagram") else present_flowchart(src)


# ---------------------------------------------------------------- HTML building

def bi(en, vi_map, cls=""):
    """Render one unit in both languages."""
    vi = vi_map.get(en, en) if needs_translation(en) else en
    a_en, h_en = inline(en, in_decisions=cls == "dec")
    _, h_vi = inline(vi, in_decisions=cls == "dec")
    anchors = "".join(f'<a id="{a}"></a>' for a in a_en)
    if h_en == h_vi:
        return anchors + h_en
    return f'{anchors}<span class="en">{h_en}</span><span class="vi">{h_vi}</span>'


def prose(text, vi_map):
    out = []
    for s in sentences(text):
        hide = " int" if INTERNAL_TEXT.search(s) else ""
        out.append(f'<span class="s{hide}">{bi(s, vi_map)}</span>')
    return " ".join(out)


def build(md_text, vi_map):
    blocks = parse(md_text)
    missing = [u for u in units_of(blocks) if not vi_map.get(u)]
    if missing:
        sys.exit(f"{len(missing)} units have no Vietnamese text. Run 'units' and fill them in.")

    body, toc, diagrams = [], [], []
    section, last_anchor, diagram_count = None, None, {}
    open_section = open_panel = False
    title = "System tour"
    for idx, b in enumerate(blocks):
        kind = b[0]
        if kind == "anchor":
            last_anchor = b[1]
            nxt = blocks[idx + 1] if idx + 1 < len(blocks) else None
            if nxt and nxt[0] == "h" and nxt[1] == 2:
                if open_panel:
                    body.append("</div></div>")
                    open_panel = False
                if open_section:
                    body.append("</section>")
                section = b[1]
                cls = " internal" if section in INTERNAL_SECTIONS else ""
                body.append(f'<section id="{section}" class="sec{cls}">')
                open_section = True
            elif nxt and nxt[0] == "h" and nxt[1] == 3 and section == "s3":
                if not open_panel:
                    body.append('<div class="tabs" role="tablist"></div><div class="panels">')
                    open_panel = True
                else:
                    body.append("</div>")
                body.append(f'<div class="panel" id="{b[1]}" role="tabpanel">')
            else:
                body.append(f'<a id="{b[1]}"></a>')
        elif kind == "h":
            level, text = b[1], b[2]
            if level == 1:
                title = text
                body.append(f'<h1>{bi(text, vi_map)}</h1>')
                continue
            hid = last_anchor if blocks[idx - 1][0] == "anchor" else None
            if level in (2, 3) and hid:
                toc.append((level, hid, bi(text, vi_map), hid in INTERNAL_SECTIONS))
            body.append(f"<h{level}>{bi(text, vi_map)}</h{level}>")
        elif kind == "p":
            # Text before the first section is a note for maintainers: hide it in Presentation mode.
            cls = ' class="int"' if section is None else ""
            body.append(f"<p{cls}>{prose(b[1], vi_map)}</p>")
        elif kind in ("ul", "ol"):
            items = []
            for it in b[1]:
                hide = ' class="int"' if INTERNAL_TEXT.search(it) else ""
                items.append(f"<li{hide}>{prose(it, vi_map)}</li>")
            body.append(f"<{kind}>{''.join(items)}</{kind}>")
        elif kind == "table":
            head, rows = b[1][0], b[1][1:]
            qcols = {i for i, h in enumerate(head) if h in INTERNAL_COLUMNS}
            dec = section == "s7"
            t = ['<div class="tw"><table><thead><tr>']
            for i, h in enumerate(head):
                t.append(f'<th class="{"qcol" if i in qcols else ""}">{bi(h, vi_map)}</th>')
            t.append("</tr></thead><tbody>")
            for r in rows:
                hide = any(INTERNAL_ROW.match(c) for c in r)
                rid = ANCHOR.search(r[0])
                t.append(f'<tr class="{"int" if hide else ""}"{" id=" + chr(34) + rid.group(1) + "-row" + chr(34) if rid else ""}>')
                for i, c in enumerate(r):
                    t.append(f'<td class="{"qcol" if i in qcols else ""}">{bi(c, vi_map, "dec" if dec else "")}</td>')
                t.append("</tr>")
            t.append("</tbody></table></div>")
            body.append("".join(t))
        elif kind == "mermaid":
            key = last_anchor or "top"
            diagram_count[key] = diagram_count.get(key, 0) + 1
            did = f"{key}#{diagram_count[key]}"
            en = b[1]
            vi = vi_map[en]
            internal = did in INTERNAL_ONLY
            diagrams.append({
                "id": did, "internal": internal,
                "en": en, "vi": vi,
                "en_pres": None if internal else present(en),
                "vi_pres": None if internal else present(vi),
            })
            cls = "dg internal" if internal else "dg"
            body.append(f'<figure class="{cls}" data-d="{len(diagrams) - 1}"><div class="mm"></div></figure>')
    if open_panel:
        body.append("</div></div>")
    if open_section:
        body.append("</section>")

    nav = []
    for level, hid, label, internal in toc:
        cls = f"l{level}" + (" internal" if internal else "")
        nav.append(f'<li class="{cls}"><a href="#{hid}">{label}</a></li>')

    vi_units = {k: v for k, v in vi_map.items() if k in set(units_of(blocks))}
    page = TEMPLATE
    page = page.replace("%%TITLE%%", html.escape(title))
    page = page.replace("%%NAV%%", "".join(nav))
    page = page.replace("%%BODY%%", "\n".join(body))
    page = page.replace("%%DIAGRAMS%%", json.dumps(diagrams, ensure_ascii=False).replace("</", "<\\/"))
    page = page.replace("%%VIUNITS%%", json.dumps(vi_units, ensure_ascii=False).replace("</", "<\\/"))
    page = page.replace("%%MERMAID%%", MERMAID_URL)
    for label in UI_LABELS:
        page = page.replace(f"%%UI:{label}%%", bi(label, vi_map))
    return page


def read_vi_from_html(path):
    if not path.exists():
        return {}
    m = re.search(r'<script type="application/json" id="vi-units">(.*?)</script>', path.read_text(), re.S)
    return json.loads(m.group(1).replace("<\\/", "</")) if m else {}


TEMPLATE = r"""<!-- Generated from SYSTEM_TOUR.md. Do not edit by hand; regenerate. -->
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>TallyMart: %%TITLE%%</title>
<style>
:root{--bg:#fff;--fg:#1a202c;--muted:#5a6475;--line:#d9dee7;--side:#f6f8fb;--core:#2b6cb0;--corebg:#e8f1fb;--prop:#777;--propbg:#f4f4f4;--acc:#2f855a;--accbg:#e6f6ec;--dec:#b7791f;--decbg:#fff4d6;--link:#2457a6}
*{box-sizing:border-box}
html{scroll-padding-top:110px}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
a{color:var(--link)}
header.top{position:sticky;top:0;z-index:10;background:#fff;border-bottom:1px solid var(--line);padding:8px 16px;display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center}
header.top .brand{font-weight:700;margin-right:auto}
.ctl{display:flex;gap:6px;align-items:center;font-size:14px}
.ctl button{font:inherit;border:1px solid var(--line);background:#fff;border-radius:6px;padding:3px 10px;cursor:pointer}
.ctl button[aria-pressed=true]{background:var(--fg);color:#fff;border-color:var(--fg)}
.legend{display:flex;flex-wrap:wrap;gap:6px;font-size:12.5px;width:100%}
.chip{border:1.5px solid;border-radius:5px;padding:1px 8px}
.chip.core{border-color:var(--core);background:var(--corebg)}
.chip.proposed{border-color:var(--prop);background:var(--propbg);border-style:dashed}
.chip.accepted{border-color:var(--acc);background:var(--accbg);border-width:3px}
.chip.decision{border-color:var(--dec);background:var(--decbg)}
.layout{display:grid;grid-template-columns:260px minmax(0,1fr);max-width:1400px;margin:0 auto}
nav.side{position:sticky;top:96px;align-self:start;max-height:calc(100vh - 96px);overflow:auto;padding:16px;border-right:1px solid var(--line);background:var(--side);font-size:14px}
nav.side ul{list-style:none;margin:0;padding:0}
nav.side li{margin:3px 0}
nav.side li.l3{padding-left:14px}
nav.side a{text-decoration:none;color:var(--fg)}
nav.side a:hover{text-decoration:underline}
main{padding:8px 32px 64px;min-width:0}
h1{font-size:28px;margin:16px 0 8px}
h2{font-size:22px;margin:36px 0 8px;padding-top:8px;border-top:1px solid var(--line)}
h3{font-size:18px;margin:24px 0 8px}
.tw{overflow-x:auto;margin:12px 0}
table{border-collapse:collapse;font-size:14px;width:100%}
th,td{border:1px solid var(--line);padding:5px 8px;text-align:left;vertical-align:top}
th{background:var(--side)}
tr:target,tr.hl{background:var(--decbg)}
code{background:#f0f2f5;border-radius:4px;padding:0 4px;font-size:.92em}
a.q{background:var(--decbg);border:1px solid var(--dec);border-radius:4px;padding:0 3px;text-decoration:none;color:#7a4d00;font-size:.9em;white-space:nowrap}
figure.dg{margin:12px 0;padding:12px;border:1px solid var(--line);border-radius:8px;overflow-x:auto;background:#fff}
figure.dg .mm{min-width:0}
figure.dg svg{max-width:100%;height:auto}
.mm a.qlink{cursor:pointer;color:#7a4d00;text-decoration:underline}
.mm text.qtext{cursor:pointer;text-decoration:underline}
.tabs{display:flex;gap:4px;border-bottom:2px solid var(--line);margin-top:16px}
.tabs button{font:inherit;font-weight:600;border:1px solid var(--line);border-bottom:none;background:var(--side);padding:6px 16px;border-radius:6px 6px 0 0;cursor:pointer}
.tabs button[aria-selected=true]{background:#fff;border-color:var(--core);color:var(--core)}
.panel{display:none}
.panel.active{display:block}
body.lang-en .vi,body.lang-vi .en{display:none}
body.pres .internal,body.pres .int,body.pres .qcol,body.pres a.q,body.pres .qx,body.pres .qm,body.pres .chip.proposed,body.pres .chip.decision{display:none !important}
.note{font-size:13px;color:var(--muted)}
@media (max-width:860px){
  .layout{grid-template-columns:minmax(0,1fr)}
  body{overflow-x:hidden}
  nav.side{position:static;max-height:none;border-right:none;border-bottom:1px solid var(--line)}
  main{padding:8px 16px 48px}
  html{scroll-padding-top:140px}
}
@media print{
  header.top .ctl,nav.side,.tabs{display:none !important}
  header.top{position:static}
  .layout{display:block}
  .panel{display:block !important}
  figure.dg,table,tr{break-inside:avoid}
  a{color:inherit;text-decoration:none}
  h2{break-before:auto}
}
</style>
</head>
<body class="lang-en">
<header class="top">
  <span class="brand">TallyMart · %%UI:System tour%%</span>
  <span class="ctl">%%UI:Presentation mode%%
    <button id="pres" aria-pressed="false">Off</button></span>
  <span class="ctl">%%UI:Language%%
    <button id="lang-en" aria-pressed="true">EN</button><button id="lang-vi" aria-pressed="false">VI</button></span>
  <span class="legend" aria-label="Legend">
    <span class="chip core">Core</span><span class="chip proposed">Proposed EP-xx</span>
    <span class="chip accepted">Accepted EP-xx</span><span class="chip decision">❓Q-xx %%UI:Undecided%%</span>
  </span>
</header>
<div class="layout">
<nav class="side"><ul>%%NAV%%</ul></nav>
<main>
%%BODY%%
</main>
</div>
<script type="application/json" id="diagrams">%%DIAGRAMS%%</script>
<script type="application/json" id="vi-units">%%VIUNITS%%</script>
<script src="%%MERMAID%%"></script>
<script>
(function(){
  var D = JSON.parse(document.getElementById('diagrams').textContent);
  var state = {lang:'en', pres:false};
  try { var saved = JSON.parse(localStorage.getItem('tour-state')||'{}'); if (saved.lang) state.lang = saved.lang; if (saved.pres) state.pres = true; } catch(e) {}
  var ok = typeof mermaid !== 'undefined';
  if (ok) mermaid.initialize({startOnLoad:false, securityLevel:'loose', theme:'default', flowchart:{htmlLabels:true}});
  var seq = 0;

  function linkMarkers(root){
    // Flowchart labels are HTML: turn each ❓Q-xx into a link.
    root.querySelectorAll('foreignObject span, foreignObject div, foreignObject p').forEach(function(el){
      el.childNodes.forEach(function(n){
        if (n.nodeType === 3 && /❓Q-\d\d/.test(n.nodeValue)) {
          var span = document.createElement('span');
          span.innerHTML = n.nodeValue.replace(/&/g,'&amp;').replace(/</g,'&lt;')
            .replace(/❓(Q-\d\d)/g, function(_, q){ return '<a class="qlink" href="#d-' + q.toLowerCase() + '">❓' + q + '</a>'; });
          n.replaceWith(span);
        }
      });
    });
    // Sequence diagram text is SVG: make the text element jump to its first question.
    root.querySelectorAll('text').forEach(function(t){
      var m = /❓(Q-\d\d)/.exec(t.textContent);
      if (m && !t.closest('foreignObject')) {
        t.classList.add('qtext');
        t.addEventListener('click', function(){ go('d-' + m[1].toLowerCase()); });
      }
    });
    root.querySelectorAll('a.qlink').forEach(function(a){
      a.addEventListener('click', function(e){ e.preventDefault(); go(a.getAttribute('href').slice(1)); });
    });
  }

  function go(id){
    var el = document.getElementById(id);
    if (!el) return;
    document.querySelectorAll('tr.hl').forEach(function(r){ r.classList.remove('hl'); });
    var row = el.closest('tr'); if (row) row.classList.add('hl');
    el.scrollIntoView({behavior:'smooth', block:'center'});
    history.replaceState(null, '', '#' + id);
  }

  async function renderVisible(){
    if (!ok) return;
    var figs = document.querySelectorAll('figure.dg');
    for (var i = 0; i < figs.length; i++) {
      // Render hidden tabs too (mermaid draws in its own element), so print shows all.
      var f = figs[i];
      var d = D[+f.dataset.d];
      var key = state.lang + (state.pres ? '-pres' : '');
      if (f.dataset.key === key) continue;
      var src = state.pres ? d[state.lang + '_pres'] : d[state.lang];
      if (!src) continue;
      try {
        var r = await mermaid.render('mmd' + (seq++), src);
        var box = f.querySelector('.mm');
        box.innerHTML = r.svg;
        linkMarkers(box);
        f.dataset.key = key;
      } catch (e) {
        f.querySelector('.mm').textContent = 'Diagram error: ' + (e.message || e);
        f.dataset.key = key;
      }
    }
  }

  function apply(){
    document.body.classList.toggle('lang-en', state.lang === 'en');
    document.body.classList.toggle('lang-vi', state.lang === 'vi');
    document.body.classList.toggle('pres', state.pres);
    document.documentElement.lang = state.lang;
    document.getElementById('lang-en').setAttribute('aria-pressed', state.lang === 'en');
    document.getElementById('lang-vi').setAttribute('aria-pressed', state.lang === 'vi');
    var p = document.getElementById('pres');
    p.setAttribute('aria-pressed', state.pres); p.textContent = state.pres ? 'On' : 'Off';
    try { localStorage.setItem('tour-state', JSON.stringify(state)); } catch(e) {}
    renderVisible();
  }

  // Role tabs.
  var panels = document.querySelectorAll('.panel');
  var tabs = document.querySelector('.tabs');
  function showTab(id){
    panels.forEach(function(p){ p.classList.toggle('active', p.id === id); });
    tabs.querySelectorAll('button').forEach(function(b){ b.setAttribute('aria-selected', b.dataset.t === id); });
    renderVisible();
  }
  if (tabs) {
    panels.forEach(function(p){
      var b = document.createElement('button');
      b.setAttribute('role','tab'); b.dataset.t = p.id;
      b.innerHTML = p.querySelector('h3').innerHTML.replace(/^\s*\d+\.\d+\s*/, '');
      b.querySelectorAll('span').forEach(function(s){ s.textContent = s.textContent.replace(/^\s*\d+\.\d+\s*/, ''); });
      b.addEventListener('click', function(){ showTab(p.id); });
      tabs.appendChild(b);
    });
    showTab(panels[0].id);
  }
  function openFor(hash){
    var id = hash.replace('#','');
    var el = id && document.getElementById(id);
    if (!el) return;
    var panel = el.closest('.panel');
    if (panel) showTab(panel.id);
    if (/^d-q-\d\d$/.test(id)) go(id);
  }
  document.addEventListener('click', function(e){
    var a = e.target.closest('a[href^="#"]');
    if (!a) return;
    var id = a.getAttribute('href').slice(1);
    var el = document.getElementById(id);
    if (!el) return;
    var panel = el.closest('.panel');
    if (panel) showTab(panel.id);
    if (/^d-q-\d\d$/.test(id)) { e.preventDefault(); go(id); }
  });
  window.addEventListener('beforeprint', function(){ panels.forEach(function(p){ p.classList.add('active'); }); renderVisible(); });
  window.addEventListener('afterprint', function(){ var a = tabs && tabs.querySelector('[aria-selected=true]'); if (a) showTab(a.dataset.t); });

  document.getElementById('pres').addEventListener('click', function(){ state.pres = !state.pres; apply(); });
  document.getElementById('lang-en').addEventListener('click', function(){ state.lang = 'en'; apply(); });
  document.getElementById('lang-vi').addEventListener('click', function(){ state.lang = 'vi'; apply(); });
  window.tourState = state; window.tourApply = apply; window.tourRender = renderVisible;
  apply();
  openFor(location.hash);
})();
</script>
</body>
</html>
"""


# ---------------------------------------------------------------- checks on the Markdown

def anchors_of(path):
    s = path.read_text()
    found = set(re.findall(r'<a id="([^"]+)"', s))
    for h in re.findall(r"^#+ (.+)$", s, re.M):
        found.add(re.sub(r"[^\w\- ]", "", h.strip().lower()).replace(" ", "-"))
    return found


def check(md_path):
    """Links resolve, every Q-ID and EP-ID exists, every section has Sources."""
    text, problems = md_path.read_text(), []
    for m in re.finditer(r"\]\(([^)\s]+)\)", text):
        link = m.group(1)
        if link.startswith("http"):
            continue
        f, _, a = link.partition("#")
        target = (md_path.parent / f).resolve() if f else md_path
        if not target.exists():
            problems.append(f"missing file: {link}")
        elif a and a not in anchors_of(target):
            problems.append(f"missing anchor: {link}")
    root = md_path.parent.parent
    oq, ep = (root / "OPEN_QUESTIONS.md").read_text(), (root / "product/EPICS.md").read_text()
    for q in sorted(set(re.findall(r"Q-\d\d", text))):
        if f'id="{q.lower()}"' not in oq:
            problems.append(f"unknown {q}")
        elif re.search(rf"^\| \[{q}\].*\| (merged|answered)[^|]*\|$", oq, re.M):
            problems.append(f"{q} is not open")
    for e in sorted(set(re.findall(r"EP-\d\d", text))):
        if f'id="{e.lower()}"' not in ep:
            problems.append(f"unknown {e}")
    for sec in re.split(r"\n(?=## )", strip_frontmatter(text))[1:]:
        if "Sources:" not in sec:
            problems.append(f"no Sources: {sec.splitlines()[0]}")
    n_links = len(re.findall(r"\]\(", text))
    n_diagrams = len(re.findall(r"```mermaid", text))
    print(f"{n_links} links, {n_diagrams} diagrams, {len(problems)} problems")
    for p in problems:
        print("  " + p)
    return not problems


def decisions(md_path):
    """Rewrite the section 7 table from the Q-IDs the other sections use."""
    text = md_path.read_text()
    oq = (md_path.parent.parent / "OPEN_QUESTIONS.md").read_text()
    summary = {m.group(1): (m.group(2), m.group(3).replace("`product` ", ""))
               for m in re.finditer(r"^\| \[(Q-\d\d)\]\(#q-\d\d\) \|\s*(★?)\s*\| (.*?) \| .*? \| .*? \|$", oq, re.M)}
    head, sep, tail = text.partition('<a id="s7"></a>')
    labels, where, cur = {}, {}, None
    for part in re.split(r'(<a id="[^"]+"></a>\n#+ [^\n]+)', head):
        m = re.match(r'<a id="([^"]+)"></a>\n#+ (\d+(?:\.\d+)?\.?)\s*(.*)', part)
        if m:
            cur = m.group(1)
            num = m.group(2).rstrip(".")
            labels[cur] = num if "." not in num else f"{num} {m.group(3).split()[0]}"
            continue
        if cur:
            for q in re.findall(r"Q-\d\d", part):
                where.setdefault(q, [])
                if cur not in where[q]:
                    where[q].append(cur)
    rows = ["| Q-ID | ★ | Question | Where it appears | Details |", "|---|---|---|---|---|"]
    for q in sorted(where):
        star, title = summary[q]
        w = " · ".join(f"[{labels[k]}](#{k})" for k in where[q])
        rows.append(f'| <a id="d-{q.lower()}"></a>{q} | {star} | {title} | {w} | '
                    f"[details](../OPEN_QUESTIONS.md#{q.lower()}) |")
    new_tail = re.sub(r"\| Q-ID \| ★ \|.*?(?=\n\nSources:)", lambda m: "\n".join(rows), tail, count=1, flags=re.S)
    md_path.write_text(head + sep + new_tail)
    print(f"section 7: {len(rows) - 2} Q-IDs")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("step", choices=["check", "decisions", "units", "build"])
    ap.add_argument("--md", default="docs/overview/SYSTEM_TOUR.md")
    ap.add_argument("--html", default="docs/overview/system-tour.html")
    ap.add_argument("--vi", help="JSON file of translation units (keep it outside the repo)")
    a = ap.parse_args()
    if a.step == "check":
        sys.exit(0 if check(Path(a.md)) else 1)
    if a.step == "decisions":
        return decisions(Path(a.md))
    if not a.vi:
        sys.exit("--vi is required for units and build")
    md = Path(a.md).read_text()
    if a.step == "units":
        old = read_vi_from_html(Path(a.html))
        path = Path(a.vi)
        if path.exists():
            old.update({k: v for k, v in json.loads(path.read_text()).items() if v})
        units = units_of(parse(md))
        data = {u: old.get(u) for u in units}
        path.write_text(json.dumps(data, ensure_ascii=False, indent=1))
        todo = sum(1 for v in data.values() if not v)
        print(f"{len(units)} units, {todo} need Vietnamese text -> {path}")
    else:
        vi_map = json.loads(Path(a.vi).read_text())
        Path(a.html).write_text(build(md, vi_map))
        print(f"wrote {a.html}")


if __name__ == "__main__":
    main()
