Source for abarker.org.

Static HTML, CSS, and JSON. No build step, no framework, no npm. Every file
committed here is a file the browser requests; source and deployed output are
identical.

## Content in JSON

Three files hold the site's text. Edit them directly, commit, push. Nothing
needs regenerating.

    site.json               landing page: bio, contact, the five categories
    pages.json              every other page's headings and body text
    recipes/recipes.json    all recipes: ingredients, steps, macros, notes

The pages fetch these at load and render client-side. The recipe count on the
landing page is derived from recipes.json, so adding a recipe updates the count
on its own.

To add a recipe, append an object to recipes/recipes.json following the shape of
the existing entries, then create recipes/<slug>/index.html by copying any
existing recipe page and changing the data-slug attribute on the body tag.

## Regenerating

build.py regenerates the whole tree from json/ and the page definitions inside
it. You do not need to run it to change text. You do need it if you change page
structure, the stylesheet, or add a category.

    python3 build.py

Requires Python 3.

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
