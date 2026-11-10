"""Library homepage (Nov 1, 2026): the BibleProject-style "library" design.

Source is home_library.html (the approved mockup, edited by hand).
This module turns its links into real site links and returns the page body.
Nov 2: the header, hero answer buttons, the whole library and the footer now come
from chrome.py, so the homepage and every other page share one set of parts.
"""
import os, re
import chrome

D = os.path.dirname(os.path.abspath(__file__)) + '/'
LIVE = 'https://discipleshiplessons-site.pages.dev/'


def _sub(h, pat, rep, flags=re.S):
    h2, n = re.subn(pat, lambda m: rep, h, count=1, flags=flags)
    assert n == 1, pat[:60]
    return h2


def library_home(yt, footer, logo, slug=None, titles=None):
    h = open(D + 'home_library.html').read()
    h = re.sub(re.escape(LIVE) + r'([a-z0-9-]+)"', r'\1.html"', h)
    h = h.replace('<a href="#" style="display: inline-block; background: #15171C;', '<a href="ambassador.html" style="display: inline-block; background: #15171C;', 1)
    # shared header
    h = _sub(h, r'<header.*?</header>', chrome.header(logo, home=True))
    # hero: an anchor, and the four answer buttons from the shared parts
    h = h.replace('<section style="padding: 64px 24px 40px; text-align: center;">', '<section id="top" class="home-hero" style="padding: 64px 24px 40px; text-align: center;">', 1)
    h = _sub(h, r'<div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; max-width: 900px; margin: 0 auto;">.*?</div>',
             chrome.picks([('#seekers', 'seekers', 'Someone curious about Jesus'), ('#new-believers', 'new-believers', 'A brand new believer'),
                           ('#foundations', 'foundations', 'A believer who wants to grow'), ('#further-growth', 'further-growth', "Someone ready for what's next")]))
    h = h.replace('<section style="padding: 0 24px 72px;">\n<div class="setcards"', '<section class="home-cards" style="padding: 0 24px 72px;">\n<div class="setcards"', 1)
    h = h.replace('<section style="padding: 0 24px 72px;">\n<div style="max-width: 1200px; margin: 0 auto; background: #EEF3EA;', '<section class="home-peek" style="padding: 0 24px 72px;">\n<div style="max-width: 1200px; margin: 0 auto; background: #EEF3EA;', 1)
    assert 'home-cards' in h and 'home-peek' in h
    # the library itself
    lib = ('<section id="library" class="home-library"><div class="lib-wrap">'
           '<div class="lib-intro"><h2>The whole library</h2><p>Twenty-three lessons in the order we walk them. Tap any one to open it.</p></div>'
           + chrome.library(slug, titles) + '</div></section>')
    h = _sub(h, r'<section id="library".*?</section>', lib)
    h = h.replace('<section style="background: #FBF7F0; padding: 72px 24px;">', '<section id="faq" style="background: #FBF7F0; padding: 72px 24px;">', 1)
    h = _sub(h, r'<footer.*?</footer>', footer)
    h = great_commission(h, logo)
    assert 'href="#"' not in h and 'pages.dev' not in h
    return h


# Nov 3, 2026: brand green header and "Go and make disciples." hero, the white
# Antioch A in place of the tree (homepage only), and no set cards: the lesson
# peek sits right under the hero. Styles: the "Nov 3" block at the end of style.css.
HERO = '''<section id="top" class="home-hero gc-hero">
<span class="gc-e">Matthew 28:19</span>
<h1 class="gc-h">Go and make<br><span class="gc-a">disciples.</span></h1>
<p class="gc-p">Jesus calls all of us to make disciples. These lessons can help you fulfill that calling with the people already in your life.</p>
<div class="gc-ask">
<span class="gc-l">Who are you meeting with this week?</span>
<div class="gc-pills">
<a class="p1" href="#seekers">A seeker</a>
<a class="p2" href="#new-believers">A new believer</a>
<a class="p3" href="#foundations">A growing disciple</a>
</div>
<span class="gc-free">Free to use, print and share.</span>
</div>
</section>'''


def great_commission(h, logo):
    mark = '<img class="antioch-a" src="/antioch-a-white.png" alt="" width="40" height="40">'
    i = h.index('</header>')
    head = h[:i].replace('<header class="topbar">', '<header class="topbar gc-top">', 1)
    assert logo in head
    h = head.replace(logo, mark, 1) + h[i:]
    h = _sub(h, r'<section id="top" class="home-hero".*?</section>', HERO)
    h = _sub(h, r'<section class="home-cards".*?</section>\s*', '')
    old = '<section class="home-peek" style="padding: 0 24px 72px;">'
    assert old in h
    return h.replace(old, '<section class="home-peek" style="padding: 64px 24px 72px;">', 1)
