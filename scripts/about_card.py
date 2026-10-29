"""Draw assets/about.svg: the About section as an animated AI "model card".

Run: python scripts/about_card.py   (reuses the palette and helpers in gen_assets.py)
"""
import base64
import math
import random
from xml.sax.saxutils import escape

from gen_assets import (OUT, BG1, CARD, LINE, LINE2, TEXT, SOFT, MUTED, CYAN, SKY, INDIGO, VIOLET,
                        PURPLE, GREEN, AMBER, svg, frame, frame_defs)

W, H = 1200, 760
SHIFT = 148  # room for the identity strip above the panels
PHOTO = OUT / "photo.jpg"


def panel(x, y, w, h, title, col, note=""):
    out = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{CARD}" fill-opacity=".82" stroke="{LINE2}"/>'
           f'<rect x="{x+18}" y="{y}" width="40" height="2" fill="{col}"/>'
           f'<text x="{x+18}" y="{y+30}" class="mono" font-size="12" font-weight="700" letter-spacing="2" fill="{col}">{escape(title)}</text>')
    if note:
        out += f'<text x="{x+w-18}" y="{y+30}" class="mono" font-size="11" fill="{MUTED}" text-anchor="end">{escape(note)}</text>'
    return out


def top_bar():
    return f"""
  <path d="M0 52H{W}" stroke="{LINE2}"/>
  <circle cx="28" cy="26" r="6" fill="#F87171"/><circle cx="48" cy="26" r="6" fill="{AMBER}"/><circle cx="68" cy="26" r="6" fill="{GREEN}"/>
  <text x="94" y="31" class="mono" font-size="14" fill="{SOFT}"><tspan fill="{CYAN}" font-weight="700">harsha-1</tspan> · model card · <tspan fill="{MUTED}">v2026.10</tspan></text>
  <rect x="{W-330}" y="13" width="306" height="26" rx="13" fill="{GREEN}" fill-opacity=".10" stroke="{GREEN}" stroke-opacity=".45"/>
  <circle cx="{W-314}" cy="26" r="4.5" fill="{GREEN}" class="blink"/>
  <text x="{W-302}" y="30.5" class="mono" font-size="12" fill="{GREEN}">ONLINE · AI Engineer @ Yukty AI</text>"""


def identity():
    x, y, w, h = 24, 68, 1152, 132
    cx, cy, r = x + 74, y + h / 2, 46
    body = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{CARD}" fill-opacity=".82" stroke="{LINE2}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r+9}" fill="none" stroke="{LINE2}" stroke-width="1"/>'
            f'<g class="spin" style="transform-origin:{cx}px {cy}px"><circle cx="{cx}" cy="{cy}" r="{r+5}" fill="none" '
            f'stroke="url(#brandRadar)" stroke-width="3" stroke-linecap="round" stroke-dasharray="70 40 20 40"/></g>')
    if PHOTO.exists():
        data = base64.b64encode(PHOTO.read_bytes()).decode()
        body += (f'<image href="data:image/jpeg;base64,{data}" x="{cx - r}" y="{cy - r}" width="{2*r}" height="{2*r}" '
                 f'preserveAspectRatio="xMidYMid slice" clip-path="url(#avatar)"/>')
    else:
        body += (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#brandRadar)" opacity=".9"/>'
                 f'<text x="{cx}" y="{cy+11}" class="sans" font-size="32" font-weight="800" fill="{BG1}" text-anchor="middle">HR</text>')
    body += (f'<circle cx="{cx + r*0.72:.1f}" cy="{cy + r*0.72:.1f}" r="8" fill="{GREEN}" stroke="{CARD}" stroke-width="3"/>'
             f'<text x="{x+150}" y="{y+50}" class="sans" font-size="28" font-weight="800" fill="{TEXT}">Harshavardhan Reddy</text>'
             f'<text x="{x+150}" y="{y+80}" class="sans" font-size="18" font-weight="700" fill="url(#brandRadar)">AI Engineer @ Yukty AI</text>'
             f'<text x="{x+150}" y="{y+106}" class="mono" font-size="12.5" fill="{MUTED}">Kadapa, India · B.Tech CSE (AI &amp; DE), LPU · ex-Futurense</text>')
    rows = [("ROLE", "AI Engineer", CYAN), ("COMPANY", "Yukty AI · yukty.com", VIOLET),
            ("FOCUS", "agents · data pipelines · local AI", GREEN)]
    for i, (k, v, c) in enumerate(rows):
        ry = y + 44 + i * 32
        body += (f'<text x="{x+w-400}" y="{ry}" class="mono" font-size="12" letter-spacing="2" fill="{c}">{k}</text>'
                 f'<text x="{x+w-300}" y="{ry}" class="mono" font-size="13.5" fill="{SOFT}">{escape(v)}</text>')
    body += f'<path d="M{x+w-424} {y+22}V{y+h-22}" stroke="{LINE2}"/>'
    return body


def terminal():
    x, y, w, h = 24, 68, 430, 300
    rows = [
        [("$ ", GREEN), ("load ", TEXT), ("harsha", CYAN), (" --role ", MUTED), ("ai+data-engineer", VIOLET)],
        [("✓ ", GREEN), ("base     ", MUTED), ("B.Tech CSE, AI & Data Eng · LPU", SOFT)],
        [("✓ ", GREEN), ("tuned    ", MUTED), ("AI & Data Eng intern · Futurense", SOFT)],
        [("✓ ", GREEN), ("trained  ", MUTED), ("45 repos · 390 contributions/yr", SOFT)],
        [("✓ ", GREEN), ("weights  ", MUTED), ("Python · SQL · LLMs · pipelines", SOFT)],
        [("✓ ", GREEN), ("deployed ", MUTED), ("AI Engineer @ Yukty AI", CYAN)],
        [("› ", AMBER), ("goal     ", MUTED), ("raw data in → self-running AI out", TEXT)],
    ]
    defs, body = "", panel(x, y, w, h, "BOOT LOG", CYAN, "~/harsha")
    for i, parts in enumerate(rows):
        ly = y + 66 + i * 30
        n = sum(len(t) for t, _ in parts)
        defs += (f'<clipPath id="tl{i}"><rect x="{x+18}" y="{ly-16}" width="{n*8.3+4:.0f}" height="22" class="type" '
                 f'style="animation-delay:{0.3 + i*0.55:.2f}s;animation-timing-function:steps({n})"/></clipPath>')
        spans = "".join(f'<tspan fill="{c}">{escape(t)}</tspan>' for t, c in parts)
        body += f'<text x="{x+18}" y="{ly}" class="mono" font-size="13.5" xml:space="preserve" clip-path="url(#tl{i})">{spans}</text>'
    cy = y + 66 + len(rows) * 30
    body += (f'<text x="{x+18}" y="{cy}" class="mono fade" font-size="13.5" fill="{GREEN}" '
             f'style="animation-delay:{0.3 + len(rows)*0.55:.2f}s">$ <tspan class="blink" fill="{CYAN}">▌</tspan></text>')
    return defs, body


def radar():
    x, y, w, h = 470, 68, 376, 300
    cx, cy, R = x + w / 2, y + 168, 80
    axes = [("Data pipelines", .90), ("LLMs & agents", .95), ("Deep learning", .80),
            ("APIs & backend", .85), ("Cloud & DevOps", .70), ("Automation", .92)]
    pt = lambda k, r: (cx + r * math.cos(math.radians(-90 + 60 * k)), cy + r * math.sin(math.radians(-90 + 60 * k)))
    body = panel(x, y, w, h, "CAPABILITIES", VIOLET, "self-assessed")
    for ring in (0.25, 0.5, 0.75, 1):
        pts = " ".join(f"{a:.1f},{b:.1f}" for a, b in (pt(k, R * ring) for k in range(6)))
        body += f'<polygon points="{pts}" fill="none" stroke="{LINE2}" stroke-width="1" opacity="{.4 + ring*.5:.2f}"/>'
    for k, (label, v) in enumerate(axes):
        ax, ay = pt(k, R)
        body += f'<path d="M{cx} {cy}L{ax:.1f} {ay:.1f}" stroke="{LINE2}" opacity=".7"/>'
        lx, ly = pt(k, R + 22)
        anchor = "middle" if k in (0, 3) else ("start" if k in (1, 2) else "end")
        body += f'<text x="{lx:.1f}" y="{ly + 4:.1f}" class="sans" font-size="12" fill="{SOFT}" text-anchor="{anchor}">{escape(label)}</text>'
    poly = [pt(k, R * v) for k, (_, v) in enumerate(axes)]
    d = "M" + "L".join(f"{a:.1f} {b:.1f}" for a, b in poly) + "Z"
    body += (f'<path d="{d}" fill="url(#radarFill)" class="fade" style="animation-delay:1.6s"/>'
             f'<path d="{d}" pathLength="100" fill="none" stroke="url(#brandRadar)" stroke-width="2.5" stroke-linejoin="round" class="draw"/>')
    for k, (a, b) in enumerate(poly):
        body += (f'<circle cx="{a:.1f}" cy="{b:.1f}" r="9" fill="{[CYAN, VIOLET, INDIGO, SKY, GREEN, PURPLE][k]}" class="halo" style="animation-delay:{k*0.3:.1f}s"/>'
                 f'<circle cx="{a:.1f}" cy="{b:.1f}" r="4" fill="{BG1}" stroke="{[CYAN, VIOLET, INDIGO, SKY, GREEN, PURPLE][k]}" stroke-width="2"/>')
    # rotating scanner sweep
    body += (f'<g class="spin" style="transform-origin:{cx}px {cy}px">'
             f'<path d="M{cx} {cy}L{cx} {cy-R}A{R} {R} 0 0 1 {cx + R*math.sin(math.radians(40)):.1f} {cy - R*math.cos(math.radians(40)):.1f}Z" fill="url(#sweep)"/></g>')
    return body


def processes():
    x, y, w, h = 862, 68, 314, 300
    procs = [
        ("truxlo", "route-optimizer", "AI logistics platform", CYAN, 2.6),
        ("social-autopilot", "daily", "1 fact-checked post a day", VIOLET, 3.4),
        ("jarvis", "local-voice", "offline voice assistant", PURPLE, 2.1),
        ("aura", "memory-graph", "remembers every decision", INDIGO, 3.9),
        ("learning", "gen-ai", "never finishes", GREEN, 1.7),
    ]
    body = panel(x, y, w, h, "RUNNING NOW", GREEN, "5 processes")
    for i, (name, task, desc, col, dur) in enumerate(procs):
        ry = y + 70 + i * 46
        body += (f'<circle cx="{x+24}" cy="{ry-4}" r="4" fill="{col}" class="blink" style="animation-delay:{i*0.37:.2f}s"/>'
                 f'<text x="{x+38}" y="{ry}" class="mono" font-size="13" fill="{TEXT}">{name}<tspan fill="{MUTED}">.{task}</tspan></text>'
                 f'<text x="{x+38}" y="{ry+18}" class="sans" font-size="12" fill="{MUTED}">{escape(desc)}</text>'
                 f'<rect x="{x+w-96}" y="{ry+8}" width="78" height="6" rx="3" fill="{LINE}"/>'
                 f'<rect x="{x+w-96}" y="{ry+8}" width="78" height="6" rx="3" fill="{col}" class="cpu" style="animation-duration:{dur}s"/>')
    return body


def loss_curve():
    x, y, w, h = 24, 384, 430, 204
    body = panel(x, y, w, h, "TRAINING LOSS", SKY, "2023 → now · lower is better")
    gx0, gx1, gy0, gy1 = x + 26, x + w - 22, y + 56, y + h - 34
    rnd = random.Random(3)
    pts = []
    for i in range(61):
        t = i / 60
        v = 0.08 + 0.85 * math.exp(-3.2 * t) + (rnd.random() - .5) * 0.07 * (1 - t * .6)
        pts.append((gx0 + t * (gx1 - gx0), gy1 - v * (gy1 - gy0)))  # high loss sits at the top
    line = "M" + "L".join(f"{a:.1f} {b:.1f}" for a, b in pts)
    area = line + f"L{gx1} {gy1}L{gx0} {gy1}Z"
    for k in range(4):
        yy = gy0 + k * (gy1 - gy0) / 3
        body += f'<path d="M{gx0} {yy:.1f}H{gx1}" stroke="{LINE}" stroke-dasharray="3 5"/>'
    for k, yr in enumerate(["2023", "2024", "2025", "2026"]):
        body += f'<text x="{gx0 + k*(gx1-gx0)/3:.1f}" y="{gy1+20}" class="mono" font-size="11" fill="{MUTED}" text-anchor="middle">{yr}</text>'
    body += (f'<path d="{area}" fill="url(#lossFill)" class="fade" style="animation-delay:1.2s"/>'
             f'<path d="{line}" pathLength="100" fill="none" stroke="url(#brandLoss)" stroke-width="2.5" stroke-linecap="round" class="draw"/>'
             f'<circle r="5" fill="{TEXT}"><animateMotion dur="7s" repeatCount="indefinite" path="{line}"/></circle>')
    for t, label, lift in [(0.12, "first ML model", 24), (0.55, "internship", 26), (0.93, "agents in production", 74)]:
        px, py = pts[int(t * 60)]
        anchor = "end" if t > 0.8 else "start"
        tx = px - 8 if t > 0.8 else px + 8
        body += (f'<path d="M{px:.1f} {py:.1f}V{py-lift:.1f}" stroke="{AMBER}" stroke-dasharray="2 3"/>'
                 f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3.5" fill="{AMBER}"/>'
                 f'<text x="{tx:.1f}" y="{py-lift-3:.1f}" class="mono" font-size="11" fill="{AMBER}" text-anchor="{anchor}">{label}</text>')
    return body


def benchmarks():
    x0, y0, cw, ch, gap = 470, 384, 227, 96, 12
    items = [
        ("30", "%", "faster data processing", "Futurense internship", CYAN),
        ("0.41", "", "ROUGE-L on medical reports", "clinical NLP model", VIOLET),
        ("8", "", "quality gates per post", "social autopilot", PURPLE),
        ("25", "+", "AI news feeds read weekly", "AI Weekly Monitor", SKY),
        ("0", "", "cloud calls needed", "JARVIS runs fully local", GREEN),
        ("40", "%", "better fleet tracking", "Truxlo GPS dashboards", INDIGO),
    ]
    body = ""
    for i, (num, suf, label, src, col) in enumerate(items):
        x, y = x0 + (i % 3) * (cw + gap), y0 + (i // 3) * (ch + gap)
        body += (f'<g class="rise" style="animation-delay:{1.0 + i*0.12:.2f}s">'
                 f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="14" fill="{CARD}" fill-opacity=".82" stroke="{LINE2}"/>'
                 f'<rect x="{x}" y="{y+18}" width="3" height="{ch-36}" rx="1.5" fill="{col}"/>'
                 f'<text x="{x+20}" y="{y+42}" class="sans" font-size="32" font-weight="800" fill="{col}">{num}<tspan font-size="20">{suf}</tspan></text>'
                 f'<text x="{x+20}" y="{y+64}" class="sans" font-size="13" fill="{SOFT}">{escape(label)}</text>'
                 f'<text x="{x+20}" y="{y+82}" class="mono" font-size="11" fill="{MUTED}">{escape(src)}</text></g>')
    return body


def build():
    tdefs, tbody = terminal()
    css = f"""
  .type {{ transform-box: fill-box; transform-origin: left; animation: type .5s both; }}
  @keyframes type {{ from {{ transform: scaleX(0); }} }}
  .fade {{ animation: fade .8s ease both; }}
  @keyframes fade {{ from {{ opacity: 0; }} }}
  .blink {{ animation: blink 1.1s steps(1) infinite; }}
  @keyframes blink {{ 50% {{ opacity: .2; }} }}
  .draw {{ stroke-dasharray: 100; animation: draw 1.8s cubic-bezier(.4,.1,.2,1) .3s both; }}
  @keyframes draw {{ from {{ stroke-dashoffset: 100; }} }}
  .halo {{ opacity: 0; transform-box: fill-box; transform-origin: center; animation: halo 2.2s ease-out infinite; }}
  @keyframes halo {{ 0% {{ opacity: .5; transform: scale(.4); }} 80%,100% {{ opacity: 0; transform: scale(1.6); }} }}
  .spin {{ animation: spin 6s linear infinite; }}
  @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
  .cpu {{ transform-box: fill-box; transform-origin: left; animation: cpu ease-in-out infinite alternate; }}
  @keyframes cpu {{ 0% {{ transform: scaleX(.25); }} 50% {{ transform: scaleX(.9); }} 100% {{ transform: scaleX(.55); }} }}
  .rise {{ animation: rise .7s cubic-bezier(.2,.7,.2,1) both; }}
  @keyframes rise {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: none; }} }}
  .scan {{ animation: scan 7s linear infinite; }}
  @keyframes scan {{ from {{ transform: translateY(-120px); }} to {{ transform: translateY({H}px); }} }}
"""
    defs = frame_defs(W, H) + tdefs + f"""
  <clipPath id="avatar"><circle cx="98" cy="134" r="46"/></clipPath>
  <linearGradient id="brandRadar" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>
  <radialGradient id="radarFill"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".05"/><stop offset="1" stop-color="{CYAN}" stop-opacity=".28"/></radialGradient>
  <linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset="1" stop-color="{CYAN}" stop-opacity=".22"/></linearGradient>
  <linearGradient id="brandLoss" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#F87171"/><stop offset=".4" stop-color="{VIOLET}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>
  <linearGradient id="lossFill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{SKY}" stop-opacity=".25"/><stop offset="1" stop-color="{SKY}" stop-opacity="0"/></linearGradient>
  <linearGradient id="scanG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset=".5" stop-color="{CYAN}" stop-opacity=".07"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>"""
    inner = (top_bar() + identity() + f'<g transform="translate(0 {SHIFT})">' + tbody + radar() + processes()
             + loss_curve() + benchmarks() + "</g>"
             + f'<rect x="0" y="0" width="{W}" height="120" fill="url(#scanG)" class="scan"/>')
    label = ("About Harshavardhan Reddy, AI Engineer at Yukty AI, presented as an AI model card. Boot log: B.Tech CSE in AI and Data Engineering at LPU; "
             "AI and Data Engineering intern at Futurense; now AI Engineer at Yukty AI; 45 repos and 390 contributions this year; from Kadapa, India; goal: raw data in, "
             "self-running AI out. Capabilities: data pipelines, LLMs and agents, ML and deep learning, APIs, cloud, automation. "
             "Running now: Truxlo, social autopilot, JARVIS, AURA, learning generative AI. Benchmarks: 30% faster data processing, "
             "0.41 ROUGE-L, 8 quality gates per post, 25+ AI feeds a week, 0 cloud calls for JARVIS, 40% better fleet tracking.")
    (OUT / "about.svg").write_text(svg(W, H, frame(W, H, inner), css, defs, label), encoding="utf-8")


if __name__ == "__main__":
    build()
    print("wrote", OUT / "about.svg")
