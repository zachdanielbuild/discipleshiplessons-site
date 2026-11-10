"""Shared site chrome (Nov 2, 2026): one header, one footer and one lesson library,
used on the homepage, the Discipleship Foundations page and every lesson page,
so the whole site reads as one green "seed to fruit" library.

Styles live at the end of site/style.css under "Nov 2: one site".
"""
import html as _h

e = _h.escape

YT = 'https://www.youtube.com/playlist?list=PLoXSy2HiYN4tfZXlu97aZf_y_zBq3rO7E'
CHALLENGE = 'https://passionandpurpose.kit.com/discipleship'
BAPTISM = 'https://antiochwaco.churchcenter.com/registrations/events/2965360'
MEMBERSHIP = 'https://antiochwaco.com/membership'
DEVOTION = 'https://passionandpurpose.kit.com/40-days-of-devotion'
MISSIONS = 'https://antiochwaco.com/missions'

# ---------- the green family, palest (Seekers) to deepest (Further Growth) ----------
# pick: hero answer buttons (bg, dot, text). tile: library tiles (bg, number, text).
SETS = {
    'seekers':        dict(pick=('#CFE5C3', '#5E8F4E', '#15371F'), tile=('#DCEBD2', '#4E7F40', '#15171C')),
    'new-believers':  dict(pick=('#9CCB8A', '#2F6B3A', '#0F3420'), tile=('#BFDDB1', '#2F6B3A', '#15171C')),
    'foundations':    dict(pick=('#4FAE74', '#0F4D30', '#08261A'), tile=('#D7EEDD', '#24764A', '#15171C')),
    'look-up':        dict(tile=('#D7EEDD', '#24764A', '#15171C')),
    'look-in':        dict(tile=('#A9D9B9', '#155C37', '#15171C')),
    'look-out':       dict(tile=('#4FAE74', '#0B3A24', '#08261A')),
    'further-growth': dict(pick=('#1F5C3E', '#B9E2C5', '#FFFFFF'), tile=('#1F5C3E', '#B9E2C5', '#FFFFFF')),
}
# lesson pages: --track is the strong color (white text sits on it), --tint the soft band behind the title
TRACK = {
    'seekers': ('#3F6B35', '#EEF5E8'),
    'new-believers': ('#2F6B3A', '#E6F1DE'),
    'look-up': ('#24764A', '#E9F5EC'),
    'look-in': ('#1E6B42', '#DDEFE3'),
    'look-out': ('#135C38', '#D6EDDE'),
    'freedom': ('#1E6B42', '#DDEFE3'),
    'deeper': ('#1F5C3E', '#E3EEE7'),
    'guides': ('#15171C', '#F1F4EE'),
}

STAR = '<svg width="14" height="14" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2l2.9 6.6 7.1.6-5.4 4.7 1.6 7-6.2-3.7-6.2 3.7 1.6-7L2 9.2l7.1-.6z" fill="currentColor"></path></svg>'
MENU_ICON = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16"></path><path d="M4 12h16"></path><path d="M4 17h16"></path></svg>'
PIN = '<svg width="14" height="19" viewBox="0 0 24 32" aria-hidden="true"><path d="M12 1C6.5 1 2 5.4 2 10.9c0 7.6 10 20.1 10 20.1s10-12.5 10-20.1C22 5.4 17.5 1 12 1z" fill="#EA4335"></path><circle cx="12" cy="11" r="3.8" fill="#A50E0E"></circle></svg>'


def header(logo, home=False):
    """Logo, four links, Start here. On phones the links fold into a Menu button."""
    h = '' if home else 'index.html'
    links = [(f'{h}#library', 'Lessons'), (YT, 'Videos'), ('#experiences', 'Experiences'), (f'{h}#faq', 'About')]
    nav = ''.join(f'<a href="{u}">{t}</a>' for u, t in links)
    return (f'<header class="topbar"><div class="topbar-in">'
            f'<a class="brand" href="{h or "#top"}">{logo}<span>DiscipleshipLessons.com</span></a>'
            f'<nav id="mainnav" aria-label="Main">{nav}</nav>'
            f'<a class="start" href="who-should-i-disciple.html">Start here</a>'
            f'<button type="button" class="menu-btn" aria-expanded="false" aria-controls="mainnav" '
            f'onclick="var h=this.closest(\'header\');var o=h.classList.toggle(\'open\');this.setAttribute(\'aria-expanded\',o)">'
            f'{MENU_ICON}<span class="sr-only">Menu</span></button>'
            f'</div></header>')


def footer(home=False):
    h = '' if home else 'index.html'
    cols = [
        ('Lessons', None, [(f'{h}#seekers', 'Seekers'), (f'{h}#new-believers', 'New Believers'), (f'{h}#look-up', 'Look Up'),
                           (f'{h}#look-in', 'Look In'), (f'{h}#look-out', 'Look Out'), (f'{h}#further-growth', 'Further Growth')]),
        ('Start here', None, [('who-should-i-disciple.html', 'Who should I disciple?'), (CHALLENGE, 'Disciplemakers Challenge'),
                              (YT, 'Life on Life series'), (f'{h}#faq', 'Questions')]),
        ('Experiences', 'experiences', [(DEVOTION, '40 Days of Devotion'), ('the-freedom-prayer-experience.html', 'Freedom Prayer'),
                                        (BAPTISM, 'Baptism'), (MEMBERSHIP, 'Church Membership'), (MISSIONS, 'Mission Trips')]),
    ]
    c = ''.join(f'<div class="foot-col"{f" id={chr(34)}{i}{chr(34)}" if i else ""}><span class="foot-label">{t}</span>'
                + ''.join(f'<a href="{u}">{n}</a>' for u, n in ls) + '</div>' for t, i, ls in cols)
    return f'''<footer class="sitefoot"><div class="foot-in">
<div class="foot-top">
<div class="foot-brand"><span class="foot-name">DiscipleshipLessons.com</span>
<span class="foot-tag">Simple and powerful lessons to help you make disciples in your sphere of influence.</span>
<span class="foot-place">{PIN}Made in Waco, Texas, for neighborhoods and nations.</span>
<a class="foot-btn" href="{CHALLENGE}">Take the Disciplemakers Challenge</a></div>
<div class="foot-cols">{c}</div>
</div>
<div class="foot-bottom"><span>Made with love by the folks at <a href="https://antiochwaco.com/">Antioch Waco</a>. Free to use, print and share.</span><span>© 2026 Antioch Community Church</span></div>
</div></footer>'''


# ---------- the lesson library ----------
def library(slug, titles, previews=False):
    """Every set in order. previews=True adds the longer set descriptions (Foundations page)."""
    L = lambda i: slug(i) + '.html'

    def tiles(key, ids, ex=()):
        bg, num, fg = SETS[key]['tile']
        out = f'<div class="lib-tiles" style="--tb:{bg};--tn:{num};--tf:{fg}">'
        for k, i in enumerate(ids, 1):
            out += f'<a class="lib-tile" href="{L(i)}"><span class="lib-num">{k}</span><span class="lib-title">{e(titles[i])}</span></a>'
        for name, cta, href in ex:
            out += (f'<a class="lib-tile lib-exp" href="{href}"><span class="lib-star">{STAR}Experience</span>'
                    f'<span class="lib-title">{e(name)}</span><span class="lib-cta">{cta} →</span></a>')
        return out + '</div>'

    def head(key, name, desc, meta, tag='h3'):
        dot ={'seekers': '#5E8F4E', 'new-believers': '#9CCB8A', 'foundations': '#4FAE74', 'further-growth': '#1F5C3E'}[key]
        return (f'<div class="lib-head"><span class="lib-dot" style="background:{dot}"></span><{tag}>{name}</{tag}>'
                f'<span class="lib-meta">{meta}</span><p class="lib-desc">{desc}</p></div>')

    def prev(t):
        return f'<p class="lib-preview">{e(t)}</p>' if previews else ''

    def part(key, label, desc, ids, ex=()):
        return (f'<div class="lib-part" id="{key}"><p class="lib-part-head"><span>{label}</span>{desc}</p>{tiles(key, ids, ex)}</div>')

    s = []
    s.append(f'<div class="lib-set" id="seekers">{head("seekers", "Seekers", "For someone who isn’t sure about Jesus yet.", "1 study · 3 reading plans")}'
             + prev('This study is designed to be done with non-Christians who are interested in Jesus. You will read through the Gospel of John together and learn more about Him.')
             + tiles('seekers', [6]) + '</div>')
    s.append(f'<div class="lib-set" id="new-believers">{head("new-believers", "New Believers", "For someone who just said yes to following Jesus.", "6 lessons · about 6 weeks")}'
             + prev('These lessons are designed to be done with new believers. You will focus on the gospel, baptism, deliverance and church membership.')
             + tiles('new-believers', [7, 8, 9, 10, 11, 12], [('Baptism Sign Up', 'Sign up', BAPTISM), ('Church Membership Class Sign Up', 'Sign up', MEMBERSHIP)]) + '</div>')
    s.append(f'<div class="lib-set" id="foundations">{head("foundations", "Discipleship Foundations", "For a believer who wants to grow.", "15 lessons · 3 parts · about 4 months")}'
             + prev('Fifteen lessons that build a lifestyle of knowing, loving and walking with Jesus. Do the three parts in order.')
             + part('look-up', 'Part 1 · Look Up', 'These lessons focus on growing a lifestyle of loving Jesus and walking with Him daily. Practically, this unit will help the person you are discipling start, strengthen, or reignite the daily habit of spending time with the Lord.', [2, 3, 1, 4, 5, 13], [('40 Days of Devotion', 'Join', DEVOTION)])
             + part('look-in', 'Part 2 · Look In', 'These lessons focus on growing a lifestyle of holiness, love, and Christlike character. Practically, this unit will help the person you are discipling walk through a freedom experience of confessing sin, finding healing, and being filled with the Holy Spirit and the truth of God’s Word.', [14, 15, 16, 17, 18], [('Freedom Prayer Experience', 'Open', 'the-freedom-prayer-experience.html')])
             + part('look-out', 'Part 3 · Look Out', 'Growing in a Great Commission lifestyle.', [19, 20, 21, 22], [('Short-Term Mission Trip', 'See trips', MISSIONS)])
             + '</div>')
    s.append(f'<div class="lib-set" id="further-growth">{head("further-growth", "Further Growth", "For when you finish the Foundations: bearing fruit in every good work and growing in the knowledge of God.", "1 guide")}'
             + prev('Plan your next season of discipleship together with good questions, books and practices.')
             + tiles('further-growth', [34]) + '</div>')
    return '<div class="lib">' + ''.join(s) + '</div>'


def picks(items):
    """Pill buttons in the set colors: [(href, key, label)]."""
    out = '<div class="picks">'
    for href, key, label in items:
        bg, dot, fg = SETS[key]['pick']
        out += f'<a href="{href}" style="background:{bg};color:{fg}"><span style="background:{dot}"></span>{label}</a>'
    return out + '</div>'
