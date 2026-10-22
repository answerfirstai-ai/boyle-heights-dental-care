(function(){
'use strict';
var d=document,lang=d.body.dataset.lang||'en',es=lang==='es';
var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
// year
d.querySelectorAll('[data-year]').forEach(function(n){n.textContent=new Date().getFullYear()});
// menu
var mb=d.querySelector('.menu-btn'),nav=d.getElementById('nav');
if(mb)mb.addEventListener('click',function(){var o=nav.classList.toggle('open');mb.setAttribute('aria-expanded',o)});
// --- live hours (America/Los_Angeles). Practice-website hours; [0]=Sun
var H={0:null,1:[570,1050],2:[780,1080],3:[570,1050],4:null,5:[570,1050],6:[540,840]};
var DN=es?['domingo','lunes','martes','miércoles','jueves','viernes','sábado']:['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
function t(m){var h=Math.floor(m/60),mm=m%60,h12=h%12||12;return h12+(mm?':'+(mm<10?'0':'')+mm:'')+(es?(h<12?' a. m.':' p. m.'):(h<12?' AM':' PM'))}
function now(){var p=new Intl.DateTimeFormat('en-US',{timeZone:'America/Los_Angeles',weekday:'short',hour:'numeric',minute:'numeric',hourCycle:'h23'}).formatToParts(new Date()),o={};p.forEach(function(x){o[x.type]=x.value});return{d:['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].indexOf(o.weekday),m:(+o.hour%24)*60+(+o.minute)}}
var n=now(),today=H[n.d],open=today&&n.m>=today[0]&&n.m<today[1],status,next,cta,sub;
if(open){status=es?'Abierto ahora':'Open now';next=(es?'Abierto hasta las ':'Open until ')+t(today[1]);cta=(es?'Llame ya, abierto hasta las ':'Call now, open until ')+t(today[1]);}
else{var k,i,lbl;
 if(today&&n.m<today[0]){k=n.d;lbl=es?'hoy':'today'}else{for(i=1;i<8;i++){k=(n.d+i)%7;if(H[k])break}lbl=i===1?(es?'mañana':'tomorrow'):(es?'el ':'')+DN[k]}
 status=es?'Cerrado ahora':'Closed now';
 next=(es?'Abrimos '+lbl+' a la'+(H[k][0]>=780?' ':'s ')+t(H[k][0]):'We open '+lbl+' at '+t(H[k][0]))+(es?'':'.')+(n.d===4?(es?' Los jueves cerramos.':' Closed Thursdays.'):'');
 cta=es?'Llame '+lbl+' a la'+(H[k][0]>=780?' ':'s ')+t(H[k][0]):'Call '+lbl+' at '+t(H[k][0]);
 sub=es?'Estamos cerrados ahora. Llámenos '+lbl+' a partir de la'+(H[k][0]>=780?' ':'s ')+t(H[k][0])+'.':'We’re closed right now. Give us a call '+lbl+' from '+t(H[k][0])+'.';}
d.querySelectorAll('[data-status]').forEach(function(s){s.textContent=status;s.classList.add(open?'open':'closed')});
d.querySelectorAll('[data-next]').forEach(function(s){s.textContent=next});
var di=(n.d+6)%7;d.querySelectorAll('[data-day="'+di+'"]').forEach(function(l){l.classList.add('is-today');l.setAttribute('aria-current','date')});
d.querySelectorAll('[data-dyn-sub]').forEach(function(s){s.textContent=open?(es?'Le contestamos en español o inglés.':'We answer in Spanish or English.'):sub});
d.querySelectorAll('[data-dyn-call] span').forEach(function(s){s.parentNode.setAttribute('aria-label',cta+' — (323) 265-3680');s.textContent=cta});
// --- map facade
d.querySelectorAll('[data-load-map]').forEach(function(b){b.addEventListener('click',function(){var w=b.closest('.map-wrap'),f=d.createElement('iframe');f.src=w.dataset.map;f.title=w.dataset.title;f.loading='lazy';f.referrerPolicy='no-referrer-when-downgrade';f.setAttribute('allowfullscreen','');w.innerHTML='';w.appendChild(f);f.focus()})});
// --- tracking hooks (no analytics installed; dataLayer-ready)
function track(ev){(window.dataLayer=window.dataLayer||[]).push({event:ev,lang:lang})}
d.addEventListener('click',function(e){var a=e.target.closest('[data-track]');if(a)track(a.dataset.track)});
// --- language: remember, navigate instantly
d.querySelectorAll('[data-lang-switch]').forEach(function(a){a.addEventListener('click',function(){var to=a.dataset.langSwitch;try{localStorage.setItem('bhdc-lang',to)}catch(_){}track('lang-'+to)})});
// below-fold reveal marking (above-fold content is never hidden)
var vh=innerHeight;if(!reduce)d.querySelectorAll('[data-reveal]').forEach(function(el){if(el.getBoundingClientRect().top>vh*0.95)el.classList.add('pre')});
if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});d.querySelectorAll('[data-reveal].pre').forEach(function(el){io.observe(el)})}else d.querySelectorAll('.pre').forEach(function(el){el.classList.remove('pre')});
// --- GSAP
function go(){
 if(!window.gsap||reduce)return;
 var g=gsap,sign=d.querySelector('[data-sign]'),tl=g.timeline({defaults:{ease:'power2.out'}});
 if(sign){tl.fromTo(sign.querySelectorAll('.w'),{clipPath:'inset(0 100% 0 0)'},{clipPath:'inset(0 0% 0 0)',duration:.18,stagger:.02},0);
  var br=sign.querySelector('.brush');if(br)tl.fromTo(br,{strokeDashoffset:440},{strokeDashoffset:0,duration:.3},0.05);}
 if(window.ScrollTrigger){g.registerPlugin(ScrollTrigger);
  var art=d.querySelector('.hero>.window-art');if(art)g.to(art,{yPercent:30,rotate:4,ease:'none',scrollTrigger:{trigger:'.hero',start:'top top',end:'bottom top',scrub:true}});
 }
}
if(document.readyState==='complete')go();else addEventListener('load',go);
})();