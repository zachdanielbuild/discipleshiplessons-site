#!/usr/bin/env bash
# Rebuild every page and copy the result to the repo root (what Cloudflare Pages serves).
# Usage: bash build/deploy.sh   (from anywhere). Then commit and push to main.
set -e
B="$(cd "$(dirname "$0")" && pwd)"; R="$(dirname "$B")"
cd "$B" && python3 buildsite.py && python3 launchfiles.py
for f in "$B"/site/*.html "$B"/site/_redirects "$B"/site/robots.txt "$B"/site/sitemap.xml "$B"/site/share.png "$B"/site/apple-touch-icon.png "$B"/site/favicon.svg "$B"/site/style.css; do
  b=$(basename "$f"); [ "$b" = index.html ] || cp "$f" "$R/"
done
python3 - "$B/site/index.html" "$R/index.html" <<'PY'
import sys
s=open(sys.argv[1]).read()
i=s.index('<div class="site home">'); head=s[:i]; body=s[i:]
lines=head.split('\n',1)
e=lambda v: v.replace('&','&amp;').replace('"','&quot;')
d='Simple and powerful lessons to help you make disciples in your sphere of influence. A time-tested resource from Antioch for neighborhoods and nations.'
meta=f'''<meta name="description" content="{e(d)}">
<link rel="canonical" href="https://www.discipleshiplessons.com/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="DiscipleshipLessons">
<meta property="og:title" content="DiscipleshipLessons">
<meta property="og:description" content="{e(d)}">
<meta property="og:url" content="https://www.discipleshiplessons.com/">
<meta property="og:image" content="https://www.discipleshiplessons.com/share.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">'''
open(sys.argv[2],'w').write('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'+lines[0]+'\n'+meta+'\n'+lines[1].rstrip()+'\n</head>\n<body>\n'+body.rstrip()+'\n</body>\n</html>\n')
PY
echo "Built. Now: git add -A && git commit && git push"
