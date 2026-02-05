#!/usr/bin/env python3
import json
import re
import textwrap
from datetime import datetime, timezone
from urllib.request import Request, urlopen

API_URL = "https://ludmil.pythonanywhere.com/my_info/"

# Portfolio colors
C_PRIMARY = "0093E9"
C_CYAN = "52E5E7"
C_TEAL = "00C9D4"
C_SOFT = "80D0C7"

def fetch_json(url: str) -> dict:
    req = Request(url, headers={"User-Agent": "github-readme-bot"})
    with urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))

def strip_html(html: str) -> str:
    if not html:
        return ""
    # Remove tags
    txt = re.sub(r"<[^>]+>", "", html)
    # Decode a few common entities
    txt = txt.replace("&nbsp;", " ").replace("&amp;", "&").replace("&quot;", '"')
    return re.sub(r"\s+", " ", txt).strip()

def pct_to_int(p: str) -> int:
    if p is None:
        return 0
    p = str(p).strip()
    p = p.replace("%", "")
    try:
        return int(float(p))
    except:
        return 0

def progress_bar(pct: int, width: int = 14) -> str:
    pct = max(0, min(100, pct))
    filled = round(width * pct / 100)
    return "█" * filled + "░" * (width - filled)

def md_escape(s: str) -> str:
    return s.replace("|", "\\|")

def build_readme(data: dict) -> str:
    info = (data.get("info") or [{}])[0] or {}
    competences = data.get("competences") or []
    experiences = data.get("experiences") or []
    projects = data.get("projects") or []
    education = data.get("education") or []

    name = info.get("name_complete") or "Ludmil Paulo"
    title_line = "Founder • Software Engineer • Full Stack Developer"

    email = info.get("email") or ""
    phone = info.get("phone") or ""
    linkedin = info.get("linkedin") or ""
    github = info.get("github") or "https://github.com/ludmilpaulo/"
    avatar = info.get("avatar") or ""
    cv = info.get("cv") or ""

    mini_about = strip_html(info.get("mini_about") or "")
    if len(mini_about) > 280:
        mini_about = mini_about[:277] + "..."

    # Pick featured projects: prefer show_in_slider, then fallback first 3
    featured = [p for p in projects if p.get("show_in_slider")]
    if not featured:
        featured = projects[:3]
    featured = featured[:4]

    # Top competences by percentage
    top_comp = sorted(
        competences,
        key=lambda c: pct_to_int(c.get("percentage")),
        reverse=True
    )[:8]

    updated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # Typing SVG (same as your portfolio vibe)
    typing_svg = (
        "https://readme-typing-svg.demolab.com"
        "?font=Inter&weight=700&size=18&duration=2600&pause=900"
        "&center=true&vCenter=true&width=900"
        "&lines=Founder+%E2%80%A2+Software+Engineer;"
        "Digital+Solutions+Expert;"
        "Full+Stack+Developer;"
        "Business+Builder;"
        "Mentor+%26+Consultant;"
        "Tech+Innovator;"
        "Problem+Solver"
    )

    # Buttons (portfolio colors)
    btn_connect = f"https://img.shields.io/badge/Let's%20Connect-{C_PRIMARY}?style=for-the-badge&logoColor=white"
    btn_work = f"https://img.shields.io/badge/See%20My%20Work-{C_TEAL}?style=for-the-badge&logoColor=white"
    btn_start = f"https://img.shields.io/badge/Start%20Project-{C_CYAN}?style=for-the-badge&logoColor=0B1B2B"

    # Build sections
    lines = []

    lines.append("<!-- AUTO-GENERATED: Do not edit by hand. Edit scripts/generate_readme.py instead. -->")
    lines.append(f"<!-- Source: {API_URL} | Updated: {updated} -->\n")

    lines.append(f'<h1 align="center">Hi, I\'m {name}</h1>\n')
    lines.append(f'<p align="center"><b>{title_line}</b></p>\n')

    lines.append('<p align="center">\n')
    lines.append(f'  ![Typing intro]({typing_svg})\n')
    lines.append('</p>\n')

    if avatar:
        lines.append(f'<p align="center"><img src="{avatar}" width="110" style="border-radius:999px;" /></p>\n')

    lines.append('<p align="center">\n')
    lines.append("  I craft scalable, user-friendly web & mobile products, help businesses grow,<br/>\n")
    lines.append("  and love solving real-world problems with code.<br/>\n")
    lines.append("  <b>Let’s build something impactful together.</b>\n")
    lines.append("</p>\n")

    # CTAs
    lines.append('<p align="center">\n')
    lines.append(f'  <a href="https://www.ludmilpaulo.co.za/#connect"><img src="{btn_connect}" /></a>\n')
    lines.append(f'  <a href="https://www.ludmilpaulo.co.za/Projects"><img src="{btn_work}" /></a>\n')
    lines.append(f'  <a href="https://www.ludmilpaulo.co.za/project-inquiry"><img src="{btn_start}" /></a>\n')
    lines.append("</p>\n")

    # Quick info row
    contact_bits = []
    if email:
        contact_bits.append(f"📧 **Email:** {email}")
    if phone:
        contact_bits.append(f"📞 **Phone:** {phone}")
    if cv:
        contact_bits.append(f"📄 **CV:** {cv}")
    if linkedin:
        contact_bits.append(f"💼 **LinkedIn:** {linkedin}")
    contact_bits.append(f"🐙 **GitHub:** {github}")

    lines.append("\n---\n")
    if mini_about:
        lines.append("## About\n")
        lines.append(f"{mini_about}\n")

    lines.append("## Contact\n")
    lines.append("\n".join([f"- {b}" for b in contact_bits]) + "\n")

    # Competences
    lines.append("\n---\n")
    lines.append("## Competences (Live)\n")
    lines.append("| Skill | Level | |\n|---|---:|---|\n")
    for c in top_comp:
        title = md_escape(c.get("title") or "Skill")
        pct = pct_to_int(c.get("percentage"))
        bar = progress_bar(pct)
        lines.append(f"| **{title}** | **{pct}%** | `{bar}` |\n")

    # Experiences (live)
    lines.append("\n---\n")
    lines.append("## Experience (Live)\n")
    for e in experiences:
        role = e.get("title") or "Role"
        company = e.get("company") or ""
        years = e.get("the_year") or ""
        desc = strip_html(e.get("description") or "")
        lines.append(f"**{role}** — *{company}*  \n{years}\n\n{desc}\n\n")

    # Featured projects from API (live)
    lines.append("\n---\n")
    lines.append("## Featured Projects (Live)\n")
    for p in featured:
        t = p.get("title") or "Project"
        demo = p.get("demo") or ""
        gh = p.get("github") or ""
        desc = strip_html(p.get("description") or "")
        if len(desc) > 220:
            desc = desc[:217] + "..."
        tools = p.get("tools") or []
        tool_titles = [x.get("title") for x in tools if x.get("title")]
        tool_str = ", ".join(tool_titles[:6]) if tool_titles else ""

        lines.append(f"### {t}\n")
        if desc:
            lines.append(f"{desc}\n\n")
        links = []
        if demo:
            links.append(f"[Live Demo]({demo})")
        if gh:
            links.append(f"[GitHub]({gh})")
        if links:
            lines.append(" • ".join(links) + "\n\n")
        if tool_str:
            lines.append(f"**Tech:** {tool_str}\n\n")

    # Education (live)
    lines.append("\n---\n")
    lines.append("## Education (Live)\n")
    for ed in education:
        t = ed.get("title") or "Education"
        y = ed.get("the_year") or ""
        d = strip_html(ed.get("description") or "")
        lines.append(f"**{t}**  \n{y}\n\n{d}\n\n")

    # GitHub stats (keep)
    lines.append("\n---\n")
    lines.append("## Live GitHub Stats\n")
    lines.append("<p align=\"center\">\n\n")
    lines.append("![GitHub Stats](https://github-readme-stats.vercel.app/api?username=ludmilpaulo&show_icons=true&include_all_commits=true&rank_icon=github&hide_border=true)\n\n")
    lines.append("![Top Languages](https://github-readme-stats.vercel.app/api/top-langs/?username=ludmilpaulo&layout=compact&hide_border=true)\n\n")
    lines.append("![GitHub Streak](https://streak-stats.demolab.com?user=ludmilpaulo&hide_border=true)\n\n")
    lines.append("</p>\n")

    lines.append(f"\n<p align=\"center\">✨ <b>Last synced from API:</b> {updated}</p>\n")
    return "".join(lines)

def main():
    data = fetch_json(API_URL)
    readme = build_readme(data)
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)

if __name__ == "__main__":
    main()
