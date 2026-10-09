"""Build the static site using only the Python standard library."""
import html
import hashlib
import json
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "public"
DATA = json.loads((ROOT / "data/site.json").read_text())
BASE_PATH = os.environ.get("SITE_BASE_PATH", "/").rstrip("/") + "/"


def esc(value):
    return html.escape(str(value), quote=True)


ARROW = '<span aria-hidden="true">↗</span>'
LOGO = '''<svg viewBox="0 0 36 40" fill="none" aria-hidden="true"><path d="M18 38V22C18 13 9 14 9 4M18 23C18 13 28 15 28 2M18 30C18 24 31 29 32 19M18 28C18 21 4 27 3 17" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/></svg>'''


def style_switcher():
    choices = [('academic', 'Academic'), ('discovery', 'Discovery'), ('editorial', 'Editorial')]
    tabs = ''.join(f'<button type="button" role="tab" id="style-{key}" aria-controls="main" aria-selected="{str(i == 0).lower()}" tabindex="{0 if i == 0 else -1}" data-style="{key}"><span class="style-number">0{i+1}</span>{label}</button>' for i, (key, label) in enumerate(choices))
    return f'<div class="style-switcher"><div class="container style-switcher-inner"><span class="style-switcher-label">EXPLORE THE DESIGNS</span><div role="tablist" aria-label="Website design">{tabs}</div><span class="style-switcher-note">Same science. Different perspectives.</span></div></div>'


def header(active):
    links = [("index.html", "Home"), ("research.html", "Research"), ("people.html", "People"), ("publications.html", "Publications")]
    nav = ''.join(f'<a href="{url}"{chr(32) + "aria-current=\"page\"" if url == active else ""}>{label}</a>' for url, label in links)
    return f'''<a class="skip-link" href="#main">Skip to content</a>
    <header class="site-header"><div class="container header-inner">
      <a class="brand" href="index.html" aria-label="Tang Vascular Research Lab home">{LOGO}<span><strong>Tang Lab<span class="brand-dot">.</span></strong><small>VASCULAR RESEARCH</small></span></a>
      <button class="menu-toggle" aria-label="Open navigation" aria-controls="site-nav" aria-expanded="false"><span></span><span></span></button>
      <nav id="site-nav" aria-label="Main navigation">{nav}<a class="nav-contact" href="#contact">Get in touch {ARROW}</a></nav>
    </div></header>'''


def footer():
    return f'''<section class="contact-band" id="contact" aria-labelledby="contact-title"><div class="container contact-inner">
      <div><p class="eyebrow light">LET’S CONNECT</p><h2 id="contact-title">Good science starts<br>with a conversation.</h2></div>
      <div class="contact-details"><p>For research collaborations and<br>academic inquiries, contact Gale Tang.</p><a class="email-link" href="mailto:{DATA['email']}">{DATA['email']} {ARROW}</a><p class="contact-location">University of Washington<br>Seattle, Washington</p></div>
    </div></section>
    <footer class="site-footer"><div class="container footer-top"><a class="brand footer-brand" href="index.html">{LOGO}<span><strong>Tang Lab.</strong><small>VASCULAR RESEARCH</small></span></a><p>Exploring the biology of blood vessels.<br>Connecting discovery to vascular care.</p><a href="{DATA['profile']}" target="_blank" rel="noopener noreferrer">UW investigator profile {ARROW}</a></div>
    <div class="container footer-bottom"><span>© 2026 Tang Vascular Research Lab</span><span>Seattle, WA <span class="footer-separator">/</span> Research & discovery</span><a href="#top">Back to top ↑</a></div></footer>'''


def shell(filename, title, description, content):
    style_version = hashlib.sha256((ROOT / 'assets/styles.css').read_bytes()).hexdigest()[:12]
    document = f'''<!doctype html>
<html lang="en" data-style="academic"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<script>try{{var s=new URLSearchParams(location.search).get('style')||localStorage.getItem('tang-lab-style');if(['academic','discovery','editorial'].includes(s))document.documentElement.dataset.style=s;}}catch(e){{}}</script>
<title>{esc(title)} | Tang Vascular Research Lab</title><meta name="description" content="{esc(description)}"><meta name="theme-color" content="#f7f6f2">
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg"><link rel="stylesheet" href="assets/site.css"><link rel="stylesheet" href="assets/styles.css?v={style_version}"><script src="assets/site.js" defer></script>
</head><body id="top">{style_switcher()}{header(filename)}<main id="main" role="tabpanel" aria-labelledby="style-academic">{content}</main>{footer()}</body></html>'''
    (OUT / filename).write_text(document)


def hero_art():
    return '''<figure class="hero-art"><div class="figure-top"><span>THE BIOLOGY OF POSSIBILITY</span><span class="figure-cross">+</span></div>
    <svg class="vessel-art" viewBox="0 0 550 520" fill="none" role="img" aria-labelledby="vessel-title vessel-desc">
    <title id="vessel-title">A branching vascular network</title><desc id="vessel-desc">Conceptual illustration of vessels branching from a central artery, representing growth, adaptation, and repair. Not experimental data.</desc>
    <defs><radialGradient id="halo"><stop stop-color="#e9bfc0" stop-opacity=".34"/><stop offset="1" stop-color="#f7f6f2" stop-opacity="0"/></radialGradient><linearGradient id="artery" x1="290" y1="480" x2="220" y2="50" gradientUnits="userSpaceOnUse"><stop stop-color="#712c3e"/><stop offset=".65" stop-color="#ad5b64"/><stop offset="1" stop-color="#cf8f8e"/></linearGradient></defs>
    <circle cx="280" cy="248" r="245" fill="url(#halo)"/><g stroke="#dadcd6" stroke-width=".8"><circle cx="275" cy="258" r="195"/><circle cx="275" cy="258" r="140" stroke-dasharray="2 6"/><path d="M275 39V477M56 258H494" stroke-dasharray="3 7"/></g>
    <g stroke="url(#artery)" stroke-linecap="round" stroke-linejoin="round">
      <path d="M291 488C287 445 283 401 279 351C274 296 278 259 260 212C244 171 230 126 237 58" stroke-width="23"/>
      <path d="M281 365C274 311 204 326 176 274C159 244 160 208 143 179C128 153 103 144 89 121" stroke-width="12"/>
      <path d="M265 237C291 205 326 201 342 158C355 123 342 99 354 64" stroke-width="15"/>
      <path d="M282 409C312 370 365 393 393 348C410 321 407 292 430 273" stroke-width="11"/>
      <path d="M249 182C211 179 204 142 181 117C160 94 143 96 125 69M176 273C196 251 211 233 205 203M161 233C122 242 103 223 69 211M341 161C375 171 397 143 420 128M394 346C357 330 366 298 343 281M283 323C312 302 319 280 321 258" stroke-width="7"/>
      <path d="M145 181C115 184 109 163 85 164M354 89L382 60M208 149C217 119 207 87 208 64M399 148L403 105M408 320L460 310M366 314L384 283M190 257L217 258M92 226L77 252M281 297C238 278 227 301 213 286" stroke-width="3.5"/>
      <path d="M89 121L78 93M125 69L109 55M181 117L177 84M69 211L51 197M85 164L61 163M420 128L444 122M382 60L402 49M343 281L335 260M430 273L444 253M460 310L479 294" stroke-width="2"/>
    </g>
    <path d="M290 484C287 446 281 400 278 350C274 296 278 259 259 210C245 169 231 124 237 61" stroke="#efd1cb" stroke-width="4" stroke-linecap="round" opacity=".65"/>
    <g stroke="#8c9695" stroke-width=".8"><path d="M339 157H454V172"/><path d="M165 274H56V288"/><path d="M395 348H476V364"/></g>
    <g fill="#526362" font-family="Arial, sans-serif" font-size="10" letter-spacing="2"><text x="396" y="190">GROWTH</text><text x="55" y="308">ADAPTATION</text><text x="424" y="383">REPAIR</text></g>
    <g fill="#f7f6f2" stroke="#8e4b57" stroke-width="1.5"><circle cx="339" cy="157" r="4"/><circle cx="165" cy="274" r="4"/><circle cx="395" cy="348" r="4"/></g>
    </svg><figcaption><span>VESSEL GROWTH · INJURY · REPAIR</span><span>Conceptual illustration</span></figcaption></figure>'''


def art(kind):
    start = '<svg viewBox="0 0 360 200" fill="none" aria-hidden="true">'
    if kind == 0:
        return start + '''<g stroke="#cdd7d0" stroke-width=".7"><circle cx="180" cy="103" r="77"/><circle cx="180" cy="103" r="50" stroke-dasharray="2 5"/></g><g stroke="#78988b" stroke-linecap="round"><path d="M180 190V125C180 87 135 100 128 64L121 17M181 132C185 84 228 106 238 67L249 18" stroke-width="12"/><path d="M163 99C138 102 105 123 87 99M204 96C235 97 268 124 280 84M128 63L90 48M238 67L275 44" stroke-width="6"/><path d="M121 21L109 7M91 99L65 108M90 48L67 36M280 84L300 70M271 44L290 33" stroke-width="2"/></g><path d="M153 91C162 71 202 66 218 91" stroke="#a55760" stroke-width="4" stroke-dasharray="2 7" stroke-linecap="round"/></svg>'''
    if kind == 1:
        return start + '''<g transform="translate(180 100) rotate(-18)"><ellipse rx="99" ry="67" fill="#e3bbb4"/><ellipse rx="79" ry="53" fill="#a9636a"/><ellipse rx="63" ry="42" fill="#efd8d0"/><ellipse rx="43" ry="28" fill="#fbf5ee"/><ellipse rx="88" ry="59" stroke="#b57576" stroke-dasharray="3 8"/><g fill="#774552"><ellipse cx="-67" cy="-10" rx="2" ry="6"/><ellipse cx="68" cy="7" rx="2" ry="6"/><ellipse cx="-23" cy="-41" rx="6" ry="2"/><ellipse cx="21" cy="42" rx="6" ry="2"/></g></g><g stroke="#aa9992" stroke-width=".8"><path d="M225 48H302M247 119H304M109 136H51"/></g><g fill="#aa9992"><circle cx="302" cy="48" r="2"/><circle cx="304" cy="119" r="2"/><circle cx="51" cy="136" r="2"/></g></svg>'''
    dots = ''.join(f'<circle cx="{98 + (i % 14) * 13}" cy="{48 + (i // 14) * 13}" r="{2.2 + (i % 3) * .5}" fill="{["#7a968a", "#bf8587", "#c4aa75", "#597f85"][((i * 7) + i // 14) % 4]}" opacity=".75"/>' for i in range(112))
    return start + '<path d="M69 37H290V167H69Z" fill="#fcfaf4" stroke="#ccd4ce"/><path d="M81 25H278M57 49V156" stroke="#b0bcb3"/>' + dots + '<circle cx="202" cy="103" r="34" stroke="#804851" stroke-width="1.5"/><path d="M226 128L266 163" stroke="#804851" stroke-width="4" stroke-linecap="round"/></svg>'


THEMES = [
    ("Arteriogenesis", "Building new paths<br>for blood flow.", "Collateral vessels provide alternative routes around arterial blockages. We investigate the cellular and molecular signals that shape this response to ischemia.", "growth"),
    ("Vein graft biology", "Understanding how<br>vessels adapt.", "A vein placed into the arterial circulation encounters a new environment. We study the remodeling processes linked to graft narrowing and failure.", "remodeling"),
    ("Spatial vascular biology", "Seeing the vessel wall<br>in greater detail.", "We investigate vascular disease across tissue layers, using spatial approaches to connect cell behavior, gene expression, and vessel structure.", "spatial")
]


def theme_cards():
    return '<div class="research-grid">' + ''.join(f'''<a class="research-card" href="research.html#{anchor}"><div class="research-image image-{i}">{art(i)}<span class="image-index">0{i+1}</span></div><div class="research-card-body"><p class="eyebrow">{name}</p><h3>{title}</h3><p>{desc}</p><span class="text-link">Explore this research {ARROW}</span></div></a>''' for i, (name, title, desc, anchor) in enumerate(THEMES)) + '</div>'


def publication(p, compact=False):
    badge = ' preprint' if p['type'] == 'Preprint' else ''
    return f'''<article class="publication{' compact' if compact else ''}" data-topic="{esc(p['topic'])}" data-search="{esc((p['title'] + ' ' + p['authors'] + ' ' + p['journal'] + ' ' + str(p['year'])).lower())}">
    <div class="pub-year">{p['year']}</div><div class="pub-content"><div class="pub-tags"><span class="pub-type{badge}">{p['type']}</span><span>{p['topic']}</span></div><h3><a href="{p['url']}" target="_blank" rel="noopener noreferrer">{esc(p['title'])}</a></h3>{'' if compact else '<p class="pub-authors">' + esc(p['authors']) + '</p>'}<p class="pub-journal">{esc(p['journal'])}</p>{'' if compact else '<p class="pub-summary">' + esc(p['summary']) + '</p>'}</div><a class="pub-arrow" href="{p['url']}" target="_blank" rel="noopener noreferrer" aria-label="Read {esc(p['title'])} (opens in a new tab)">{ARROW}</a></article>'''


def intro(kicker, title, body):
    return f'<section class="page-intro"><div class="container"><p class="eyebrow">{kicker}</p><h1>{title}</h1><p class="intro-copy">{body}</p></div></section>'


def build_home():
    content = f'''<section class="hero"><div class="container hero-grid"><div class="hero-copy"><p class="eyebrow"><span class="status-dot"></span>UNIVERSITY OF WASHINGTON · SEATTLE</p><h1>Understanding<br>vessels.<br><em>Advancing repair.</em></h1><p class="hero-description">We explore how blood vessels grow, respond to injury, and remodel—connecting fundamental biology to the challenges of vascular disease.</p><div class="hero-actions"><a class="button" href="research.html">Explore our research <span aria-hidden="true">↗</span></a><a class="understated-link" href="people.html">Meet the people <span aria-hidden="true">→</span></a></div><div class="hero-footnote"><span class="line-marker"></span><p>Cellular discovery.<br>A clinical perspective.</p></div></div>{hero_art()}</div></section>
    <section class="affiliation-strip"><div class="container"><p>ROOTED IN RESEARCH.<br>CONNECTED TO CARE.</p><span>University of Washington<small>Division of Vascular Surgery</small></span><span class="affiliation-divider"></span><span>VA Puget Sound<small>Health Care System</small></span></div></section>
    <section class="section container" aria-labelledby="research-title"><div class="section-heading"><div><p class="eyebrow">OUR SCIENTIFIC FOCUS</p><h2 id="research-title">Small-scale mechanisms.<br>Far-reaching questions.</h2></div><p class="section-aside">From the growth of collateral arteries to the biology of a vein graft, we study what helps vessels adapt—and what happens when they cannot.</p></div>{theme_cards()}<p class="art-note">Research illustrations are conceptual, not experimental images.</p></section>
    <section class="people-feature"><div class="container people-feature-grid"><div class="portrait-panel"><div class="portrait-frame"><img src="assets/gale-tang.jpg" alt="Gale L. Tang, MD" width="250" height="310" loading="lazy"></div><span class="portrait-caption">GALE L. TANG, MD <span>Principal investigator</span></span></div><div class="people-feature-copy"><p class="eyebrow">THE PEOPLE BEHIND THE QUESTIONS</p><h2>A surgeon’s perspective.<br>A scientist’s curiosity.</h2><p>Led by Gale L. Tang, our research brings a vascular surgeon’s perspective to fundamental questions of vessel growth and repair.</p><p>Our work connects vascular biology with engineering and clinical investigation through research collaborations at the University of Washington and beyond.</p><a class="text-link" href="people.html">Meet our research community {ARROW}</a></div></div></section>
    <section class="section container" aria-labelledby="publications-title"><div class="section-heading"><div><p class="eyebrow">FROM THE LAB</p><h2 id="publications-title">Recent work.</h2></div><a class="text-link" href="publications.html">View selected publications {ARROW}</a></div><div class="publication-list">{''.join(publication(p, True) for p in DATA['publications'][:3])}</div></section>'''
    shell('index.html', 'Vascular growth, injury & repair', 'Vascular biology research led by Gale L. Tang at the University of Washington. Exploring collateral growth, vein graft remodeling, and spatial vascular biology.', content)


def build_research():
    details = [
        ("How does the circulation find another way?", "When an artery is blocked, existing collateral vessels can enlarge to help restore blood flow. Our research examines the molecular regulators of this adaptation, including syndecan-1 and the cell-cycle inhibitor p27. These studies use experimental models of limb ischemia to understand the biology of collateral growth.", ["Cellular and molecular regulation", "Collateral artery development", "Experimental limb ischemia"], [DATA['publications'][6], DATA['publications'][7]]),
        ("What determines how a vein graft remodels?", "Veins used for arterial bypass must adapt to a different mechanical and biological environment. Research in this area examines vascular smooth muscle cells, responses to injury, and the tissue changes associated with graft narrowing. The broader program includes human vein graft models and perfused chip approaches.", ["Vascular responses to injury", "Human vein graft biology", "Cell behavior and tissue remodeling"], [DATA['publications'][4], DATA['publications'][5]]),
        ("What can we learn by preserving spatial context?", "A blood vessel is made of distinct layers with different cellular environments. Spatial profiling allows gene expression to be studied in the context of tissue structure. Recent work develops methods for analyzing calcified human arteries and explores region-specific changes in vein grafts.", ["Calcified artery preparation", "Layer-specific gene expression", "Spatial analysis of vein grafts"], [DATA['publications'][2], DATA['publications'][0]])
    ]
    body = intro('OUR RESEARCH', 'The vessel wall.<br><em>A world of questions.</em>', 'We study the mechanisms that help blood vessels grow and adapt, and the changes that contribute to vascular disease.')
    for i, ((name, title, desc, anchor), (question, text, topics, pubs)) in enumerate(zip(THEMES, details)):
        body += f'''<section class="research-detail container" id="{anchor}"><div class="research-detail-art image-{i}">{art(i)}<span>0{i+1} / {name}</span></div><div><p class="eyebrow">{name}</p><h2>{question}</h2><p>{text}</p><ul class="research-topics">{''.join('<li>' + x + '</li>' for x in topics)}</ul><div class="related-work"><p class="eyebrow">RELATED WORK</p>{''.join(f'<a href="{p["url"]}" target="_blank" rel="noopener noreferrer">{esc(p["title"])}{(" <span class=\"inline-badge\">Preprint</span>" if p["type"] == "Preprint" else "")} {ARROW}</a>' for p in pubs)}</div></div></section>'''
    body += '<section class="research-outlook container"><p class="eyebrow">A CONNECTED PROGRAM</p><h2>From cell behavior<br>to vessel-wall integrity.</h2><p>Related studies of aortic smooth muscle cells and abdominal aortic aneurysm extend these questions to the broader biology of vascular remodeling.</p><a class="text-link" href="publications.html">Explore selected publications ↗</a></section>'
    shell('research.html', 'Research', 'Explore research on collateral artery growth, vein graft biology, vascular calcification, and spatial profiling.', body)


def build_people():
    body = intro('OUR PEOPLE', 'Different perspectives.<br><em>Shared questions.</em>', 'A research community connecting vascular surgery, cell biology, and engineering.')
    body += f'''<section class="container pi-section"><figure class="pi-portrait"><img src="assets/gale-tang.jpg" alt="Gale L. Tang, MD" width="250" height="310"><figcaption>Portrait: <a href="{DATA['profile']}" target="_blank" rel="noopener noreferrer">UW Department of Surgery</a></figcaption></figure><div><p class="eyebrow">PRINCIPAL INVESTIGATOR</p><h2>Gale L. Tang<span class="degree">MD, FACS, RPVI</span></h2><p class="pi-role">Associate Professor, Vascular Surgery<br>University of Washington</p><p>Gale Tang is a vascular surgeon-scientist whose research focuses on collateral artery development, vein graft biology, and vascular responses to injury. Her clinical work is based at VA Puget Sound, with laboratory research at UW’s South Lake Union research facility.</p><p>Her work combines experimental models and human vascular tissue studies to investigate mechanisms relevant to limb ischemia and vascular repair. She is also committed to the education of medical students and surgical trainees.</p><div class="pi-links"><a class="text-link" href="{DATA['profile']}" target="_blank" rel="noopener noreferrer">UW investigator profile {ARROW}</a><a class="text-link" href="mailto:{DATA['email']}">Email Gale {ARROW}</a></div></div></section>
    <section class="collaborators-section"><div class="container"><div class="section-heading"><div><p class="eyebrow">ACROSS DISCIPLINES</p><h2>Research collaborators.</h2></div><p class="section-aside">Collaborators listed in Gale Tang’s <a href="{DATA['profile']}" target="_blank" rel="noopener noreferrer">UW Surgery research profile</a>.</p></div><div class="collaborator-grid">'''
    for person in DATA['collaborators']:
        initials = ''.join(x[0] for x in person['name'].replace('D. ', '').split())
        body += f'''<article class="collaborator"><span class="person-monogram" aria-hidden="true">{initials}</span><p class="eyebrow">{person['field']}</p><h3>{person['name']}<span>{person['degree']}</span></h3><p>{person['affiliation']}</p></article>'''
    body += '</div></div></section><section class="section container"><div class="section-heading"><div><p class="eyebrow">FROM THE RESEARCH RECORD</p><h2>Earlier contributors.</h2></div><p class="section-aside">Selected historical roles documented in public records. These are not a current team roster.</p></div><div class="historical-grid">'
    for person in DATA['historicalContributors']:
        body += f'''<article class="historical-person"><p class="eyebrow">{person['role']}</p><h3>{person['name']}</h3><p>{person['context']}</p><a class="text-link" href="{person['source']}" target="_blank" rel="noopener noreferrer">{person['sourceLabel']} {ARROW}</a></article>'''
    body += '</div></section>'
    shell('people.html', 'People', 'Meet Gale L. Tang and explore the collaborations behind the vascular research program.', body)


def build_publications():
    body = intro('PUBLICATIONS', 'Questions explored.<br><em>Knowledge shared.</em>', 'Selected recent and foundational work in vascular growth, injury, and remodeling.')
    topics = ['All research', 'Arteriogenesis', 'Vein grafts', 'Spatial biology', 'Vascular remodeling']
    body += f'''<section class="container publications-section" aria-label="Selected publications"><form class="publication-controls" role="search"><label class="search-label" for="publication-search"><span aria-hidden="true">⌕</span><input type="search" id="publication-search" placeholder="Search by title, author, or year" autocomplete="off"><span class="sr-only">Search selected publications</span></label><div class="filter-buttons" role="group" aria-label="Filter by research area">{''.join(f'<button type="button" class="filter-button{(" active" if i == 0 else "")}" data-filter="{esc(t)}" aria-pressed="{str(i == 0).lower()}">{t}</button>' for i, t in enumerate(topics))}</div></form><div class="results-meta"><p id="result-count" aria-live="polite">{len(DATA['publications'])} selected publications</p><span>Most recent first · Grouped by publication year</span></div><div class="publication-list">{''.join(publication(p) for p in DATA['publications'])}</div><div id="no-results" hidden><h2>No publications found.</h2><p>Try a different search term or research area.</p><button type="button" id="reset-filters" class="button">Reset filters</button></div><div class="publication-note"><p>This is a selected bibliography, not a complete publication record. Preprints are labeled separately and have not been peer reviewed. The 2025 p27 aneurysm article appeared online in 2025 and in the 2026 journal volume.</p><a class="text-link" href="https://pubmed.ncbi.nlm.nih.gov/?term=Tang+GL%5BAuthor%5D+AND+%28Washington%5BAffiliation%5D+OR+Puget%5BAffiliation%5D%29" target="_blank" rel="noopener noreferrer">Search PubMed for related work {ARROW}</a></div></section>'''
    shell('publications.html', 'Selected publications', 'Selected publications from Gale Tang and collaborators, covering arteriogenesis, vein grafts, and spatial vascular biology.', body)


if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    shutil.copytree(ROOT / 'assets', OUT / 'assets', dirs_exist_ok=True)
    for build in [build_home, build_research, build_people, build_publications]:
        build()
    (OUT / '404.html').write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found | Tang Lab</title><link rel="stylesheet" href="{esc(BASE_PATH)}assets/site.css"></head><body><main class="container section"><p class="eyebrow">404 / PAGE NOT FOUND</p><h1>Let’s find another path.</h1><p>The page you requested could not be found.</p><a class="button" href="{esc(BASE_PATH)}">Return to the homepage →</a></main></body></html>')
    print(f'Built 4 pages and 404 page in {OUT}')
