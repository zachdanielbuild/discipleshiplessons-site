import json, re, html
from html.parser import HTMLParser
import os
D=os.path.dirname(os.path.abspath(__file__))+'/'
OUT=D+'site/'
items=json.load(open(D+'xml/items.json'))
# clean addresses (Oct 30); old ones redirect in launchfiles.py
for _k,_new in ((33,'/john-wesleys-22-questions'),(36,'/disciplemaking-stories')): items[_k]['link']=_new
YT='https://www.youtube.com/playlist?list=PLoXSy2HiYN4tfZXlu97aZf_y_zBq3rO7E'
ROADMAP='https://www.discipleshiplessons.com/s/DiscipleshipRoadmap.pdf'
CHALLENGE='https://passionandpurpose.kit.com/discipleship'
slug=lambda i: items[i]['link'].strip('/')
# ---------- structure ----------
TRACKS=[
 ('seekers','Seekers','#1D1D1D',[6]),
 ('new-believers','New Believers','#1D1D1D',[7,8,9,10,11,12]),
 ('look-up','Look Up','#1F7A4D',[2,3,1,4,5,13]),
 ('look-in','Look In','#B4561C',[14,15,16,17,18]),
 ('look-out','Look Out','#1B4FA0',[19,20,21,22]),
 ('freedom','Freedom Prayer Experience','#5B3F8C',[24,25,26,27,28,29,30,31]),
 ('deeper','Further Growth','#1D1D1D',[23,34,32,33,36]),
 ('guides','Start Here','#1D1D1D',[37,35]),
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
LINKFIX={'start-here':'discipleship-foundation-lessons','whats-next':'going-deeper-in-discipleship','lessons':'discipleship-foundation-lessons','devoted-to-gods-word':'church-membership','home':'index','faq':'index','whats-next-1':'disciplemaking-stories','john-wesleys-22-accountability-questoins':'john-wesleys-22-questions'}
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
# Worksheets are hosted on this site in /files (moved off Squarespace Oct 30)
WS={'xsT5cRq_iss':'tending-your-heart-1-invitation-to-intimacy.pdf','Q6uoDldx_n4':'tending-your-heart-2-hindrances-to-hearing-god.pdf','l5k3Qp8jxbM':'tending-your-heart-3-overcoming-wounds-and-lies.pdf','mF6RlNBjXwE':'tending-your-heart-4-how-to-tend-your-heart.pdf'}
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
        if pdf: out+=f'<a class="media-link alt" href="files/{pdf}">Worksheet for lesson {n[0]} (PDF)</a>'
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
# Discipleship Roadmap PDF retired (Oct 30): drop its homepage question and footer link
_n=len(H)
H=re.sub(r'<div id="roadmap">.*?</div></div>\n','',H,count=1)
H=H.replace(f'<a href="{ROADMAP}" style="text-decoration: none">The Discipleship Roadmap</a>\n','',1)
assert 'DiscipleshipRoadmap' not in H and len(H)<_n
# homepage sample lesson card: show the new five-part lesson format
_card_old=H[H.index('<div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 10px; font-size: 14px; font-weight: 800; text-transform: uppercase'):H.index('<div style="position: absolute; top: -104px')]
_blank=lambda w,c: f'<span style="display: inline-block; min-width: {w}px; border-bottom: 2px solid #1D1D1D; text-align: center; font-family: \'Caveat\', cursive; font-size: 30px; line-height: 1; color: {c}">'
_steps=''.join(f'<span class="card-step{" on" if k==2 else ""}"><b>{k+1}</b>{n}</span>' for k,n in enumerate(['Connection','Vision','Biblical Foundations','Modeling','Practice']))
_card_new=f'''<div style="font-size: 14px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.06em; color: #555555">Look Out  ·  Lesson 1 of 4</div>
<div style="font-weight: 900; font-size: 34px; line-height: 1.1; letter-spacing: -0.02em">Your Identity as a Witness and Ambassador</div>
<div class="card-why"><b>Why?</b> Look Out starts with identity, not technique. Help them see that being a witness is who they already are in Christ, and start them praying daily to notice the opportunities around them.</div>
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

SET_NEXT={6:(7,'Up next: New Believers'),12:(2,'Up next: Look Up'),13:(14,'Up next: Look In'),18:(24,'Up next'),31:(19,'Up next: Look Out'),22:(34,'Up next: Further Growth')}
def page(i):
    inf=info[i]; ids=inf['ids']; n=inf['n']; t=TITLES[i]
    lessonish=inf['track'] in('new-believers','look-up','look-in','look-out','freedom') and not(inf['track']=='freedom' and n==0)
    if inf['track']=='freedom': eyebrow=f'Freedom Prayer Experience · Inventory {n}' if n else 'Freedom Prayer Experience'
    elif lessonish: eyebrow=f'{inf["trackname"]} · Lesson {n+1} of {len(ids)}'
    else: eyebrow=inf['trackname']
    crumbs='<a href="index.html">Home</a>'
    SEP='<span aria-hidden="true">/</span>'
    if inf['track'] in('look-up','look-in','look-out'):
        crumbs+=f'{SEP}<a href="discipleship-foundation-lessons.html#foundations">Discipleship Foundations</a>{SEP}<a class="crumb-track" href="discipleship-foundation-lessons.html#{inf["track"]}">{inf["trackname"]}</a>'
    elif inf['track'] in('new-believers','seekers'):
        crumbs+=f'{SEP}<a class="crumb-track" href="discipleship-foundation-lessons.html#{inf["track"]}">{inf["trackname"]}</a>'
    elif inf['track']=='freedom' and n: crumbs+=f'{SEP}<a href="the-freedom-prayer-experience.html">Freedom Prayer Experience</a>'
    elif inf['track']=='deeper' and n: crumbs+=f'{SEP}<a href="discipleship-foundation-lessons.html#further-growth">Further Growth</a>'
    nav=''
    if inf['track']!='guides':
        prev=ids[n-1] if n>0 else None; nxt=ids[n+1] if n+1<len(ids) else None
        upnext=None
        if nxt is None and i in SET_NEXT: upnext=SET_NEXT[i]
        if prev is not None or nxt is not None or upnext:
            nav='<nav class="pager" aria-label="Lesson navigation">'
            nav+=f'<a class="prev" href="{slug(prev)}.html"><span>Previous</span>{html.escape(TITLES[prev])}</a>' if prev is not None else '<span></span>'
            if nxt is not None: nav+=f'<a class="next" href="{slug(nxt)}.html"><span>Next</span>{html.escape(TITLES[nxt])}</a>'
            elif upnext: nav+=f'<a class="next up-next" href="{slug(upnext[0])}.html"><span>{upnext[1]}</span>{html.escape(TITLES[upnext[0]])}</a>'
            else: nav+='<span></span>'
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
        fp=re.search(r'<p>(.*?)</p>',bodyhtml); desc=re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',fp.group(1))) if fp else t
        if inf['track']=='freedom' and n: desc=f'A guided prayer time from the Freedom Prayer Experience: identify {t[len("Freedom From "):].lower()}, confess and repent, and receive the healing and freedom Jesus brings.'
        if i==33: desc='22 questions John Wesley and his friends used to grow in holiness and love. Use them to write accountability questions for your own discipleship group.'
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
{SAVE_JS if has_blanks else ''}{LONG_JS if 'class="long"' in bodyhtml else ''}
</body>
</html>
'''

LONG_JS='<script>(function(){var d=document.querySelectorAll("details.long");if(matchMedia("(max-width: 720px)").matches)d.forEach(function(e){e.open=false});addEventListener("beforeprint",function(){d.forEach(function(e){e.open=true})})})();</script>'
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

# ---------- refinement pass (Oct 30 audit) ----------
# Literal find-and-replace fixes per page, applied after FIXES and layout().
# Each pair must match at least once, so the build fails loudly if the source text moves.
INPUT='<input type="text" class="blank" aria-label="Fill in the blank" autocomplete="off" style="width:14em">'
NAMES='<ol class="name-lines">'+''.join(f'<li>{INPUT}</li>' for _ in range(5))+'</ol>'
LOOKUP_CONN=('Ask how have the 40 Days of Devotion gone so far.','Ask how the 40 Days of Devotion are going.')
REFINE={
 'the-gospel':[('with God and with others relationships?','with God and with others?')],
 'your-testimony':[('The Gaderene Demoniac','The Gerasene Demoniac'),
   ('<p>&quot;Jesus did not let him, but said, &#x27;Go home to your own people and tell them how much the Lord has done for you, and how he has had mercy on you.&#x27;</p><p>So the man went away and began to tell in the Decapolis how much Jesus had done for him. And all the people were amazed.&quot;</p>',
    '<p class="scripture"><strong>Mark 5:19-20</strong> &quot;Jesus did not let him, but said, &#x27;Go home to your own people and tell them how much the Lord has done for you, and how he has had mercy on you.&#x27; So the man went away and began to tell in the Decapolis how much Jesus had done for him. And all the people were amazed.&quot;</p>')],
 'water-baptism':[('your Lord and Savior Yes','your Lord and Savior? Yes')],
 'deliverance':[('who you are in Christ..','who you are in Christ.')],
 'spirit-baptism':[('the Ephesians believers','the Ephesian believers'),('Baptism of the Holy Spirit</h2>','Baptism in the Holy Spirit</h2>'),('The baptism of the Holy Spirit however','The baptism in the Holy Spirit, however,'),('<em>witness</em>—boldly','<em>witness</em>: boldly')],
 'church-membership':[('<p>Why Membership Matters<ul>','<h3>Why Membership Matters</h3><ul>')],
 'vision-for-a-vibrant-relationship-with-the-lord':[('explain how it your relationship','explain how it shapes your relationship')],
 'devoted-to-the-word':[LOOKUP_CONN],'devoted-to-worship':[LOOKUP_CONN],'devoted-to-prayer':[LOOKUP_CONN],
 'devoted-to-listening-to-the-holy-spirit':[LOOKUP_CONN,('in your life?What makes','in your life?</li><li>What makes')],
 'devoted-to-abiding-and-obeying':[('extend your devotional life into your entire day.</p>','extend your devotional life into your entire day. This week, also try these:</p><ul><li><strong>Set three reminders.</strong> Pick three moments in your day (waking up, lunch, your drive home) to pause and say, “Jesus, I’m here with You. What are You saying?”</li><li><strong>Do the one thing.</strong> Write down the one area where you sense God calling you to greater obedience. Take one concrete step in it before we meet again.</li><li><strong>Notice His promptings.</strong> When you sense a nudge to encourage someone, pray for someone or let something go, act on it. Jot down what happened.</li><li><strong>Share it.</strong> Next time we meet, share one moment when you sensed Jesus with you during the day.</li></ul>'),LOOKUP_CONN,('consumed by one another.</p><p class="scripture">16 But I say','consumed by one another. 16 But I say')],
 'growing-into-our-new-life-in-christ':[('how you view yourself ?What does','how you view yourself?</li><li>What does')],
 'confession':[('Ask how have the identity in Christ meditations are going.','Ask how the identity in Christ meditations are going.'),('selfishness (verse 18)?','selfishness (verses 19-21)?')],
 'replace':[('Here are a few tools that God uses to replacing a lifestyle of sin with a lifestyle of holiness and love. One of them is the ministry of the Holy Spirit.',
   'One of the main ways God replaces a lifestyle of sin with a lifestyle of holiness and love is through the ministry of the Holy Spirit.'),
   ('take time to practice confession of sin. How did it go in uprooting these areas from your lives?','How has it gone partnering with God to uproot the sins you confessed?')],
 'restore':[('go through our Freedom Prayer Experience together. This experience takes the what you learned','go through our <a href="the-freedom-prayer-experience.html">Freedom Prayer Experience</a> together. This experience takes what you learned')],
 'ambassador':[('<p>Welcome to &quot;Look Out,&quot; a discipleship guide designed to help plant and water the seeds of a Great Commission lifestyle in the lives of God’s people.</p><p>Our hope is that as you these lessons you will develop a hunger to live on mission, and the habit of sharing your faith, making disciples, and stewarding your resources for God’s Kingdom and glory!</p>',
   '<p>As you get started, catch up on how y’all are doing since you last met. Celebrate how God has been at work in your lives.</p><p>This is the first lesson in Look Out. Over these four lessons, our hope is that you will develop a hunger to live on mission and a habit of sharing your faith and making disciples.</p>')],
 'in-jerusalem':[('His witness and ambassadors','His witnesses and ambassadors'),('What are some “areas of influence” has God assigned to you?','What “areas of influence” has God assigned to you?'),
   ('find him. Yet he is actually not far from each one of us','find him. Yet he is actually not far from each one of us.'),
   ('Write their names here:</p>','Write their names here:</p>'+NAMES)],
 'sharing-the-gospel':[('<p>Use the Steps to Peace With God Tract and the Two Minute Testimony Worksheet to model sharing the Gospel and sharing your testimony.</p>',''),('<h2>Biblical Foundations</h2><p>God has given us all a mission to be His witness and ambassadors. He has given each of us different spheres of influence where we live out that calling.</p>','<h2>Biblical Foundations</h2>')],
 'gospel-of-john-discovery-study':[('(John 20:31).”','(John 20:31).'),('<p>Below we outline three plans','<p class="scripture"><strong>John 20:31</strong> “But these are written that you may believe that Jesus is the Messiah, the Son of God, and that by believing you may have life in his name.”</p><p>Below we outline three plans'),('21 weeks (about a semester)','21 weeks')],
 'freedom-from-generational-sin':[('Manasseh’s worshipped','Manasseh worshipped'),
   ('(2 Chronicles</p><p>20:19)','(2 Chronicles 34:19)'),('gave him a blessing</p><p>(2 Chronicles 20.26)','gave him a blessing (2 Chronicles 34:26-28)'),
   ('As we walk forward from lies into truth, medidate on Romans 5 and the generational blessing that is ours in Jesus:','As you walk forward in freedom, meditate on Romans 5 and the generational blessing that is ours in Jesus.')],
 'freedom-from-idolatry':[('found as worship you alone','found as we worship you alone'),('as a next in bearing','as a next step in bearing'),('He wants heal you','He wants to heal you'),
   ('1 Samuel 16.14.23','1 Samuel 16.14-23'),('Zaccheus','Zacchaeus'),('(Easton’s Bible Dictionary) in Scripture we see','(Easton’s Bible Dictionary). In Scripture we see')],
 'freedom-from-bitterness':[('Matthew 7.43-48','Matthew 5.43-48'),('as a next in bearing','as a next step in bearing'),('my heart, my thought and my life','my heart, my thoughts and my life'),
   ('While Joseph forgave his brothers and initiated</p><p>reconciliation with his brothers who had sold him into slavery.','Joseph forgave the brothers who had sold him into slavery and initiated reconciliation with them.')],
 'freedom-from-rebellion':[('They rebellion against God','Their rebellion against God'),('Absolom','Absalom'),('Saphira','Sapphira'),('search my hearts, my thoughts','search my heart, my thoughts')],
 'freedom-from-pride':[('are currently walked in pride','are currently walking in pride')],
 'freedom-from-lies-and-deception':[('list of common areas people walked in pride in Scripture','list of common lies people believe, each with a Scripture that speaks to it'),('are currently walked in lies and deception','are currently walking in lies and deception')],
 'freedom-from-habitual-sin':[('<p>Romans 5:12“','<p>Romans 6:12-14 “'),('receive forgiveness and grace for humility','receive forgiveness and grace to walk in the Spirit'),
   ('As we release these lies','As we release these patterns'),('Galatians 5 and Mark 7.20-23)','Galatians 5 and Mark 7.20-23'),('Debauchery;','Debauchery'),('Idolatry and witchcraft;','Idolatry and witchcraft')],
 'going-deeper-in-discipleship':[('https://antiochwaco.com/prayer','https://antiochwaco.com/hop'),('https://www.amazon.com/product-reviews/1732625255/','https://www.amazon.com/Business-Revival-Getting-Inside-Workplace/dp/1732625255'),('<a href="https://thefreedomfight.org/">Freedom Fight</a> together.','<a href="https://thefreedomfight.org/">Freedom Fight</a> together, a faith-based program for anyone fighting pornography.'),('curated activities to building on','curated activities for building on'),('laid in looking in and cultivating a Great Commission','laid in Look Out and cultivating a Great Commission')],
 'planning-your-next-season-of-discipleship':[('Using these 6 questions at the start of any season, to put together','Use these 6 questions at the start of any season to put together'),('next season of a discipleship group:','next season with a discipleship group:')],
 'tending-your-heart-curriculum':[('<p>These videos and handouts are designed to help you build a richer relationship with the Lord through listening prayer.</p>','<p>These four short videos and worksheets are designed to help you build a richer relationship with the Lord through listening prayer. Watch one together each time you meet, then work through its worksheet.</p>'),('<div class="media"><a class="media-link" href="https://www.youtube.com/watch?v=xsT5cRq_iss">', '<h3 class="session"><span>1</span>The Father’s Invitation to Intimacy</h3><p class="session-desc">Jesus died so we could enjoy two-way conversation with God. Learn how Jesus lived listening to the Father, and a simple test for recognizing God’s voice.</p><div class="media"><a class="media-link" href="https://www.youtube.com/watch?v=xsT5cRq_iss">'),('<div class="media"><a class="media-link" href="https://www.youtube.com/watch?v=Q6uoDldx_n4">', '<h3 class="session"><span>2</span>Hindrances to Hearing God</h3><p class="session-desc">What gets in the way of listening, and how to prepare your heart: worship, surrender, quieting distractions, asking simple questions and keeping a listening journal.</p><div class="media"><a class="media-link" href="https://www.youtube.com/watch?v=Q6uoDldx_n4">'),('<div class="media"><a class="media-link" href="https://www.youtube.com/watch?v=l5k3Qp8jxbM">', '<h3 class="session"><span>3</span>Overcoming Wounds and Lies</h3><p class="session-desc">Lies are often sown in wounds. Walk through forgiving those who hurt you, renouncing the lies, and receiving God’s truth in their place.</p><div class="media"><a class="media-link" href="https://www.youtube.com/watch?v=l5k3Qp8jxbM">'),('<div class="media"><a class="media-link" href="https://www.youtube.com/watch?v=mF6RlNBjXwE">', '<h3 class="session"><span>4</span>How to Tend Your Heart</h3><p class="session-desc">Keep talking with God through the day. When something triggers you, ask Him what it’s really about, and receive what He has for you in exchange.</p><div class="media"><a class="media-link" href="https://www.youtube.com/watch?v=mF6RlNBjXwE">')],
 'disciplemaking-stories':[('Kyle faithfully lead a','Kyle faithfully leads a')],
 'who-should-i-disciple':[('you might be asking of were do I start with them?','you might be asking where to start with them.'),
   ('without hesitation when Jesus called.','without hesitation when Jesus calls.'),('who recognized her need for a Savior rather than thinking they have','who recognizes her need for a Savior rather than thinking she has')],
 'the-freedom-prayer-experience':[('Freedom From Habitual Sins of the Flesh','Freedom From Habitual Sin')],
}
# A paragraph that opens with a Bible reference and then quotes the passage becomes a Scripture card.
_BOOK=r'(?:[123] )?(?:Genesis|Exodus|Leviticus|Numbers|Deuteronomy|Joshua|Judges|Ruth|Samuel|Kings|Chronicles|Nehemiah|Job|Psalms?|Proverbs|Isaiah|Jeremiah|Lamentations|Ezekiel|Daniel|Hosea|Joel|Jonah|Micah|Habakkuk|Matthew|Mark|Luke|John|Acts|Romans|Corinthians|Galatians|Ephesians|Philippians|Colossians|Col|Thessalonians|Timothy|Titus|Hebrews|James|Peter|Jude|Revelation)'
_REF=_BOOK+r' \d+[:.]\d+(?:[-–]\d+)?(?:,\s?\d+)?(?: \((?:NIV|ESV|NASB)\))?'
def promote_verses(x):
    def para(m):
        inner=m.group(1)
        flat=re.sub(r'</?(?:em|strong)>','',inner)
        mm=re.match(r'\s*(\d+\.\s+)?('+_REF+r')\s*(?:-\s*|:\s*|—\s*)?(?=[“"&A-Z\d<])(.*)$',flat,re.S)
        if not mm: return m.group(0)
        rest=mm.group(3).strip()
        if len(re.sub(r'<[^>]+>','',rest))<25: return m.group(0)
        label=(mm.group(1) or '').replace('.','').strip()
        ref=mm.group(2)
        lab=f'{label} · {ref}' if label else ref
        return f'<p class="scripture"><strong>{lab}</strong> {rest}</p>'
    return re.sub(r'<p>((?:(?!</?p[ >]|<ul>|<ol>|<h\d).)*?)</p>',para,x,flags=re.S)
def idol_cards(x):
    # heart idols: "1. Idolatry of ..." with a list of verses and examples -> heading, verse cards, examples line
    def grp(m):
        out=f'<h4 class="idol-head">{m.group(1).strip().rstrip(":")}</h4>'
        for li in re.findall(r'<li>(.*?)</li>',m.group(2),re.S):
            ex=re.match(r'Common (?:current )?examples:\s*(.*)$',li,re.I|re.S)
            if ex: out+=f'<p class="examples"><strong>Common examples:</strong> {ex.group(1).rstrip(")").strip()}</p>'
            else:
                v=re.match(r'('+_REF+r'):\s*(.*)$',li,re.S)
                out+=f'<p class="scripture"><strong>{v.group(1)}</strong> {v.group(2)}</p>' if v else f'<p>{li}</p>'
        return out
    return re.sub(r'<p><strong>(\d\. Idolatry of[^<]*)</strong><ul>(.*?)</ul>',grp,x,flags=re.S)
def passage_card(x,lead_end,ref):
    # paragraphs after a stray "—" line are one long passage -> one card
    i=x.index('<p>—</p>'); j=x.find('<h2>',i); j=len(x) if j<0 else j
    paras=re.findall(r'<p>(.*?)</p>',x[i+8:j],re.S)
    card=f'<details class="long" open><summary>Read {ref}</summary><p class="scripture passage"><strong>{ref}</strong> '+'<br><br>'.join(paras)+'</p></details>'
    return x[:i]+card+x[j:]
_body_for_fixed=body_for
def body_for(i):
    x=_body_for_fixed(i); s=slug(i)
    for a,b in REFINE.get(s,[]):
        assert a in x,(s,a[:70]); x=x.replace(a,b)
    if s=='freedom-from-generational-sin':
        x,n=re.subn(r'<p>R<em>omans 5\.15 (.*?)</em></p>',r'<p class="scripture"><strong>Romans 5:15-17</strong> \1</p>',x,flags=re.S); assert n==1
        x=passage_card(x,None,'Romans 5')
    if s=='freedom-from-idolatry':
        x=idol_cards(x); x=passage_card(x,None,'1 Thessalonians 1')
    if s=='freedom-from-lies-and-deception':
        a='continue in the truth found in Jesus:<ul>'; assert a in x
        k=x.index(a)+len(a)-4; e=x.index('</ul>',k)+5
        x=x[:k]+'<details class="long" open><summary>Read the 11 declarations of truth</summary>'+x[k:e]+'</details>'+x[e:]
    if s=='spirit-baptism':
        for lab,ref in (('New Fruit','Galatians 5:22-23'),('New Gifts','1 Corinthians 12:7')):
            x,n=re.subn(r'<p><strong>'+lab+r'-? </strong><em>'+re.escape(ref)+r' (.*?)</em></p>',f'<p class="scripture"><strong>{lab} · {ref}</strong> \\1</p>',x,flags=re.S); assert n==1,(lab)
    return promote_verses(x)

# ---------- Why? and Vision copy (approved by Zach in Notion, Oct 30) ----------
# Why? = for the discipler. Vision = what the discipler shares with the person they are discipling.
WHY={
 6:'John wrote his Gospel so that people would “believe that Jesus is the Messiah, the Son of God, and that by believing you may have life in his name” (John 20:31). Your goal isn’t to win an argument. It’s to read Jesus’ story together and let Him speak for Himself.',
 7:'This may be the most important conversation you ever have with them. Walk through the good news simply and clearly, and give them a real chance to respond to Jesus.',
 8:'New believers often think they need to know a lot before they can talk about Jesus. This lesson shows them their own story is already a powerful witness, and helps them get ready to share it this week.',
 9:'Baptism is one of the first steps of obedience Jesus has for every believer. Help them understand what it means, answer their questions, and help them make a plan to be baptized.',
 10:'Many new believers carry things from their old life: sin, demons, bitterness, wounds. This lesson helps them understand the freedom they have in Christ and walk through a prayer to break with the past.',
 11:'Jesus told His disciples to wait for the power of the Holy Spirit before they went out. This lesson helps them understand that promise and gives you time to pray together for them to be filled.',
 12:'Following Jesus was never meant to be done alone. This lesson helps them see why a local church matters and take the next step to belong to one.',
 2:'Everything else in Look Up grows out of this. Help them see that Jesus wants them with Him first, and get them started on a daily habit of time with Him through 40 Days of Devotion.',
 3:'A disciple who can feed themselves from Scripture will keep growing long after you stop meeting. This lesson helps them taste how good God’s Word is and build a daily habit of reading it.',
 1:'Worship turns their attention from themselves to God. This lesson helps them discover worship as a privilege, not a duty, and find simple ways to worship in their daily time with Jesus.',
 4:'The early church was devoted to prayer and saw God answer. This lesson helps them grow from occasional prayer to a living conversation with God, using the Lord’s Prayer as a guide.',
 5:'Many believers have never been taught that God speaks. This lesson gives them biblical confidence that He does, and time to practice listening together in a safe place.',
 13:'This lesson connects their time with Jesus to the rest of their day. Help them see abiding and obeying as one walk with Him, and name one area where God is calling them to obey.',
 14:'This lesson grounds their identity as God’s child, and lays the foundation for walking in a lifestyle of holiness and love.',
 15:'Hidden sin keeps people stuck. This lesson helps them see confession as freedom, not shame, and prepares them to practice it with you next time you meet.',
 16:'Confession names the sin; repentance turns from it. This lesson helps them move from feeling sorry to real change, and to partner with God in uprooting what they confessed.',
 17:'Removing sin leaves an empty space. This lesson helps them fill it with truth, healing and new habits, and invites the Holy Spirit to heal what’s underneath their sin.',
 18:'This is where Look In lands: holiness and love. Help them see what God is restoring in them, then lead them into the Freedom Prayer Experience.',
 19:'Look Out starts with identity, not technique. Help them see that being a witness is who they already are in Christ, and start them praying daily to notice the opportunities around them.',
 20:'Most people come to Jesus through someone they already know. This lesson helps them map their relationships and start praying by name for the people God has placed around them.',
 21:'Fear keeps many believers quiet. This lesson builds their confidence in the power of the gospel, gives them a simple way to share it, and gets you out sharing together.',
 22:'This is the goal of everything you’ve done together: that they would do the same with someone else. Help them identify who they could invest in and take a first step this week.',
}
SHARE={
 7:'God loves you, and He wants you to experience real peace and life, both now and forever. Jesus said He came so you could have life to the full. Today we’re going to look at how that’s possible, and what it means to say yes to Him.',
 8:'Every disciple of Jesus has a story of what God has done in their life. Sharing these stories is a powerful way to give glory to God and witness to others.',
 9:'Baptism is a picture of what Jesus has already done in you. Going under the water shows that your old life has died with Christ, and coming up shows that you’ve been raised to a brand new life. It’s a joyful, public way of saying, “I belong to Jesus now.”',
 10:'God has rescued you from the kingdom of darkness and brought you into the kingdom of His Son. You are a new creation. Today we get to stand on that truth together and close the door on anything from your old life.',
 11:'When you gave your life to Jesus, the Holy Spirit came to live inside you. This lesson is about being filled with His power to live boldly for Him, receiving gifts to serve others, and growing new fruit in your character.',
 12:'You were not meant to follow Jesus alone. God has given you a family in the church: people to encourage you, walk with you and serve alongside you. Joining a local church is how you say yes to that family.',
 2:'Jesus didn’t call His disciples just to work for Him. He called them first and foremost to be with Him. Before He ever sent them out, He wanted them to know His presence, learn from Him and become His friends. That’s what He wants with you too: a real, growing, daily friendship.',
 3:'Jesus said we don’t live on bread alone, but on every word that comes from the mouth of God. The Bible is daily bread for your soul. It nourishes you, steadies you, and is one of the main ways Jesus speaks to you as a friend.',
 1:'God is worthy of all our praise, and He invites us into His presence with thanksgiving. Worship isn’t just singing on Sunday. It’s a heart that turns toward God throughout the day, and it’s one of the sweetest parts of friendship with Jesus.',
 4:'Prayer is simply talking with your Father, who loves you and loves to answer. The first disciples devoted themselves to prayer, and they saw God move in amazing ways. Jesus invites you into that same kind of prayer life.',
 5:'The Holy Spirit lives inside you. He is God’s presence with you always, your Helper and your guide. Jesus said His sheep know His voice, and He wants you to learn to recognize it. Friendship goes both ways: we talk to God, and He speaks to us.',
 13:'Jesus doesn’t just want an hour of your day. He wants to walk with you through all of it. As you keep in step with the Spirit and say yes to what He asks, you’ll find His life, joy and peace growing in you.',
 14:'The moment you put your faith in Jesus, you became a child of God. You were adopted into His family, and He is a loving Father who is committed to making you more like Jesus. You don’t grow to earn His love. You grow because you already have it.',
 15:'To confess simply means to agree with God. When we bring our sin into the light, God is faithful to forgive us and cleanse us.',
 16:'Confession names the sin; repentance turns from it. Repentance is more than feeling bad. It’s a change of mind, heart and direction: turning away from sin and toward God. And the Bible promises that when we repent, times of refreshing come from the Lord.',
 17:'God doesn’t just want to pull the weeds of sin out of your life. He wants to plant something good in their place. As you put off your old self, He clothes you with compassion, kindness, humility and love. The Christian life isn’t only about what you avoid. It’s about who you’re becoming.',
 18:'Everything God is doing in you is leading somewhere beautiful: a life of holiness and love that looks like Jesus. You were created for this. As He heals and transforms you, you’ll find yourself loving God and loving others more freely than ever.',
 19:'When you put your faith in Jesus, you didn’t just get a new identity as God’s child. You got a new purpose. You are Christ’s ambassador, and God is making His appeal to the world through you. You don’t have to become a witness. You already are one.',
 20:'God has placed you exactly where you are on purpose. Your family, friends, neighbors and coworkers are your Jerusalem: the people God has given you to love and reach. Your mission field isn’t far away. It starts right where you live.',
 21:'The gospel is the power of God for salvation. That means the power isn’t in how well you say it. It’s in the message itself. Your part is to share it clearly and with love, and trust God with the results.',
 22:'Jesus’ last command wasn’t just to make converts. It was to make disciples who make disciples. Someone invested in you, and now it’s your turn. As you pour into a few faithful people and they pour into others, the gospel multiplies far beyond what any of us could do alone.',
}
for _k,_v in WHY.items(): VISION[_k]='Why? '+_v
_restructure_old=restructure
def restructure(i,secs):
    vision,secs=_restructure_old(i,secs)
    if i in WHY: vision='Why? '+WHY[i]
    if i==12: secs[0][1]+='<p>This lesson walks through God’s design for the church and how to become part of a local church.</p>'
    if i in SHARE:
        lead=f'<p class="vision-lead">{html.escape(SHARE[i],quote=False)}</p>'
        vs=[s for s in secs if s[0]=='Vision']
        if vs: vs[0][1]=lead
        else: secs.insert(1,['Vision',lead])
    return vision,secs

# Pride: 1 Peter 5:5-6 replaces the borrowed Psalm 68 (Zach, Oct 30)
_body_for_v3=body_for
def body_for(i):
    x=_body_for_v3(i)
    if slug(i)=='freedom-from-pride':
        b=lambda w: f'<input type="text" class="blank" aria-label="Fill in the blank" autocomplete="off" style="width:{w}em">'
        new=('<p class="scripture"><strong>1 Peter 5:5-6 (NIV)</strong> “All of you, clothe yourselves with '+b(5.4)+' toward one another, because, ‘God opposes the proud but shows favor to the humble.’ Humble yourselves, therefore, under God’s mighty hand, that he may '+b(5.4)+' in due time.”</p>')
        x,n=re.subn(r'<p class="scripture"><strong>Psalm 68:5-6 \(NIV\)</strong>.*?</p>',lambda m:new,x,count=1,flags=re.S); assert n==1
    return x

# Inventory groups on Idolatry and Lies fold up on phones (open on laptops and in print) (Zach, Oct 30)
_body_for_v4=body_for
def _inv(title,inner): return f'<details class="long inv" open><summary>{title}</summary><div class="inv-body">{inner}</div></details>'
def body_for(i):
    x=_body_for_v4(i); s=slug(i)
    if s=='freedom-from-idolatry':
        x,n=re.subn(r'<h4 class="idol-head">(.*?)</h4>(.*?)(?=<h4 class="idol-head">|<h3>)',lambda m:_inv(m.group(1),m.group(2)),x,flags=re.S); assert n==5,n
        def sp(m):
            t,refs,ex=m.group(1).strip(),m.group(2),m.group(3).strip()
            return _inv(t,f'<p class="examples"><strong>In Scripture:</strong> {refs}</p><p class="examples"><strong>Common examples:</strong> {ex}</p>')
        x,n=re.subn(r'<p><strong>(\d\. [^(<]*?)\s*\(([^)]*)\)\s*</strong>Common Current Examples:\s*(.*?)</p>',sp,x,flags=re.S); assert n==5,n
    if s=='freedom-from-lies-and-deception':
        # the old site split these lists in two; join them so each fold holds its whole list
        x,n=re.subn(r'</ul></details><ul>(.*?)</ul>',r'\1</ul></details>',x,count=1,flags=re.S); assert n==1
        x=x.replace('</li></ul><ul><li>Believing the lie','</li><li>Believing the lie')
        x,n=re.subn(r'<p><strong>(Lies (?:About God|about Life)):</strong><ul>(.*?)</ul>',lambda m:_inv(m.group(1).replace('about','About'),'<ul>'+m.group(2)+'</ul>'),x,flags=re.S); assert n==2,n
        a=x.index('<p><strong>Fears and Anxieties Inventory: </strong></p>'); b=x.index('<p>As we identify these fears',a)
        blk=x[a:b]
        lies=re.findall(r'<li>(.*?)(?:</li>|</p>)',blk)
        assert len(lies)==6,lies
        inner=('<p>Our fears and anxieties often stem from believing lies about:</p><ul>'+''.join(f'<li>{l}</li>' for l in lies[:3])+'</ul>'
               '<p>For example:</p><ul>'+''.join(f'<li>{l}</li>' for l in lies[3:])+'</ul>')
        x=x[:a]+_inv('Fears and Anxieties',inner)+x[b:]
    return x

files=[]
for i in info:
    fn=slug(i)+'.html'; open(OUT+fn,'w').write((foundations() if i==35 else page(i)).replace('Discipleship Planning Guide','Further Growth Planning Guide')); files.append(fn)
json.dump(files,open(D+'site_files.json','w'))
print(len(files),'pages')
