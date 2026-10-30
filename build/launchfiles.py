import re,json,os,html
D=os.path.dirname(os.path.abspath(__file__))+'/'
S=D+'site/'
open(S+'_redirects','w').write('''# Old Squarespace addresses
/start-here            /discipleship-foundation-lessons   301
/lessons               /discipleship-foundation-lessons   301
/whats-next            /going-deeper-in-discipleship      301
/home                  /                                  301
/faq                   /#faq                              301
/devoted-to-gods-word  /devoted-to-the-word               301
# Clean addresses (Oct 30)
/john-wesleys-22-accountability-questoins  /john-wesleys-22-questions  301
/john-wesleys-22-accountability-questions  /john-wesleys-22-questions  301
/whats-next-1  /disciplemaking-stories  301
# Tending Your Heart worksheets moved off Squarespace
/s/Tending-Your-Heart-Handout-1_-Invitation-to-Intimacy.pdf  /files/tending-your-heart-1-invitation-to-intimacy.pdf  301
/s/Tending-Your-Heart-Handout-2_-Hindrances-To-Hearing-God.pdf  /files/tending-your-heart-2-hindrances-to-hearing-god.pdf  301
/s/Tending-Your-Heart-Handout-3_-Overcoming-Wounds-Lies.pdf  /files/tending-your-heart-3-overcoming-wounds-and-lies.pdf  301
/s/Part-4-Handout-Tending-Your-Heart.pdf  /files/tending-your-heart-4-how-to-tend-your-heart.pdf  301
# Retired Discipleship Roadmap PDF
/s/DiscipleshipRoadmap.pdf  /discipleship-foundation-lessons  301
# Keep the build kit off the public site
/build/*  /page-not-found  302
''')
open(S+'robots.txt','w').write('User-agent: *\nAllow: /\nSitemap: https://www.discipleshiplessons.com/sitemap.xml\n')
pages=sorted(f[:-5] for f in os.listdir(S) if f.endswith('.html') and f not in('404.html',))
urls=''.join(f'<url><loc>https://www.discipleshiplessons.com/{"" if p=="index" else p}</loc></url>\n' for p in pages)
open(S+'sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+urls+'</urlset>\n')
# 404 page from a lesson page's chrome
t=open(S+'discipleship-foundation-lessons.html').read()
head=t[:t.index('<main>')]; foot=t[t.index('</main>'):]
head=re.sub(r'<title>.*?</title>','<title>Page not found | DiscipleshipLessons.com</title>',head)
head=re.sub(r'<meta name="description"[^>]*>\n<link rel="canonical"[^>]*>\n(<meta property[^>]*>\n|<meta name="twitter[^>]*>\n?)*','',head)
foot=re.sub(r'<script>.*?</script>\n','',foot,flags=re.S)
body='''<main>
<section class="lesson-hero"><div class="wrap"><div class="hero-main">
<span class="pill">Page not found</span>
<h1>We couldn’t find that page.</h1>
<p class="hero-lead">The lessons may have moved when the site was updated. These will get you back on track.</p>
</div></div></section>
<div class="wrap foundations"><div class="rows" style="max-width: 640px">
<a class="row" href="/discipleship-foundation-lessons"><span class="num" style="background:#1D1D1D">1</span><span class="row-title">All the Discipleship Foundations lessons</span></a>
<a class="row" href="/who-should-i-disciple"><span class="num" style="background:#1D1D1D">2</span><span class="row-title">Who should I disciple?</span></a>
<a class="row" href="/"><span class="num" style="background:#1D1D1D">3</span><span class="row-title">Back to the homepage</span></a>
</div></div>
'''
h404=head+body+foot
h404=h404.replace('href="index.html','href="/index.html').replace('href="style.css"','href="/style.css"').replace('href="favicon.svg"','href="/favicon.svg"').replace('href="apple-touch-icon.png"','href="/apple-touch-icon.png"')
h404=re.sub(r'href="([a-z0-9-]+)\.html','href="/\\1',h404)
open(S+'404.html','w').write(h404)
print('ok',len(pages))
