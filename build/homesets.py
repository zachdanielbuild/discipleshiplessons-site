# Homepage "lesson sets" section: four tabs (Seekers, New Believers, Foundations, Further Growth).
# New Believers is open by default. Styles live in site/style.css under "homepage lesson sets".
import html as _h

ARR = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14"></path><path d="M13 6l6 6-6 6"></path></svg>'
PART_ICON = {
    'up': '<path d="M12 19V5"></path><path d="M6 11l6-6 6 6"></path>',
    'in': '<path d="M12 5v14"></path><path d="M6 13l6 6 6-6"></path>',
    'out': '<path d="M5 12h14"></path><path d="M13 6l6 6-6 6"></path>',
}


def sets_section(slug):
    L = lambda i: slug(i) + '.html'
    e = _h.escape
    SETS = [
        dict(key='seekers', name='Seekers', color='#D9483B', meta='1 study',
             quote='They’re not sure about Jesus...',
             blurb='Read the Gospel of John together and get to know Jesus. No pressure, just Jesus.',
             chips=['1 study', '3 ways to do it', 'At your own pace'],
             start=('Start here', 'Gospel of John Discovery Study', L(6)),
             button=('Open the study', L(6)),
             list_title='Gospel of John Study', list_meta='3 plans',
             rows=[('1', 'Read a Chapter Together Each Time You Meet', L(6)),
                   ('2', 'Read a Chapter a Day, Meet Weekly for 3 Weeks', L(6)),
                   ('3', 'Seven-Week Highlights Plan', L(6))]),
        dict(key='new-believers', name='New Believers', color='#1D1D1D', meta='6 lessons',
             quote='They just said yes to following Jesus',
             blurb='Six lessons on the Gospel, their story, baptism, freedom and church. The first steps of following Jesus, walked together.',
             chips=['6 lessons', 'About 6 weeks', '2 experiences'],
             start=('Start here', 'Lesson 1: Gospel Presentation', L(7)),
             button=('Open the workbook', L(7)),
             list_title='New Believers', list_meta='6 lessons',
             rows=[('1', 'Gospel Presentation', L(7)), ('2', 'Your Testimony', L(8)), ('3', 'Water Baptism', L(9)),
                   ('exp', 'Experience: Baptism', 'https://antiochwaco.churchcenter.com/registrations/events/2965360'),
                   ('4', 'Deliverance Prayer', L(10)), ('5', 'Baptism of the Holy Spirit', L(11)), ('6', 'Church Membership', L(12)),
                   ('exp', 'Experience: Church Membership', 'https://antiochwaco.com/membership')]),
        dict(key='foundations', name='Foundations', color='#006747', meta='15 lessons',
             quote='They want to grow',
             blurb='Fifteen lessons that build a lifestyle of knowing, loving and walking with Jesus. Three simple directions, done in order.',
             chips=['15 lessons', '3 parts', 'About 4 months'],
             parts=[('up', 'Look Up', '6 lessons · Knowing, loving and walking with the Lord.', L(2), '#B9E2C5', '#1D1D1D'),
                    ('in', 'Look In', '5 lessons · Holiness, love and Christlike character.', L(14), '#4FAE74', '#1D1D1D'),
                    ('out', 'Look Out', '4 lessons · A Great Commission lifestyle.', L(19), '#006747', '#FFFFFF')],
             button=('Start with Look Up', L(2)),
             link=('See all 15 lessons', 'discipleship-foundation-lessons.html'),
             list_title='Foundations', list_meta='15 lessons',
             groups=[('Look Up', '#B9E2C5', '#1D1D1D', [(2, 'Vision for a Vibrant Relationship'), (3, 'Devoted to God’s Word'), (1, 'Devoted to Worship'), (4, 'Devoted to Prayer'), (5, 'Devoted to Listening'), (13, 'Devoted to Abiding and Obeying')]),
                     ('Look In', '#4FAE74', '#1D1D1D', [(14, 'Our New Life in Christ'), (15, 'Confession'), (16, 'Repentance'), (17, 'Replacement'), (18, 'Restoration')]),
                     ('Look Out', '#006747', '#FFFFFF', [(19, 'Your Identity as a Witness'), (20, 'Your Sphere of Influence'), (21, 'Sharing the Gospel with Confidence'), (22, 'Making Disciples Who Make Disciples')])]),
        dict(key='further-growth', name='Further Growth', color='#B8862F', meta='Next steps',
             quote='They’re ready for what’s next',
             blurb='Plan your next season together with good questions, books and practices for going deeper in Look Up, Look In and Look Out.',
             chips=['1 planning guide', 'Books and practices', 'Go at your pace'],
             start=('Start here', 'Discipleship Planning Guide', 'planning-your-next-season-of-discipleship.html'),
             button=('Go deeper', 'going-deeper-in-discipleship.html'),
             list_title='Going Deeper', list_meta='Next steps',
             rows=[('•', 'Discipleship Planning Guide', 'planning-your-next-season-of-discipleship.html'),
                   ('↑', 'Going Deeper in Looking Up', 'going-deeper-in-discipleship.html'),
                   ('↓', 'Going Deeper in Looking In', 'going-deeper-in-discipleship.html'),
                   ('→', 'Going Deeper in Looking Out', 'going-deeper-in-discipleship.html'),
                   ('•', 'Tending Your Heart curriculum', 'tending-your-heart-curriculum.html'),
                   ('•', 'John Wesley’s 22 accountability questions', 'john-wesleys-22-accountability-questoins.html')]),
    ]
    DEFAULT = 'new-believers'

    def phone(s):
        out = [f'<div class="sets-list" aria-label="What’s inside {e(s["name"])}"><div class="sets-list-head"><span>{e(s["list_title"])}</span><span>{e(s["list_meta"])}</span></div>']
        if 'groups' in s:
            for gname, bg, fg, lessons in s['groups']:
                out.append(f'<div class="sets-group"><div class="sets-group-head" style="background:{bg};color:{fg}"><span>{gname}</span><span>{len(lessons)} lessons</span></div>')
                for k, (i, t) in enumerate(lessons, 1):
                    out.append(f'<a class="sets-mini" href="{L(i)}"><b style="background:{bg};color:{fg}">{k}</b>{e(t)}</a>')
                out.append('</div>')
        else:
            for n, t, href in s['rows']:
                if n == 'exp':
                    out.append(f'<a class="sets-exp" href="{href}">{e(t)}</a>')
                else:
                    first = ' first' if n in ('1',) else ''
                    out.append(f'<a class="sets-row{first}" href="{href}"><b>{n}</b>{e(t)}</a>')
        out.append('</div>')
        return ''.join(out)

    def panel(s):
        hid = '' if s['key'] == DEFAULT else ' hidden'
        chips = ''.join(f'<span>{e(c)}</span>' for c in s['chips'])
        mid = ''
        if 'parts' in s:
            mid = '<ol class="sets-parts">' + ''.join(
                f'<li><a href="{href}"><span class="sets-part-icon" style="background:{bg};color:{fg}"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{PART_ICON[ic]}</svg></span><span class="sets-part-text"><strong>Part {k}: {nm}</strong><span>{e(d)}</span></span></a></li>'
                for k, (ic, nm, d, href, bg, fg) in enumerate(s['parts'], 1)) + '</ol>'
        else:
            lab, t, href = s['start']
            mid = f'<a class="sets-start" href="{href}"><span class="sets-start-num" style="background:{s["color"]}">1</span><span><span class="sets-start-label">{lab}</span><strong>{e(t)}</strong></span></a>'
        extra = f'<a class="sets-more" href="{s["link"][1]}">{s["link"][0]}</a>' if 'link' in s else ''
        btxt, bhref = s['button']
        return f'''<div class="sets-card" role="tabpanel" id="set-{s['key']}" aria-labelledby="tab-{s['key']}" style="--set:{s['color']}"{hid}>
<div class="sets-stripe" aria-hidden="true"></div>
<div class="sets-body">
<div class="sets-phone">{phone(s)}</div>
<div class="sets-info">
<span class="sets-quote">“{e(s['quote'])}”</span>
<h3>{e(s['name'])}</h3>
<p>{e(s['blurb'])}</p>
<div class="sets-chips">{chips}</div>
{mid}
<div class="sets-actions"><a class="sets-btn" href="{bhref}">{btxt}{ARR}</a>{extra}</div>
</div>
</div>
</div>'''

    tabs = ''.join(
        f'<button type="button" role="tab" id="tab-{s["key"]}" aria-controls="set-{s["key"]}" aria-selected="{"true" if s["key"] == DEFAULT else "false"}" tabindex="{"0" if s["key"] == DEFAULT else "-1"}" data-set="{s["key"]}"><span class="sets-dot" style="background:{s["color"]}" aria-hidden="true"></span>{e(s["name"])}</button>'
        for s in SETS)
    dots = ''.join(f'<span data-dot="{s["key"]}" style="--set:{s["color"]}"></span>' for s in SETS)
    data = ','.join(f'{{k:"{s["key"]}",n:"{s["name"]}",m:"{s["meta"]}",c:"{s["color"]}"}}' for s in SETS)
    return f'''<section id="start" class="sets" aria-labelledby="sets-title">
<div class="sets-intro">
<span class="sets-hand">Start wherever they are.</span>
<h2 id="sets-title">So, who are you meeting with?</h2>
<p>Pick the one that fits where they are. Every lesson follows the same simple rhythm.</p>
</div>
<div class="sets-tabs" role="tablist" aria-label="Lesson sets">{tabs}</div>
<div class="sets-stage">
<button type="button" class="sets-peek prev" data-go="-1"><span class="sets-peek-stripe"></span><span class="sets-peek-text"><strong></strong><span></span></span></button>
<button type="button" class="sets-peek next" data-go="1"><span class="sets-peek-stripe"></span><span class="sets-peek-text"><strong></strong><span></span></span></button>
{''.join(panel(s) for s in SETS)}
</div>
<div class="sets-dots" aria-hidden="true">{dots}</div>
<p class="sets-help">Haven’t picked someone yet? <a href="who-should-i-disciple.html">Here’s how to know who to disciple.</a></p>
<script>(function(){{var S=[{data}];var sec=document.getElementById('start');if(!sec)return;var tabs=[].slice.call(sec.querySelectorAll('[role=tab]'));var cur=1;
function show(i,focus){{cur=(i+S.length)%S.length;tabs.forEach(function(t,j){{var on=j===cur;t.setAttribute('aria-selected',on);t.tabIndex=on?0:-1;document.getElementById('set-'+S[j].k).hidden=!on;}});if(focus)tabs[cur].focus();
[['prev',-1],['next',1]].forEach(function(p){{var s=S[(cur+p[1]+S.length)%S.length];var b=sec.querySelector('.sets-peek.'+p[0]);b.querySelector('.sets-peek-stripe').style.background=s.c;b.querySelector('strong').textContent=s.n;b.querySelector('.sets-peek-text span').textContent=s.m;b.setAttribute('aria-label','Show '+s.n);}});
[].forEach.call(sec.querySelectorAll('[data-dot]'),function(d,j){{d.className=j===cur?'on':'';}});}}
tabs.forEach(function(t,j){{t.addEventListener('click',function(){{show(j);}});t.addEventListener('keydown',function(ev){{if(ev.key==='ArrowRight'){{ev.preventDefault();show(cur+1,true);}}else if(ev.key==='ArrowLeft'){{ev.preventDefault();show(cur-1,true);}}}});}});
[].forEach.call(sec.querySelectorAll('[data-go]'),function(b){{b.addEventListener('click',function(){{show(cur+parseInt(b.getAttribute('data-go'),10));}});}});
var x0=null;var st=sec.querySelector('.sets-stage');st.addEventListener('touchstart',function(ev){{x0=ev.touches[0].clientX;}},{{passive:true}});st.addEventListener('touchend',function(ev){{if(x0===null)return;var dx=ev.changedTouches[0].clientX-x0;if(Math.abs(dx)>60)show(cur+(dx<0?1:-1));x0=null;}});
show(cur);}})();</script>
</section>'''
