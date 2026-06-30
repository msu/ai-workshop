#!/usr/bin/env python3
"""Build the AI workshop GitHub Pages site.

Output: repo root  (plain static HTML, no Jekyll build needed)
Generated paths: index.html, .nojekyll, assets/, sessions/, notes/

Content sources:
  - slides:   ./slides/<base>.md          (rendered into readable notes)
  - slide PDFs: ./slides/pdfs/<base>.pdf  (copied + linked)
  - summaries:  ./content/summaries/<num>.md     (optional; placeholder if absent)
  - transcripts:./content/transcripts/<num>.md   (optional; placeholder if absent)
  - topics:     ./content/topics/<num>.md        (optional; placeholder if absent)

When the YouTube transcripts become available, drop them in content/transcripts/
and write timestamped summaries in content/summaries/ (link with
https://youtu.be/<id>?t=SECONDS), then re-run this script.
"""
import re
import shutil
from pathlib import Path

import markdown

HERE = Path(__file__).resolve().parent
SLIDES = HERE / "slides"
CONTENT = HERE / "content"
WWW = HERE  # site is served from the repo root (GitHub Pages standard)

# Paths produced by the build; only these are removed on a clean rebuild so
# sources (build.py, slides/, content/) at the root are never touched.
GENERATED_DIRS = ("assets", "sessions", "notes")
GENERATED_FILES = ("index.html", ".nojekyll")

SESSIONS = [
    dict(num=1, slug="command-line-agents",
         title="Command-Line Agents",
         subtitle="Moving past the chat window",
         video="gOUW4jmGJVY", base="1_command_line_agents"),
    dict(num=2, slug="authoring-materials",
         title="Authoring AI-Friendly Materials",
         subtitle="Course materials as plain-text markdown",
         video="5i7lhEwNf_Q", base="2_authoring_materials"),
    dict(num=3, slug="building-assessments",
         title="Authoring Quizzes & Assessments",
         subtitle="Quizzes, keys, and study guides from your notes",
         video="ThDrQYSa1hs", base="3_building_assessments"),
    dict(num=4, slug="running-the-course",
         title="Using AI to Run Your Course",
         subtitle="Automation, grading, and tooling",
         video="sy7_FeHPPRo", base="4_running_the_course"),
    dict(num=5, slug="discussion-workshop",
         title="Discussion & Hands-On Workshop",
         subtitle="Student AI policy, Q&A, and pairing",
         video="qnng0s1sNaU", base="5_qa_and_handson"),
]

MD = markdown.Markdown(extensions=["fenced_code", "tables"])


def render_md(text):
    MD.reset()
    return MD.convert(text)


def fmt_ts(secs):
    secs = int(secs)
    h, m, s = secs // 3600, (secs % 3600) // 60, secs % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def linkify_topics(html, s):
    """Point rendered topic links at the internal session page (with ?t=) and
    append the timestamp to the link text."""
    href = f"sessions/{s['num']}-{s['slug']}.html"
    pat = r'<a href="https://youtu\.be/[\w-]+\?t=(\d+)">(.*?)</a>'

    def repl(m):
        secs, label = m.group(1), m.group(2)
        return (f'<a href="{href}?t={secs}">{label} '
                f'<span class="ts">{fmt_ts(secs)}</span></a>')

    return re.sub(pat, repl, html)


def parse_slides(md_text):
    """Return [{title, html}] for content slides (skips cover/end title slides)."""
    blocks, cur = [], []
    for ln in md_text.split("\n"):
        if ln.strip() == "---":
            blocks.append("\n".join(cur)); cur = []
        else:
            cur.append(ln)
    blocks.append("\n".join(cur))

    def is_frontmatter(b):
        lines = [l for l in b.split("\n") if l.strip()]
        if not lines:
            return True
        for l in lines:
            if l.lstrip().startswith(("#", "*", "|", "```", ">")):
                return False
        return any(re.match(r"^\s*[\w.]+:", l) for l in lines)

    slides, pending_layout = [], None
    for b in blocks:
        if is_frontmatter(b):
            m = re.search(r"^layout:\s*(\S+)", b, re.MULTILINE)
            pending_layout = m.group(1) if m else None
            continue
        layout = pending_layout or "two-cols"
        pending_layout = None
        if layout in ("cover", "end"):
            continue
        b = re.sub(r"<!--.*?-->", "", b, flags=re.DOTALL)
        b = re.sub(r"^::right::\s*$", "", b, flags=re.MULTILINE)
        mt = re.search(r"^##\s+(.*)$", b, re.MULTILINE)
        title = mt.group(1).strip() if mt else ""
        body = re.sub(r"^##\s+.*$", "", b, count=1, flags=re.MULTILINE).strip()
        if not title and not body:
            continue
        slides.append(dict(title=title, html=render_md(body)))
    return slides


def optional(path, placeholder_html):
    if path.exists():
        return render_md(path.read_text())
    return placeholder_html


PLACEHOLDER_SUMMARY = (
    '<p class="placeholder">A timestamped summary will be added once the '
    "recording's transcript is available.</p>"
)
PLACEHOLDER_TRANSCRIPT = (
    '<p class="placeholder">The transcript will be posted once YouTube finishes '
    "processing the recording.</p>"
)
PLACEHOLDER_TOPICS = (
    '<ul class="topics placeholder">\n'
    "      <li>Topics covered &mdash; coming soon</li>\n"
    "    </ul>"
)


def page(title, body, depth=0):
    root = "../" * depth
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="{root}assets/style.css">
</head>
<body>
<header class="site">
  <div class="wrap">
    <a class="brand" href="{root}index.html">
      <span class="brand-name">Montana State University</span>
      <span class="brand-dept">Computer Science</span>
    </a>
    <span class="brand-title">Effective AI for Educators</span>
  </div>
</header>
<main class="wrap">
{body}
</main>
<footer class="site">
  <div class="wrap">
    <p>Montana State University &middot; Gianforte School of Computing</p>
    <p>Workshop materials by Carson Gross. Recordings hosted on YouTube.</p>
  </div>
</footer>
</body>
</html>
"""


def build_index():
    rows = []
    for s in SESSIONS:
        thumb = f"https://img.youtube.com/vi/{s['video']}/hqdefault.jpg"
        href = f"sessions/{s['num']}-{s['slug']}.html"
        topics = optional(CONTENT / "topics" / f"{s['num']}.md", PLACEHOLDER_TOPICS)
        topics = topics.replace("<ul>", '<ul class="topics">', 1)
        topics = linkify_topics(topics, s)
        rows.append(f"""    <article class="row">
      <a class="thumb" href="{href}">
        <img src="{thumb}" alt="" loading="lazy">
        <span class="num">{s['num']}</span>
      </a>
      <div class="row-body">
        <h3><a href="{href}">Session {s['num']}: {s['title']}</a></h3>
        <p class="sub">{s['subtitle']}</p>
        <p class="topics-label">Topics covered</p>
        {topics}
      </div>
    </article>""")
    tldr_path = CONTENT / "tldr.md"
    tldr = ""
    if tldr_path.exists():
        tldr = (f'  <details class="tldr">\n'
                f'    <summary>TL;DR &mdash; the highest-impact, labor-saving tricks</summary>\n'
                f'    <div class="tldr-body">\n{render_md(tldr_path.read_text())}\n    </div>\n'
                f'  </details>\n')
    body = f"""  <section class="hero">
    <h1>Effective AI for Educators</h1>
    <p class="lede">A hands-on workshop on using command-line AI coding agents to
    author course materials, build assessments, and run a course. Recordings,
    notes, and transcripts for each session are collected below.</p>
  </section>
{tldr}  <section class="list">
{chr(10).join(rows)}
  </section>
"""
    (WWW / "index.html").write_text(page("Effective AI for Educators | MSU CS", body))


def build_session(s):
    slides = parse_slides((SLIDES / f"{s['base']}.md").read_text())
    notes = []
    for sl in slides:
        h = f'<h3>{sl["title"]}</h3>' if sl["title"] else ""
        notes.append(f'<article class="note">{h}\n{sl["html"]}</article>')
    notes_html = "\n".join(notes)

    summary = optional(CONTENT / "summaries" / f"{s['num']}.md", PLACEHOLDER_SUMMARY)
    transcript = optional(CONTENT / "transcripts" / f"{s['num']}.md", PLACEHOLDER_TRANSCRIPT)

    pdf_rel = f"../notes/{s['base']}.pdf"
    seek_js = (
        "<script>\n"
        "(function(){\n"
        "  var t=parseInt(new URLSearchParams(location.search).get('t'),10);\n"
        "  if(isNaN(t))return;\n"
        "  var f=document.getElementById('player');\n"
        "  f.src='https://www.youtube.com/embed/VIDEO?start='+t+'&autoplay=1';\n"
        "  var v=f.closest('.video'); if(v)v.scrollIntoView();\n"
        "})();\n"
        "</script>"
    ).replace("VIDEO", s["video"])
    body = f"""  <nav class="crumbs"><a href="../index.html">Sessions</a> / {s['title']}</nav>
  <section class="session-head">
    <span class="kicker">Session {s['num']}</span>
    <h1>{s['title']}</h1>
    <p class="lede">{s['subtitle']}</p>
  </section>

  <div class="video">
    <iframe id="player" src="https://www.youtube.com/embed/{s['video']}" title="{s['title']}"
      frameborder="0" loading="lazy"
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
      allowfullscreen></iframe>
  </div>
  {seek_js}

  <section id="summary" class="block">
    <h2>Summary</h2>
    {summary}
  </section>

  <section id="transcript" class="block">
    <h2>Transcript</h2>
    {transcript}
  </section>

  <section id="notes" class="block">
    <h2>Notes</h2>
    <p class="notes-meta">Rendered from the session slides.
      <a href="{pdf_rel}">Download slides (PDF)</a></p>
    {notes_html}
  </section>
"""
    out = WWW / "sessions" / f"{s['num']}-{s['slug']}.html"
    out.write_text(page(f"{s['title']} | MSU CS AI Workshop", body, depth=1))


STYLE = """:root{
  --blue:#00205b; --blue-2:#003a8c; --gold:#c1a875; --ink:#1b1e23;
  --muted:#5b6470; --line:#e2e5ea; --bg:#ffffff; --panel:#f6f7f9;
  --mono:"Cascadia Mono",ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  --sans:"Atkinson Hyperlegible",system-ui,-apple-system,Segoe UI,Roboto,sans-serif;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;font-family:var(--sans);color:var(--ink);background:var(--bg);line-height:1.55}
.wrap{width:min(880px,92vw);margin:0 auto}
a{color:var(--blue-2);text-decoration:none}
a:hover{text-decoration:underline}

header.site{background:var(--blue);color:#fff;border-bottom:4px solid var(--gold)}
header.site .wrap{display:flex;align-items:baseline;gap:1.25rem;padding:.85rem 0;flex-wrap:wrap}
.brand{color:#fff;display:flex;flex-direction:column;line-height:1.1}
.brand:hover{text-decoration:none}
.brand-name{font-weight:700;font-size:1rem}
.brand-dept{font-size:.78rem;color:var(--gold);letter-spacing:.04em;text-transform:uppercase}
.brand-title{margin-left:auto;font-size:.9rem;color:#cdd6e6}

main.wrap{padding:2.5rem 0 3.5rem}

.hero h1{font-size:2.1rem;margin:0 0 .5rem;color:var(--blue)}
.lede{color:var(--muted);font-size:1.05rem;max-width:60ch}

.tldr{margin-top:1.75rem;border:1px solid var(--line);border-left:4px solid var(--gold);
  border-radius:8px;background:var(--panel);padding:.75rem 1.1rem}
.tldr>summary{cursor:pointer;font-weight:700;color:var(--blue);list-style:none}
.tldr>summary::-webkit-details-marker{display:none}
.tldr>summary::before{content:"\\25B6";color:var(--gold);font-size:.7em;margin-right:.5rem}
.tldr[open]>summary::before{content:"\\25BC"}
.tldr-body{margin-top:.75rem}
.tldr-body p{margin:.5rem 0;font-size:.95rem}
.tldr-body ul{margin:.4rem 0;padding-left:1.2rem}
.tldr-body li{margin:.3rem 0;font-size:.95rem}

.list{display:flex;flex-direction:column;gap:1.25rem;margin-top:2rem}
.row{display:flex;gap:1.5rem;border:1px solid var(--line);border-radius:8px;background:#fff;
  padding:1.1rem;align-items:flex-start}
.thumb{position:relative;display:block;width:320px;flex:0 0 320px;aspect-ratio:16/9;
  border-radius:6px;overflow:hidden;background:var(--panel)}
.thumb img{width:100%;height:100%;object-fit:cover;display:block}
.thumb .num{position:absolute;left:.5rem;bottom:.5rem;background:var(--blue);color:#fff;
  width:1.9rem;height:1.9rem;border-radius:50%;display:grid;place-items:center;font-weight:700;
  border:2px solid var(--gold)}
.thumb:hover{box-shadow:0 4px 14px rgba(0,32,91,.18)}
.row-body{flex:1;min-width:0}
.row-body h3{margin:0 0 .2rem;font-size:1.2rem}
.row-body h3 a{color:var(--blue)}
.row-body .sub{margin:0 0 .9rem;color:var(--muted);font-size:.95rem}
.topics-label{margin:0 0 .35rem;font-size:.72rem;text-transform:uppercase;letter-spacing:.07em;
  color:var(--gold);font-weight:700}
.topics{margin:0;padding-left:1.1rem;font-size:.92rem}
.topics li{margin:.15rem 0}
.topics .ts{color:var(--muted);font-family:var(--mono);font-size:.82em;white-space:nowrap}
ul.topics.placeholder{list-style:none;padding:.6rem .9rem;border:1px dashed var(--line);
  border-radius:6px;background:var(--panel);color:var(--muted);font-style:italic}

.crumbs{font-size:.85rem;color:var(--muted);margin-bottom:1.25rem}
.session-head{margin-bottom:1.5rem}
.kicker{font-size:.78rem;text-transform:uppercase;letter-spacing:.08em;color:var(--gold);font-weight:700}
.session-head h1{margin:.25rem 0 .4rem;font-size:1.9rem;color:var(--blue)}

.video{position:relative;aspect-ratio:16/9;margin:0 0 2.25rem;border-radius:8px;overflow:hidden;
  border:1px solid var(--line);background:#000}
.video iframe{position:absolute;inset:0;width:100%;height:100%}

.block{margin:2.5rem 0;padding-top:1.5rem;border-top:1px solid var(--line)}
.block>h2{color:var(--blue);font-size:1.4rem;margin:0 0 1rem}
.placeholder{color:var(--muted);font-style:italic;background:var(--panel);
  border:1px dashed var(--line);border-radius:6px;padding:1rem}
.notes-meta{color:var(--muted);font-size:.9rem;margin:-.25rem 0 1.25rem}

.note{border:1px solid var(--line);border-radius:8px;padding:1rem 1.25rem;margin:0 0 1rem;background:#fff}
.note h3{margin:0 0 .6rem;color:var(--blue);font-size:1.1rem}
.note ul{margin:.25rem 0;padding-left:1.2rem}
.note li{margin:.2rem 0}
.note table{border-collapse:collapse;width:100%;font-size:.9rem}
.note th,.note td{border:1px solid var(--line);padding:.35rem .55rem;text-align:left}
.note th{background:var(--panel)}

pre{background:#0f1729;color:#e6edf3;padding:.85rem 1rem;border-radius:6px;overflow:auto;
  font-family:var(--mono);font-size:.85rem;line-height:1.45}
code{font-family:var(--mono)}
:not(pre)>code{background:var(--panel);padding:.1rem .35rem;border-radius:4px;font-size:.88em}

footer.site{border-top:1px solid var(--line);background:var(--panel);color:var(--muted);
  font-size:.85rem;margin-top:3rem}
footer.site .wrap{padding:1.5rem 0}
footer.site p{margin:.15rem 0}

@media(max-width:640px){
  .row{flex-direction:column}
  .thumb{width:100%;flex-basis:auto}
}
@media(max-width:560px){.brand-title{margin-left:0;flex-basis:100%}}
"""


def main():
    for d in GENERATED_DIRS:
        if (WWW / d).exists():
            shutil.rmtree(WWW / d)
    for f in GENERATED_FILES:
        if (WWW / f).exists():
            (WWW / f).unlink()
    (WWW / "assets").mkdir(parents=True)
    (WWW / "sessions").mkdir()
    (WWW / "notes").mkdir()

    (WWW / "assets" / "style.css").write_text(STYLE)
    # GitHub Pages: skip Jekyll so _ and folders serve as-is
    (WWW / ".nojekyll").write_text("")

    for s in SESSIONS:
        pdf = SLIDES / "pdfs" / f"{s['base']}.pdf"
        if pdf.exists():
            shutil.copy2(pdf, WWW / "notes" / pdf.name)
        shutil.copy2(SLIDES / f"{s['base']}.md", WWW / "notes" / f"{s['base']}.md")
        build_session(s)

    build_index()
    print(f"Built site at {WWW}")



if __name__ == "__main__":
    main()
