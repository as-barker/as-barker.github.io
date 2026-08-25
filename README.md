Source for abarker.org.

Static HTML, CSS, and JSON. No build step, no framework, no npm. Every file
committed here is a file the browser requests; source and deployed output are
identical.

## Content in JSON

Two files hold content that changes often. Edit them directly, commit, push.
Nothing needs regenerating.

    site.json               the five categories on the landing page:
                            name, description, colour, count, revision date
    recipes/recipes.json    all recipes: ingredients, steps, macros, notes

The pages fetch these at load and render client-side. The recipe count on the
landing page is derived from recipes.json, so adding a recipe updates the count
on its own.

To add a recipe, append an object to recipes/recipes.json following the shape of
the existing entries, then create recipes/<slug>/index.html by copying any
existing recipe page and changing the data-slug attribute on the body tag.

## Content in HTML

Long documents are hand-authored HTML, not JSON. Prose with tables does not
survive being escaped into a JSON string, and the diffs become unreadable.

    evidence/prehospital-blood/index.html
    training/vent/**/index.html
    programs/, austere/          category stubs

## Regenerating

build.py regenerates the whole tree into dist/ from json/ and the page
definitions inside it. You do not need to run it to change JSON content. You do
need it if you change page structure, the stylesheet, or add a category.

    python3 build.py

Requires Python 3 and the markdown package for the evidence review only.

## Local preview

Because the pages fetch JSON, opening index.html directly from the filesystem
will not work; the browser blocks the request. Serve the directory instead:

    python3 -m http.server 8000

Then open http://localhost:8000

## Deployment

GitHub Pages, main branch, root. The CNAME file binds abarker.org. DNS is an
ALIAS on the apex and a CNAME on www, both to as-barker.github.io.

## Known dependencies

Fonts load from Google at view time. Self-hosting them would remove the last
third-party call on the site.
