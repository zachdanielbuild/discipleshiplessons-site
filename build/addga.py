"""Google Analytics 4 (Nov 15, 2026): property "DiscipleshipLessons.com" (564376811), measurement ID G-RNY0H1PHDL.
Adds the Google tag right after <head> on every page in the repo root. Run by deploy.sh; safe to run twice."""
import sys, glob, os

ID = 'G-RNY0H1PHDL'
TAG = ('<!-- Google tag (gtag.js) -->\n'
       f'<script async src="https://www.googletagmanager.com/gtag/js?id={ID}"></script>\n'
       "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}"
       f"gtag('js',new Date());gtag('config','{ID}');</script>")

n = 0
for f in glob.glob(os.path.join(sys.argv[1], '*.html')):
    s = open(f).read()
    if ID in s or '<head>' not in s:
        continue
    open(f, 'w').write(s.replace('<head>', '<head>\n' + TAG, 1))
    n += 1
print('GA tag added to', n, 'pages')
