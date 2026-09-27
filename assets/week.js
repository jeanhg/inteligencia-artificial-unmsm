(() => {
  'use strict';
  const id=Number(document.body.dataset.week);
  const titles={informe:'Informe de investigación',presentacion:'Presentación',ejemplo:'Ejemplo o prototipo'};
  const descriptions={informe:'Documento académico en PDF o Word.',presentacion:'Diapositivas para la exposición.',ejemplo:'Código fuente, documentación o demostración práctica.'};
  const host=document.getElementById('resource-list');
  function addResource(name,item){
    const el=document.createElement('article');el.className='resource-card';
    const text=document.createElement('div');const title=document.createElement('strong');title.textContent=titles[name];
    const p=document.createElement('p');p.textContent=descriptions[name];text.append(title,p);el.append(text);
    if(item && item.url){const a=document.createElement('a');a.className='resource-link';a.textContent=item.label||'Abrir recurso ↗';a.href='../../'+item.url;if(/^https?:/.test(item.url))a.href=item.url;if(a.href.startsWith('http')&&new URL(a.href).origin!==window.location.origin){a.target='_blank';a.rel='noopener noreferrer';}el.append(a);}
    else{const span=document.createElement('span');span.className='resource-unavailable';span.textContent='Aún no publicado';el.append(span);}
    host.append(el);
  }
  fetch('../../data/semanas.json')
  .then(r=>{if(!r.ok)throw Error();return r.json();})
  .then(data=>{
    const w=data.find(x=>x.week===id);if(!w)throw Error();
    document.title='Semana '+id+' · '+w.title+' | Repositorio IA UNMSM';
    document.getElementById('week-tag').textContent='SEMANA '+String(id).padStart(2,'0');
    document.getElementById('week-title').textContent=w.title;
    document.getElementById('week-summary').textContent=w.summary;
    document.getElementById('week-area').textContent=w.area;
    const project=document.getElementById('week-project');if(w.project){project.textContent='Proyecto: '+w.project;project.hidden=false;}
    Object.entries(titles).forEach(([key])=>addResource(key,w.materials?.[key]||null));
    document.getElementById('github-week').href='https://github.com/jeanhg/inteligencia-artificial-unmsm/tree/main/semanas/semana-'+String(id).padStart(2,'0');
  })
  .catch(()=>{document.getElementById('week-title').textContent='No se pudo cargar esta semana';document.getElementById('week-summary').textContent='Puedes consultar los archivos disponibles en GitHub.';});
})();