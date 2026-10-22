import os, json, html
OUT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE='https://answerfirstai-ai.github.io/boyle-heights-dental-care/'
TEL='+13232653680'; PHONE='(323) 265-3680'
MAPS='https://goo.gl/maps/TSoP34AJ6tGVCvuz5'
MAPQ='https://www.google.com/maps/search/?api=1&query=Boyle+Heights+Dental+Care+2206+E+Cesar+E+Chavez+Ave+Los+Angeles+CA+90033'
EMBED='https://www.google.com/maps?q=Boyle+Heights+Dental+Care,+2206+E+Cesar+E+Chavez+Ave,+Los+Angeles,+CA+90033&output=embed'
FB='https://www.facebook.com/EugeneSongDDS/'; YELP='https://www.yelp.com/biz/boyle-heights-dental-care-los-angeles'
# practice website hours (TODO confirm vs Google 9:15)
HOURS=[('Mo','09:30','17:30'),('Tu','13:00','18:00'),('We','09:30','17:30'),('Th',None,None),('Fr','09:30','17:30'),('Sa','09:00','14:00'),('Su',None,None)]
SLUG={'home':{'en':'','es':''},'services':{'en':'services/','es':'servicios/'},'new':{'en':'new-patients/','es':'primera-visita/'},'hours':{'en':'hours-location/','es':'horario-ubicacion/'},'contact':{'en':'contact/','es':'contacto/'}}
T={
'en':{'locale':'en_US','nav':[('services','Services'),('new','New patients'),('hours','Hours & location'),('contact','Contact')],
 'call':'Call '+PHONE,'callnow':'Call now','req':'Get directions','skip':'Skip to content','menu':'Menu','days':['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'],'short':['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],'closed':'Closed','today':'Today','hourshead':'Hours','dir':'Get directions','addr':'2206 E Cesar E Chavez Ave<br>Los Angeles, CA 90033','showmap':'Load the map','mapnote':'Map loads from Google when you ask for it.',
 'trust':['Se habla español','USC-trained dentist','Medi-Cal accepted','Implants &amp; dentures in-office'],
 'hoursfine':'Hours from the office’s own website.','need':'NEED'},
'es':{'locale':'es_US','nav':[('services','Servicios'),('new','Primera visita'),('hours','Horario y ubicación'),('contact','Contacto')],
 'call':'Llamar '+PHONE,'callnow':'Llamar ahora','req':'Cómo llegar','skip':'Ir al contenido','menu':'Menú','days':['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo'],'short':['Lun','Mar','Mié','Jue','Vie','Sáb','Dom'],'closed':'Cerrado','today':'Hoy','hourshead':'Horario','dir':'Cómo llegar','addr':'2206 E Cesar E Chavez Ave<br>Los Angeles, CA 90033','showmap':'Ver el mapa','mapnote':'El mapa se carga desde Google cuando usted lo pida.',
 'trust':['Hablamos español','Dentista formado en USC','Aceptamos Medi-Cal','Implantes y dentaduras aquí mismo'],
 'hoursfine':'Horario según el sitio web de la oficina.','need':'FALTA'}}
def fmt(t,lang):
  h,m=map(int,t.split(':')); ap='AM' if h<12 else 'PM'; h12=h%12 or 12
  if lang=='es': return f"{h12}:{m:02d} {'a. m.' if h<12 else 'p. m.'}"
  return f"{h12}:{m:02d} {ap}"
def rng(i,lang):
  d,o,c=HOURS[i]; return T[lang]['closed'] if not o else f"{fmt(o,lang)} – {fmt(c,lang)}"
I={
'phone':'<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2Z"/></svg>',
'pin':'<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 22s7-6.3 7-12a7 7 0 1 0-14 0c0 5.7 7 12 7 12Z"/><circle cx="12" cy="10" r="2.5"/></svg>',
'sms':'<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20.5l1.4-4.9A8 8 0 1 1 21 12Z"/><path d="M8.5 12h.01M12 12h.01M15.5 12h.01"/></svg>',
'check':'<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="m5 12.5 4.5 4.5L19 7"/></svg>',
'tooth':'<svg viewBox="0 0 32 32" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M9 4c-3.5 0-5.5 3-5 7 .4 3 2 5 2.6 8 .6 3.2 1.2 9 3.9 9 2.4 0 2.2-6.5 5.5-6.5S19.6 28 22 28c2.8 0 3.3-5.8 3.9-9 .6-3 2.3-5 2.6-8 .5-4-1.5-7-5-7-3 0-4.4 1.6-7.5 1.6S12 4 9 4Z" fill="#F2A900" fill-opacity=".35"/></svg>',
'spark':'<svg viewBox="0 0 32 32" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M16 3v8M16 21v8M3 16h8M21 16h8"/><circle cx="16" cy="16" r="3.5" fill="#F2A900"/></svg>',
'implant':'<svg viewBox="0 0 32 32" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 3h14c1.5 0 2.5 1.5 2 3l-1.5 5h-15L7 6c-.5-1.5.5-3 2-3Z" fill="#F2A900" fill-opacity=".35"/><path d="M11 14h10M12 18h8M13 22h6M14.5 26h3"/></svg>'}
UNDER='<svg class="sign-line" viewBox="0 0 420 18" preserveAspectRatio="none" aria-hidden="true"><path class="brush" d="M3 12C70 5 160 4 230 8s130 6 187-2" fill="none" stroke="currentColor" stroke-width="7" stroke-linecap="round"/></svg>'
ART='''<svg class="window-art" viewBox="0 0 240 200" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 30c40 10 80 8 120 30s70 50 95 52"/><path d="M70 41c-6-14 2-24 10-26M110 52c4-16 16-22 26-20M150 70c-2 14 6 24 16 26M190 92c10-10 22-10 30-4"/><g fill="#F2A900" fill-opacity=".9" stroke="#5B3A8C"><circle cx="80" cy="15" r="5"/><circle cx="92" cy="22" r="4"/><circle cx="136" cy="32" r="5"/><circle cx="146" cy="42" r="3.5"/><circle cx="166" cy="96" r="5"/><circle cx="220" cy="88" r="4.5"/><circle cx="208" cy="80" r="3"/></g><g fill="#B79AE0" fill-opacity=".55"><circle cx="58" cy="28" r="4"/><circle cx="120" cy="60" r="4"/><circle cx="178" cy="100" r="3.5"/></g></svg>'''
def need(lang,txt): return f'<span class="need">[{T[lang]["need"]}: {txt}]</span>'
def url(page,lang,depth): return ('../'*depth)+lang+'/'+SLUG[page][lang]
def callbtn(lang,cls='btn btn-accent',where='x',dyn=True):
  d=' data-dyn-call' if dyn else ''
  return f'<a class="{cls}" href="tel:{TEL}" data-track="call-{where}"{d}>{I["phone"]}<span>{T[lang]["call"]}</span></a>'
def trust(lang):
  return '<ul class="trust" role="list">'+''.join(f'<li>{I["check"]}{t}</li>' for t in T[lang]['trust'])+'</ul>'
def weeklist(lang):
  return ''.join(f'<li data-day="{i}"{" class=off" if not HOURS[i][1] else ""}><span>{T[lang]["days"][i]}</span><span>{rng(i,lang)}</span></li>' for i in range(7))
def todaycard(lang):
  t=T[lang]
  return f'''<aside class="today" aria-labelledby="hoy-{lang}" data-hours-card>
<div class="today-head"><h2 id="hoy-{lang}">{t["today"]}</h2><span class="status" data-status>{t["hourshead"]}</span></div>
<p class="next" data-next>{"Tuesdays we open at 1. Thursdays we’re closed." if lang=="en" else "Martes abrimos a la 1. Los jueves cerramos."}</p>
<ul class="week" role="list">{weeklist(lang)}</ul>
<p class="fine">{t["hoursfine"]}</p></aside>'''
def weekgrid(lang):
  return '<ul class="week-grid" role="list">'+''.join(f'<li data-day="{i}"{" class=off" if not HOURS[i][1] else ""}><b>{T[lang]["short"][i]}</b><span>{rng(i,lang).replace(" – ","<br>– ")}</span></li>' for i in range(7))+'</ul>'
def hourscard(lang):
  t=T[lang]; en=lang=='en'
  return f'''<div class="hours-card"><div class="today-head"><h3>{t["hourshead"]}</h3><span class="status" data-status>{t["hourshead"]}</span></div><p class="next" data-next></p>{weekgrid(lang)}<p class="fine">{t["hoursfine"]} {need(lang,"confirm opening times; Google lists 9:15" if en else "confirmar hora de apertura; Google indica 9:15")}</p></div>'''
VINE='<svg class="vine" viewBox="0 0 240 200" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M20 30c40 10 80 8 120 30s70 50 95 52"/><path d="M70 41c-6-14 2-24 10-26M110 52c4-16 16-22 26-20M150 70c-2 14 6 24 16 26M190 92c10-10 22-10 30-4"/><g fill="currentColor"><circle cx="80" cy="15" r="5"/><circle cx="136" cy="32" r="5"/><circle cx="166" cy="96" r="5"/><circle cx="220" cy="88" r="4.5"/></g></svg>'
def pic(n,alt,cls='',eager=False):
  ld='' if eager else ' loading="lazy"'
  return f'<picture class="{cls}"><source type="image/avif" srcset="../assets/img/{n}-640.avif 640w, ../assets/img/{n}-1024.avif 1024w" sizes="(max-width:700px) 100vw, 60vw"><source type="image/webp" srcset="../assets/img/{n}-640.webp 640w, ../assets/img/{n}-1024.webp 1024w" sizes="(max-width:700px) 100vw, 60vw"><img src="../assets/img/{n}-1024.webp" width="1024" height="{576 if n=="corner" else 768}" alt="{alt}"{ld} decoding="async"></picture>'
def illus(lang): return '<span class="illus">'+('Illustrative scene' if lang=='en' else 'Escena ilustrativa')+'</span>'
def shelf(lang):
  en=lang=='en'
  cards=[f'<article class="shelf-card photo-card">{pic("room","" )}{illus(lang)}<div class="pc-cap"><b>{"Everything in one office." if en else "Todo en una sola oficina."}</b><span>{"Generic treatment room, not our office." if en else "Sala genérica, no es nuestra oficina."}</span></div></article>']
  for ic,h,p,li in SERV[lang]:
    for j in range(0,len(li),4):
      cards.append(f'<article class="shelf-card"><span class="sc-eb">{h}</span><h3>{p if j==0 else ("More " if en else "Más: ")+h.lower()}</h3><ul role="list">{"".join(f"<li>{x}</li>" for x in li[j:j+4])}</ul></article>')
  return '<div class="shelf" tabindex="0" role="region" aria-label="'+('Services' if en else 'Servicios')+'">'+''.join(cards)+'</div>'
def mapblock(lang):
  t=T[lang]
  return f'''<div class="map-wrap" data-map="{html.escape(EMBED)}" data-title="{'Mapa de Boyle Heights Dental Care' if lang=='es' else 'Map of Boyle Heights Dental Care'}"><div class="map-ph">{ART.replace('window-art','map-art')}<div><button type="button" class="btn btn-ghost btn-sm" data-load-map>{I["pin"]}{t["showmap"]}</button><p class="muted small">{t["mapnote"]}</p></div></div></div>'''
def actions(lang,where):
  en=lang=='en'
  items=[('tel:'+TEL,'phone','Call' if en else 'Llamar',PHONE,'act-call','call'),(MAPS,'pin','Directions' if en else 'Cómo llegar','2206 E Cesar E Chavez Ave','act-dir','directions')]
  out=''
  for h,ic,lb,sub,cls,tr in items:
    ext=' target="_blank" rel="noopener"' if h.startswith('http') else ''
    out+=f'<a class="act {cls}" href="{h}"{ext} data-track="{tr}-{where}"><span class="act-ic">{I[ic]}</span><span class="act-t"><b>{lb}</b><small>{sub}</small></span><span class="act-arrow" aria-hidden="true">→</span></a>'
  return f'<div class="acts" data-reveal>{out}</div>'
def schema(lang):
  oh=[]
  for d,o,c in HOURS:
    if o: oh.append({"@type":"OpeningHoursSpecification","dayOfWeek":"https://schema.org/"+{'Mo':'Monday','Tu':'Tuesday','We':'Wednesday','Fr':'Friday','Sa':'Saturday'}[d],"opens":o,"closes":c})
  return {"@context":"https://schema.org","@type":"Dentist","@id":BASE+"#practice","name":"Boyle Heights Dental Care","legalName":"Eugene Song DDS Inc","url":BASE+lang+"/","logo":BASE+"assets/img/logo.png","image":[BASE+"assets/img/storefront-2206.jpg",BASE+"assets/img/og.jpg"],"telephone":"+1-323-265-3680",
   "address":{"@type":"PostalAddress","streetAddress":"2206 E Cesar E Chavez Ave","addressLocality":"Los Angeles","addressRegion":"CA","postalCode":"90033","addressCountry":"US"},
   "areaServed":["Boyle Heights","East Los Angeles","Los Angeles"],"hasMap":MAPS,"sameAs":[FB,YELP],"openingHoursSpecification":oh,
   "availableLanguage":["es","en"],"paymentAccepted":"Cash, Credit Card, CareCredit","currenciesAccepted":"USD",
   "employee":{"@type":"Person","name":"Eugene Song","honorificSuffix":"DDS","jobTitle":"Dentist","alumniOf":{"@type":"CollegeOrUniversity","name":"University of Southern California"}},
   "makesOffer":{"@type":"Offer","name":"New patient exam and X-rays" if lang=='en' else "Examen y radiografías para pacientes nuevos","price":"50","priceCurrency":"USD"},
   "medicalSpecialty":"Dentistry","inLanguage":lang}
def page(lang,key,title,desc,body,crumb=None):
  other='es' if lang=='en' else 'en'; depth=1+(1 if SLUG[key][lang] else 0); r='../'*depth; t=T[lang]
  canon=BASE+lang+'/'+SLUG[key][lang]
  nav=''.join(f'<a href="{url(k,lang,depth)}"{" aria-current=page" if k==key else ""}>{n}</a>' for k,n in t['nav'])
  ld=[schema(lang)]
  if crumb: ld.append({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Boyle Heights Dental Care","item":BASE+lang+"/"},{"@type":"ListItem","position":2,"name":crumb,"item":canon}]})
  if key=='new': ld.append(FAQLD[lang])
  wk=''.join(f'<li><span>{t["short"][i]}</span><span>{rng(i,lang)}</span></li>' for i in range(7))
  doc=f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="en" href="{BASE}en/{SLUG[key]['en']}">
<link rel="alternate" hreflang="es" href="{BASE}es/{SLUG[key]['es']}">
<link rel="alternate" hreflang="x-default" href="{BASE}en/{SLUG[key]['en']}">
<meta name="theme-color" content="#5B3A8C">
<meta property="og:type" content="website"><meta property="og:site_name" content="Boyle Heights Dental Care"><meta property="og:locale" content="{t['locale']}"><meta property="og:locale:alternate" content="{T[other]['locale']}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{BASE}assets/img/og.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Boyle Heights Dental Care storefront at 2206 E Cesar E Chavez Ave">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{title}"><meta name="twitter:description" content="{desc}"><meta name="twitter:image" content="{BASE}assets/img/og.jpg">
<link rel="icon" href="{r}favicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="32x32" href="{r}assets/img/icon-32.png"><link rel="apple-touch-icon" href="{r}assets/img/icon-180.png"><link rel="manifest" href="{r}site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Bricolage+Grotesque:opsz,wght@12..96,600..800&display=swap">
<link rel="stylesheet" href="{r}assets/css/site.css">
<script>document.documentElement.classList.add('js')</script>
<script type="application/ld+json">{json.dumps(ld if len(ld)>1 else ld[0],ensure_ascii=False)}</script>
</head>
<body data-lang="{lang}" data-page="{key}">
<a class="skip" href="#main">{t['skip']}</a>
<header class="site-header"><div class="wrap">
<a class="brand" href="{url('home',lang,depth)}" aria-label="Boyle Heights Dental Care — {'inicio' if lang=='es' else 'home'}"><picture><source srcset="{r}assets/img/logo.webp" type="image/webp"><img src="{r}assets/img/logo.png" alt="Boyle Heights Dental Care" width="600" height="126"></picture></a>
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav">{t['menu']}</button>
<nav class="nav" id="nav" aria-label="{'Principal' if lang=='es' else 'Main'}">{nav}</nav>
<div class="lang" role="group" aria-label="{'Idioma' if lang=='es' else 'Language'}"><a href="{r}es/{SLUG[key]['es']}" hreflang="es" lang="es" data-lang-switch="es" aria-current="{str(lang=='es').lower()}">ES</a><a href="{r}en/{SLUG[key]['en']}" hreflang="en" lang="en" data-lang-switch="en" aria-current="{str(lang=='en').lower()}">EN</a></div>
<a class="btn btn-accent btn-sm hdr-call" href="tel:{TEL}" data-track="call-header">{I['phone']}<span>{PHONE}</span></a>
</div></header>
<main id="main">
{body}
</main>
<footer class="site-footer"><div class="wrap">
<div class="foot-grid">
<div><img class="foot-logo" src="{r}assets/img/logo-white.png" alt="" width="421" height="300" loading="lazy">
<p>{"Dentista familiar en Boyle Heights, desde limpiezas hasta implantes." if lang=='es' else "Family dentistry in Boyle Heights, from cleanings to implants."}</p>
<p><a href="tel:{TEL}" data-track="call-footer"><strong>{PHONE}</strong></a></p></div>
<div><h2>{'Visítenos' if lang=='es' else 'Visit'}</h2><address class="addr-f">Boyle Heights Dental Care<br>{t['addr']}</address><p><a href="{MAPS}" rel="noopener" target="_blank">{t['dir']}</a></p></div>
<div><h2>{t['hourshead']}</h2><ul class="foot-week" role="list">{wk}</ul></div>
<div><h2>{'Páginas' if lang=='es' else 'Pages'}</h2><ul role="list">{''.join(f'<li><a href="{url(k,lang,depth)}">{n}</a></li>' for k,n in t['nav'])}<li><a href="{FB}" rel="noopener" target="_blank">Facebook</a></li><li><a href="{YELP}" rel="noopener" target="_blank">Yelp</a></li></ul></div>
</div>
<div class="legal"><span>© <span data-year>2026</span> Boyle Heights Dental Care · Eugene Song DDS Inc</span><span>{"Aceptamos la mayoría de los seguros. Llame para confirmar su plan." if lang=='es' else "Most insurance accepted. Call to confirm your plan."}</span></div>
</div></footer>
<div class="mobile-bar">{callbtn(lang,'btn btn-accent','mobilebar',False).replace(t['call'],t['callnow'])}<a class="btn btn-ghost" href="{MAPS}" target="_blank" rel="noopener" data-track="directions-mobilebar">{I['pin']}{t['req']}</a></div>
<div class="brush-wipe" aria-hidden="true"></div>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js" defer></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js" defer></script>
<script src="{r}assets/js/site.js" defer></script>
</body></html>'''
  p=os.path.join(OUT,lang,SLUG[key][lang]); os.makedirs(p,exist_ok=True); open(os.path.join(p,'index.html'),'w').write(doc)
  return canon

FAQ={'en':[('What does the $50 first visit include?','The practice’s website lists a new patient exam and X-rays for $50. '+'%NEED1%'),
 ('Do you take my insurance?','The office accepts most insurance, including Delta Dental, Cigna, Aetna, Guardian, Anthem, MetLife, United Concordia, Principal and Medi-Cal (Denti-Cal). Plans change, so call and we’ll check yours. '+'%NEED2%'),
 ('Can I bring my kids?','Yes. Children’s dentistry is part of our family practice, so the whole family can be seen in one place.'),
 ('Is the staff bilingual?','We serve patients in English and Spanish, and our patient forms come in both languages. '+'%NEED3%'),
 ('Why are you closed on Thursdays?','That’s our regular schedule: closed Thursday and Sunday, afternoons only on Tuesday (1–6 PM), and Saturday mornings.')],
'es':[('¿Qué incluye la primera visita de $50?','El sitio web de la oficina ofrece examen y radiografías para pacientes nuevos por $50. '+'%NEED1%'),
 ('¿Aceptan mi seguro?','Aceptamos la mayoría de los seguros, incluidos Delta Dental, Cigna, Aetna, Guardian, Anthem, MetLife, United Concordia, Principal y Medi-Cal (Denti-Cal). Los planes cambian; llámenos y revisamos el suyo. '+'%NEED2%'),
 ('¿Puedo traer a mis hijos?','Sí. La odontología para niños es parte de nuestra práctica familiar: toda la familia en un solo lugar.'),
 ('¿El personal habla español?','Atendemos en inglés y en español, y los formularios para pacientes están en los dos idiomas. '+'%NEED3%'),
 ('¿Por qué cierran los jueves?','Es nuestro horario fijo: cerrado jueves y domingo, martes solo por la tarde (1 a 6 p. m.) y sábados por la mañana.')]}
NEEDS={'en':['what’s included and terms','confirm the office checks coverage by phone','confirm Spanish-speaking staff'],'es':['qué incluye y condiciones','confirmar que revisan el seguro por teléfono','confirmar personal que habla español']}
import re
def strip(s): return re.sub(r'\s*%NEED\d%','',s)
FAQLD={l:{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":strip(a)}} for q,a in FAQ[l][2:]+FAQ[l][4:4]]} for l in FAQ}
def faqhtml(lang,items):
  out=''
  for q,a in items:
    for i in range(3): a=a.replace(f'%NEED{i+1}%',need(lang,NEEDS[lang][i]))
    out+=f'<details><summary>{q}</summary><div class="a"><p>{a}</p></div></details>'
  return f'<div class="faq">{out}</div>'

SERV={'en':[('tooth','Family &amp; general','Checkups, cleanings and everyday care for every age.',["Children’s dentistry","Cleanings &amp; exams","Fillings","Sealants","Gum disease treatment","Extractions","Oral cancer screenings","Root canals"]),
  ('spark','Cosmetic','Brighter, straighter smiles without a big production.',["Clear aligners (ClearCorrect)","Dental bonding","Teeth whitening"]),
  ('implant','Restorative &amp; implants','Dentures that stay put, held by implants.',["Dental implants","Implant-supported dentures","Dentures","Crowns","Bridges","Bone grafting"])],
 'es':[('tooth','Familiar y general','Chequeos, limpiezas y el cuidado de todos los días, para todas las edades.',["Odontología para niños","Limpiezas y exámenes","Empastes","Selladores","Tratamiento de encías","Extracciones","Detección de cáncer oral","Endodoncias (tratamiento de conducto)"]),
  ('spark','Estética','Sonrisas más blancas y alineadas, sin complicaciones.',["Alineadores transparentes (ClearCorrect)","Adhesión dental (bonding)","Blanqueamiento dental"]),
  ('implant','Restauración e implantes','Dentaduras que no se mueven: sostenidas con implantes.',["Implantes dentales","Dentaduras sobre implantes","Dentaduras","Coronas","Puentes","Injerto óseo"])]}
def svcgrid(lang):
  return '<div class="svc-grid">'+''.join(f'<article class="svc" data-reveal><h3>{I[ic]}{h}</h3><p class="muted">{p}</p><ul role="list">{"".join(f"<li>{x}</li>" for x in li)}</ul></article>' for ic,h,p,li in SERV[lang])+'</div>'

def home(lang):
  en=lang=='en'; t=T[lang]; d=1
  h1=("Your first visit, $50.","Right here on Cesar Chavez.") if en else ("Su primera visita, $50.","Aquí en Cesar Chavez.")
  words=lambda s:' '.join(f'<span class="w">{w}</span>' for w in s.split())
  body=f'''<section class="hero" aria-labelledby="h1"><div class="wrap">
<div class="window">
<p class="kicker">{"Your dentist on the block" if en else "Su dentista de la cuadra"}</p>
<h1 id="h1" class="sign" data-sign><span class="sign-text">{words(h1[0])} <span class="hl">{words(h1[1])}</span></span>{UNDER}</h1>
<p class="lede">{"Family dentistry in Boyle Heights, from cleanings to implants." if en else "Dentista familiar en Boyle Heights, desde limpiezas hasta implantes."}</p>
<div class="cta-row">{callbtn(lang,'btn btn-accent btn-xl','hero')}<a class="text-link" href="{MAPS}" target="_blank" rel="noopener" data-track="directions-hero">{t['req']} →</a></div>
<p class="cta-sub" data-dyn-sub aria-live="polite"></p>
{trust(lang)}
</div>
{todaycard(lang)}
</div>{ART}</section>
<section class="band" aria-label="{'New patient special' if en else 'Especial para pacientes nuevos'}"><div class="wrap">
<p><strong>$50</strong> {"new patient exam &amp; X-rays." if en else "examen y radiografías para pacientes nuevos."} <span class="terms">{need(lang,NEEDS[lang][0])}</span></p>
{callbtn(lang,'btn btn-accent btn-sm','band',False)}</div></section>
<section class="section tone-gold" aria-labelledby="first">{VINE}<div class="wrap">
<div class="section-head"><h2 id="first" class="two-tone">{"Three steps." if en else "Tres pasos."} <span>{"No surprises." if en else "Sin sorpresas."}</span></h2><p>{"We listen first, then explain what we see and what it costs before any treatment starts." if en else "Primero le escuchamos. Luego le explicamos lo que vemos y lo que cuesta, antes de empezar cualquier tratamiento."}</p></div>
<ol class="steps big">
<li data-reveal><span class="num">01</span><h3>{"Call us" if en else "Llámenos"}</h3><p>{"Pick a time that works. We answer in English or Spanish." if en else "Escoja un horario que le funcione. Le atendemos en español o inglés."}</p></li>
<li data-reveal><span class="num">02</span><h3>{"Exam &amp; X-rays" if en else "Examen y radiografías"}</h3><p>{"Dr. Song checks your teeth and gums and takes the X-rays he needs." if en else "El Dr. Song revisa sus dientes y encías y toma las radiografías necesarias."}</p></li>
<li data-reveal><span class="num">03</span><h3>{"Your plan &amp; price" if en else "Su plan y su precio"}</h3><p>{"You leave knowing what you need, what it costs and what insurance covers." if en else "Usted sale sabiendo qué necesita, cuánto cuesta y qué cubre su seguro."}</p></li>
</ol>
</div></section>
<section class="section tone-purple" aria-labelledby="svc">{VINE}<div class="wrap">
<div class="section-head"><h2 id="svc" class="two-tone">{"Our services." if en else "Nuestros servicios."} <span>{"Cleanings to implants, on Cesar Chavez." if en else "De limpiezas a implantes, en la Cesar Chavez."}</span></h2><p>{"All done here, in our office on Cesar Chavez Ave." if en else "Todo aquí, en nuestra oficina de la Cesar Chavez."} <a href="{url('services',lang,d)}">{"See all services" if en else "Ver todos los servicios"} →</a></p></div></div>
{shelf(lang)}
</section>
<section class="section" aria-labelledby="doc"><div class="wrap split">
<div class="doc" data-reveal><div class="monogram" aria-hidden="true">ES</div><div>
<span class="eyebrow">{"Your dentist" if en else "Su dentista"}</span>
<h2 id="doc">Dr. Eugene Song, DDS</h2>
<p>{"A Southern California native, Dr. Song earned his bachelor’s degree at the University of Southern California and studied dentistry at USC’s Herman Ostrow School of Dentistry. Outside the office you’ll find him on a tennis court. He’s proud to care for Boyle Heights and greater Los Angeles." if en else "Originario del sur de California, el Dr. Song obtuvo su licenciatura en la University of Southern California y estudió odontología en la Herman Ostrow School of Dentistry de USC. Fuera de la oficina, lo encontrará en una cancha de tenis. Es un honor para él atender a Boyle Heights y a todo Los Ángeles."}</p>
<p class="muted small">{need(lang,'headshot of Dr. Song' if en else 'foto del Dr. Song')}</p>
</div></div>
<figure class="photo" data-reveal><picture><source srcset="../assets/img/storefront-2206.webp" type="image/webp"><img src="../assets/img/storefront-2206.jpg" width="640" height="480" loading="lazy" decoding="async" alt="{'Storefront of Boyle Heights Dental Care at 2206 E Cesar E Chavez Ave, with a DENTIST sign and bilingual window lettering' if en else 'Fachada de Boyle Heights Dental Care en 2206 E Cesar E Chavez Ave, con el letrero DENTIST y letreros bilingües en las ventanas'}"></picture></figure>
</div></section>
<section class="section tone-gold" aria-labelledby="wk">{VINE}<div class="wrap split hours-split">
<div><h2 id="wk" class="two-tone">{"Tuesdays we open at 1." if en else "Martes abrimos a la 1."} <span>{"Thursdays we’re closed." if en else "Los jueves cerramos."}</span></h2><p>{"Saturday mornings too, for the week you can’t get away." if en else "También sábados por la mañana, para las semanas en que no puede salir del trabajo."}</p>{callbtn(lang,'btn btn-dark','week')}</div>
{hourscard(lang)}
</div></section>
<section class="corner" aria-labelledby="loc">
<div class="corner-media" data-push>{pic("corner","")}</div>{illus(lang)}
<div class="wrap corner-in"><div class="corner-card" data-reveal><span class="eyebrow">{"Find us" if en else "Encuéntrenos"}</span><h2 id="loc">{"On Cesar Chavez Ave, in the heart of Boyle Heights." if en else "En la Cesar Chavez, en el corazón de Boyle Heights."}</h2>
<address class="addr">{t['addr']}</address>
<div class="cta-row"><a class="btn btn-accent" href="{MAPS}" target="_blank" rel="noopener" data-track="directions-home">{I['pin']}<span>{t['dir']}</span></a></div>
<p class="small" style="margin-top:1rem">{"Parking:" if en else "Estacionamiento:"} {need(lang,'parking details' if en else 'detalles de estacionamiento')}</p>
<p class="small muted-l">{"Photo: generic illustrative street scene, not the actual office or block." if en else "Foto: escena ilustrativa genérica, no es la oficina ni la cuadra real."}</p></div></div>
</section>
<section class="section alt" aria-labelledby="fq"><div class="wrap">
<div class="section-head"><div><span class="eyebrow">{"Questions" if en else "Preguntas"}</span><h2 id="fq">{"Before you call" if en else "Antes de llamar"}</h2></div><p><a href="{url('new',lang,d)}">{"More for new patients" if en else "Más para pacientes nuevos"}</a></p></div>
{faqhtml(lang,FAQ[lang][:4])}
</div></section>
{finalband(lang,d)}'''
  title='Boyle Heights Dental Care | Family Dentist on Cesar Chavez Ave' if en else 'Boyle Heights Dental Care | Dentista familiar en Cesar Chavez'
  desc='Family dentistry in Boyle Heights, LA 90033. Implants, dentures and checkups. $50 new patient visit. Call (323) 265-3680.' if en else 'Dentista familiar en Boyle Heights. Implantes, dentaduras y limpiezas. Primera visita $50. Llame al (323) 265-3680.'
  return page(lang,'home',title,desc,body)
def finalband(lang,d):
  en=lang=='en'
  return f'''<section class="final tone-purple" aria-labelledby="fin-{lang}"><div class="wrap">{VINE}<h2 id="fin-{lang}" class="bi"><span lang="en">Call today.</span><span lang="es">Llame hoy.</span></h2><p class="bi-sub">{"We answer in Spanish or English." if en else "Le contestamos en español o inglés."}</p>{actions(lang,'final')}</div></section>'''
def phero(lang,eb,h,p):
  return f'<section class="page-hero"><div class="wrap"><span class="eyebrow">{eb}</span><h1 class="sign" data-sign><span class="sign-text">{" ".join(f"<span class=w>{w}</span>" for w in h.split())}</span>{UNDER}</h1><p>{p}</p><div class="cta-row">{callbtn(lang,"btn btn-accent","pagehero")}</div></div></section>'
def services(lang):
  en=lang=='en'; d=2
  det=''.join(f'<article class="svc-detail" data-reveal><div><h2>{h}</h2><p class="muted">{p}</p></div><ul>{"".join(f"<li>{x}</li>" for x in li)}</ul></article>' for ic,h,p,li in SERV[lang])
  body=phero(lang,"Services" if en else "Servicios","Dental care for the whole family." if en else "Cuidado dental para toda la familia.","Seventeen services under one roof on Cesar Chavez Ave, from your child’s first checkup to implant-supported dentures." if en else "Diecisiete servicios bajo un mismo techo en la Cesar Chavez, desde el primer chequeo de su hijo hasta dentaduras sobre implantes.")+f'<section class="section" style="padding-top:1rem"><div class="wrap">{det}<p class="muted">{"Not sure what you need? Call and describe it; we’ll tell you what kind of visit to book." if en else "¿No sabe qué necesita? Llámenos y descríbalo; le decimos qué tipo de cita hacer."}</p></div></section>'+finalband(lang,d)
  return page(lang,'services',"Dental Services in Boyle Heights | Implants, Dentures, Cleanings" if en else "Servicios dentales en Boyle Heights | Implantes, dentaduras, limpiezas",
   "Cleanings, fillings, root canals, whitening, ClearCorrect aligners, implants and implant-supported dentures on Cesar Chavez Ave. Call (323) 265-3680." if en else "Limpiezas, empastes, endodoncias, blanqueamiento, alineadores ClearCorrect, implantes y dentaduras sobre implantes en la Cesar Chavez. Llame al (323) 265-3680.",body,"Services" if en else "Servicios")
def newp(lang):
  en=lang=='en'; d=2
  ins=["Delta Dental","Cigna","Aetna","Guardian","Anthem","MetLife","United Concordia","Principal","Medi-Cal (Denti-Cal)"]
  body=phero(lang,"New patients" if en else "Pacientes nuevos","Your first visit, $50." if en else "Su primera visita, $50.","New patient exam and X-rays, explained in plain words and in your language." if en else "Examen y radiografías para pacientes nuevos, explicado claro y en su idioma.")+f'''
<section class="section" style="padding-top:1rem"><div class="wrap"><div class="cards">
<div class="card" data-reveal><h2 class="h3">{"What the $50 covers" if en else "Qué cubre la visita de $50"}</h2><p>{"New patient exam and X-rays." if en else "Examen y radiografías para pacientes nuevos."}</p><p>{need(lang,NEEDS[lang][0])}</p></div>
<div class="card" data-reveal><h2 class="h3">{"What to bring" if en else "Qué traer"}</h2><ul><li>{"Photo ID" if en else "Identificación con foto"}</li><li>{"Your insurance card, if you have one" if en else "Su tarjeta de seguro, si tiene"}</li><li>{"A list of medicines you take" if en else "Una lista de las medicinas que toma"}</li></ul></div>
<div class="card" data-reveal><h2 class="h3">{"Patient forms" if en else "Formularios"}</h2><p>{"Registration, medical history and consent forms are available in English and Spanish." if en else "Registro, historial médico y consentimientos, en español y en inglés."}</p><p>{need(lang,'forms download link' if en else 'enlace para descargar formularios')}</p></div>
</div></div></section>
<section class="section alt"><div class="wrap split">
<div data-reveal><span class="eyebrow">{"Insurance &amp; payment" if en else "Seguros y pagos"}</span><h2>{"Not sure about your insurance? Call and we’ll check." if en else "¿Su seguro? Llámenos y lo revisamos."}</h2><p>{"We accept most insurance, including:" if en else "Aceptamos la mayoría de los seguros, entre ellos:"}</p><ul class="chips" role="list">{"".join(f"<li>{x}</li>" for x in ins)}</ul></div>
<div data-reveal><h3>{"Other ways to pay" if en else "Otras formas de pago"}</h3><p>{"Cash, Visa, Mastercard, American Express and Discover. Financing through CareCredit." if en else "Efectivo, Visa, Mastercard, American Express y Discover. Financiamiento con CareCredit."}</p></div>
</div></section>
<section class="section"><div class="wrap"><h2>{"Questions" if en else "Preguntas"}</h2>{faqhtml(lang,FAQ[lang])}</div></section>'''+finalband(lang,d)
  return page(lang,'new',"New Patients: $50 Exam & X-Rays | Boyle Heights Dental Care" if en else "Pacientes nuevos: examen y radiografías $50 | Boyle Heights Dental Care",
   "New patient exam and X-rays for $50 in Boyle Heights. Most insurance and Medi-Cal accepted, CareCredit financing. Call (323) 265-3680." if en else "Examen y radiografías para pacientes nuevos por $50 en Boyle Heights. Aceptamos la mayoría de los seguros y Medi-Cal. Llame al (323) 265-3680.",body,"New patients" if en else "Pacientes nuevos")
def hoursp(lang):
  en=lang=='en'; d=2
  body=phero(lang,T[lang]['hourshead'],"Hours &amp; location" if en else "Horario y ubicación","2206 E Cesar E Chavez Ave, Los Angeles, CA 90033.")+f'''
<section class="section" style="padding-top:1rem"><div class="wrap">{weekgrid(lang)}<p class="muted small" style="margin-top:1rem">{T[lang]['hoursfine']}</p></div></section>
<section class="section alt"><div class="wrap split">
<div data-reveal><h2>{"Getting here" if en else "Cómo llegar"}</h2><address class="addr">Boyle Heights Dental Care<br>{T[lang]['addr']}</address>
<p>{"Transit:" if en else "Transporte:"} {need(lang,'nearest Metro stop' if en else 'parada de Metro más cercana')}</p>
<p>{"Parking:" if en else "Estacionamiento:"} {need(lang,'parking details' if en else 'detalles de estacionamiento')}</p>
<div class="cta-row"><a class="btn btn-ghost" href="{MAPS}" target="_blank" rel="noopener" data-track="directions-hours">{I['pin']}<span>{T[lang]['dir']}</span></a>{callbtn(lang,'btn btn-accent','hours',False)}</div></div>
<div data-reveal>{mapblock(lang)}</div></div></section>'''
  return page(lang,'hours',"Hours & Directions | Boyle Heights Dental Care, Cesar Chavez Ave" if en else "Horario y cómo llegar | Boyle Heights Dental Care",
   "Open Mon, Wed, Fri, Tue afternoons and Saturday mornings at 2206 E Cesar E Chavez Ave, Los Angeles 90033. Closed Thursday and Sunday." if en else "Abierto lunes, miércoles, viernes, martes por la tarde y sábados por la mañana en 2206 E Cesar E Chavez Ave. Cerrado jueves y domingo.",body,"Hours & location" if en else "Horario y ubicación")
def contact(lang):
  en=lang=='en'; d=2
  days=T[lang]['short']
  chips=''.join(f'<label class="chip"><input type="checkbox" name="day" value="{days[i]}"><span>{days[i]}</span></label>' for i in (0,1,2,4,5))
  body=phero(lang,"Contact" if en else "Contacto","The fastest way is a phone call." if en else "Lo más rápido es una llamada.","We pick up in Spanish or English." if en else "Le contestamos en español o inglés.")+f'''
<section class="section" style="padding-top:1rem" id="reach"><div class="wrap split" style="align-items:start">
<div data-reveal>{todaycard(lang)}</div>
<div data-reveal><h2 class="h3">{"Call us or come by" if en else "Llámenos o venga a vernos"}</h2><p class="muted">{"Call during office hours, or get directions to the office on Cesar Chavez Ave." if en else "Llame en horario de oficina o vea cómo llegar a la oficina en la Cesar Chavez."}</p>{actions(lang,'contact')}</div></div></section>'''
  return page(lang,'contact',"Contact & Book a Visit | Boyle Heights Dental Care (323) 265-3680" if en else "Contacto y citas | Boyle Heights Dental Care (323) 265-3680",
   "Call (323) 265-3680 or get directions to our Boyle Heights family dentist. English and Spanish spoken. 2206 E Cesar E Chavez Ave." if en else "Llame al (323) 265-3680 o vea cómo llegar con su dentista familiar en Boyle Heights. Hablamos español e inglés.",body,"Contact" if en else "Contacto")
urls=[]
for l in ('en','es'):
  for f in (home,services,newp,hoursp,contact): urls.append((f(l),l))
# sitemap with hreflang
keys=['home','services','new','hours','contact']
sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
for k in keys:
  for l in ('en','es'):
    sm+=f'<url><loc>{BASE}{l}/{SLUG[k][l]}</loc><lastmod>2026-10-22</lastmod>'+''.join(f'<xhtml:link rel="alternate" hreflang="{a}" href="{BASE}{a}/{SLUG[k][a]}"/>' for a in ('en','es'))+f'<xhtml:link rel="alternate" hreflang="x-default" href="{BASE}en/{SLUG[k]["en"]}"/></url>\n'
open(OUT+'/sitemap.xml','w').write(sm+'</urlset>\n')
open(OUT+'/robots.txt','w').write(f'User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n')
open(OUT+'/site.webmanifest','w').write(json.dumps({"name":"Boyle Heights Dental Care","short_name":"BH Dental","start_url":"./en/","display":"browser","theme_color":"#5B3A8C","background_color":"#F7F8FC","icons":[{"src":"assets/img/icon-180.png","sizes":"180x180","type":"image/png"},{"src":"assets/img/icon-512.png","sizes":"512x512","type":"image/png"}]}))
open(OUT+'/.nojekyll','w').write('')
open(OUT+'/index.html','w').write(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Boyle Heights Dental Care | Family Dentist on Cesar Chavez Ave</title><meta name="description" content="Family dentistry in Boyle Heights, LA 90033. Choose English or Spanish."><link rel="canonical" href="{BASE}en/"><link rel="alternate" hreflang="en" href="{BASE}en/"><link rel="alternate" hreflang="es" href="{BASE}es/"><link rel="alternate" hreflang="x-default" href="{BASE}en/"><link rel="icon" href="favicon.ico"><script>(function(){{var s=null;try{{s=localStorage.getItem('bhdc-lang')}}catch(e){{}}var l=s||((navigator.language||'en').toLowerCase().indexOf('es')===0?'es':'en');location.replace(l+'/')}})()</script><noscript><meta http-equiv="refresh" content="0; url=en/"></noscript><style>body{{font-family:system-ui;background:#F7F8FC;color:#1E1830;display:grid;place-items:center;min-height:100vh;margin:0}}a{{color:#5B3A8C;font-weight:700;margin:0 .5rem}}</style></head><body><main><h1>Boyle Heights Dental Care</h1><p><a href="es/" hreflang="es">Español</a> · <a href="en/" hreflang="en">English</a> · <a href="tel:{TEL}">{PHONE}</a></p></main></body></html>''')
open(OUT+'/404.html','w').write(f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Página no encontrada / Page not found | Boyle Heights Dental Care</title><meta name="robots" content="noindex"><link rel="icon" href="/boyle-heights-dental-care/favicon.ico"><link rel="stylesheet" href="/boyle-heights-dental-care/assets/css/site.css"></head><body><main id="main" class="section"><div class="wrap"><p class="eyebrow">404</p><h1>Esta página no existe.<br>This page doesn’t exist.</h1><p class="lede">Pero la oficina sí: 2206 E Cesar E Chavez Ave. / But the office does.</p><div class="cta-row"><a class="btn btn-accent" href="tel:{TEL}">{PHONE}</a><a class="btn btn-ghost" href="/boyle-heights-dental-care/es/">Inicio</a><a class="btn btn-ghost" href="/boyle-heights-dental-care/en/">Home</a></div></div></main></body></html>''')
print(len(urls),'pages')
