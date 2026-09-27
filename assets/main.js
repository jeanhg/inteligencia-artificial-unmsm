(() => {
  'use strict';
  const grid = document.getElementById('week-grid');
  const search = document.getElementById('week-search');
  const filter = document.getElementById('area-filter');
  const count = document.getElementById('result-count');
  const error = document.getElementById('load-error');
  const materialCount = w => Object.values(w.materials || {}).filter(m => m && m.url).length;
  const pad = n => String(n).padStart(2,'0');
  let weeks = [];
  function buildCard(w) {
    const a = document.createElement('a');
    a.className = 'week-card' + (w.week === 1 ? ' week-featured' : '');
    a.href = 'semanas/semana-' + pad(w.week) + '/';
    a.setAttribute('aria-label','Ver semana ' + w.week + ': ' + w.title);
    const top = document.createElement('div');
    top.className='week-top';
    const number=document.createElement('span');
    number.className='week-number';number.textContent='SEMANA '+pad(w.week);
    const status=document.createElement('span');
    const items=materialCount(w);
    status.className='status' + (items ? ' status-ready':'');
    status.textContent=items ? items+' recurso'+(items===1?'':'s') : 'En preparación';
    top.append(number,status);
    const title=document.createElement('h3');title.textContent=w.title;
    const desc=document.createElement('p');desc.textContent=w.summary;
    a.append(top,title,desc);
    if(w.project){const tag=document.createElement('div');tag.className='week-project';tag.textContent='Proyecto: '+w.project;a.append(tag);}
    const meta=document.createElement('div');meta.className='week-meta';
    const area=document.createElement('span');area.className='area-pill';area.textContent=w.area;
    const arrow=document.createElement('span');arrow.className='week-arrow';arrow.setAttribute('aria-hidden','true');arrow.textContent='↗';
    meta.append(area,arrow);a.append(meta);return a;
  }
  function render() {
    const text=search.value.trim().toLocaleLowerCase('es');
    const area=filter.value;
    const visible=weeks.filter(w=>(!area||w.area===area) && (!text||[w.week,String(w.week).padStart(2,'0'),w.title,w.summary,w.project||''].join(' ').toLocaleLowerCase('es').includes(text)));
    grid.replaceChildren(...visible.map(buildCard));
    if(!visible.length){const p=document.createElement('p');p.className='empty-state';p.textContent='No encontramos semanas con esos criterios.';grid.append(p);}
    count.textContent=visible.length+' de '+weeks.length+' semanas';
  }
  fetch('data/semanas.json')
    .then(r=>{if(!r.ok)throw Error('No se pudo cargar el catálogo');return r.json();})
    .then(data=>{
      weeks=data;
      document.getElementById('stat-weeks').textContent=data.length;
      document.getElementById('stat-materials').textContent=data.reduce((n,w)=>n+materialCount(w),0);
      document.getElementById('stat-projects').textContent=data.filter(w=>w.project).length;
      [...new Set(data.map(w=>w.area))].forEach(area=>{const o=document.createElement('option');o.value=area;o.textContent=area;filter.append(o);});
      search.addEventListener('input',render);filter.addEventListener('change',render);render();
    })
    .catch(()=>{grid.replaceChildren();error.hidden=false;count.textContent='';});
})();