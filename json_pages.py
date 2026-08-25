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
  + `<p class="tbl-note">${esc(r.note)}</p></div></div>`;
}
render();
"""
