arcadeKh4n — Web Hub

This small web bundle gives you a lightweight, dynamic hub for the games in this repo.

How to use
1. Unzip these files into the root of your arcadeKh4n repository (so index.html and web/ folder are at repo root).
2. Commit and push, or use GitHub Pages:
   - For GitHub Pages from `main/docs/`: move the `web/` folder and `index.html` under `docs/` and enable Pages.
   - For GitHub Pages from `gh-pages` branch: put the site root on that branch.
3. The hub lists each game's file and provides a "View / Download" link (runs must be done locally — Python not executed in browser).

Local usage:
- To preview locally, you can open index.html in a browser (links to local repo files will work if served), or run a local static server:
  python -m http.server 8000
  and open http://127.0.0.1:8000/index.html

Notes:
- The hub references Python files (relative links). It doesn’t execute them in-browser — users should download and run games locally.
- You can customize web/games.json to show new games or add descriptions/tags.
- If you want me to add search-by-tag, or embed code excerpts, I can extend the page.
