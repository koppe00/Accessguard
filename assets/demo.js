/* Klinq: het voorbeeld op de homepage. Alles gebeurt in deze pagina; er wordt niets verstuurd. */
(function(){
  var sheet=document.getElementById('demo');
  if(sheet){
    var rows=[].slice.call(sheet.querySelectorAll('tbody tr')),btn=document.getElementById('demoRun'),
        why=document.getElementById('demoWhy'),count=document.getElementById('demoCount'),
        still=matchMedia('(prefers-reduced-motion: reduce)').matches,done=false;
    var orig=rows.map(function(r){return{cls:r.className,res:r.querySelector('.res').textContent}});
    function reset(){rows.forEach(function(r){r.className='';r.querySelector('.res').textContent='·';r.removeAttribute('tabindex');r.removeAttribute('role')});why.hidden=true;count.textContent='nog niet gecontroleerd';}
    function select(r){
      rows.forEach(function(x){x.classList.remove('sel');x.setAttribute('aria-selected','false')});
      r.classList.add('sel');r.setAttribute('aria-selected','true');
      why.querySelector('.ttl').textContent=r.dataset.rule;
      why.querySelector('.txt').textContent=r.dataset.why;
      why.querySelectorAll('button').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.v===(r.dataset.oordeel||'')?'true':'false')});
      why.querySelector('.after').textContent=r.dataset.oordeel?'Vastgelegd. In de echte versie komt hier een verplichte toelichting bij.':'';
      why.hidden=false;
    }
    function finish(){
      done=true;var flags=rows.filter(function(r){return r.classList.contains('flag')});
      count.textContent=rows.length+' gecontroleerd · '+flags.length+' signalen';
      flags.forEach(function(r){r.classList.add('pick');r.tabIndex=0;r.setAttribute('role','button');r.setAttribute('aria-selected','false')});
      if(flags[0])select(flags[0]);
      btn.textContent='Opnieuw';
    }
    function run(){
      reset();btn.disabled=true;var i=0;
      (function step(){
        if(i>=rows.length){btn.disabled=false;finish();return}
        var r=rows[i],o=orig[i];r.className=o.cls;r.querySelector('.res').textContent=o.res;i++;
        still?step():setTimeout(step,110);
      })();
    }
    reset();
    btn.addEventListener('click',run);
    sheet.addEventListener('click',function(e){var r=e.target.closest('tr.pick');if(r)select(r)});
    sheet.addEventListener('keydown',function(e){var r=e.target.closest('tr.pick');if(r&&(e.key==='Enter'||e.key===' ')){e.preventDefault();select(r)}});
    why.addEventListener('click',function(e){var b=e.target.closest('button[data-v]');if(!b)return;var r=sheet.querySelector('tr.sel');if(!r)return;r.dataset.oordeel=b.dataset.v;select(r)});
  }
  var calc=document.getElementById('calc');
  if(calc){
    var a=calc.querySelector('#cTot'),b=calc.querySelector('#cMan'),out=calc.querySelector('output');
    function upd(){
      var t=Math.max(0,+a.value||0),m=Math.max(0,+b.value||0);
      if(!t){out.innerHTML='Vul het aantal inzages per maand in.';return}
      var p=Math.min(100,100*m/t),s=p<0.1?p.toLocaleString('nl-NL',{maximumSignificantDigits:2}):p.toLocaleString('nl-NL',{maximumFractionDigits:1});
      out.innerHTML='Nu bekijk je <mark>'+s+'%</mark> van de inzages.<small>Dat betekent dat '+Math.max(0,t-m).toLocaleString('nl-NL')+' inzages per maand niet worden bekeken. AccessGuard legt ze allemaal naast de zorgcontacten, en laat je alleen de signalen beoordelen.</small>';
    }
    a.addEventListener('input',upd);b.addEventListener('input',upd);upd();
  }
})();
