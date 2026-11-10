# Discipleship Foundations page body.
# Nov 2, 2026: rebuilt in the homepage's green library look. The same library parts as the
# homepage (chrome.library) with the longer set descriptions, under a matching hero.
# Styles live at the end of site/style.css under "Nov 2: one site".
import chrome


def body(slug, ARROW, titles):
    picks = chrome.picks([('#seekers', 'seekers', '1 · Seekers'), ('#new-believers', 'new-believers', '2 · New Believers'),
                          ('#foundations', 'foundations', '3 · Foundations')])
    hero = f'''<section class="fd2-hero"><div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a></nav>
<h1>Discipleship Foundations</h1>
<p class="fd2-lead">Jesus calls all of us to make disciples (Matthew 28). These lessons can help you fulfill that calling. Start wherever the person you’re meeting with is.</p>
{picks}
</div></section>'''
    main = f'<section class="fd2-library"><div class="lib-wrap">{chrome.library(slug, titles, previews=True)}</div></section>'
    return hero, main, ''
