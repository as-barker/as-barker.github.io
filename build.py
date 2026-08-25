#!/usr/bin/env python3
import json as _json
from json_pages import LANDING_JS, RECIPE_INDEX_JS, RECIPE_PAGE_JS
"""Generates the whole static site into ./dist from the data below."""
import os, shutil, html

OUT = "dist"
CATS = {
    "evidence": ("Evidence reviews", "#17545A"),
    "programs": ("Programs and tools", "#7C5216"),
    "training": ("Training", "#8E3324"),
    "austere":  ("Austere medicine", "#354A66"),
    "recipes":  ("Recipes", "#48592A"),
}

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
 '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
 '<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800'
 '&family=IBM+Plex+Mono:wght@400;500;600&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600'
 '&display=swap" rel="stylesheet">')


def page(depth, title, colour, body, crumbs=None):
    up = "../" * depth if depth else ""
    css = f'<link rel="stylesheet" href="{up}style.css">'
    style = f'<style>:root{{--c:{colour}}}</style>' if colour else ""
    crumb = ""
    if crumbs:
        parts = []
        for label, href in crumbs[:-1]:
            parts.append(f'<a href="{up}{href}">{html.escape(label)}</a>')
        parts.append(f'<span>{html.escape(crumbs[-1][0])}</span>')
        crumb = '<nav class="crumb">' + '<span class="sep">/</span>'.join(parts) + '</nav>'
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>{FONTS}{css}{style}</head>
<body><div class="w">{crumb}
{body}
<footer><a href="mailto:ab@abarker.org">ab@abarker.org</a></footer>
</div></body></html>
"""


def write(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(content)


STYLE = """
:root{--paper:#F5F6F5;--ink:#14181A;--muted:#5F6968;--rule:#D2D8D5;--hair:#E4E9E7;
--flag:#A33A2A;--c:#14181A;--measure:34rem}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);
font-family:"Source Serif 4",Cambria,Georgia,serif;font-size:17px;line-height:1.6}
.w{max-width:50rem;margin:0 auto;padding:4.5rem 1.5rem 6rem}

.crumb{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.72rem;
letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-bottom:2.5rem}
.crumb a{color:var(--muted);text-decoration:none;border-bottom:1px solid var(--rule)}
.crumb a:hover,.crumb a:focus-visible{color:var(--c);border-bottom-color:var(--c)}
.crumb .sep{padding:0 .5rem;color:var(--rule)}

.mast{padding-bottom:2.25rem;border-bottom:3px solid var(--ink);margin-bottom:3.25rem}
.mast h1{font-family:Archivo,Calibri,system-ui,sans-serif;font-weight:700;
font-size:clamp(2.6rem,7vw,3.4rem);letter-spacing:-.05em;line-height:1;margin:0 0 1.15rem}
.mast p{margin:0;max-width:31rem}
.mast p+p{margin-top:.45rem;color:var(--muted)}
.mast .note{margin-top:1.5rem;padding-top:1.1rem;border-top:1px solid var(--rule);
max-width:31rem;color:var(--muted);font-family:"IBM Plex Mono",ui-monospace,monospace;
font-size:.78rem;letter-spacing:.04em;line-height:1.7}

.ix{list-style:none;margin:0;padding:0}
.ix li{margin-bottom:2.75rem}
.ix a{display:block;text-decoration:none;color:inherit}
.tag{display:inline-block;background:var(--tc,var(--c));color:#fff;
font-family:Archivo,Calibri,system-ui,sans-serif;font-weight:600;font-size:1.3rem;
letter-spacing:-.02em;padding:.55rem 1.1rem .6rem;margin-bottom:1rem;
transition:transform .16s ease,box-shadow .16s ease}
.ix a:hover .tag,.ix a:focus-visible .tag{transform:translate(-3px,-3px);
box-shadow:5px 5px 0 0 var(--ink)}
.ix a:focus-visible{outline:2px solid var(--tc,var(--c));outline-offset:6px}
.ix p{margin:0 0 .95rem;max-width:29rem;color:var(--muted)}
.meta{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.7rem;
letter-spacing:.13em;text-transform:uppercase;color:var(--muted)}
.meta b{color:var(--tc,var(--c));font-weight:600}
.meta .no{color:var(--flag)}

h1.doc{font-family:Archivo,Calibri,system-ui,sans-serif;font-weight:700;
font-size:2.3rem;letter-spacing:-.035em;line-height:1.08;margin:0 0 1.1rem;
max-width:22ch;color:var(--c)}
.standfirst{max-width:var(--measure);color:var(--muted);margin:0 0 1.75rem}
.standfirst.lede{color:var(--ink);font-size:1.18rem;line-height:1.5;
padding-bottom:1.5rem;border-bottom:1px solid var(--rule);margin-bottom:2.75rem}
.control{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.72rem;
letter-spacing:.1em;text-transform:uppercase;color:var(--muted);display:flex;
flex-wrap:wrap;gap:.4rem 1.5rem;padding:.7rem 0;border-top:2px solid var(--c);
border-bottom:1px solid var(--rule);margin-bottom:2.75rem}
.control .live{color:var(--c);font-weight:500}
.control .prov{color:var(--flag)}

h2.sec{font-family:Archivo,Calibri,system-ui,sans-serif;font-weight:600;
font-size:1.4rem;letter-spacing:-.018em;line-height:1.2;margin:3rem 0 1rem;
padding-top:1rem;border-top:1px solid var(--rule)}
p{max-width:var(--measure);margin:0 0 1.1rem}
a{color:var(--c)}
ul.pts{max-width:var(--measure);margin:0 0 1.5rem;padding:0;list-style:none}
ul.pts li{position:relative;padding-left:1.4rem;margin-bottom:.7rem}
ul.pts li::before{content:"";position:absolute;left:0;top:.62em;width:.5rem;
height:1px;background:var(--c)}

.loading{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.8rem;
letter-spacing:.08em;color:var(--muted);list-style:none}
.loadfail{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.82rem;
line-height:1.7;color:var(--flag);border:1px dashed var(--rule);padding:1.25rem;
max-width:var(--measure)}
#bio p{margin:0;max-width:31rem}
#bio p.muted{margin-top:.45rem;color:var(--muted)}
#bio p.note{margin-top:1.5rem;padding-top:1.1rem;border-top:1px solid var(--rule);
max-width:31rem;color:var(--muted);font-family:"IBM Plex Mono",ui-monospace,monospace;
font-size:.78rem;letter-spacing:.04em;line-height:1.7}
.empty{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.8rem;
letter-spacing:.08em;color:var(--flag);border:1px dashed var(--rule);
padding:1.5rem;max-width:var(--measure);line-height:1.7}

figure{margin:2rem 0 2.5rem}
figure img,figure svg{width:100%;height:auto;display:block;border:1px solid var(--rule)}
figcaption{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.72rem;
letter-spacing:.03em;color:var(--muted);margin-top:.65rem;max-width:var(--measure);
line-height:1.5}

.tbl-label{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.72rem;
letter-spacing:.1em;text-transform:uppercase;color:var(--c);margin:2.25rem 0 .6rem}
.scroller{overflow-x:auto;-webkit-overflow-scrolling:touch;margin-bottom:.75rem}
table{border-collapse:collapse;width:100%;min-width:34rem;font-size:.9rem;line-height:1.45}
th,td{text-align:left;vertical-align:top;padding:.65rem .9rem .65rem 0;
border-bottom:1px solid var(--hair)}
thead th{font-family:Archivo,Calibri,system-ui,sans-serif;font-weight:600;
font-size:.82rem;border-bottom:1.5px solid var(--ink);padding-bottom:.5rem}
tbody th{font-family:Archivo,Calibri,system-ui,sans-serif;font-weight:600;
font-size:.85rem;width:11rem}
.num{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.85em}
.tbl-note{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.7rem;
color:var(--muted);line-height:1.55;margin:0 0 2rem;max-width:var(--measure);
letter-spacing:.02em}

.refs{font-size:.88rem;line-height:1.5}
.refs p{margin-bottom:.85rem;max-width:44rem}
.refs .unver{color:var(--flag);font-family:"IBM Plex Mono",ui-monospace,monospace;
font-size:.75rem}

.embed{position:relative;padding-bottom:56.25%;height:0;margin:1.25rem 0 .6rem;
border:1px solid var(--rule)}
.embed iframe{position:absolute;top:0;left:0;width:100%;height:100%;border:0}
.embed.embed-form{padding-bottom:0;height:min(78vh,720px)}
.credit{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.72rem;
letter-spacing:.05em;color:var(--muted);max-width:var(--measure);line-height:1.6}

/* recipe: two columns, ingredients scroll independently */
.recipe{display:grid;grid-template-columns:17rem 1fr;gap:0 3rem;align-items:start}
.ing{position:sticky;top:2rem;max-height:calc(100vh - 4rem);overflow-y:auto;
padding-right:.75rem}
.ing h2{font-family:Archivo,Calibri,system-ui,sans-serif;font-weight:600;
font-size:.78rem;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);
margin:0 0 .9rem;padding-bottom:.5rem;border-bottom:1px solid var(--c)}
.ing ul{list-style:none;margin:0;padding:0;font-size:.92rem;line-height:1.5}
.ing li{padding:.45rem 0;border-bottom:1px solid var(--hair)}
.ing .g{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.85em;
color:var(--c);font-weight:500}
.method{min-width:0}
.method ol{margin:0 0 2rem;padding-left:1.4rem}
.method li{margin-bottom:1rem;max-width:var(--measure)}
.macros{margin-top:2rem;padding-top:1.25rem;border-top:2px solid var(--c)}
.macros table{min-width:0;max-width:22rem}
.macros td{padding:.4rem .9rem .4rem 0}
.macros td:first-child{font-family:"IBM Plex Mono",ui-monospace,monospace;
font-size:.75rem;letter-spacing:.09em;text-transform:uppercase;color:var(--muted);width:9rem}

footer{margin-top:3.5rem;padding-top:1.1rem;border-top:1px solid var(--rule);
font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.7rem;
letter-spacing:.13em;color:var(--muted)}
footer a{color:var(--muted);text-decoration:none;border-bottom:1px solid var(--rule)}
footer a:hover,footer a:focus-visible{color:var(--ink);border-bottom-color:var(--ink)}

@media(max-width:52rem){
  .recipe{grid-template-columns:1fr;gap:0}
  .ing{position:static;max-height:none;overflow:visible;padding-right:0;
       margin-bottom:2.25rem;padding-bottom:1.5rem;border-bottom:1px solid var(--rule)}
}
@media(max-width:34rem){
  .w{padding:2.5rem 1.15rem 4rem}
  body{font-size:16px}
  .tag{font-size:1.1rem}
  h1.doc{font-size:1.8rem}
  tbody th{width:8rem}
}
@media(prefers-reduced-motion:reduce){*{transition:none!important}}
"""

# ---------------------------------------------------------------- landing
def build_landing():
    body = """<header class="mast"><h1>AB</h1>
<div id="bio"></div></header>
<ul class="ix" id="index"><li class="loading">Loading&hellip;</li></ul>"""
    html = page(0, "AB", None, body)
    html = html.replace('<footer><a href="mailto:ab@abarker.org">ab@abarker.org</a></footer>',
                        '<footer id="mail"></footer>')
    html = html.replace('</body>', f'<script>{LANDING_JS}</script>\n</body>')
    write("index.html", html)
    write("site.json", open("json/site.json").read())


# ------------------------------------------------------- simple category
def category(slug, depth, crumbs, heading, blurb, items=None, empty_msg=None):
    name, col = CATS[slug]
    if items:
        li = []
        for href, t, d, meta in items:
            li.append(f'<li style="--tc:{col}"><a href="{href}">'
                      f'<span class="tag">{t}</span><p>{d}</p>'
                      f'<div class="meta">{meta}</div></a></li>')
        inner = f'<ul class="ix">{chr(10).join(li)}</ul>'
    else:
        inner = f'<div class="empty">{empty_msg}</div>'
    body = (f'<h1 class="doc">{heading}</h1>'
            f'<p class="standfirst lede">{blurb}</p>{inner}')
    return page(depth, f"{heading} \u00b7 AB", col, body, crumbs)


def build_categories():
    write("programs/index.html", category(
        "programs", 1, [("AB","index.html"),("Programs and tools",None)],
        "Programs and tools",
        "The tools I built or borrowed to make programs run. Steal away.",
        empty_msg="Nothing posted yet."))

    write("austere/index.html", category(
        "austere", 1, [("AB","index.html"),("Austere medicine",None)],
        "Austere medicine",
        "Reading, coursework, and my own research as it happens.",
        empty_msg="Nothing posted yet."))

    write("evidence/index.html", category(
        "evidence", 1, [("AB","index.html"),("Evidence reviews",None)],
        "Evidence reviews",
        "The literature behind prehospital practice, as I read it.",
        items=[("prehospital-blood/", "Prehospital blood",
                "Quick overview of the evidence surrounding prehospital blood administration. More in-depth review to follow.",
                "<b>Review</b> &nbsp; Compiled 2026-08-24")]))

    write("training/index.html", category(
        "training", 1, [("AB","index.html"),("Training",None)],
        "Training",
        "What I teach, and the material behind it.",
        items=[("vent/", "Ventilators for Critical Care Paramedics",
                "Pre-course reading, course material, and assessment for the ventilator program.",
                "<b>3 sections</b> &nbsp; Updated 2026-08-24")]))

    _, col = CATS["training"]
    secs = [
        ("pre-course/", "Pre-course materials",
         "Reading and video to work through before the course.",
         "<b>4 resources</b> &nbsp; Updated 2026-08-24"),
        ("course/", "Course resources",
         "Lecture slides and in-class material.",
         '<span class="no">Not posted yet</span>'),
        ("assessment/", "Assessment resources",
         "Written examination, practical examination, and scenario documentation.",
         '<span class="no">Held until after the first course</span>'),
    ]
    li = [f'<li style="--tc:{col}"><a href="{h}"><span class="tag">{t}</span>'
          f'<p>{d}</p><div class="meta">{m}</div></a></li>' for h,t,d,m in secs]
    body = ('<h1 class="doc">Ventilators for Critical Care Paramedics</h1>'
            '<p class="standfirst lede">A prehospital ventilator training program '
            'built around the HAMILTON-T1.</p>'
            f'<ul class="ix">{chr(10).join(li)}</ul>')
    write("training/vent/index.html", page(
        2, "Ventilators for Critical Care Paramedics \u00b7 AB", col, body,
        [("AB","index.html"),("Training","training/"),("Ventilators for Critical Care Paramedics",None)]))


def build_vent_pages():
    _, col = CATS["training"]
    crumbs = [("AB","index.html"),("Training","training/"),
              ("Ventilators for Critical Care Paramedics","training/vent/")]

    pre = """<h1 class="doc">Pre-course materials</h1>
<p class="standfirst">Work through these before the course. The written examination comes first, so
do it before you read anything else, or the baseline is worthless.</p>
<div class="control"><span class="live">4 resources</span><span>Updated 2026-08-24</span></div>

<h2 class="sec">1. Written examination</h2>
<p>Twenty-five items. This is not the credential and it is not graded against you. It measures
whether the teaching worked and shows where coaching should go. Do it before you read anything
below, or the baseline is worthless.</p>
<div class="embed embed-form"><iframe
src="https://forms.cloud.microsoft/Pages/ResponsePage.aspx?id=csweVMRVaE2CRqvM1CUJ8MKbGMS0Y9NOi_lGkbZ0XshUQzhFUzU5NU9aR0g4NlFRVFJXWkYxTzE1Si4u&amp;embed=true"
title="Ventilator written examination" loading="lazy"
allowfullscreen></iframe></div>
<p class="credit">If the examination will not load or sign you in here,
<a href="https://forms.cloud.microsoft/Pages/ResponsePage.aspx?id=csweVMRVaE2CRqvM1CUJ8MKbGMS0Y9NOi_lGkbZ0XshUQzhFUzU5NU9aR0g4NlFRVFJXWkYxTzE1Si4u" rel="noopener">open it in a new tab</a>.</p>

<h2 class="sec">2. Reading</h2>
<p>Two handouts from Scott Weingart's EMCrit ventilator series. Read the management article first,
then keep the handout to hand during the course.</p>
<ul class="pts">
<li><a href="https://emcrit.org/emcrit/vent-part-1/" rel="noopener">EMCrit ventilator management, part 1</a>,
and the <a href="https://emcrit.org/wp-content/uploads/2010/05/Managing-Initial-Vent-ED.pdf" rel="noopener">article PDF</a></li>
<li><a href="https://emcrit.org/emcrit/vent-part-2/" rel="noopener">EMCrit ventilator management, part 2</a>,
and the <a href="https://emcrit.org/wp-content/uploads/vent-handout.pdf" rel="noopener">handout PDF</a></li>
</ul>

<h2 class="sec">3. Video</h2>
<div class="embed"><iframe src="https://www.youtube-nocookie.com/embed/G9TiP3kkK9Q"
title="Ventilator lecture, part 1" loading="lazy"
allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
allowfullscreen></iframe></div>
<div class="embed"><iframe src="https://www.youtube-nocookie.com/embed/rsArr9tu1yM"
title="Ventilator lecture, part 2" loading="lazy"
allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
allowfullscreen></iframe></div>
<p class="credit">Reading and video by Scott Weingart, EMCrit. Linked with credit, not reproduced.</p>"""
    write("training/vent/pre-course/index.html", page(
        3, "Pre-course materials \u00b7 AB", col, pre,
        crumbs + [("Pre-course materials", None)]))

    course = """<h1 class="doc">Course resources</h1>
<p class="standfirst">Lecture slides and in-class material.</p>
<div class="empty">Not posted yet. Slides go up once the deck is finished.</div>"""
    write("training/vent/course/index.html", page(
        3, "Course resources \u00b7 AB", col, course,
        crumbs + [("Course resources", None)]))

    assess = """<h1 class="doc">Assessment resources</h1>
<p class="standfirst lede">Written examination, practical examination, and scenario documentation. The practical check-off is the credential.</p>
<div class="empty">Held until after the first course has run.</div>"""
    write("training/vent/assessment/index.html", page(
        3, "Assessment resources \u00b7 AB", col, assess,
        crumbs + [("Assessment resources", None)]))


def build_recipes():
    _, col = CATS["recipes"]
    write("recipes/recipes.json", open("json/recipes.json").read())

    body = ('<h1 class="doc">Recipes</h1>'
            '<p class="standfirst lede">Imperial with grams alongside, macros at the bottom. '
            'Ingredients sit in their own panel so you can weigh everything out before you start.</p>'
            '<ul class="ix" id="index"><li class="loading">Loading&hellip;</li></ul>')
    html = page(1, "Recipes \u00b7 AB", col, body,
                [("AB","index.html"),("Recipes",None)])
    html = html.replace('</body>', f'<script>{RECIPE_INDEX_JS}</script>\n</body>')
    write("recipes/index.html", html)

    for r in _json.load(open("json/recipes.json")):
        body = ('<h1 class="doc" id="title">&nbsp;</h1>'
                '<p class="standfirst" id="blurb"></p>'
                '<div class="control"><span class="live" id="serves"></span></div>'
                '<div class="recipe" id="recipe"><p class="loading">Loading&hellip;</p></div>')
        html = page(2, "Recipe \u00b7 AB", col, body,
                    [("AB","index.html"),("Recipes","recipes/"),("__HERE__", None)])
        html = html.replace('<span>__HERE__</span>', '<span id="here"></span>')
        html = html.replace('<body>', f'<body data-slug="{r["slug"]}">')
        html = html.replace('</body>', f'<script>{RECIPE_PAGE_JS}</script>\n</body>')
        write(f"recipes/{r['slug']}/index.html", html)


def build_evidence_doc():
    _, col = CATS["evidence"]
    inner = open("doc_body.html").read()
    write("evidence/prehospital-blood/index.html", page(
        2, "Prehospital blood \u00b7 AB", col, inner,
        [("AB","index.html"),("Evidence reviews","evidence/"),("Prehospital blood", None)]))


if __name__ == "__main__":
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    write("style.css", STYLE)
    build_landing()
    build_categories()
    build_vent_pages()
    build_recipes()
    build_evidence_doc()
    shutil.copy("site/evidence/prehospital-blood.html".replace("prehospital-blood.html",""), OUT) if False else None
    with open(os.path.join(OUT, ".nojekyll"), "w") as f:
        f.write("")
    with open(os.path.join(OUT, "CNAME"), "w") as f:
        f.write("abarker.org\n")
    n = sum(len(fs) for _, _, fs in os.walk(OUT))
    print(f"built {n} files")
