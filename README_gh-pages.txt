arcadeKh4n — Game Hub (gh-pages bundle)

Unzip these files to your repo root and push them to the gh-pages branch (or follow the commands I provided earlier).

To publish:
1. git checkout --orphan gh-pages
2. git reset --hard
3. cp -r path/to/unzipped/* .
4. git add index.html web && git commit -m "Publish web hub to gh-pages" && git push -u origin gh-pages

Visit your repository Settings → Pages to confirm the published URL.
