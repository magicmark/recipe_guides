# Dinner, sorted.

A small, cheerful, mobile-friendly recipe site: weekly menus, eight-portion recipes, a shopping checklist saved in the current browser, and a printable guide. No backend or JavaScript dependencies.

## Enable GitHub Pages

In [Settings → Pages](https://github.com/magicmark/recipe_guides/settings/pages), choose **Deploy from a branch → main → /docs**, then **Save**.

Expected address after GitHub finishes publishing: https://magicmark.github.io/recipe_guides/

## Add or edit a week

Use `.codex/skills/new-recipes/SKILL.md`. Keep each guide in `week-of-YYYY-MM-DD/README.md`. The site builder reads the headings, recipes and shopping list directly from these files; don't maintain a second copy of recipe data.

Run `python3 site/build.py` from the repository root, then commit the source changes and regenerated `docs/` files. Pages publishes those committed files automatically once enabled. The home page shows the latest week, with dated pages for previous weeks.

The builder supports headings, paragraphs, bold text, inline code, external links, numbered and bulleted lists, task checkboxes and tables. Keep the existing guide's section names and weekday recipe headings. It requires Python 3 and no installed packages.

`site/template.html`, `site/style.css` and `site/app.js` control the presentation. `docs/food-photo.jpg` is a licensed site asset, not generated output; preserve it when rebuilding.

## Photo

[Lemon chicken photograph by Sternsteiger Stahlwaren](https://www.pexels.com/photo/top-view-of-roasted-chicken-on-a-pan-with-fresh-vegetables-lying-around-on-the-table-16510619/), used under the [Pexels license](https://www.pexels.com/license/). It is illustrative rather than a photograph of a tested recipe from this guide.
