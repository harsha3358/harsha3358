"""Generate the animated SVGs for the harsha3358 GitHub profile README.

Run: python scripts/gen_assets.py   (writes into assets/)

Palette (3-tier):
  primary   cyan   #22D3EE = data, violet #A78BFA = AI (gradient = data -> AI)
  neutrals  slate ramp tinted blue
  supporting emerald #34D399 (live), amber #FBBF24 (private)
"""
import math
import random
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(parents=True, exist_ok=True)

BG0, BG1 = "#060A13", "#0B1222"
CARD, LINE, LINE2 = "#0F172A", "#1E293B", "#334155"
TEXT, SOFT, MUTED = "#F1F5F9", "#CBD5E1", "#94A3B8"
CYAN, SKY, INDIGO, VIOLET, PURPLE = "#22D3EE", "#38BDF8", "#818CF8", "#A78BFA", "#C084FC"
GREEN, AMBER = "#34D399", "#FBBF24"
SANS = "'Segoe UI', Inter, -apple-system, 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', 'Cascadia Code', Consolas, 'SF Mono', Menlo, monospace"

BASE_CSS = f"""
  .sans {{ font-family: {SANS}; }}
  .mono {{ font-family: {MONO}; }}
  @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
"""


def svg(w, h, body, css="", defs="", label=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'role="img" aria-label="{escape(label)}">\n<title>{escape(label)}</title>\n'
        f"<style>{BASE_CSS}{css}</style>\n<defs>{defs}</defs>\n{body}\n</svg>\n"
    )


def frame_defs(w, h, gid="bg"):
    return f"""
  <linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{BG0}"/><stop offset="1" stop-color="{BG1}"/>
  </linearGradient>
  <linearGradient id="brand" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{CYAN}"/><stop offset="0.5" stop-color="{INDIGO}"/><stop offset="1" stop-color="{VIOLET}"/>
  </linearGradient>
  <linearGradient id="brandShift" x1="0" y1="0" x2="1" y2="0" gradientUnits="objectBoundingBox">
    <stop offset="0" stop-color="{CYAN}"/><stop offset="0.35" stop-color="{INDIGO}"/>
    <stop offset="0.65" stop-color="{VIOLET}"/><stop offset="1" stop-color="{CYAN}"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="-1 0; 0 0" dur="6s" repeatCount="indefinite"/>
  </linearGradient>
  <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">
    <path d="M32 0H0V32" fill="none" stroke="{LINE}" stroke-width="1" opacity="0.55"/>
  </pattern>
  <clipPath id="round"><rect width="{w}" height="{h}" rx="18"/></clipPath>
"""


def frame(w, h, inner):
    return f"""<g clip-path="url(#round)">
  <rect width="{w}" height="{h}" fill="url(#bg)"/>
  <rect width="{w}" height="{h}" fill="url(#grid)"/>
  {inner}
</g>
<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="18" fill="none" stroke="{LINE2}"/>"""


# --------------------------------------------------------------------------- hero
def hero():
    W, H = 1200, 340
    rnd = random.Random(7)
    layers = [
        (800, [100, 160, 220, 280]),
        (910, [76, 133, 190, 247, 304]),
        (1020, [76, 133, 190, 247, 304]),
        (1120, [160, 220]),
    ]
    edges, pulses = [], []
    for li in range(len(layers) - 1):
        x1, ys1 = layers[li]
        x2, ys2 = layers[li + 1]
        for y1 in ys1:
            for y2 in ys2:
                d = f"M{x1} {y1}L{x2} {y2}"
                edges.append(f'<path d="{d}" class="edge"/>')
                if rnd.random() < 0.45:
                    col = [CYAN, INDIGO, VIOLET][li]
                    dur = 2.2 + rnd.random() * 1.6
                    delay = rnd.random() * 3
                    pulses.append(
                        f'<path d="{d}" pathLength="100" class="pulse" stroke="{col}" '
                        f'style="animation-duration:{dur:.2f}s;animation-delay:-{delay:.2f}s"/>'
                    )
    nodes = []
    for li, (x, ys) in enumerate(layers):
        col = [CYAN, SKY, INDIGO, VIOLET][li]
        for ni, y in enumerate(ys):
            delay = (li * 0.35 + ni * 0.18) % 2.4
            nodes.append(
                f'<circle cx="{x}" cy="{y}" r="15" fill="{col}" class="halo" style="animation-delay:{delay:.2f}s"/>'
                f'<circle cx="{x}" cy="{y}" r="8" fill="{CARD}" stroke="{col}" stroke-width="2.5"/>'
                f'<circle cx="{x}" cy="{y}" r="3" fill="{col}"/>'
            )
    # data packets streaming into the input layer (data -> AI)
    stream = []
    for i, y in enumerate([100, 160, 220, 280]):
        for k in range(3):
            delay = i * 0.4 + k * 1.1
            stream.append(
                f'<rect x="652" y="{y-3}" width="6" height="6" rx="1.5" fill="{CYAN}" class="packet" '
                f'style="animation-delay:{delay:.2f}s"/>'
            )
        stream.append(f'<path d="M640 {y}H788" stroke="{LINE2}" stroke-dasharray="2 6"/>')

    steps = ["collect", "clean", "store", "model", "ship"]
    step_cols = [CYAN, SKY, INDIGO, VIOLET, GREEN]
    chips, x = [], 270
    for i, (s, c) in enumerate(zip(steps, step_cols)):
        chips.append(
            f'<g class="step" style="animation-delay:{i*0.7:.1f}s">'
            f'<circle cx="{x}" cy="291" r="4" fill="{c}"/>'
            f'<text x="{x+10}" y="296" class="mono" font-size="14" fill="{SOFT}">{s}</text></g>'
        )
        x += 22 + len(s) * 8.6 + 12

    css = f"""
  .edge {{ stroke: {LINE2}; stroke-width: 1; opacity: .55; fill: none; }}
  .pulse {{ fill: none; stroke-width: 2.2; stroke-linecap: round; stroke-dasharray: 9 91;
           animation: flow linear infinite; }}
  @keyframes flow {{ from {{ stroke-dashoffset: 100; }} to {{ stroke-dashoffset: 0; }} }}
  .halo {{ opacity: 0; transform-box: fill-box; transform-origin: center; animation: halo 2.4s ease-out infinite; }}
  @keyframes halo {{ 0% {{ opacity: .45; transform: scale(.4); }} 70%,100% {{ opacity: 0; transform: scale(1.35); }} }}
  .packet {{ opacity: 0; animation: packet 3.3s linear infinite; }}
  @keyframes packet {{ 0% {{ opacity: 0; transform: translateX(0); }} 15% {{ opacity: 1; }}
                       85% {{ opacity: 1; }} 100% {{ opacity: 0; transform: translateX(128px); }} }}
  .step {{ opacity: .25; animation: step 3.5s ease-in-out infinite; }}
  @keyframes step {{ 0%,100% {{ opacity: .3; }} 20%,60% {{ opacity: 1; }} }}
  .type {{ transform-box: fill-box; transform-origin: left; animation: type 2.4s steps(40) .3s both; }}
  @keyframes type {{ from {{ transform: scaleX(0); }} to {{ transform: scaleX(1); }} }}
  .caret {{ animation: blink 1s steps(1) infinite; }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
  .rise {{ animation: rise .9s cubic-bezier(.2,.7,.2,1) both; }}
  @keyframes rise {{ from {{ opacity: 0; transform: translateY(14px); }} to {{ opacity: 1; transform: none; }} }}
  .glow {{ animation: glow 5s ease-in-out infinite; }}
  @keyframes glow {{ 0%,100% {{ opacity: .35; }} 50% {{ opacity: .7; }} }}
"""
    defs = frame_defs(W, H) + f"""
  <radialGradient id="orbC" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{CYAN}" stop-opacity=".35"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
  <radialGradient id="orbV" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".35"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>
  <clipPath id="typeClip"><rect class="type" x="64" y="186" width="620" height="60"/></clipPath>
"""
    inner = f"""
  <circle cx="140" cy="40" r="260" fill="url(#orbC)" class="glow"/>
  <circle cx="1040" cy="300" r="300" fill="url(#orbV)" class="glow" style="animation-delay:-2.5s"/>
  <g class="rise">
    <text x="64" y="92" class="mono" font-size="15" letter-spacing="3" fill="{CYAN}">AI ENGINEER <tspan fill="{MUTED}">·</tspan> <tspan fill="{VIOLET}">DATA ENGINEER</tspan></text>
    <text x="62" y="156" class="sans" font-size="54" font-weight="800" fill="url(#brandShift)">Harshavardhan Reddy</text>
  </g>
  <g clip-path="url(#typeClip)">
    <text x="64" y="204" class="sans" font-size="21" fill="{TEXT}">I build data pipelines and AI systems that run on their own.</text>
    <text x="64" y="234" class="sans" font-size="17" fill="{MUTED}">Raw data in, working product out: collect, clean, store, model, ship.</text>
  </g>
  <g class="rise" style="animation-delay:.6s">
    <rect x="64" y="266" width="584" height="42" rx="10" fill="{CARD}" stroke="{LINE2}"/>
    <text x="82" y="293" class="mono" font-size="14" fill="{GREEN}">$</text>
    <text x="98" y="293" class="mono" font-size="14" fill="{SOFT}">run pipeline</text>
    <text x="216" y="293" class="mono" font-size="14" fill="{MUTED}">&#8594;</text>
    {''.join(chips)}
  </g>
  {''.join(stream)}
  {''.join(edges)}
  {''.join(pulses)}
  {''.join(nodes)}
  <text x="800" y="330" class="mono" font-size="11" fill="{MUTED}" text-anchor="middle">data in</text>
  <text x="1120" y="262" class="mono" font-size="11" fill="{MUTED}" text-anchor="middle">insight out</text>
"""
    (OUT / "hero.svg").write_text(
        svg(W, H, frame(W, H, inner), css, defs,
            "Harshavardhan Reddy, AI Engineer and Data Engineer. I build data pipelines and AI systems that run on their own."),
        encoding="utf-8")


# ------------------------------------------------------------------ section header
def header(slug, num, title, sub, light=False):
    W, H = 1200, 76
    acc, ttl, sb = ("#0891B2", "#0F172A", "#475569") if light else (CYAN, TEXT, MUTED)
    css = f"""
  .bar {{ transform-box: fill-box; transform-origin: left; animation: grow 1.6s cubic-bezier(.2,.7,.2,1) both; }}
  @keyframes grow {{ from {{ transform: scaleX(0); }} to {{ transform: scaleX(1); }} }}
  .dot {{ animation: blink 2s ease-in-out infinite; }}
  @keyframes blink {{ 50% {{ opacity: .25; }} }}
"""
    defs = f"""
  <linearGradient id="brand" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{CYAN}"/><stop offset=".5" stop-color="{INDIGO}"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/>
  </linearGradient>"""
    body = f"""
  <circle cx="10" cy="30" r="5" fill="{acc}" class="dot"/>
  <text x="26" y="37" class="mono" font-size="15" letter-spacing="2" fill="{acc}">{num}</text>
  <text x="60" y="38" class="sans" font-size="28" font-weight="700" fill="{ttl}">{escape(title)}</text>
  <text x="62" y="62" class="sans" font-size="15" fill="{sb}">{escape(sub)}</text>
  <rect x="0" y="73" width="1200" height="3" rx="1.5" fill="url(#brand)" class="bar"/>
"""
    (OUT / f"h-{slug}{'-light' if light else ''}.svg").write_text(svg(W, H, body, css, defs, f"{title}. {sub}"), encoding="utf-8")


# ------------------------------------------------------------------------ workflow
ICONS = {
    "collect": '<path d="M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2"/><path d="M7 11l5 5l5-5"/><path d="M12 4v12"/>',
    "clean": '<path d="M4 4h16v2.17a2 2 0 0 1-.59 1.42L15 12v7l-6 2v-8.5L4.52 7.57A2 2 0 0 1 4 6.23z"/>',
    "store": '<ellipse cx="12" cy="6" rx="8" ry="3"/><path d="M4 6v6a8 3 0 0 0 16 0V6"/><path d="M4 12v6a8 3 0 0 0 16 0v-6"/>',
    "model": '<rect x="5" y="5" width="14" height="14" rx="2"/><rect x="9" y="9" width="6" height="6" rx="1"/>'
             '<path d="M3 10h2M3 14h2M10 3v2M14 3v2M21 10h-2M21 14h-2M14 21v-2M10 21v-2"/>',
    "ship": '<path d="M4 13a8 8 0 0 1 7 7a6 6 0 0 0 3-5a9 9 0 0 0 6-8a3 3 0 0 0-3-3a9 9 0 0 0-8 6a6 6 0 0 0-5 3"/>'
            '<path d="M7 14a6 6 0 0 0-3 6a6 6 0 0 0 6-3"/><circle cx="15" cy="9" r="1"/>',
}


def workflow():
    W, H = 1200, 400
    stages = [
        ("collect", "01", "Collect", "Pull data in", ["APIs · RSS · scrapers", "Playwright · Puppeteer", "schedulers · cron"], CYAN),
        ("clean", "02", "Clean", "Make it trustworthy", ["Pandas · PySpark", "validation · dedupe", "ETL jobs"], SKY),
        ("store", "03", "Store", "Keep it findable", ["PostgreSQL · pgvector", "SQLite · Supabase", "MongoDB · MySQL"], INDIGO),
        ("model", "04", "Model", "Make it smart", ["LLMs · RAG · agents", "BERT · LSTM · CNN", "scikit-learn · XGBoost"], VIOLET),
        ("ship", "05", "Ship", "Put it to work", ["FastAPI · Docker", "AWS · Vercel", "GitHub Actions"], GREEN),
    ]
    cw, ch, gap, x0, y0 = 196, 196, 44, 22, 96
    cards, links = [], []
    for i, (key, num, title, sub, tools, col) in enumerate(stages):
        x = x0 + i * (cw + gap)
        tl = "".join(
            f'<text x="{x+20}" y="{y0+128+j*22}" class="mono" font-size="12.5" fill="{SOFT}">{escape(t)}</text>'
            for j, t in enumerate(tools))
        cards.append(f"""
  <g>
    <rect x="{x}" y="{y0}" width="{cw}" height="{ch}" rx="14" fill="{CARD}" stroke="{LINE2}"/>
    <rect x="{x}" y="{y0}" width="{cw}" height="{ch}" rx="14" fill="none" stroke="{col}" stroke-width="2" class="lit" style="animation-delay:{i*0.8:.1f}s"/>
    <rect x="{x}" y="{y0}" width="{cw}" height="4" rx="2" fill="{col}"/>
    <g transform="translate({x+20} {y0+24}) scale(1.35)" fill="none" stroke="{col}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICONS[key]}</g>
    <text x="{x+cw-20}" y="{y0+42}" class="mono" font-size="13" fill="{MUTED}" text-anchor="end">{num}</text>
    <text x="{x+20}" y="{y0+86}" class="sans" font-size="22" font-weight="700" fill="{TEXT}">{title}</text>
    <text x="{x+20}" y="{y0+106}" class="sans" font-size="14" fill="{MUTED}">{sub}</text>
    {tl}
  </g>""")
        if i < len(stages) - 1:
            ax = x + cw
            links.append(
                f'<path d="M{ax+6} {y0+ch/2}H{ax+gap-6}" stroke="{LINE2}" stroke-width="2"/>'
                f'<path d="M{ax+gap-12} {y0+ch/2-5}l6 5l-6 5" fill="none" stroke="{LINE2}" stroke-width="2"/>')
    # packets travelling along the whole line
    track = f"M{x0+cw} {y0+ch/2}H{x0+4*(cw+gap)}"
    packets = "".join(
        f'<circle r="4.5" fill="{c}"><animateMotion dur="5s" begin="{-k*1.25}s" repeatCount="indefinite" path="{track}"/></circle>'
        for k, c in enumerate([CYAN, SKY, INDIGO, VIOLET]))
    # feedback loop: ship -> collect
    lx1, lx2, ly = x0 + cw / 2, x0 + 4 * (cw + gap) + cw / 2, y0 + ch
    loop = f"M{lx2} {ly+6}V{ly+38}H{lx1}V{ly+6}"
    feedback = f"""
  <path d="{loop}" fill="none" stroke="{LINE2}" stroke-width="2" stroke-dasharray="4 6"/>
  <path d="M{lx1-5} {ly+14}l5-6l5 6" fill="none" stroke="{LINE2}" stroke-width="2"/>
  <circle r="4" fill="{GREEN}"><animateMotion dur="6s" repeatCount="indefinite" path="{loop}"/></circle>
  <rect x="{W/2-150}" y="{ly+26}" width="300" height="26" rx="13" fill="{BG1}" stroke="{LINE2}"/>
  <text x="{W/2}" y="{ly+44}" class="mono" font-size="12.5" fill="{SOFT}" text-anchor="middle">monitor · evaluate · improve</text>"""
    # team labels
    dx2 = x0 + 3 * (cw + gap) - gap
    ax1 = x0 + 3 * (cw + gap)
    labels = f"""
  <text x="{x0}" y="44" class="mono" font-size="13" letter-spacing="3" fill="{CYAN}">DATA ENGINEERING</text>
  <path d="M{x0} 58H{dx2}" stroke="{CYAN}" stroke-width="2" stroke-linecap="round" opacity=".7"/>
  <text x="{ax1}" y="44" class="mono" font-size="13" letter-spacing="3" fill="{VIOLET}">AI ENGINEERING</text>
  <path d="M{ax1} 58H{W-x0}" stroke="{VIOLET}" stroke-width="2" stroke-linecap="round" opacity=".7"/>
  <text x="{W-x0}" y="44" class="sans" font-size="13" fill="{MUTED}" text-anchor="end">every project runs this loop</text>"""
    css = f"""
  .lit {{ opacity: 0; animation: lit 4s ease-in-out infinite; }}
  @keyframes lit {{ 0%,100% {{ opacity: 0; }} 15%,35% {{ opacity: 1; }} 55% {{ opacity: 0; }} }}
"""
    inner = labels + "".join(links) + packets + "".join(cards) + feedback
    (OUT / "workflow.svg").write_text(
        svg(W, H, frame(W, H, inner), css, frame_defs(W, H),
            "How I build: 1 Collect, 2 Clean, 3 Store (data engineering), 4 Model, 5 Ship (AI engineering), then monitor, evaluate and improve."),
        encoding="utf-8")


# --------------------------------------------------------------------- project card
def card(slug, tag, tag_col, title, lines, stack, status, status_col):
    W, H = 580, 250
    text = "".join(
        f'<text x="28" y="{124+i*24}" class="sans" font-size="16" fill="{SOFT}">{escape(l)}</text>'
        for i, l in enumerate(lines))
    chips, x = [], 28
    for s in stack:
        w = len(s) * 7.4 + 22
        chips.append(
            f'<rect x="{x}" y="196" width="{w:.0f}" height="28" rx="14" fill="{BG1}" stroke="{LINE2}"/>'
            f'<text x="{x + w/2:.0f}" y="215" class="mono" font-size="12" fill="{SOFT}" text-anchor="middle">{escape(s)}</text>')
        x += w + 8
    sw = len(status) * 7.6 + 34
    css = f"""
  .sweep {{ animation: sweep 4s ease-in-out infinite; }}
  @keyframes sweep {{ 0% {{ transform: translateX(-200px); }} 60%,100% {{ transform: translateX({W+200}px); }} }}
  .live {{ animation: blink 1.8s ease-in-out infinite; }}
  @keyframes blink {{ 50% {{ opacity: .3; }} }}
"""
    defs = frame_defs(W, H) + f"""
  <linearGradient id="shine" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{tag_col}"/><stop offset="1" stop-color="{VIOLET if tag_col != VIOLET else CYAN}"/>
  </linearGradient>"""
    inner = f"""
  <rect width="{W}" height="4" fill="url(#accent)"/>
  <rect x="0" y="0" width="160" height="4" fill="url(#shine)" class="sweep" opacity=".8"/>
  <rect x="28" y="30" width="{len(tag)*8.4+24:.0f}" height="26" rx="6" fill="{tag_col}" fill-opacity=".14" stroke="{tag_col}" stroke-opacity=".5"/>
  <text x="40" y="48" class="mono" font-size="12" letter-spacing="1.5" font-weight="700" fill="{tag_col}">{escape(tag)}</text>
  <rect x="{W-28-sw:.0f}" y="30" width="{sw:.0f}" height="26" rx="13" fill="{status_col}" fill-opacity=".12" stroke="{status_col}" stroke-opacity=".5"/>
  <circle cx="{W-28-sw+15:.0f}" cy="43" r="4" fill="{status_col}" class="live"/>
  <text x="{W-28-sw+25:.0f}" y="47.5" class="mono" font-size="12" fill="{status_col}">{escape(status)}</text>
  <text x="28" y="94" class="sans" font-size="26" font-weight="700" fill="{TEXT}">{escape(title)}</text>
  {text}
  {''.join(chips)}
"""
    (OUT / f"p-{slug}.svg").write_text(
        svg(W, H, frame(W, H, inner), css, defs, f"{title}: {' '.join(lines)} Built with {', '.join(stack)}."),
        encoding="utf-8")


# --------------------------------------------------------------------------- stack
def stack():
    W, H = 1200, 300
    groups = [
        ("AI & MACHINE LEARNING", CYAN if False else VIOLET,
         ["LLMs · prompt design", "RAG · vector search", "AI agents · tool calling", "BERT · LSTM · CNN", "scikit-learn · XGBoost"]),
        ("GENERATIVE & LOCAL AI", PURPLE,
         ["Claude · Gemini · Ollama", "Hugging Face · Diffusers", "LangChain · LlamaIndex", "Whisper · TTS", "FLUX · Stable Diffusion"]),
        ("DATA ENGINEERING", CYAN,
         ["Python · SQL", "Pandas · PySpark", "Kafka · ETL pipelines", "PostgreSQL · pgvector", "Power BI · dashboards"]),
        ("BACKEND & CLOUD", GREEN,
         ["FastAPI · Flask", "Celery · Redis", "Docker", "AWS (EC2 · Lambda · S3)", "GitHub Actions · Vercel"]),
    ]
    gw, gap, x0 = 276, 18, 24
    cols = []
    for i, (name, col, items) in enumerate(groups):
        x = x0 + i * (gw + gap)
        rows = "".join(
            f'<circle cx="{x+26}" cy="{98+j*36}" r="3.5" fill="{col}" class="b" style="animation-delay:{(i*5+j)*0.15:.2f}s"/>'
            f'<text x="{x+40}" y="{103+j*36}" class="sans" font-size="15.5" fill="{SOFT}">{escape(t)}</text>'
            for j, t in enumerate(items))
        cols.append(f"""
  <rect x="{x}" y="24" width="{gw}" height="252" rx="14" fill="{CARD}" stroke="{LINE2}"/>
  <rect x="{x}" y="24" width="{gw}" height="4" rx="2" fill="{col}"/>
  <text x="{x+20}" y="62" class="mono" font-size="12.5" font-weight="700" letter-spacing="2" fill="{col}">{escape(name)}</text>
  {rows}""")
    css = """
  .b { animation: b 3s ease-in-out infinite; }
  @keyframes b { 0%,100% { opacity: 1; } 50% { opacity: .3; } }
"""
    (OUT / "stack.svg").write_text(
        svg(W, H, frame(W, H, "".join(cols)), css, frame_defs(W, H),
            "Skills: " + "; ".join(f"{g[0].title()}: {', '.join(g[2])}" for g in groups)),
        encoding="utf-8")


# -------------------------------------------------------------------------- footer
def footer():
    W, H = 1200, 150
    waves = []
    for i, (col, amp, dur, op) in enumerate([(CYAN, 14, 9, .55), (INDIGO, 18, 12, .4), (VIOLET, 10, 7, .5)]):
        pts = " ".join(f"L{x} {90 + amp*math.sin((x/2400)*math.pi*8 + i):.1f}" for x in range(0, 2401, 20))
        waves.append(
            f'<path d="M0 90 {pts}" fill="none" stroke="{col}" stroke-width="2" opacity="{op}" class="w" style="animation-duration:{dur}s"/>')
    css = """
  .w { animation: w linear infinite; }
  @keyframes w { from { transform: translateX(0); } to { transform: translateX(-1200px); } }
"""
    inner = f"""
  {''.join(waves)}
  <text x="{W/2}" y="52" class="sans" font-size="22" font-weight="700" fill="{TEXT}" text-anchor="middle">Thanks for stopping by.</text>
  <text x="{W/2}" y="134" class="mono" font-size="13" fill="{MUTED}" text-anchor="middle">data in · intelligence out · always learning</text>
"""
    (OUT / "footer.svg").write_text(
        svg(W, H, frame(W, H, inner), css, frame_defs(W, H), "Thanks for stopping by."), encoding="utf-8")


# ----------------------------------------------------------------------- icon wall
SIMPLE_ICONS = "https://cdn.jsdelivr.net/npm/simple-icons@13.21.0"
ICON_ROWS = [
    ("AI & LLMS", VIOLET, [
        ("huggingface", "Hugging Face"), ("langchain", "LangChain"), ("ollama", "Ollama"), ("anthropic", "Claude"),
        ("googlegemini", "Gemini"), ("pytorch", "PyTorch"), ("tensorflow", "TensorFlow"), ("scikitlearn", "scikit-learn")]),
    ("DATA", CYAN, [
        ("python", "Python"), ("pandas", "Pandas"), ("numpy", "NumPy"), ("jupyter", "Jupyter"),
        ("apachespark", "Spark"), ("apachekafka", "Kafka"), ("postgresql", "PostgreSQL"), ("sqlite", "SQLite"),
        ("supabase", "Supabase"), ("mongodb", "MongoDB"), ("redis", "Redis"), ("sqlalchemy", "SQLAlchemy")]),
    ("SHIP", GREEN, [
        ("fastapi", "FastAPI"), ("flask", "Flask"), ("celery", "Celery"), ("docker", "Docker"),
        ("amazonwebservices", "AWS"), ("awslambda", "Lambda"), ("amazons3", "S3"), ("githubactions", "Actions"),
        ("vercel", "Vercel"), ("puppeteer", "Puppeteer"), ("react", "React"), ("tailwindcss", "Tailwind"),
        ("chartdotjs", "Chart.js")]),
]


def icon_wall():
    import json
    import re
    import urllib.request

    def get(url):
        with urllib.request.urlopen(url) as r:
            return r.read().decode("utf-8")

    meta = json.loads(get(f"{SIMPLE_ICONS}/_data/simple-icons.json"))
    meta = meta["icons"] if isinstance(meta, dict) else meta
    colors = {}
    for m in meta:
        slug = m.get("slug") or re.sub(r"[^a-z0-9]", "", m["title"].lower().replace("+", "plus").replace(".", "dot"))
        colors[slug] = "#" + m["hex"]

    def readable(hexcol):
        # near-black brand colors vanish on the dark tile, so fall back to the soft text color
        r, g, b = (int(hexcol[i:i + 2], 16) / 255 for i in (1, 3, 5))
        return hexcol if 0.2126 * r + 0.7152 * g + 0.0722 * b > 0.28 else SOFT

    W, tile, gap = 1200, 72, 16
    rows_svg, y = [], 30
    for ri, (label, col, items) in enumerate(ICON_ROWS):
        rows_svg.append(
            f'<text x="24" y="{y+12}" class="mono" font-size="12.5" font-weight="700" letter-spacing="2" fill="{col}">{escape(label)}</text>'
            f'<path d="M24 {y+22}H{W-24}" stroke="{LINE}" />')
        y += 38
        total = len(items) * tile + (len(items) - 1) * gap
        x0 = (W - total) / 2
        for ci, (slug, name) in enumerate(items):
            path = re.search(r'<path d="([^"]+)"', get(f"{SIMPLE_ICONS}/icons/{slug}.svg")).group(1)
            c = readable(colors[slug])
            x = x0 + ci * (tile + gap)
            delay = ci * 0.12 + ri * 0.35
            rows_svg.append(f"""
  <g class="rise" style="animation-delay:{delay*0.5:.2f}s">
    <rect x="{x:.1f}" y="{y}" width="{tile}" height="{tile}" rx="16" fill="{CARD}" stroke="{LINE2}"/>
    <rect x="{x:.1f}" y="{y}" width="{tile}" height="{tile}" rx="16" fill="{c}" fill-opacity=".10" stroke="{c}" stroke-width="1.5" class="lit" style="animation-delay:{delay:.2f}s"/>
    <g transform="translate({x + (tile-32)/2:.1f} {y + (tile-32)/2}) scale({32/24:.4f})"><path d="{path}" fill="{c}"/></g>
    <text x="{x + tile/2:.1f}" y="{y+tile+18}" class="sans" font-size="12" fill="{SOFT}" text-anchor="middle">{escape(name)}</text>
  </g>""")
        y += tile + 44
    H = y - 10
    css = """
  .lit { opacity: 0; animation: lit 5s ease-in-out infinite; }
  @keyframes lit { 0%,100% { opacity: 0; } 12%,28% { opacity: 1; } 45% { opacity: 0; } }
  .rise { animation: rise .7s cubic-bezier(.2,.7,.2,1) both; }
  @keyframes rise { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: none; } }
"""
    names = "; ".join(f"{label.title()}: {', '.join(n for _, n in items)}" for label, _, items in ICON_ROWS)
    (OUT / "icons.svg").write_text(
        svg(W, H, frame(W, H, "".join(rows_svg)), css, frame_defs(W, H), f"Tools: {names}"), encoding="utf-8")


if __name__ == "__main__":
    hero()
    workflow()
    stack()
    footer()
    icon_wall()
    for args in [
        ("about", "01", "About me", "Who I am and what I'm working on right now"),
        ("workflow", "02", "How I build", "The same five steps behind every project"),
        ("projects", "03", "What I've built", "Public and private work, newest first"),
        ("stack", "04", "Tools I use", "Grouped by the job they do"),
        ("stats", "05", "Activity", "Live numbers from GitHub"),
        ("contact", "06", "Let's talk", "Open to AI and data engineering roles and projects"),
    ]:
        header(*args)
        header(*args, light=True)
    PRIVATE, LIVE, PUBLIC = AMBER, GREEN, SKY
    for args in [
        ("aura", "AI AGENT", VIOLET, "AURA",
         ["A personal AI that remembers your decisions,", "why you made them, and plans your next day."],
         ["FastAPI", "pgvector", "Celery", "Ollama", "React"], "Open source", PUBLIC),
        ("jarvis", "LOCAL AI", PURPLE, "MARK XL · JARVIS",
         ["A voice assistant that runs fully on your own", "computer. Listens, thinks, acts. No cloud."],
         ["Whisper", "Ollama", "tool calling", "TTS"], "Private repo", PRIVATE),
        ("autopilot", "AI AUTOMATION", VIOLET, "Social Autopilot",
         ["Writes, fact-checks and posts one LinkedIn and", "X post a day. 8 quality gates before it posts."],
         ["Claude", "FLUX.2", "Real-ESRGAN", "Chromium"], "Private repo", PRIVATE),
        ("weekly", "DATA PIPELINE", CYAN, "AI Weekly Monitor",
         ["Reads 25+ AI news feeds every Monday, keeps", "the real launches and publishes a report."],
         ["Gemini", "Puppeteer", "GitHub Actions"], "Live site", LIVE),
        ("weather", "DATA ENGINEERING", CYAN, "Weather Data Pipeline",
         ["Collects weather data on a schedule, keeps the", "history and shows it on a live dashboard."],
         ["FastAPI", "APScheduler", "SQLAlchemy", "React"], "Open source", PUBLIC),
        ("rag", "GENERATIVE AI", VIOLET, "RAG, built by hand",
         ["Answers questions from your own documents.", "Compares hand-built search with LangChain."],
         ["FAISS", "BM25", "embeddings", "FastAPI"], "Open source", PUBLIC),
        ("medical", "NLP", PURPLE, "Medical Report NER",
         ["Summarises medical reports and pulls out", "diseases and drugs. ROUGE-L score of 0.41."],
         ["BERT", "LSTM seq2seq", "FastAPI"], "Open source", PUBLIC),
        ("reel", "DATA ANALYTICS", CYAN, "Reel Register",
         ["Audits a library of video lessons: speaking", "pace, silences, broken captions, duplicates."],
         ["Python", "speech analysis", "JavaScript"], "Live demo", LIVE),
    ]:
        card(*args)
    print("wrote", sorted(p.name for p in OUT.iterdir()))
