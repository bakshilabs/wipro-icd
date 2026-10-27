/* Shared chart helpers. Plain JS, no dependencies. Exposes window.VZ. */
(function(){
var NS="http://www.w3.org/2000/svg";
var VZ={};
/* create an SVG element: VZ.el("rect",{x:0,...},parent) */
VZ.el=function(tag,attrs,parent){var e=document.createElementNS(NS,tag);for(var k in attrs||{})e.setAttribute(k,attrs[k]);if(parent)parent.appendChild(e);return e};
VZ.svg=function(host,w,h,label){var s=VZ.el("svg",{viewBox:"0 0 "+w+" "+h,role:"img","aria-label":label||""});host.appendChild(s);return s};
/* linear scale */
VZ.lin=function(d0,d1,r0,r1){return function(v){return r0+(v-d0)/(d1-d0)*(r1-r0)}};
/* read a CSS custom property, e.g. VZ.c("--s1") */
VZ.c=function(name){return getComputedStyle(document.documentElement).getPropertyValue(name).trim()};
/* the series colour as a CSS var reference, slot 1..8 */
VZ.s=function(i){return "var(--s"+i+")"};
/* bar with 4px rounded data end and square baseline. horizontal if dir="h" */
VZ.bar=function(parent,x,y,w,h,fill,dir){var r=Math.min(4,dir==="h"?h/2:w/2,dir==="h"?w:h);var d;
 if(w<=0||h<=0)d="";
 else if(dir==="h")d="M"+x+","+y+"h"+(w-r)+"a"+r+","+r+" 0 0 1 "+r+","+r+"v"+(h-2*r)+"a"+r+","+r+" 0 0 1 -"+r+","+r+"h-"+(w-r)+"z";
 else d="M"+x+","+(y+h)+"v-"+(h-r)+"a"+r+","+r+" 0 0 1 "+r+",-"+r+"h"+(w-2*r)+"a"+r+","+r+" 0 0 1 "+r+","+r+"v"+(h-r)+"z";
 return VZ.el("path",{d:d,fill:fill},parent)};
/* tooltip: VZ.tip(el, function(){return "<b>Title</b>text"}) ; works with mouse, touch and keyboard focus */
var tip;function T(){if(!tip){tip=document.createElement("div");tip.className="vz-tip";tip.setAttribute("role","tooltip");document.body.appendChild(tip)}return tip}
function place(x,y){var t=T(),w=t.offsetWidth,h=t.offsetHeight,X=x+14,Y=y+14;if(X+w>innerWidth-8)X=x-w-14;if(Y+h>innerHeight-8)Y=y-h-14;t.style.left=Math.max(8,X)+"px";t.style.top=Math.max(8,Y)+"px"}
VZ.tip=function(el,fn){
 el.addEventListener("pointerenter",function(e){var t=T();t.innerHTML=fn();t.classList.add("on");place(e.clientX,e.clientY)});
 el.addEventListener("pointermove",function(e){place(e.clientX,e.clientY)});
 el.addEventListener("pointerleave",function(){if(pinned!==el)T().classList.remove("on")});
 if(!el.hasAttribute("tabindex"))el.setAttribute("tabindex","0");
 el.addEventListener("focus",function(){var t=T(),r=el.getBoundingClientRect();t.innerHTML=fn();t.classList.add("on");place(r.left+r.width/2,r.top+r.height/2)});
 el.addEventListener("blur",function(){if(pinned!==el)T().classList.remove("on")});
 /* click, tap or Enter pins the tooltip until the next click elsewhere */
 el.addEventListener("click",function(e){var t=T(),r=el.getBoundingClientRect();t.innerHTML=fn();t.classList.add("on");pinned=el;place(e.clientX||r.left+r.width/2,e.clientY||r.top+r.height/2);e.stopPropagation()});
 el.addEventListener("keydown",function(e){if(e.key==="Enter"||e.key===" "){if(el.tagName!=="BUTTON")e.preventDefault();el.dispatchEvent(new MouseEvent("click",{bubbles:true}))}});
};
var pinned=null;
document.addEventListener("click",function(){if(pinned){pinned=null;if(tip)tip.classList.remove("on")}});
addEventListener("scroll",function(){if(pinned){pinned=null;if(tip)tip.classList.remove("on")}},{passive:true});
VZ.hideTip=function(){if(tip)tip.classList.remove("on")};
/* tabs: container with [role=tablist] buttons[role=tab][aria-controls] */
VZ.tabs=function(list,onChange){var tabs=[].slice.call(list.querySelectorAll("[role=tab]"));
 function sel(t){tabs.forEach(function(x){var on=x===t;x.setAttribute("aria-selected",on);x.tabIndex=on?0:-1;var p=document.getElementById(x.getAttribute("aria-controls"));if(p)p.hidden=!on});if(onChange)onChange(t)}
 tabs.forEach(function(t,i){t.addEventListener("click",function(){sel(t)});t.addEventListener("keydown",function(e){var k=e.key==="ArrowRight"?1:e.key==="ArrowLeft"?-1:0;if(k){var n=tabs[(i+k+tabs.length)%tabs.length];n.focus();sel(n)}})});
 sel(tabs.filter(function(t){return t.getAttribute("aria-selected")==="true"})[0]||tabs[0]);};
/* count up numbers: <b class="count" data-to="22" data-suffix="%"> */
function count(el){var to=parseFloat(el.dataset.to),dec=(el.dataset.to.split(".")[1]||"").length,pre=el.dataset.prefix||"",suf=el.dataset.suffix||"",t0=null;
 if(matchMedia("(prefers-reduced-motion: reduce)").matches){el.textContent=pre+to.toLocaleString("en-GB",{minimumFractionDigits:dec,maximumFractionDigits:dec})+suf;return}
 function f(ts){if(!t0)t0=ts;var p=Math.min(1,(ts-t0)/1100),v=to*(1-Math.pow(1-p,3));el.textContent=pre+v.toLocaleString("en-GB",{minimumFractionDigits:dec,maximumFractionDigits:dec})+suf;if(p<1)requestAnimationFrame(f)}requestAnimationFrame(f)}
/* reveal on scroll: add class "rv" to anything; ".count" inside counts up */
VZ.reveal=function(){var els=[].slice.call(document.querySelectorAll(".rv,.count"));
 if(!("IntersectionObserver" in window)){els.forEach(function(e){e.classList.add("in");if(e.classList.contains("count"))count(e)});return}
 var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){en.target.classList.add("in");if(en.target.classList.contains("count"))count(en.target);io.unobserve(en.target)}})},{threshold:.15});
 els.forEach(function(e){io.observe(e)})};
/* redraw on theme toggle: VZ.onTheme(fn) */
VZ.onTheme=function(fn){new MutationObserver(fn).observe(document.documentElement,{attributes:true,attributeFilter:["data-theme"]});matchMedia("(prefers-color-scheme: dark)").addEventListener("change",fn)};

/* section navigation: a rail of labelled dots with previous and next buttons, plus paged scrolling.
   Sections are the visible top-level blocks of <main>. With paging on, one wheel turn, PageDown, Space or an arrow key
   moves a whole section; a section taller than the screen scrolls normally until its end, then the next one snaps in. */
VZ.secnav=function(){var main=document.getElementById("main");if(!main||document.querySelector(".secnav"))return;
 function blocks(el){return [].slice.call(el.children).filter(function(e){return !/^(SCRIPT|STYLE|NOSCRIPT|TEMPLATE)$/.test(e.tagName)&&e.offsetHeight>40&&getComputedStyle(e).position!=="fixed"})}
 function wrapper(e){var k=blocks(e);return k.length>1&&(!e.className||k.filter(function(c){return c.tagName==="SECTION"}).length>1)&&e.tagName!=="SECTION"}
 function flat(L,d){var o=[];L.forEach(function(e){if(d<3&&wrapper(e))o=o.concat(flat(blocks(e),d+1));else o.push(e)});return o}
 function secs(){var L=blocks(main),d=0;while(L.length===1&&d++<3){var k=blocks(L[0]);if(k.length<2)break;L=k}return flat(L,0)}
 var S=secs();if(S.length<2)return;
 function label(e,i){var h=e.querySelector("h1,h2,h3,.eyebrow,caption,legend");var t=(h&&h.textContent||"").replace(/\s+/g," ").trim();if(!t)t="Section "+(i+1);return t.length>44?t.slice(0,42)+"…":t}
 var reduce=matchMedia("(prefers-reduced-motion: reduce)").matches;
 var touch=matchMedia("(pointer: coarse)").matches;
 var paged=!touch;try{var v=localStorage.getItem("paged");if(v!==null)paged=v==="1"}catch(x){}
 var nav=document.createElement("nav");nav.className="secnav";nav.setAttribute("aria-label","Section navigation");
 var dots=S.map(function(e,i){return '<li><button type="button" class="dot" data-i="'+i+'"><span class="lab"></span></button></li>'}).join("");
 nav.innerHTML='<button type="button" class="up" aria-label="Previous section"><svg viewBox="0 0 24 24"><path d="M6 15l6-6 6 6"/></svg></button><ol class="rail">'+dots+'</ol><output aria-live="polite"></output><button type="button" class="dn" aria-label="Next section"><svg viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"/></svg></button><button type="button" class="pg" aria-pressed="'+paged+'" title="Move one section per scroll"><svg viewBox="0 0 24 24"><rect x="5" y="3" width="14" height="8" rx="1.5"/><rect x="5" y="13" width="14" height="8" rx="1.5"/></svg><span class="sr">Move one section per scroll</span></button>';
 document.body.appendChild(nav);
 var up=nav.querySelector(".up"),dn=nav.querySelector(".dn"),out=nav.querySelector("output"),pg=nav.querySelector(".pg"),D=[].slice.call(nav.querySelectorAll(".dot"));
 D.forEach(function(d,i){var t=label(S[i],i);d.querySelector(".lab").textContent=t;d.setAttribute("aria-label","Go to section "+(i+1)+": "+t);d.addEventListener("click",function(){to(i)})});
 function off(){var h=document.querySelector(".sitenav");return (h?h.offsetHeight:0)+12}
 function cur(){var y=scrollY+off()+4,i=0;S.forEach(function(e,k){if(e.getBoundingClientRect().top+scrollY<=y)i=k});
  if(innerHeight+scrollY>=document.documentElement.scrollHeight-2)i=S.length-1;return i}
 function upd(){var i=cur();out.textContent=(i+1)+" / "+S.length;up.disabled=scrollY<4;dn.disabled=atBottom();
  D.forEach(function(d,k){if(k===i)d.setAttribute("aria-current","step");else d.removeAttribute("aria-current")})}
 var lock=0;
 function to(i){i=Math.max(0,Math.min(S.length-1,i));var y=i===0?0:S[i].getBoundingClientRect().top+scrollY-off();
  lock=Date.now()+(reduce?150:750);scrollTo({top:y,behavior:reduce?"auto":"smooth"})}
 function topOf(k){return S[k].getBoundingClientRect().top+scrollY-off()}
 function atBottom(){return innerHeight+scrollY>=document.documentElement.scrollHeight-2}
 function go(d){var k;if(d>0){if(atBottom())return;for(k=0;k<S.length&&topOf(k)<=scrollY+8;k++);if(k<S.length)to(k);else{lock=Date.now()+(reduce?150:750);scrollTo({top:document.documentElement.scrollHeight,behavior:reduce?"auto":"smooth"})}}
  else{for(k=S.length-1;k>=0&&topOf(k)>=scrollY-8;k--);to(Math.max(k,0))}}
 up.addEventListener("click",function(){go(-1)});dn.addEventListener("click",function(){go(1)});
 pg.addEventListener("click",function(){paged=!paged;pg.setAttribute("aria-pressed",paged);try{localStorage.setItem("paged",paged?"1":"0")}catch(x){}});
 /* should this step leave the current section? only when its edge is on screen */
 function atEdge(dir){var i=cur(),r=S[i].getBoundingClientRect();
  if(dir>0)return !atBottom()&&r.bottom<=innerHeight+4;
  return r.top>=off()-8&&!(i===0&&scrollY<4)}
 function scrollsInside(t,dir){for(var e=t;e&&e!==document.body;e=e.parentElement){var cs=getComputedStyle(e);if(/(auto|scroll)/.test(cs.overflowY)&&e.scrollHeight>e.clientHeight+1){if(dir>0?e.scrollTop+e.clientHeight<e.scrollHeight-1:e.scrollTop>0)return true}}return false}
 addEventListener("wheel",function(e){if(!paged||e.ctrlKey||Math.abs(e.deltaY)<Math.abs(e.deltaX))return;
  var dir=e.deltaY>0?1:-1;if(Date.now()<lock){e.preventDefault();return}
  if(scrollsInside(e.target,dir))return;
  if(atEdge(dir)){e.preventDefault();go(dir)}},{passive:false});
 document.addEventListener("keydown",function(e){var t=e.target;if(e.altKey||e.ctrlKey||e.metaKey||/^(INPUT|SELECT|TEXTAREA)$/.test(t.tagName)||t.isContentEditable)return;
  var k=e.key,inCtl=/^(BUTTON|A|SUMMARY)$/.test(t.tagName)||t.getAttribute("role")==="tab"||t.hasAttribute("tabindex")&&t!==document.body&&t.id!=="main";
  if(k==="j"){go(1);e.preventDefault();return}if(k==="k"){go(-1);e.preventDefault();return}
  if(!paged)return;
  var dir=(k==="PageDown"||(k===" "&&!e.shiftKey&&!inCtl)||(k==="ArrowDown"&&!inCtl))?1:(k==="PageUp"||(k===" "&&e.shiftKey&&!inCtl)||(k==="ArrowUp"&&!inCtl))?-1:0;
  if(k==="Home"&&!inCtl){to(0);e.preventDefault();return}if(k==="End"&&!inCtl){to(S.length-1);e.preventDefault();return}
  if(!dir)return;if(Date.now()<lock){e.preventDefault();return}
  if(k.indexOf("Arrow")===0&&!atEdge(dir))return;
  e.preventDefault();if(atEdge(dir))go(dir);else{lock=Date.now()+(reduce?150:600);scrollBy({top:dir*(innerHeight-off()-48),behavior:reduce?"auto":"smooth"})}});
 var raf;addEventListener("scroll",function(){cancelAnimationFrame(raf);raf=requestAnimationFrame(upd)},{passive:true});addEventListener("resize",upd);upd();};
window.VZ=VZ;
document.addEventListener("DOMContentLoaded",function(){VZ.reveal();VZ.secnav()});
})();
