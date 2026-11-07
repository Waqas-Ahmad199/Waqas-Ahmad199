#!/usr/bin/env python3
"""Calculates days on GitHub, repositories, contributions and streak, then writes assets/stats.svg.
Runs daily in GitHub Actions (uses GITHUB_TOKEN). Standard library only."""
import json, os, sys, urllib.request
from datetime import date, datetime
from pathlib import Path

LOGIN = os.environ.get("GH_LOGIN", "Waqas-Ahmad199")
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
OUT = Path(__file__).resolve().parent.parent / "assets/stats.svg"

QUERY = """query($l:String!){user(login:$l){createdAt followers{totalCount}
repositories(ownerAffiliations:OWNER){totalCount}
contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}}}"""

def api(url, data=None):
    req = urllib.request.Request(url, data=data, headers={"Accept": "application/vnd.github+json", "User-Agent": "profile-stats",
        **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {})})
    return json.load(urllib.request.urlopen(req, timeout=30))

def fetch():
    if TOKEN:
        u = api("https://api.github.com/graphql", json.dumps({"query": QUERY, "variables": {"l": LOGIN}}).encode())["data"]["user"]
        cal = u["contributionsCollection"]["contributionCalendar"]
        days = sorted((d["date"], d["contributionCount"]) for w in cal["weeks"] for d in w["contributionDays"])
        streak = 0
        for i, (_, n) in enumerate(reversed(days)):
            if n: streak += 1
            elif i: break          # today may still be empty
        return u["createdAt"], u["repositories"]["totalCount"], cal["totalContributions"], streak
    u = api(f"https://api.github.com/users/{LOGIN}")   # fallback: no contributions without a token
    return u["created_at"], u["public_repos"], None, None

def main():
    try:
        created, repos, contrib, streak = fetch()
        days = (date.today() - datetime.fromisoformat(created.replace("Z", "+00:00")).date()).days
    except Exception as e:
        print("stats fetch failed:", e, file=sys.stderr); days = repos = contrib = streak = None
    f = lambda v: "-" if v is None else f"{v:,}"
    cards = [(f(days), "Days on GitHub", min((days or 0) / 1095, 1)), (f(repos), "Repositories", min((repos or 0) / 30, 1)),
             (f(contrib), "Contributions, last 12 months", min((contrib or 0) / 1000, 1)), (f(streak), "Current streak, days", min((streak or 0) / 30, 1))]
    body = ""
    for i, (v, label, p) in enumerate(cards):
        x = 20 + i * 305
        body += f'''<g class="c" style="animation-delay:{i*.18}s"><rect x="{x}" y="20" width="285" height="150" rx="14" fill="#0b1a33" stroke="#d4af37" stroke-opacity=".35"/>
<text x="{x+24}" y="88" class="n">{v}</text><text x="{x+24}" y="116" class="l">{label}</text>
<rect x="{x+24}" y="136" width="237" height="4" rx="2" fill="#fff" fill-opacity=".08"/>
<rect x="{x+24}" y="136" height="4" rx="2" fill="#d4af37" class="b" style="--w:{237*p:.0f}px;animation-delay:{.5+i*.18}s"/></g>'''
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1240 190" width="1240" height="190" role="img" aria-label="GitHub activity summary">
<style>.n{{font:700 48px Georgia,serif;fill:#f4efe3}}.l{{font:15px 'Segoe UI',Arial,sans-serif;fill:#9aa9c2}}
.c{{opacity:0;animation:u .8s cubic-bezier(.2,.7,.2,1) forwards}}@keyframes u{{from{{opacity:0;transform:translateY(18px)}}to{{opacity:1;transform:none}}}}
.b{{width:0;animation:w 1.4s ease-out forwards}}@keyframes w{{to{{width:var(--w)}}}}</style>{body}</svg>'''
    OUT.write_text(svg, encoding="utf-8"); print("stats.svg:", days, repos, contrib, streak)

main()
