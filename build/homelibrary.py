"""Library homepage (Nov 1, 2026): the BibleProject-style "library" design.

Source is home_library.html (the approved mockup, edited by hand).
This module turns its links into real site links and returns the page body.
"""
import os, re

D = os.path.dirname(os.path.abspath(__file__)) + '/'
LIVE = 'https://discipleshiplessons-site.pages.dev/'


def library_home(yt, footer, logo):
    h = open(D + 'home_library.html').read()
    # lesson links in the mockup point at the test site; make them relative like every other page
    h = re.sub(re.escape(LIVE) + r'([a-z0-9-]+)"', r'\1.html"', h)
    # placeholder links in the header and the peek
    fixes = [
        ('<a href="#" style="display: flex; align-items: center; gap: 10px; color: #15171C;', '<a href="index.html" style="display: flex; align-items: center; gap: 10px; color: #15171C;'),
        ('<a href="#" style="text-decoration: none;">Videos</a>', f'<a href="{yt}" style="text-decoration: none;">Videos</a>'),
        ('<a href="#" style="text-decoration: none;">Experiences</a>', '<a href="#new-believers" style="text-decoration: none;">Experiences</a>'),
        ('<a href="#" style="text-decoration: none;">About</a>', '<a href="#faq" style="text-decoration: none;">About</a>'),
        ('<a href="#" style="display: inline-block; background: #15171C;', '<a href="ambassador.html" style="display: inline-block; background: #15171C;'),
    ]
    for a, b in fixes:
        assert h.count(a) == 1, a
        h = h.replace(a, b)
    # the mockup's search box isn't wired up yet: swap it for a Start here button
    h, n = re.subn(r'<label for="search".*?</label>\s*<input id="search"[^>]*>',
                   '<a href="who-should-i-disciple.html" style="background: #15171C; color: #FFFFFF; text-decoration: none; font-weight: 700; font-size: 14px; padding: 9px 16px; border-radius: 999px;">Start here</a>',
                   h, count=1, flags=re.S)
    assert n == 1
    # the site logo (pin and ripples) in place of the mockup's plain pin
    h, n = re.subn(r'<svg width="22" height="28" viewBox="0 0 24 30".*?</svg>', logo, h, count=1, flags=re.S)
    assert n == 1
    # FAQ gets an anchor; the mockup's simple footer becomes the site footer
    h = h.replace('<section style="background: #FBF7F0; padding: 72px 24px;">', '<section id="faq" style="background: #FBF7F0; padding: 72px 24px;">', 1)
    h = re.sub(r'<footer.*?</footer>', footer, h, count=1, flags=re.S)
    assert 'href="#"' not in h and 'pages.dev' not in h
    return h
