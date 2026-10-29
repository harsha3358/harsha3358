"""Draw assets/stats.svg from live GitHub data.

Runs daily from .github/workflows/stats.yml. Needs GITHUB_TOKEN in the environment.
Set INCLUDE_PRIVATE=1 (with a token that can see private repos) to count private repos too.
Standard library only.
"""
import json
import os
import urllib.request
from datetime import date
from pathlib import Path

LOGIN = "harsha3358"
OUT = Path(__file__).resolve().parent.parent / "assets" / "stats.svg"

BG0, BG1, CARD, LINE2 = "#060A13", "#0B1222", "#0F172A", "#334155"
TEXT, SOFT, MUTED = "#F1F5F9", "#CBD5E1", "#94A3B8"
RAMP = ["#22D3EE", "#38BDF8", "#818CF8", "#A78BFA", "#C084FC", "#34D399"]
SANS = "'Segoe UI', Inter, -apple-system, 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', 'Cascadia Code', Consolas, 'SF Mono', Menlo, monospace"

QUERY = """
query($login: String!, $privacy: RepositoryPrivacy) {
  user(login: $login) {
    followers { totalCount }
    contributionsCollection {
      contributionCalendar { totalContributions weeks { contributionDays { contributionCount } } }
    }
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false, privacy: $privacy) {
      totalCount
      nodes {
        primaryLanguage { name }
      }
    }
  }
}"""


def fetch():
    privacy = None if os.environ.get("INCLUDE_PRIVATE") == "1" else "PUBLIC"
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": LOGIN, "privacy": privacy}}).encode(),
        headers={"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as r:
        body = json.load(r)
    if "errors" in body:
        raise SystemExit(body["errors"])
    return body["data"]["user"], privacy is None


def draw(user, with_private):
    cal = user["contributionsCollection"]["contributionCalendar"]
    weeks = [sum(d["contributionCount"] for d in w["contributionDays"]) for w in cal["weeks"]][-52:]
    repos = user["repositories"]
    active = sum(1 for w in weeks if w)
    langs = {}
    # Count repos by main language: byte counts let generated HTML reports drown out the Python
    for n in repos["nodes"]:
        if n["primaryLanguage"]:
            name = n["primaryLanguage"]["name"]
            langs[name] = langs.get(name, 0) + 1
    top = sorted(langs.items(), key=lambda kv: -kv[1])[:6]
    total = sum(v for _, v in top) or 1

    W, H = 1200, 340
    tiles = [
        (f"{cal['totalContributions']:,}", "contributions this year"),
        (f"{repos['totalCount']}", "repositories" if with_private else "public repositories"),
        (f"{active}/{len(weeks)}", "weeks with contributions"),
        (f"{user['followers']['totalCount']}", "followers"),
    ]
    tile_svg = ""
    for i, (num, label) in enumerate(tiles):
        x, y = 24 + (i % 2) * 262, 68 + (i // 2) * 82
        tile_svg += (
            f'<g class="rise" style="animation-delay:{i*0.12:.2f}s">'
            f'<rect x="{x}" y="{y}" width="250" height="70" rx="12" fill="{CARD}" stroke="{LINE2}"/>'
            f'<rect x="{x}" y="{y+16}" width="3" height="38" rx="1.5" fill="{RAMP[i]}"/>'
            f'<text x="{x+20}" y="{y+38}" font-family="{SANS}" font-size="28" font-weight="800" fill="{TEXT}">{num}</text>'
            f'<text x="{x+20}" y="{y+58}" font-family="{SANS}" font-size="13" fill="{MUTED}">{label}</text></g>'
        )

    bx, bw = 572, 604
    seg, legend, x = "", "", bx
    for i, (name, size) in enumerate(top):
        w = bw * size / total
        seg += f'<rect x="{x:.1f}" y="92" width="{w:.1f}" height="14" fill="{RAMP[i]}"/>'
        x += w
        lx, ly = bx + (i % 2) * 302, 140 + (i // 2) * 30
        legend += (
            f'<circle cx="{lx+6}" cy="{ly-5}" r="5" fill="{RAMP[i]}"/>'
            f'<text x="{lx+20}" y="{ly}" font-family="{SANS}" font-size="15" fill="{SOFT}">{name}</text>'
            f'<text x="{lx+280}" y="{ly}" font-family="{MONO}" font-size="13" fill="{MUTED}" text-anchor="end">{size} repos</text>'
        )

    peak = max(weeks) or 1
    bars = ""
    step = 1152 / len(weeks)
    for i, c in enumerate(weeks):
        h = max(2, 56 * c / peak)
        bars += (
            f'<rect x="{24 + i*step + 2:.1f}" y="{318-h:.1f}" width="{step-5:.1f}" height="{h:.1f}" rx="2" '
            f'fill="url(#ramp)" class="grow" style="animation-delay:{i*0.018:.3f}s"><title>{c}</title></rect>'
        )

    scope = "public + private repos" if with_private else "public repos"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="GitHub activity: {cal['totalContributions']} contributions this year, {repos['totalCount']} repositories, active {active} of {len(weeks)} weeks">
<title>GitHub activity for {LOGIN}</title>
<style>
  .rise {{ animation: rise .8s cubic-bezier(.2,.7,.2,1) both; }}
  @keyframes rise {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: none; }} }}
  .bar {{ transform-box: fill-box; transform-origin: left; animation: wide 1.4s cubic-bezier(.2,.7,.2,1) .3s both; }}
  @keyframes wide {{ from {{ transform: scaleX(0); }} to {{ transform: scaleX(1); }} }}
  .grow {{ transform-box: fill-box; transform-origin: bottom; animation: grow .7s cubic-bezier(.2,.7,.2,1) both; }}
  @keyframes grow {{ from {{ transform: scaleY(0); }} to {{ transform: scaleY(1); }} }}
  @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
</style>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG0}"/><stop offset="1" stop-color="{BG1}"/></linearGradient>
  <linearGradient id="ramp" x1="24" y1="0" x2="1176" y2="0" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{RAMP[0]}"/><stop offset=".5" stop-color="{RAMP[2]}"/><stop offset="1" stop-color="{RAMP[3]}"/></linearGradient>
  <clipPath id="round"><rect width="{W}" height="{H}" rx="18"/></clipPath>
  <clipPath id="barclip"><rect x="{bx}" y="92" width="{bw}" height="14" rx="7"/></clipPath>
</defs>
<g clip-path="url(#round)"><rect width="{W}" height="{H}" fill="url(#bg)"/></g>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="18" fill="none" stroke="{LINE2}"/>
<text x="24" y="44" font-family="{MONO}" font-size="13" letter-spacing="3" fill="{RAMP[0]}">LAST 12 MONTHS</text>
<text x="{bx}" y="44" font-family="{MONO}" font-size="13" letter-spacing="3" fill="{RAMP[3]}">LANGUAGES I WRITE MOST</text>
<text x="1176" y="44" font-family="{SANS}" font-size="12" fill="{MUTED}" text-anchor="end">{scope} · updated {date.today().isoformat()}</text>
<text x="{bx}" y="78" font-family="{SANS}" font-size="13" fill="{MUTED}">main language of each project</text>
{tile_svg}
<g clip-path="url(#barclip)"><g class="bar"><rect x="{bx}" y="92" width="{bw}" height="14" fill="{CARD}"/>{seg}</g></g>
{legend}
<text x="24" y="252" font-family="{MONO}" font-size="12" letter-spacing="2" fill="{MUTED}">CONTRIBUTIONS PER WEEK</text>
<path d="M24 318.5H1176" stroke="{LINE2}"/>
{bars}
</svg>
"""


if __name__ == "__main__":
    user, with_private = fetch()
    OUT.write_text(draw(user, with_private), encoding="utf-8")
    print("wrote", OUT)
