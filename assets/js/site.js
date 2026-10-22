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
 sub=es?'¿Fuera de horario? Mándenos un texto al (323) 265-3680.':'After hours? Text us at (323) 265-3680.';}
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
// --- language: remember + signature brush repaint
d.querySelectorAll('[data-lang-switch]').forEach(function(a){a.addEventListener('click',function(e){
 var to=a.dataset.langSwitch;try{localStorage.setItem('bhdc-lang',to)}catch(_){}
 if(to===lang||reduce||!window.gsap)return;e.preventDefault();track('lang-'+to);
 var words=d.querySelectorAll('[data-sign] .w'),wipe=d.querySelector('.brush-wipe');
 var tl=gsap.timeline({onComplete:function(){location.href=a.href}});
 tl.to(words,{opacity:0,y:-8,duration:.18,stagger:.03,ease:'power1.in'})
   .set(wipe,{visibility:'visible',clipPath:'inset(0 100% 0 0)'})
   .to(wipe,{clipPath:'inset(0 0% 0 0)',duration:.38,ease:'power3.inOut'},'-=.05');
 try{sessionStorage.setItem('bhdc-wipe','1')}catch(_){}
})});
// --- GSAP
function go(){
 if(!window.gsap){d.documentElement.classList.remove('js');return}
 var g=gsap;var sign=d.querySelector('[data-sign]');var cameFromSwitch=false;try{cameFromSwitch=sessionStorage.getItem('bhdc-wipe')==='1';sessionStorage.removeItem('bhdc-wipe')}catch(_){}
 if(reduce){d.documentElement.classList.remove('js');return}
 var tl=g.timeline({defaults:{ease:'power3.out'}});
 if(cameFromSwitch){var wipe=d.querySelector('.brush-wipe');g.set(wipe,{visibility:'visible',clipPath:'inset(0 0 0 0%)'});tl.to(wipe,{clipPath:'inset(0 0 0 100%)',duration:.45,ease:'power3.inOut'}).set(wipe,{visibility:'hidden'})}
 if(sign){var ws=sign.querySelectorAll('.w');
  tl.fromTo(ws,{clipPath:'inset(0 100% 0 0)'},{clipPath:'inset(0 0% 0 0)',duration:.6,stagger:.06,ease:'power2.out'},cameFromSwitch?'-=.25':0)
    .fromTo(sign.querySelector('.brush'),{strokeDashoffset:440},{strokeDashoffset:0,duration:.55,ease:'power2.inOut'},'-=.35');}
 var card=d.querySelector('.hero [data-hours-card]');if(card)tl.from(card,{y:-28,opacity:0,rotate:-1.5,duration:.6,ease:'back.out(1.6)'},'-=.3');
 if(window.ScrollTrigger){g.registerPlugin(ScrollTrigger);
  ScrollTrigger.batch('[data-reveal]',{start:'top 88%',once:true,onEnter:function(b){g.fromTo(b,{opacity:0,y:24},{opacity:1,y:0,duration:.6,stagger:.08,overwrite:true})}});
  var art=d.querySelector('.hero>.window-art');if(art)g.to(art,{yPercent:30,rotate:4,ease:'none',scrollTrigger:{trigger:'.hero',start:'top top',end:'bottom top',scrub:true}});
  d.querySelectorAll('.week-grid').forEach(function(w){g.from(w.children,{y:30,opacity:0,duration:.5,stagger:.05,scrollTrigger:{trigger:w,start:'top 85%',once:true}})});
 } else g.set('[data-reveal]',{opacity:1});
}
go();
})();
