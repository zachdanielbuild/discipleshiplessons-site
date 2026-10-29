import json, re, html
from html.parser import HTMLParser
import os
D=os.path.dirname(os.path.abspath(__file__))+'/'
OUT=D+'site/'
items=json.load(open(D+'xml/items.json'))
YT='https://www.youtube.com/playlist?list=PLoXSy2HiYN4tfZXlu97aZf_y_zBq3rO7E'
ROADMAP='https://www.discipleshiplessons.com/s/DiscipleshipRoadmap.pdf'
CHALLENGE='https://passionandpurpose.kit.com/discipleship'
slug=lambda i: items[i]['link'].strip('/')
# ---------- structure ----------
TRACKS=[
 ('seekers','For Seekers','#1D1D1D',[6]),
 ('new-believers','New Believers','#1D1D1D',[7,8,9,10,11,12]),
 ('look-up','Look Up','#1F7A4D',[2,3,1,4,5,13]),
 ('look-in','Look In','#B4561C',[14,15,16,17,18]),
 ('look-out','Look Out','#1B4FA0',[19,20,21,22]),
 ('freedom','Freedom Prayer Experience','#5B3F8C',[24,25,26,27,28,29,30,31]),
 ('deeper','Going Deeper','#1D1D1D',[23,34,32,33,36]),
 ('guides','Guides','#1D1D1D',[37,35]),
]
TITLES={1:'Devoted to Worship',2:'Vision for a Vibrant Relationship with the Lord',3:"Devoted to God's Word",4:'Devoted to Prayer',5:'Devoted to Listening to the Holy Spirit',13:'Devoted to Abiding and Obeying',
 7:'The Gospel',8:'Your Testimony',9:'Water Baptism',10:'Deliverance',11:'Baptism in the Holy Spirit',12:'Church Membership',
 14:'Growing Into Our New Life in Christ',15:'Confession',16:'Repentance',17:'Replace',18:'Restore',
 19:'Your Identity as a Witness and Ambassador',20:'Your Sphere of Influence',21:'Sharing the Gospel with Confidence',22:'Making Disciples Who Make Disciples',
 6:'Gospel of John Discovery Study',23:'Going Deeper in Discipleship',24:'Freedom Prayer Experience',32:'Tending Your Heart',33:"John Wesley's 22 Questions",34:'Further Growth Planning Guide',35:'Discipleship Foundations',36:'Disciplemaking Stories',37:'Who Should I Disciple?'}
for i in range(25,32): TITLES[i]=items[i]['title'].split(': ',1)[1]
info={}
for key,name,color,ids in TRACKS:
    for n,i in enumerate(ids):
        info[i]=dict(track=key,trackname=name,color=color,n=n,ids=ids)
SLUGS={slug(i) for i in info}
LINKFIX={'start-here':'discipleship-foundation-lessons','whats-next':'going-deeper-in-discipleship','lessons':'discipleship-foundation-lessons','devoted-to-gods-word':'church-membership','home':'index','faq':'index','whats-next-1':'whats-next-1'}
def fixlink(h):
    if h.startswith('/') and not h.startswith('//'): h='https://www.discipleshiplessons.com'+h
    m=re.match(r'https?://(www\.)?discipleshiplessons\.com/([^?#]*)(.*)',h)
    if not m: return h
    p=m.group(2).strip('/')
    if p.startswith('s/'): return h
    if p=='' : return 'index.html'
    p=LINKFIX.get(p,p)
    if p=='index': return 'index.html'
    return p+'.html' if p in SLUGS else h
# ---------- html cleaner ----------
KEEP={'h1','h2','h3','h4','p','ul','ol','li','strong','b','em','i','a','br','blockquote','hr'}
class Clean(HTMLParser):
    def __init__(s): super().__init__(convert_charrefs=True); s.out=[]; s.skip=0; s.videos=[]
    def handle_starttag(s,t,a):
        a=dict(a)
        if t in('script','style','noscript'): s.skip+=1; return
        if s.skip: return
        if t=='iframe':
            src=a.get('src') or ''
            m=re.search(r'watch%3Fv%3D([\w-]+)',src)
            if m: s.out.append(f'<!--VIDEO:{m.group(1)}-->')
            return
        if t not in KEEP: return
        t={'b':'strong','i':'em'}.get(t,t)
        if t=='a': s.out.append(f'<a href="{html.escape(fixlink(a.get("href","")),quote=True)}">')
        elif t in('br','hr'): s.out.append(f'<{t}>')
        else: s.out.append(f'<{t}>')
    def handle_endtag(s,t):
        if t in('script','style','noscript'): s.skip=max(0,s.skip-1); return
        if s.skip or t not in KEEP or t in('br','hr'): return
        t={'b':'strong','i':'em'}.get(t,t); s.out.append(f'</{t}>')
    def handle_data(s,d):
        if s.skip: return
        s.out.append(html.escape(d.replace('‍','').replace('​','').replace('\xa0',' ')))
def clean(h):
    c=Clean(); c.feed(h); x=''.join(c.out)
    x=re.sub(r'\s+',' ',x)
    x=re.sub(r'<li>\s*<p>(.*?)</p>\s*</li>',r'<li>\1</li>',x)
    x=re.sub(r'<li>\s*<p>',r'<li>',x); x=re.sub(r'</p>\s*(<ul>|<ol>)',r' \1',x)
    for _ in range(3):
        x=re.sub(r'<(strong|em)>\s*</\1>','',x); x=re.sub(r'</(strong|em)>(\s*)<\1>',r'\2',x)
        x=re.sub(r'<p>\s*</p>','',x); x=re.sub(r'<(h[1-4])>\s*</\1>','',x)
    x=re.sub(r'<(h[1-4])>\s*<strong>(.*?)</strong>\s*</\1>',r'<\1>\2</\1>',x)
    x=re.sub(r'\s*(</?(?:p|h[1-4]|ul|ol|li|blockquote|hr)>)\s*',r'\1',x)
    x=re.sub(r'(<(?:p|li|h[1-4])>)\s+',r'\1',x)
    return x
def blanks(x):
    return re.sub(r'_{3,}',lambda m:f'<span class="blank" style="width:{min(10,max(3,len(m.group(0))*0.32)):.1f}em" aria-label="blank"></span>',x)
WS={'xsT5cRq_iss':'Tending-Your-Heart-Handout-1_-Invitation-to-Intimacy.pdf','Q6uoDldx_n4':'Tending-Your-Heart-Handout-2_-Hindrances-To-Hearing-God.pdf','l5k3Qp8jxbM':'Tending-Your-Heart-Handout-3_-Overcoming-Wounds-Lies.pdf','mF6RlNBjXwE':'Part-4-Handout-Tending-Your-Heart.pdf'}
def body_for(i):
    x=clean(items[i]['content'])
    pre_extra=WHO if i==37 else ''
    # drop eyebrow + first title
    m=re.search(r'<h[12]>.*?</h[12]>',x)
    if m:
        pre=x[:m.start()]; x=x[m.end():]
    x=re.sub(r'<h[123]>(.*?)</h[123]>',lambda m:'<h2>'+re.sub(r':\s*$','',m.group(1))+'</h2>',x)
    x=re.sub(r'<h4>(.*?)</h4>',lambda m:'<h3>'+re.sub(r':\s*$','',m.group(1))+'</h3>',x)
    x=re.sub(r'<p><em>((?:(?!</?p>).)*)</em></p>',r'<p class="scripture">\1</p>',x)
    x=re.sub(r'<p><strong><em>((?:(?!</?p>).)*?)</em></strong>\s*<em>((?:(?!</?p>).)*)</em></p>',r'<p class="scripture"><strong>\1</strong> \2</p>',x)
    n=[0]
    def vid(m):
        n[0]+=1; v=m.group(1); pdf=WS.get(v)
        out=f'<div class="media"><a class="media-link" href="https://www.youtube.com/watch?v={v}">Watch lesson {n[0]} on YouTube</a>'
        if pdf: out+=f'<a class="media-link alt" href="https://www.discipleshiplessons.com/s/{pdf}">Worksheet for lesson {n[0]} (PDF)</a>'
        return out+'</div>'
    x=re.sub(r'<!--VIDEO:([\w-]+)-->',vid,x)
    x=re.sub(r'<p class="scripture">((?:[1-3] )?[A-Z][a-z]+(?: of [A-Z][a-z]+)? \d+[.:]\d+(?:[-–]\d+)?(?:,\s?\d+)?(?:\s?&amp;\s?\d+)?)\s+',r'<p class="scripture"><strong>\1</strong> ',x)
    if i==36: x=x.split('<h2>Planning the Next Phase of Discipleship</h2>')[0]
    return pre_extra+blanks(x)
_sv=json.load(open(D+'tree_svgs.json'))
WHO='''<figure class="strategy"><div class="strategy-card">'''+_sv['F2']+'''</div><figcaption>Jesus poured His life into a few, and they reached the world. 2 Timothy 2:2 is how it keeps going: you invest in a few faithful people, and they invest in others.</figcaption></figure>
<section class="yourfew" aria-labelledby="yourfew-title"><h2 id="yourfew-title">Who are your few?</h2><p>Ask the Lord who He is putting on your heart. Write down two or three names, then read the four questions below with them in mind.</p>
<div class="yourfew-fields"><label for="few1">Name 1<input id="few1" type="text" autocomplete="off" placeholder="Spiritually hungry"></label><label for="few2">Name 2<input id="few2" type="text" autocomplete="off" placeholder="Humble and teachable"></label><label for="few3">Name 3<input id="few3" type="text" autocomplete="off" placeholder="Faithful and reliable"></label></div>
<p class="yourfew-note">These names stay on this device only. Nobody else can see them.</p></section>
<script>(function(){['few1','few2','few3'].forEach(function(id){var el=document.getElementById(id);if(!el)return;try{var v=localStorage.getItem('dl-'+id);if(v)el.value=v;}catch(e){}el.addEventListener('input',function(){try{localStorage.setItem('dl-'+id,el.value);}catch(e){}});});})();</script>
'''
# ---------- shared chrome ----------
home=open(D+'home_frozen.dc.html').read().split('\n')
HMAP={21:'index.html',26:'discipleship-foundation-lessons.html',27:'index.html#letter',28:'index.html#faq',29:'index.html#start',
 37:'#start',38:YT,77:'who-should-i-disciple.html',119:'gospel-of-john-discovery-study.html',125:'the-gospel.html',131:'vision-for-a-vibrant-relationship-with-the-lord.html',137:'going-deeper-in-discipleship.html',144:'who-should-i-disciple.html',
 224:'who-should-i-disciple.html',227:ROADMAP,228:YT,236:'#start',247:CHALLENGE,
 251:'gospel-of-john-discovery-study.html',252:'the-gospel.html',253:'vision-for-a-vibrant-relationship-with-the-lord.html',254:'growing-into-our-new-life-in-christ.html',255:'ambassador.html',256:'going-deeper-in-discipleship.html',
 260:'who-should-i-disciple.html',261:ROADMAP,262:CHALLENGE,263:YT,264:'index.html#faq',268:'https://passionandpurpose.kit.com/40-days-of-devotion',269:'the-freedom-prayer-experience.html',270:'https://antiochwaco.churchcenter.com/registrations/events/2965360',271:'https://antiochwaco.com/membership',275:'https://antiochwaco.com/'}
paths=[slug(i)+'.html' for i in [2,3,1,4,5,13,14,15,16,17,18,19,20,21,22]]
for ln,p in zip([158,159,160,161,162,163,170,171,172,173,174,181,182,183,184],paths): HMAP[ln]=p
for ln,h in HMAP.items():
    line=home[ln-1]; assert '<a href="' in line,(ln,line)
    home[ln-1]=re.sub(r'<a href="[^"]*"',f'<a href="{h}"',line,count=1)
H='\n'.join(home)
# homepage sample lesson card: show the new five-part lesson format
_card_old=H[H.index('<div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 10px; font-size: 14px; font-weight: 800; text-transform: uppercase'):H.index('<div style="position: absolute; top: -104px')]
_blank=lambda w,c: f'<span style="display: inline-block; min-width: {w}px; border-bottom: 2px solid #1D1D1D; text-align: center; font-family: \'Caveat\', cursive; font-size: 30px; line-height: 1; color: {c}">'
_steps=''.join(f'<span class="card-step{" on" if k==2 else ""}"><b>{k+1}</b>{n}</span>' for k,n in enumerate(['Connection','Vision','Biblical Foundations','Modeling','Practice']))
_card_new=f'''<div style="font-size: 14px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.06em; color: #555555">Look Out  ·  Lesson 1 of 4</div>
<div style="font-weight: 900; font-size: 34px; line-height: 1.1; letter-spacing: -0.02em">Your Identity as a Witness and Ambassador</div>
<div class="card-why"><b>Why?</b> When you placed your faith in Christ, you received a new identity as God’s child and a new purpose as His witness and ambassador.</div>
<div class="card-steps" aria-label="Every lesson has five parts">{_steps}</div>
<div class="card-scripture"><div class="card-ref">Acts 1:8</div>"But you will receive {_blank(120,'#1B4FA0')}power</span> when the Holy Spirit comes on you; and you will be my {_blank(140,'#1B4FA0')}witnesses</span> in Jerusalem, and in all Judea and Samaria, and to the ends of the earth."</div>
<div style="display: flex; flex-direction: column; gap: 8px">
<div style="font-weight: 800">Questions for Discussion</div>
<div>What aspects of being a witness feel challenging to you?</div>
<div style="font-family: 'Caveat', cursive; font-size: 26px; line-height: 1.2; color: #1B4FA0">Bringing it up with my brother, Marcus.</div>
</div>
</div>
'''
H=H.replace(_card_old,_card_new,1)
LOGO='<svg width="40" height="40" aria-hidden="true" viewBox="0 0 120 120"><ellipse cx="60" cy="92" rx="17" ry="5" fill="none" stroke="#006747" stroke-width="4" stroke-opacity="0.95"/><ellipse cx="60" cy="92" rx="33" ry="10" fill="none" stroke="#006747" stroke-width="3.5" stroke-opacity="0.6"/><ellipse cx="60" cy="92" rx="50" ry="15" fill="none" stroke="#006747" stroke-width="3" stroke-opacity="0.3"/><g transform="translate(34.8 26.89999999999999) scale(2.1)"><path d="M12 1C6.5 1 2 5.4 2 10.9c0 7.6 10 20.1 10 20.1s10-12.5 10-20.1C22 5.4 17.5 1 12 1z" fill="#EA4335"/><circle cx="12" cy="11" r="3.8" fill="#A50E0E"/></g></svg>'
H=re.sub(r'<svg width="38" height="38" viewBox="0 0 40 40".*?</svg>',LOGO,H,count=1,flags=re.S)
MENU_BTN='<button type="button" class="menu-btn" aria-expanded="false" aria-controls="mainnav" onclick="var h=this.closest(\'header\');var o=h.classList.toggle(\'open\');this.setAttribute(\'aria-expanded\',o)"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16"></path><path d="M4 12h16"></path><path d="M4 17h16"></path></svg><span class="sr-only">Menu</span></button>'
H=H.replace('<nav aria-label="Main"',MENU_BTN+'<nav id="mainnav" aria-label="Main"',1)
header=H[H.index('<header'):H.index('</header>')+9]
footer=H[H.index('<footer'):H.index('</footer>')+9]
footer=footer.replace('href="#start"','href="index.html#start"')
inner=H[H.index('<x-dc>')+6:H.index('</x-dc>')]
inner=re.sub(r'<helmet>.*?</helmet>','',inner,flags=re.S)
FONTS='<link rel="icon" href="favicon.svg" type="image/svg+xml">\n<link rel="apple-touch-icon" href="apple-touch-icon.png">\n<meta name="theme-color" content="#FFFFFF">\n<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;700;800;900&family=Caveat:wght@500;700&display=swap" rel="stylesheet">'
# homepage order: hero, sample lesson, lesson sets (tabs), testimonials, postcard, questions, closing
from homesets import sets_section
def _cut(s,start,end):
    i=s.index(start); j=s.index(end,i); return s[i:j]
_m=['<section id="top"','<section aria-label="A peek at a lesson"','<section id="letter"','<section id="start"','<section id="path"','<section aria-label="By the numbers"','<section aria-label="What people say"','<section id="faq"','<footer']
_pos=[inner.index(m) for m in _m]
assert _pos==sorted(_pos),'homepage sections moved'
_seg={m:inner[a:b] for m,a,b in zip(_m,_pos,_pos[1:]+[len(inner)])}
inner=(inner[:_pos[0]]+_seg[_m[0]]+_seg[_m[1]]+sets_section(slug)+'\n\n'+_seg[_m[6]]+_seg[_m[2]]+_seg[_m[7]]+inner[inner.index('<footer'):])
# ---------- index ----------
idx=f'''<title>DiscipleshipLessons.com</title>
{FONTS}
<link rel="stylesheet" href="style.css">
<div class="site home">
{inner.strip()}
</div>
'''
open(OUT+'index.html','w').write(idx)
# ---------- content pages ----------
def page(i):
    inf=info[i]; ids=inf['ids']; n=inf['n']; t=TITLES[i]
    lessonish=inf['track'] in('new-believers','look-up','look-in','look-out','freedom') and not(inf['track']=='freedom' and n==0)
    if inf['track']=='freedom': eyebrow=f'Freedom Prayer Experience · Inventory {n}' if n else 'Freedom Prayer Experience'
    elif lessonish: eyebrow=f'{inf["trackname"]} · Lesson {n+1} of {len(ids)}'
    else: eyebrow=inf['trackname']
    if inf['track'] in('new-believers','look-up','look-in','look-out'): crumb=('discipleship-foundation-lessons.html','Discipleship Foundations')
    elif inf['track']=='freedom' and n: crumb=('the-freedom-prayer-experience.html','Freedom Prayer Experience')
    elif inf['track']=='deeper' and n: crumb=('going-deeper-in-discipleship.html','Going Deeper')
    else: crumb=None
    crumbs='<a href="index.html">Home</a>'+(f'<span aria-hidden="true">/</span><a href="{crumb[0]}">{crumb[1]}</a>' if crumb else '')
    nav=''
    if len(ids)>1 and inf['track']!='guides':
        prev=ids[n-1] if n>0 else None; nxt=ids[n+1] if n+1<len(ids) else None
        nav='<nav class="pager" aria-label="Lesson navigation">'
        nav+=f'<a class="prev" href="{slug(prev)}.html"><span>Previous</span>{html.escape(TITLES[prev])}</a>' if prev is not None else '<span></span>'
        nav+=f'<a class="next" href="{slug(nxt)}.html"><span>Next</span>{html.escape(TITLES[nxt])}</a>' if nxt is not None else '<span></span>'
        nav+='</nav>'
    note=''
    if inf['track'] in('look-up','look-in','look-out','new-believers','seekers') or (inf['track']=='freedom' and n):
        note='<aside class="howto"><strong>How to use this lesson</strong><span>Read the Scriptures together and fill in the blanks. The leader shares their own story in Modeling. Then pick one thing to practice before you meet again.</span></aside>' if inf['track']!='seekers' and inf['track']!='freedom' else ''
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(t)} | DiscipleshipLessons.com</title>
{FONTS}
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="site">
{header}
<main>
<section class="lesson-hero" style="--track: {inf['color']}">
<div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb">{crumbs}</nav>
<span class="pill">{html.escape(eyebrow)}</span>
<h1>{html.escape(t)}</h1>
<a class="original" href="https://www.discipleshiplessons.com{items[i]['link']}">View on the current site</a>
</div>
</section>
<article class="lesson wrap narrow" style="--track: {inf['color']}">
{note}
{body_for(i)}
{nav}
</article>
</main>
{footer}
</div>
</body>
</html>
'''
# ---------- content fixes (punch list) ----------
B=r'(<input type="text" class="blank"[^>]*>)'
FIXES={
 'sharing-the-gospel':[(r'<p>Go out together and pray for people, and share the Gospel\. A good rule of thumb is for you and the person you are discipling to each share at least three times with people\.</p>','')],
 'growing-into-our-new-life-in-christ':[(r'growing in in a lifestyle','growing in a lifestyle')],
 'freedom-from-idolatry':[
  (r'I know that these of the idols of '+B+r' \(name them specifically\)\. ',''),
  (r'involvement worship are evil and offensive in Your sight\. I renounce any and all involvement with the idols with the idols of'+B+r' \(name them specifically\), and I cancel out any and of'+B+r' \(name them specifically\), and I cancel out any and all ground that the all ground that the enemy gained in my life through this activity\. I ask for and humbly receive enemy gained in my life through this activity\. I ask for and humbly receive your forgiveness and the your forgiveness and the cleansing',
   r'involvement with the idols of \1 (name them specifically), and I cancel out any and all ground that the enemy gained in my life through this activity. I ask for and humbly receive your forgiveness and the cleansing'),
  (r'is still still filled','is still filled')],
 'freedom-from-bitterness':[(r'bitterness against</p><p>In the name of the true and living God, Jesus Christ, I confess, repent and renounce my worship '+B,r'bitterness against \1')],
 'freedom-from-rebellion':[(r'<strong>Places of Bitterness</strong>','<strong>Places of Rebellion</strong>')],
 'freedom-from-pride':[(r'<h3>Rebellion Inventory</h3>','<h3>Pride Inventory</h3>'),
  (r'our thoughts and our we have been walking in pride','our thoughts and our lives and reveal to us any places we have been walking in pride'),
  (r'As we we release','As we release')],
 'freedom-from-habitual-sin':[(r'our thoughts and our have been walking in the flesh','our thoughts and our lives and reveal to us any places we have been walking in the flesh')],
 'freedom-from-generational-sin':[(r'any places we been impacted','any places we have been impacted')],
 'freedom-from-lies-and-deception':[(r'considered the Pride Inventory','considered the Lies and Deception Inventory'),(r'receive forgiveness and grace for humility','receive forgiveness and grace to walk in the truth')],
}
_body_for_raw=body_for
def body_for(i):
    x=_body_for_raw(i)
    for pat,rep in FIXES.get(slug(i),[]):
        x,n=re.subn(pat,rep,x)
        assert n>=1,(slug(i),pat[:60])
    return layout(i,x)

ROW_ARROW='<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14"></path><path d="M13 6l6 6-6 6"></path></svg>'
def layout(i,x):
    # discussion questions run together in one paragraph -> numbered list
    def qsplit(m):
        qs=[q.strip() for q in re.split(r'(?<=\?)\s+(?=[A-Z“"])',m.group(2).strip()) if q.strip()]
        merged=[]
        for q in qs:
            if merged and len(q.split())<=3: merged[-1]+=' '+q
            else: merged.append(q)
        qs=merged
        if len(qs)<2: return m.group(0)
        return f'<p class="qlabel"><strong>{m.group(1)}</strong></p><ol class="questions">'+''.join(f'<li>{q}</li>' for q in qs)+'</ol>'
    x=re.sub(r'<p><strong>(Questions for Discussion:?)\s*</strong>\s*((?:(?!</?p>|<ul>|<ol>).)*?)</p>',qsplit,x)
    if i==6:  # Gospel of John plan options as cards
        def card(m):
            items=re.findall(r'<li>((?:(?!</?li>).)*?)</li>',m.group(3).split('<ul>')[0] if False else m.group(3))
            top=m.group(3)
            sched=''
            sm=re.search(r'<li>Example Schedule:</li><ul>(.*)$',top)
            if sm: sched=sm.group(1); top=top[:sm.start()]
            rows=''
            for li in re.findall(r'<li>(.*?)</li>',top):
                k,_,v=li.partition(': ')
                cls=' class="dur"' if k=='Duration' else ''
                rows+=f'<div{cls}><span>{k}:</span>{v}</div>'
            if sched: rows+=f'<div class="sched"><span>Example Schedule:</span><ul>{sched}</ul></div>'
            L=m.group(1)[-1]
            return f'<article class="plan-card"><div class="plan-head"><span class="plan-letter">{L}</span><span class="plan-opt">{m.group(1)}</span></div><h3>{m.group(2)}</h3>{rows}</article>'
        x=re.sub(r'<p><strong>(Option [ABC]): (.*?)</strong>\s*<ul>(.*?)</ul></ul>',card,x)
        x=re.sub(r'((?:<article class="plan-card">.*?</article>)+)',r'<div class="plan-cards">\1</div>',x,count=1,flags=re.S)
    if i==34:  # prayer questions were italic on the old site, not Scripture
        qs=re.findall(r'<p class="scripture">\d+\.\s*(.*?)\s*</p>',x)
        x=re.sub(r'(?:<p class="scripture">\d+\..*?</p>)+','<ol class="questions big">'+''.join(f'<li>{re.sub(r"\?(?=[A-Z])","? ",q)}</li>' for q in qs)+'</ol>',x,count=1)
    if i==37:  # the four principles become numbered sections
        x=re.sub(r'<p><strong>\d+\.\s*(.*?)\s*</strong></p>',lambda m:'<h2>'+re.sub(r'</?em>','',m.group(1)).strip()+'</h2>',x)
    if i==36:  # story titles become real section headings
        x=re.sub(r'<h3><em>(.*?)</em></h3>',r'<h2>\1</h2>',x)
    if i==24:  # inventories as tappable rows
        m=re.search(r'<ul>(<li><a href="freedom-.*?)</ul>',x)
        rows=''
        for k,(h,t) in enumerate(re.findall(r'<li><a href="([^"]+)">(.*?)</a></li>',m.group(1))):
            t=re.sub(r'^Inventory \d+:\s*','',t).replace('The Freedom From','Freedom From').strip()
            rows+=f'<a class="row" href="{h}"><span class="num" style="background:#5B3F8C">{k+1}</span><span class="row-title">{t}</span>{ROW_ARROW}</a>'
        x=x[:m.start()]+'</p><div class="rows inventories">'+rows+'</div>'+x[m.end():]
    return x

# ---------- v2: Option A trail layout ----------
def blanks(x):
    return re.sub(r'_{3,}',lambda m:f'<input type="text" class="blank" aria-label="Fill in the blank" autocomplete="off" style="width:{min(10,max(3,len(m.group(0))*0.32))+1.2:.1f}em">',x)
SHARE_BTN='<button type="button" class="print-btn share-btn" data-title="{title}" data-label="{label}"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"></path></svg><span>{label}</span></button><script>(function(){{var b=document.currentScript.previousElementSibling;var s=b.querySelector("span");var canShare=!!navigator.share&&matchMedia("(pointer: coarse)").matches;if(!canShare)s.textContent="Copy link to send";b.addEventListener("click",function(){{var url=location.origin+location.pathname;var t=b.getAttribute("data-title");if(canShare){{navigator.share({{title:t,text:"Here is the lesson for when we meet: "+t,url:url}}).catch(function(){{}});return;}}function done(){{s.textContent="Link copied!";setTimeout(function(){{s.textContent="Copy link to send";}},2200);}}if(navigator.clipboard&&navigator.clipboard.writeText){{navigator.clipboard.writeText(url).then(done,function(){{prompt("Copy this link:",url);}});}}else{{prompt("Copy this link:",url);}}}});}})();</script>'
PRINT_ICON='<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 9V3h10v6"></path><rect x="3" y="9" width="18" height="8" rx="2"></rect><path d="M7 14h10v7H7z"></path></svg>'
ARROW='<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14"></path><path d="M13 6l6 6-6 6"></path></svg>'
CHECK='<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"></path></svg>'
PIN='<svg width="{w}" height="{h}" viewBox="0 0 24 32" aria-hidden="true"><path d="M12 1C6.5 1 2 5.4 2 10.9c0 7.6 10 20.1 10 20.1s10-12.5 10-20.1C22 5.4 17.5 1 12 1z" fill="#EA4335"></path><circle cx="12" cy="11" r="3.8" fill="#A50E0E"></circle></svg>'
# Vision ("Why?") statements. Only lessons that have one get the box. 3 is a DRAFT awaiting Zach's edit.
VISION={
 3:'Why? God’s Word is daily bread for our souls. When we feed on it together, it nourishes us, gives us a firm foundation, and draws us deeper into friendship with Jesus.',
 7:'Why? God loves you and wants you to experience peace and life, abundant and eternal. This lesson walks through the good news of Jesus and gives an opportunity to respond to Him.',
 8:'Why? Like the blind man Jesus healed, every believer has a simple but powerful story: “I was blind but now I see!” Your story can have the same impact.',
 9:'Why? Baptism is an important step of obedience to Jesus. It shows that you have died to your old life and been raised to a new life in Christ.',
 10:'Why? God has rescued you from darkness and brought you into His kingdom. In Christ you are a new creation, no longer defined by your past, your sins, or your struggles.',
 11:'Why? The Holy Spirit fills believers with power to live boldly for Christ, gives gifts for service, and grows new fruit in our character.',
 12:'Why? You were not meant to follow Jesus alone. The church is the body of Christ, a place to belong, grow, and serve in God’s family.',
 2:'Why? Jesus didn’t just call His disciples to work for Him, but first and foremost to be with Him. A daily habit of time with Jesus plants the seeds for a lifelong, life-giving friendship with the Lord.',
 1:'Why? Worship is both a priority and a privilege for God’s people. A heart of worship is a key building block in a lifestyle of devotion and friendship with Jesus.',
 4:'Why? The early disciples were known for their devotion to prayer and for answers to prayer. Prayer is a vital building block in our friendship with Jesus.',
 5:'Why? The Holy Spirit is our Helper who lives within us, God’s presence with us always. Learning to listen for His guidance draws us deeper into friendship with Jesus.',
 13:'Why? Jesus wants us to keep in step with the Spirit, obeying His leadership and enjoying ongoing communion with Him. As we walk with Him, we walk in His life and peace.',
 14:'Why? The moment you placed your faith in Christ, you became a child of God. As a loving Father, He works in your life by His Spirit to make you more like Jesus.',
 15:'Why? Confession means agreeing with God about sin, about ourselves, and about His truth. When we confess, He is faithful to forgive us and cleanse us.',
 16:'Why? Repentance is a change of mind, heart, action, and direction. It is how we partner with the Lord to uproot sin and find times of refreshing.',
 17:'Why? God doesn’t just call us to stop sinful patterns. He wants to grow godly virtues in their place, feeding us with new truth, new healing, new grace, and new actions.',
 18:'Why? God’s work of transformation leads to restoration: walking in the holiness we were created for and loving others like Jesus.',
 19:'Why? When you placed your faith in Christ, you received a new identity as God’s child and a new purpose as His witness and ambassador.',
 20:'Why? God has given every one of us a mission to be His witnesses, and a unique sphere of influence where we live out that calling.',
 21:'Why? The gospel message has power in itself. Our part is to share it clearly and confidently, trusting God with the results.',
 22:'Why? Jesus’ final command wasn’t just to make converts, but to make disciples who make more disciples. That is how a multiplication movement begins.',
}

def split_sections(x):
    parts=re.split(r'(<h2>.*?</h2>)',x)
    pre=parts[0]; secs=[]
    for k in range(1,len(parts),2):
        name=re.sub(r'<h2>(.*?)</h2>',r'\1',parts[k]); secs.append([name,parts[k+1] if k+1<len(parts) else ''])
    return pre,secs

def restructure(i,secs):
    vision=VISION.get(i)
    for s in secs:
        if s[0]=='Introduction' and info[i]['track'] in ('new-believers','look-up','look-in','look-out'): s[0]='Connection'
    if i==6:
        m=re.search(r'<p>(Why\?.*?)</p>',secs[0][1])
        if m: vision=m.group(1); secs[0][1]=secs[0][1].replace(m.group(0),'',1)
    # New Believers: Connection first, then a Vision section built from each lesson's own vision sentence
    if info[i]['track']=='new-believers' and secs and secs[0][0]=='Connection':
        CATCH='<p>As you get started, catch up on how y’all are doing since you last met. Celebrate how God has been at work in your lives.</p>'
        FIRST='<p>As you get started, take a few minutes to catch up and hear how they are doing.</p>'
        NBV={7:(1,'<p>God loves you and wants you to experience peace and life—abundant and eternal.</p>'),
             8:(1,'<p>Like the blind man healed by Jesus, we each have a powerful testimony in Jesus.</p>'),
             9:(1,'<p>Water Baptism is an important step of obedience in your discipleship to Jesus.</p>'),
             10:(1,'<p>God has rescued you from darkness and brought you into His kingdom. This transfer of kingdoms is central to understanding deliverance.</p>')}
        conn=secs[0][1]
        if i in NBV:
            k,snip=NBV[i]; assert snip in secs[k][1],(i,'vision sentence moved')
            secs[k][1]=secs[k][1].replace(snip,'',1); vtxt=snip[3:-4]
        elif i==11:
            a='<p>This lesson will help you experience baptism in the Holy Spirit. '
            assert conn.startswith(a),(i,'connection text changed')
            vtxt=conn[len(a):conn.index('</p>')]; conn='<p>This lesson will help you experience baptism in the Holy Spirit.</p>'+conn[conn.index('</p>')+4:]
        elif i==12:
            m=re.match(r'<p>(.*?)</p>',conn); vtxt=m.group(1); conn=conn[m.end():]
        else:
            vtxt=None
        secs[0][1]=(FIRST if i==7 else CATCH)+conn
        if vtxt: secs.insert(1,['Vision',f'<p class="vision-lead">{vtxt}</p>'])
    if info[i]['track'] in ('look-up','look-in','look-out') and any(s[0]=='Biblical Foundations' for s in secs):
        bf=[s for s in secs if s[0]=='Biblical Foundations'][0]
        m=re.match(r'<p>(.*?)</p>',bf[1])
        if m:
            bf[1]=bf[1][m.end():]
            lead=re.sub(r':\s*$','.',m.group(1).strip())
            secs.insert(secs.index(bf),['Vision',f'<p class="vision-lead">{lead}</p>'])
    return vision,secs

def trail_html(secs):
    out='<div class="trail">'
    for k,(name,body) in enumerate(secs):
        out+=f'<section class="step" id="s{k+1}"><span class="marker" aria-hidden="true">{k+1}</span><div class="step-body"><h2>{name}</h2>{body}</div></section>'
    return out+'</div>'

def page(i):
    inf=info[i]; ids=inf['ids']; n=inf['n']; t=TITLES[i]
    lessonish=inf['track'] in('new-believers','look-up','look-in','look-out','freedom') and not(inf['track']=='freedom' and n==0)
    if inf['track']=='freedom': eyebrow=f'Freedom Prayer Experience · Inventory {n}' if n else 'Freedom Prayer Experience'
    elif lessonish: eyebrow=f'{inf["trackname"]} · Lesson {n+1} of {len(ids)}'
    else: eyebrow=inf['trackname']
    crumbs='<a href="index.html">Home</a>'
    if inf['track'] in('new-believers','look-up','look-in','look-out','seekers'):
        anchor={'seekers':'seekers','new-believers':'new-believers','look-up':'look-up','look-in':'look-in','look-out':'look-out'}[inf['track']]
        crumbs+=f'<span aria-hidden="true">/</span><a href="discipleship-foundation-lessons.html">Discipleship Foundations</a><span aria-hidden="true">/</span><a class="crumb-track" href="discipleship-foundation-lessons.html#{anchor}">{inf["trackname"]}</a>'
    elif inf['track']=='freedom' and n: crumbs+='<span aria-hidden="true">/</span><a href="the-freedom-prayer-experience.html">Freedom Prayer Experience</a>'
    elif inf['track']=='deeper' and n: crumbs+='<span aria-hidden="true">/</span><a href="going-deeper-in-discipleship.html">Going Deeper</a>'
    nav=''
    if len(ids)>1 and inf['track']!='guides':
        prev=ids[n-1] if n>0 else None; nxt=ids[n+1] if n+1<len(ids) else None
        nav='<nav class="pager" aria-label="Lesson navigation">'
        nav+=f'<a class="prev" href="{slug(prev)}.html"><span>Previous</span>{html.escape(TITLES[prev])}</a>' if prev is not None else '<span></span>'
        nav+=f'<a class="next" href="{slug(nxt)}.html"><span>Next</span>{html.escape(TITLES[nxt])}</a>' if nxt is not None else '<span></span>'
        nav+='</nav>'
    note=''
    if inf['track'] in('look-up','look-in','look-out','new-believers'):
        note='<aside class="howto"><strong>How to use this lesson</strong><span>Read the Scriptures together and fill in the blanks. The leader shares their own story in Modeling. Then pick one thing to practice before you meet again.</span></aside>'
    is_lesson=inf['track'] in ('seekers','new-believers','look-up','look-in','look-out') or (inf['track']=='freedom' and n>0)
    pre,secs=split_sections(body_for(i))
    vision,secs=restructure(i,secs)
    progress=''
    if lessonish and len(ids)>1:
        tot,cur=(len(ids)-1,n-1) if inf['track']=='freedom' else (len(ids),n)
        progress='<div class="progress" aria-label="'+f'{cur+1} of {tot}'+'">'+''.join(f'<span class="{"on" if k<=cur else ""}"></span>' for k in range(tot))+'</div>'
    steps=''
    if len(secs)>1:
        def short(nm):
            nm2=re.sub(r' in Your Sphere of Influence\?$','?',nm)
            if nm2!=nm: return nm2
            if len(nm)>24:
                for sep in (' - ',' — ',': '):
                    if sep in nm: return nm.split(sep)[0]
            return nm
        steps='<nav class="steps" aria-label="In this lesson">'+''.join(f'<a href="#s{k+1}"><span>{k+1}</span>{short(name)}</a>' for k,(name,_) in enumerate(secs))+'</nav>'
    vbox=f'<figure class="vision-box">{re.sub(r"^Why\?",'<span class="why">Why?</span>',vision)}</figure>' if vision else ''
    printnote='<div class="print-only print-notes"><span>Notes</span><i></i><i></i><i></i></div>'
    prehtml=f'<div class="pre">{pre}</div>' if pre and re.sub(r'<[^>]+>','',pre).strip() else ''
    bodyhtml=label_blanks(prehtml+(trail_html(secs) if secs else ''))
    has_blanks='class="blank"' in bodyhtml
    clear='<button type="button" class="clear-answers">Clear my answers</button>' if has_blanks else ''
    if vision: desc=re.sub(r'^Why\?\s*','',vision)
    else:
        fp=re.search(r'<p>(.*?)</p>',bodyhtml); desc=re.sub(r'<[^>]+>','',fp.group(1)) if fp else t
    desc=html.unescape(desc).strip()
    if len(desc)>200: desc=desc[:197].rsplit(' ',1)[0]+'...'
    meta=share_meta(t+' | DiscipleshipLessons.com',desc,slug(i))
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(t)} | DiscipleshipLessons.com</title>
{meta}
{FONTS}
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="site">
{header}
<main>
<section class="lesson-hero" style="--track: {inf['color']}">
<div class="wrap">
<div class="hero-grid{' has-vision' if vision else ''}">
<div class="hero-main">
<nav class="crumbs" aria-label="Breadcrumb">{crumbs}</nav>
<span class="pill">{html.escape(eyebrow)}</span>
<h1>{html.escape(t)}</h1>
{progress}
<div class="lesson-actions"><button type="button" class="print-btn" onclick="window.print()">{PRINT_ICON}{'Print this lesson' if is_lesson else 'Print this page'}</button>{SHARE_BTN.format(label='Text this lesson' if is_lesson else 'Text this page', title=html.escape(t, quote=True)) }</div>
</div>
{vbox}
</div>
{steps}
</div>
</section>
<article class="lesson wrap" style="--track: {inf['color']}">
<p class="print-only print-head">{html.escape(t)} · {html.escape(eyebrow)} · discipleshiplessons.com</p>
{note}
{bodyhtml}
{printnote}
{nav}
{clear}
</article>
</main>
{footer}
</div>
{SAVE_JS if has_blanks else ''}
</body>
</html>
'''

SITE='https://www.discipleshiplessons.com/'
def share_meta(title,desc,path):
    e=lambda v: html.escape(v,quote=True)
    url=SITE+('' if path=='index' else path)
    return f'''<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="DiscipleshipLessons.com">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}share.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">'''
def label_blanks(h):
    out=[]; pos=0; n=[0]
    def para(m):
        ref=re.search(r'<strong>(.*?)</strong>',m.group(0))
        k=[0]; tot=m.group(0).count('class="blank"')
        def lab(b):
            k[0]+=1; n[0]+=1
            where=f' in {ref.group(1)}' if ref else ''
            return b.group(0).replace('aria-label="Fill in the blank"',f'aria-label="Blank {k[0]} of {tot}{where}" id="b{n[0]}"')
        return re.sub(r'<input type="text" class="blank"[^>]*>',lab,m.group(0))
    return re.sub(r'<(p|li)[^>]*>(?:(?!</?(?:p|li)[ >]).)*?class="blank".*?</\1>',para,h,flags=re.S)
SAVE_JS='<script>(function(){var k="dl-ans-"+location.pathname.replace(/\\.html$/,"");var d={};try{d=JSON.parse(localStorage.getItem(k)||"{}")}catch(e){}document.querySelectorAll("input.blank[id]").forEach(function(el){if(d[el.id])el.value=d[el.id];el.addEventListener("input",function(){d[el.id]=el.value;try{localStorage.setItem(k,JSON.stringify(d))}catch(e){}})});var c=document.querySelector(".clear-answers");if(c)c.addEventListener("click",function(){d={};try{localStorage.removeItem(k)}catch(e){}document.querySelectorAll("input.blank").forEach(function(el){el.value=""})})})();</script>'

def foundations():
    def rows(idlist, names, color):
        return '<div class="rows">'+''.join(f'<a class="row" href="{slug(j)}.html"><span class="num" style="background:{color}">{k+1}</span><span class="row-title">{nm}</span>{ARROW}</a>' for k,(j,nm) in enumerate(zip(idlist,names)))+'</div>'
    def chips(label, links):
        if not links: return ''
        return f'<div class="exp"><span>{label}</span>'+''.join(f'<a class="chip" href="{h}">{t}</a>' for t,h in links)+'</div>'
    def stop(anchor,num,color,title,preview,label,idlist,names,exlabel=None,ex=(),part=None):
        head=f'<div class="part-head"><span class="part" style="color:{color}">{part}</span><h3 style="color:{color}">{title}</h3></div>' if part else f'<h2>{title}</h2>'
        cnt=f'{len(idlist)} lesson'+('s' if len(idlist)>1 else '')
        return f'''<section class="stop" id="{anchor}" style="--c:{color}"><span class="marker" aria-hidden="true">{num}</span><div class="stop-card"><details open><summary>{head}<span class="toggle"><span class="more">Show {cnt}</span><span class="less">Hide lessons</span></span></summary><div class="stop-inner"><p class="preview"><strong>Preview:</strong> {preview}</p><span class="label">{label}</span>{rows(idlist,names,color)}{chips(exlabel,ex)}</div></details></div></section>'''
    S=[]
    S.append(stop('seekers','1','#1D1D1D','Foundations for Seekers','This discipleship lesson is designed to be done with non-Christians who are interested in Jesus. In it, you will read through the Gospel of John together and learn more about Him.','Lesson:',[6],['Gospel of John Bible Study']))
    S.append(stop('new-believers','2','#1D1D1D','Foundations for New Believers','This set of discipleship lessons is designed to be done with new believers. In it, you will focus on the Gospel, baptism, deliverance and church membership.','Lessons:',[7,8,9,10,11,12],['Gospel Presentation','Your Testimony','Water Baptism','Deliverance Prayer','Baptism of the Holy Spirit','Church Membership'],'Experiences:',[('Baptism','https://antiochwaco.churchcenter.com/registrations/events/2965360'),('Church Membership','https://antiochwaco.com/membership')]))
    S.append('<div class="grow-head"><h2>Foundations for Growing Disciples</h2></div>')
    S.append(stop('look-up','3','#1F7A4D','Look Up','This set of discipleship lessons are designed to be done with a growing disciple and lays the foundation for developing a lifestyle of knowing, loving and walking with the Lord.','Lessons:',[2,3,1,4,5,13],['Vision For A Vibrant Relationship with the Lord','Devoted to God’s Word','Devoted to Worship','Devoted to Prayer','Devoted to Listening','Devoted to Abiding and Obeying'],'Experiences in Look Up:',[('40 Days of Devotion','https://passionandpurpose.kit.com/40-days-of-devotion')],part='Part 1:'))
    S.append(stop('look-in','4','#B4561C','Look In','This set of discipleship lessons are designed to be done with a growing disciple after completing Look Up. Look In lays the foundations for a lifestyle of holiness, love and Christlike character.','Lessons:',[14,15,16,17,18],['Our New Life in Christ','Confession - Agreeing with God’s Truth','Repentance - Turning Away from Sin','Replacement - Weeding and Feeding','Restoration - Living in Holiness and Love'],'Experiences in:',[('Freedom Prayer Experience','the-freedom-prayer-experience.html')],part='Part 2:'))
    S.append(stop('look-out','5','#1B4FA0','Look Out','This set of discipleship lessons are designed to be done with a growing disciple after completing Look Up and Look In. Look Out lays the foundation for a Great Commission lifestyle.','Lessons:',[19,20,21,22],['Your Identity as a Witness and Ambassador','Your Sphere of Influence','Sharing the Gospel with Confidence','Making Disciples Who Make Disciples'],part='Part 3:'))
    S.append(f'<section class="stop next-stop" id="next"><span class="marker pin" aria-hidden="true">{PIN.format(w=36,h=48)}</span><div class="stop-card dark"><h2>What’s Next?</h2><p>When you finish these foundations, you might be asking “what’s next?” Here are some good next steps in discipleship.</p><a class="btn-yellow" href="going-deeper-in-discipleship.html">What’s Next{ARROW}</a></div></section>')
    from foundpage import body as _fd
    FD_HERO,FD_MAIN,FD_SCRIPT=_fd(slug,ARROW)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Discipleship Foundations | DiscipleshipLessons.com</title>
{share_meta('Discipleship Foundations | DiscipleshipLessons.com','Jesus calls all of us to make disciples (Matthew 28). These lessons can help you fulfill that calling.','discipleship-foundation-lessons')}
{FONTS}
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="site">
{header}
<main>
{FD_HERO}
{FD_MAIN}
</main>
{footer}
</div>
{FD_SCRIPT}
</body>
</html>
'''

files=[]
for i in info:
    fn=slug(i)+'.html'; open(OUT+fn,'w').write((foundations() if i==35 else page(i)).replace('Discipleship Planning Guide','Further Growth Planning Guide')); files.append(fn)
json.dump(files,open(D+'site_files.json','w'))
print(len(files),'pages')
