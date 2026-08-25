"""Hand-authored HTML shells that read the JSON at runtime."""

LANDING_JS = """
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

async function countFrom(path){
  try { const r = await fetch(path); const d = await r.json(); return d.length; }
  catch(e){ return null; }
}

async function render(){
  const el = document.getElementById('index');
  let site;
  try {
    const r = await fetch('site.json');
    if(!r.ok) throw new Error(r.status);
    site = await r.json();
  } catch(e){
    el.innerHTML = '<p class="loadfail">Could not load the index. '
      + '<a href="site.json">site.json</a> lists everything on here.</p>';
    return;
  }

  document.getElementById('bio').innerHTML =
    site.bio.map((p,i) => `<p${i?' class="muted"':''}>${esc(p)}</p>`).join('')
    + `<p class="note">${esc(site.note)}</p>`;
  document.getElementById('mail').innerHTML =
    `<a href="mailto:${esc(site.email)}">${esc(site.email)}</a>`;

  const rows = await Promise.all(site.categories.map(async c => {
    let meta;
    if (c.countFrom) {
      const n = await countFrom(c.countFrom);
      meta = n === null
        ? '<span class="no">Count unavailable</span>'
        : `<b>${n} ${esc(c.unit)}${n===1?'':'s'}</b> &nbsp; Updated ${esc(c.revised)}`;
    } else if (c.count) {
      meta = `<b>${esc(c.count)}</b> &nbsp; Updated ${esc(c.revised)}`;
    } else {
      meta = '<span class="no">Nothing posted yet</span>';
    }
    return `<li style="--tc:${esc(c.colour)}"><a href="${esc(c.slug)}/">`
         + `<span class="tag">${esc(c.name)}</span>`
         + `<p>${esc(c.description)}</p>`
         + `<div class="meta">${meta}</div></a></li>`;
  }));
  el.innerHTML = rows.join('');
}
render();
"""

RECIPE_INDEX_JS = """
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
async function render(){
  const el = document.getElementById('index');
  try {
    const pr = await fetch(document.body.dataset.up + 'pages.json');
    if(pr.ok){ const pd = await pr.json();
      document.getElementById('lede').textContent = pd.categories.recipes.lede; }
  } catch(e){}
  try {
    const r = await fetch('recipes.json');
    if(!r.ok) throw new Error(r.status);
    const rs = await r.json();
    el.innerHTML = rs.map(x =>
      `<li style="--tc:#48592A"><a href="${esc(x.slug)}/">`
      + `<span class="tag">${esc(x.title)}</span>`
      + `<p>${esc(x.blurb)}</p>`
      + `<div class="meta"><b>${esc(x.serves)}</b></div></a></li>`).join('');
  } catch(e){
    el.innerHTML = '<p class="loadfail">Could not load the recipes. '
      + 'The data is in <a href="recipes.json">recipes.json</a>.</p>';
  }
}
render();
"""

RECIPE_PAGE_JS = """
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const SLUG = document.body.dataset.slug;
async function render(){
  const el = document.getElementById('recipe');
  let r;
  try {
    const res = await fetch('../recipes.json');
    if(!res.ok) throw new Error(res.status);
    const all = await res.json();
    r = all.find(x => x.slug === SLUG);
    if(!r) throw new Error('not found');
  } catch(e){
    el.innerHTML = '<p class="loadfail">Could not load this recipe. '
      + 'The data is in <a href="../recipes.json">recipes.json</a>.</p>';
    return;
  }
  document.title = r.title + ' \\u00b7 AB';
  document.getElementById('title').textContent = r.title;
  document.getElementById('blurb').textContent = r.blurb;
  document.getElementById('serves').textContent = r.serves;
  document.getElementById('here').textContent = r.title;

  const ing = r.ingredients.map(i => {
    const amt = i.imperial ? esc(i.imperial) + ' ' : '';
    const g = i.grams ? ` <span class="g">(${esc(i.grams)})</span>` : '';
    return `<li>${amt}${esc(i.name)}${g}</li>`;
  }).join('');
  const steps = r.steps.map(s => `<li>${s}</li>`).join('');
  const mac = r.macros.map(m => `<tr><td>${esc(m.label)}</td><td>${esc(m.value)}</td></tr>`).join('');

  el.innerHTML =
    `<aside class="ing"><h2>Ingredients</h2><ul>${ing}</ul></aside>`
  + `<div class="method"><ol>${steps}</ol>`
  + `<div class="macros"><p class="tbl-label">Macros</p>`
  + `<table><tbody>${mac}</tbody></table>`
  + (r.note ? `<p class="tbl-note">${esc(r.note)}</p>` : '')
  + `</div></div>`;
}
render();
"""


CATEGORY_JS = """
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const KEY = document.body.dataset.cat;
const UP  = document.body.dataset.up || '';
async function render(){
  let d;
  try {
    const r = await fetch(UP + 'pages.json');
    if(!r.ok) throw new Error(r.status);
    d = await r.json();
  } catch(e){
    document.getElementById('index').innerHTML =
      '<p class="loadfail">Could not load this page. The text is in '
      + '<a href="' + UP + 'pages.json">pages.json</a>.</p>';
    return;
  }
  const c = d.categories[KEY];
  document.getElementById('title').textContent = c.heading;
  document.getElementById('here').textContent = c.heading;
  document.title = c.heading + ' \u00b7 AB';
  document.getElementById('lede').textContent = c.lede;
  const items = (d.items || {})[KEY];
  const el = document.getElementById('index');
  if (items && items.length) {
    el.className = 'ix';
    el.innerHTML = items.map(i =>
      `<li style="--tc:${esc(document.body.dataset.colour)}"><a href="${esc(i.href)}">`
      + `<span class="tag">${esc(i.title)}</span><p>${esc(i.description)}</p>`
      + `<div class="meta">${i.meta}</div></a></li>`).join('');
  } else {
    el.className = '';
    el.innerHTML = `<div class="empty">${esc(c.empty || 'Nothing posted yet.')}</div>`;
  }
}
render();
"""

VENT_JS = """
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const UP = document.body.dataset.up;
async function render(){
  let d;
  try {
    const r = await fetch(UP + 'pages.json');
    if(!r.ok) throw new Error(r.status);
    d = (await r.json()).vent;
  } catch(e){
    document.getElementById('index').innerHTML =
      '<p class="loadfail">Could not load this page. The text is in '
      + '<a href="' + UP + 'pages.json">pages.json</a>.</p>';
    return;
  }
  document.getElementById('title').textContent = d.heading;
  document.getElementById('here').textContent = d.heading;
  document.title = d.heading + ' \u00b7 AB';
  document.getElementById('lede').textContent = d.lede;
  document.getElementById('index').innerHTML = d.sections.map(s =>
    `<li style="--tc:#8E3324"><a href="${esc(s.href)}">`
    + `<span class="tag">${esc(s.title)}</span><p>${esc(s.description)}</p>`
    + `<div class="meta">${s.meta}</div></a></li>`).join('');
}
render();
"""

PRECOURSE_JS = """
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const UP = document.body.dataset.up;
async function render(){
  let p, v;
  try {
    const r = await fetch(UP + 'pages.json');
    if(!r.ok) throw new Error(r.status);
    v = (await r.json()).vent; p = v.precourse;
  } catch(e){
    document.getElementById('main').innerHTML =
      '<p class="loadfail">Could not load this page. The text is in '
      + '<a href="' + UP + 'pages.json">pages.json</a>.</p>';
    return;
  }
  document.getElementById('title').textContent = p.heading;
  document.getElementById('here').textContent = p.heading;
  document.getElementById('vent-crumb').textContent = v.heading;
  document.getElementById('lede').textContent = p.lede;
  document.getElementById('control').innerHTML = p.control;

  const reading = p.reading.map(r =>
    `<li><a href="${esc(r.page)}" rel="noopener">${esc(r.pageLabel)}</a>, and the `
    + `<a href="${esc(r.pdf)}" rel="noopener">${esc(r.pdfLabel)}</a></li>`).join('');
  const videos = p.videos.map((id,i) =>
    `<div class="embed"><iframe src="https://www.youtube-nocookie.com/embed/${esc(id)}" `
    + `title="Ventilator lecture, part ${i+1}" loading="lazy" allowfullscreen></iframe></div>`).join('');

  document.getElementById('main').innerHTML =
    `<h2 class="sec">${esc(p.examHeading)}</h2><p>${esc(p.examText)}</p>`
  + `<div class="embed embed-form"><iframe src="${esc(p.formUrl)}&amp;embed=true" `
  + `title="Ventilator written examination" loading="lazy" allowfullscreen></iframe></div>`
  + `<p class="credit">If the examination will not load or sign you in here, `
  + `<a href="${esc(p.formUrl)}" rel="noopener">open it in a new tab</a>.</p>`
  + `<h2 class="sec">${esc(p.readingHeading)}</h2><p>${esc(p.readingText)}</p>`
  + `<ul class="pts">${reading}</ul>`
  + `<h2 class="sec">${esc(p.videoHeading)}</h2>${videos}`
  + `<p class="credit">${esc(p.credit)}</p>`;
}
render();
"""

STUB_JS = """
const KEY = document.body.dataset.stub;
const UP  = document.body.dataset.up;
async function render(){
  let d;
  try {
    const r = await fetch(UP + 'pages.json');
    if(!r.ok) throw new Error(r.status);
    d = (await r.json()).vent;
  } catch(e){
    document.getElementById('main').innerHTML =
      '<p class="loadfail">Could not load this page. The text is in '
      + '<a href="' + UP + 'pages.json">pages.json</a>.</p>';
    return;
  }
  const s = d[KEY];
  document.getElementById('title').textContent = s.heading;
  document.getElementById('here').textContent = s.heading;
  document.getElementById('vent-crumb').textContent = d.heading;
  document.getElementById('lede').textContent = s.lede;
  document.getElementById('main').innerHTML = `<div class="empty">${s.empty}</div>`;
}
render();
"""
