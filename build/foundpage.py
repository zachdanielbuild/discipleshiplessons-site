# Discipleship Foundations page body (Oct 29, 2026 design: "green band" option).
# Four stops: Seekers, New Believers, Foundations (a band holding Look Up, Look In, Look Out), Further Growth.
# Styles live in site/style.css under "foundations page (fd-)".
import html as _h

RED, INK, GREEN, GOLD = '#D9483B', '#1D1D1D', '#006747', '#B8862F'
PARTS_C = {'up': ('#B9E2C5', '#1D1D1D'), 'in': ('#4FAE74', '#1D1D1D'), 'out': ('#006747', '#FFFFFF')}
ICON = {'up': '<path d="M12 19V5"></path><path d="M6 11l6-6 6 6"></path>',
        'in': '<path d="M12 5v14"></path><path d="M6 13l6 6 6-6"></path>',
        'out': '<path d="M5 12h14"></path><path d="M13 6l6 6-6 6"></path>'}
BAPTISM = 'https://antiochwaco.churchcenter.com/registrations/events/2965360'
MEMBERSHIP = 'https://antiochwaco.com/membership'
DEVOTION = 'https://passionandpurpose.kit.com/40-days-of-devotion'


def icon(k, size=22, sw=2.8):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[k]}</svg>'


def body(slug, ARROW):
    L = lambda i: slug(i) + '.html'
    e = _h.escape

    def rows(items, bg, fg):
        return '<div class="fd-rows">' + ''.join(
            f'<a class="fd-row" href="{L(i)}"><span class="fd-num" style="background:{bg};color:{fg}">{k}</span><span class="fd-row-title">{e(t)}</span>{ARROW}</a>'
            for k, (i, t) in enumerate(items, 1)) + '</div>'

    def exps(label, ex):
        if not ex:
            return ''
        return f'<div class="fd-exp"><span>{label}</span>' + ''.join(f'<a href="{h}">{e(t)}</a>' for t, h in ex) + '</div>'

    def toggle(n):
        return f'<span class="fd-toggle"><span class="more">Show {n}</span><span class="less">Hide</span></span>'

    def stop(anchor, num, color, fg, name, count, quote, preview, items, ex=()):
        n = f'{len(items)} lesson' + ('s' if len(items) > 1 else '') if anchor != 'further-growth' else '1 guide'
        if anchor == 'seekers':
            n = '1 study'
        return f'''<section class="fd-stop" id="{anchor}" style="--c:{color}">
<span class="fd-marker" style="background:{color};color:{fg}" aria-hidden="true">{num}</span>
<div class="fd-card"><div class="fd-stripe" aria-hidden="true"></div>
<details class="fd-fold" open{' data-single' if len(items)==1 else ''}><summary><span class="fd-head"><h2>{e(name)}</h2><span class="fd-meta">{count} · “{e(quote)}”</span></span>{'' if len(items)==1 else toggle(n)}</summary>
<div class="fd-inner"><p class="fd-preview">{e(preview)}</p>{rows(items, color, fg)}{exps('Experiences', ex)}</div>
</details></div></section>'''

    def part(k, key, name, preview, items, ex=()):
        bg, fg = PARTS_C[key]
        return f'''<section class="fd-part" id="{name.lower().replace(' ', '-')}">
<span class="fd-part-marker" style="background:{bg};color:{fg}" aria-hidden="true">{icon(key, 24, 3)}</span>
<div class="fd-part-card"><details class="fd-fold" open><summary class="fd-part-head" style="background:{bg};color:{fg}"><h3>Part {k}: {name}</h3><span class="fd-part-count">{len(items)} lessons</span>{toggle(f'{len(items)} lessons')}</summary>
<div class="fd-inner"><p class="fd-preview">{e(preview)}</p>{rows(items, bg, fg)}{exps('Experience', ex)}</div>
</details></div></section>'''

    journey = [('seekers', '1', 'Seekers', '1 study', RED, '#FFFFFF'),
               ('new-believers', '2', 'New Believers', '6 lessons', INK, '#FFFFFF'),
               ('foundations', '3', 'Foundations', '15 lessons · 3 parts', GREEN, '#FFFFFF'),
               ('further-growth', '4', 'Further Growth', '1 guide', GOLD, '#1D1D1D')]
    jbar = '<nav class="fd-journey" aria-label="The journey">' + ''.join(
        f'<a href="#{a}"><span class="fd-jnum" style="background:{c};color:{f}">{n}</span><span><strong>{t}</strong><span>{m}</span></span></a>'
        for a, n, t, m, c, f in journey) + '</nav>'

    seekers = stop('seekers', '1', RED, '#FFFFFF', 'Seekers', '1 study', 'They’re not sure about Jesus...',
                   'This study is designed to be done with non-Christians who are interested in Jesus. In it, you will read through the Gospel of John together and learn more about Him.',
                   [(6, 'Gospel of John Bible Study')])
    nb = stop('new-believers', '2', INK, '#FFFFFF', 'New Believers', '6 lessons', 'They just said yes to following Jesus',
              'This set of discipleship lessons is designed to be done with new believers. In it, you will focus on the Gospel, baptism, deliverance and church membership.',
              [(7, 'The Gospel'), (8, 'Your Testimony'), (9, 'Water Baptism'), (10, 'Deliverance'), (11, 'Baptism in the Holy Spirit'), (12, 'Church Membership')],
              [('Baptism', BAPTISM), ('Church Membership', MEMBERSHIP)])
    parts = (part(1, 'up', 'Look Up', 'Lays the foundation for developing a lifestyle of knowing, loving and walking with the Lord.',
                  [(2, 'Vision for a Vibrant Relationship with the Lord'), (3, 'Devoted to God’s Word'), (1, 'Devoted to Worship'), (4, 'Devoted to Prayer'), (5, 'Devoted to Listening'), (13, 'Devoted to Abiding and Obeying')],
                  [('40 Days of Devotion', DEVOTION)])
             + part(2, 'in', 'Look In', 'Lays the foundation for a lifestyle of holiness, love and Christlike character. Best after Look Up.',
                    [(14, 'Our New Life in Christ'), (15, 'Confession: Agreeing with God’s Truth'), (16, 'Repentance: Turning Away from Sin'), (17, 'Replacement: Weeding and Feeding'), (18, 'Restoration: Living in Holiness and Love')],
                    [('Freedom Prayer Experience', 'the-freedom-prayer-experience.html')])
             + part(3, 'out', 'Look Out', 'Lays the foundation for a Great Commission lifestyle. Best after Look Up and Look In.',
                    [(19, 'Your Identity as a Witness and Ambassador'), (20, 'Your Sphere of Influence'), (21, 'Sharing the Gospel with Confidence'), (22, 'Making Disciples Who Make Disciples')]))
    found = f'''<section class="fd-found" id="foundations">
<div class="fd-found-head"><span class="fd-marker" style="background:{GREEN};color:#FFFFFF" aria-hidden="true">3</span><span class="fd-head"><h2>Discipleship Foundations</h2><span class="fd-meta">15 lessons in 3 parts · “They want to grow”</span></span></div>
<div class="fd-band">
<div class="fd-band-top"><p>Fifteen lessons for a growing disciple that build a lifestyle of knowing, loving and walking with Jesus. Do the three parts in order.</p>
<div class="fd-order" aria-label="Order"><a href="#look-up" style="background:#B9E2C5">Look Up</a><span aria-hidden="true">→</span><a href="#look-in" style="background:#4FAE74">Look In</a><span aria-hidden="true">→</span><a href="#look-out" style="background:#FFFFFF;color:{GREEN}">Look Out</a></div></div>
<div class="fd-parts">{parts}</div>
</div></section>'''
    grow = stop('further-growth', '4', GOLD, '#1D1D1D', 'Further Growth', '1 guide', 'They’re ready for what’s next',
                'When you finish these foundations, you might be asking “what’s next?” Plan your next season of discipleship together with good questions, books and practices.',
                [(34, 'Further Growth Planning Guide')])
    hero = f'''<section class="fd-hero"><div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a></nav>
<h1>Discipleship Foundations</h1>
<p class="fd-lead">Jesus calls all of us to make disciples (Matthew 28). These lessons can help you fulfill that calling.</p>
{jbar}
</div></section>'''
    main = f'''<div class="wrap fd-wrap"><div class="fd-trail">{seekers}{nb}{found}{grow}</div></div>'''
    script = '''<script>(function(){var m=window.matchMedia('(max-width: 720px)');var h=location.hash.slice(1);document.querySelectorAll('.fd-fold').forEach(function(d){var sec=d.closest('section');if(m.matches&&!d.hasAttribute('data-single')&&!(h&&sec&&sec.id===h))d.open=false;d.querySelector('summary').addEventListener('click',function(e){if(!m.matches||d.hasAttribute('data-single'))e.preventDefault();});});window.addEventListener('beforeprint',function(){document.querySelectorAll('.fd-fold').forEach(function(d){d.open=true;});});document.querySelectorAll('a[href^="#"]').forEach(function(a){a.addEventListener('click',function(){var t=document.getElementById(a.getAttribute('href').slice(1));if(t){var d=t.querySelector('.fd-fold');if(d)d.open=true;}});});})();</script>'''
    return hero, main, script
