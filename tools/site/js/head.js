(function(d){var r=d.documentElement,p={};r.classList.add('js');try{p=JSON.parse(localStorage.getItem('oow703:prefs')||'{}')||{};
if(/^(light|sepia|dark)$/.test(p.theme))r.setAttribute('data-theme',p.theme);if(p.face==='sans')r.setAttribute('data-face','sans');
var s=[.9,1,1.1,1.2,1.35][p.step];if(s&&s!==1)r.style.setProperty('--scale',s);if(p.selftest===true)r.classList.add('selftest');
if(localStorage.getItem('oow703:last'))r.classList.add('has-last');}catch(e){}
if(/^https?:$/.test(location.protocol)){var f=(r.getAttribute('data-fonts')||'').split(' '),b=r.getAttribute('data-root')||'',i,l;
for(i=0;i<f.length;i++)if(f[i]&&!(p.face==='sans'&&/^trirong/.test(f[i]))){l=d.createElement('link');l.rel='preload';l.as='font';
l.type='font/woff2';l.crossOrigin='';l.href=b+'assets/fonts/'+f[i]+'.woff2';d.head.appendChild(l)}}})(document);
