const nav=document.getElementById('side-nav');
const sideTitle=document.querySelector('.side-title');
const heroTitle=document.querySelector('.hero h1');
const content=document.getElementById('content')||document.querySelector('.content');

if(nav&&heroTitle&&content){
  const buildOutline=()=>{
    if(sideTitle)sideTitle.textContent='このページ';
    const headings=[heroTitle,...content.querySelectorAll('h2,h3')];
    const headingById=new Map();
    const seen=new Set();
    const slug=text=>{
      const base=String(text||'').trim().toLowerCase().replace(/[`'"“”‘’]/g,'').replace(/[^a-z0-9\u3040-\u30ff\u3400-\u9fff]+/g,'-').replace(/^-+|-+$/g,'')||'section';
      let value=base,n=2;
      while(seen.has(value)||(document.getElementById(value)&&!headings.some(h=>h.id===value)))value=`${base}-${n++}`;
      return value;
    };
    headings.forEach((heading,index)=>{
      if(heading.id&&!seen.has(heading.id)){seen.add(heading.id);headingById.set(heading.id,heading);return;}
      heading.id=index===0?'article-top':slug(heading.textContent);
      seen.add(heading.id);
      headingById.set(heading.id,heading);
    });
    const toc=document.querySelector('#toc ul');
    if(toc){
      const fragment=document.createDocumentFragment();
      for(const heading of headings.filter(h=>h.tagName==='H2')){
        const li=document.createElement('li'),a=document.createElement('a');
        a.href=`#${heading.id}`;a.textContent=heading.textContent.trim();li.appendChild(a);fragment.appendChild(li);
      }
      toc.replaceChildren(fragment);
    }
    const makeList=()=>{const ul=document.createElement('ul');ul.className='outline-children';return ul;};
    const makeItem=(heading,level)=>{const li=document.createElement('li');li.className=`outline-item outline-item-${level}`;li.dataset.headingId=heading.id;li.dataset.level=String(level);const a=document.createElement('a');a.className=`outline-link outline-level-${level}`;a.href=`#${heading.id}`;a.textContent=heading.textContent.trim();li.appendChild(a);return li;};
    const root=document.createElement('ul');root.className='outline-root';
    const h1Item=makeItem(heroTitle,1),h1Children=makeList();h1Item.appendChild(h1Children);root.appendChild(h1Item);
    let currentH2=null;
    for(const heading of headings.slice(1)){
      const level=Number(heading.tagName.slice(1)),item=makeItem(heading,level);
      if(level===2){const children=makeList();item.appendChild(children);h1Children.appendChild(item);currentH2=item;}
      else{const parent=currentH2?currentH2.querySelector(':scope > .outline-children'):h1Children;parent.appendChild(item);}
    }
    const ns='http://www.w3.org/2000/svg';
    const rail=document.createElementNS(ns,'svg');rail.classList.add('outline-rail');rail.setAttribute('aria-hidden','true');
    const basePath=document.createElementNS(ns,'path');basePath.classList.add('outline-rail-base');
    const activePath=document.createElementNS(ns,'path');activePath.classList.add('outline-rail-active');rail.append(basePath,activePath);
    const live=document.createElement('span');live.className='outline-live';live.setAttribute('aria-hidden','true');
    const livePing=document.createElement('span');livePing.className='outline-live-ping';
    const liveDot=document.createElement('span');liveDot.className='outline-live-dot';
    live.append(livePing,liveDot);
    nav.replaceChildren(rail,root,live);
    nav.dataset.outlineOwner='article-outline-v2';
    const items=[...nav.querySelectorAll('.outline-item')],itemById=new Map(items.map(item=>[item.dataset.headingId,item]));
    let activeId=null,navigationTargetId=null,navigationTimer=0,raf=0;
    const xForLevel=level=>({1:20,2:32,3:46}[level]||20);
    const points=()=>{const nr=nav.getBoundingClientRect();return items.map(item=>{const link=item.querySelector(':scope > .outline-link'),lr=link.getBoundingClientRect();return{item,x:xForLevel(Number(item.dataset.level)),y:lr.top-nr.top+lr.height/2};});};
    const transitionParts=(p,n)=>{const gap=Math.max(1,n.y-p.y),dh=Math.max(14,Math.min(30,gap*.58)),mid=p.y+gap/2,start=Math.max(p.y,mid-dh/2),end=Math.min(n.y,mid+dh/2);return{start,end};};
    const pathFor=pts=>{if(!pts.length)return'';let d=`M ${pts[0].x} ${pts[0].y}`;for(let i=1;i<pts.length;i++){const p=pts[i-1],n=pts[i];if(p.x===n.x){d+=` V ${n.y}`;continue;}const{start,end}=transitionParts(p,n);d+=` V ${start} L ${n.x} ${end} V ${n.y}`;}return d;};
    const drawRail=()=>{
      const pts=points();if(!pts.length)return;
      const total=Math.max(nav.scrollHeight,pts[pts.length-1].y+14);
      rail.setAttribute('viewBox',`0 0 52 ${total}`);rail.style.height=`${total}px`;
      basePath.setAttribute('d',pathFor(pts));
      const found=pts.findIndex(p=>p.item.dataset.headingId===activeId),idx=found<0?0:found;
      activePath.setAttribute('d',pathFor(pts.slice(0,idx+1)));
      const activePoint=pts[idx]||pts[0];
      live.style.left=`${activePoint.x}px`;
      live.style.top=`${activePoint.y}px`;
      live.dataset.level=activePoint.item.dataset.level||'1';
    };
    const markActive=id=>{if(!id||id===activeId)return;activeId=id;items.forEach(i=>i.classList.remove('is-active','is-ancestor'));const active=itemById.get(id);if(!active)return;active.classList.add('is-active');let p=active.parentElement?.closest('.outline-item');while(p){p.classList.add('is-ancestor');p=p.parentElement?.closest('.outline-item');}drawRail();};
    const currentHeading=()=>{const threshold=window.innerWidth<=980?132:92;let current=headings[0];for(const h of headings){if(h.getBoundingClientRect().top<=threshold)current=h;else break;}if(window.innerHeight+window.scrollY>=document.documentElement.scrollHeight-4)current=headings[headings.length-1];return current;};
    const finishNavigation=()=>{if(!navigationTargetId)return;navigationTargetId=null;if(navigationTimer){clearTimeout(navigationTimer);navigationTimer=0;}markActive(currentHeading().id);drawRail();};
    const update=()=>{if(navigationTargetId){drawRail();return;}markActive(currentHeading().id);drawRail();};
    const schedule=()=>{if(raf)return;raf=requestAnimationFrame(()=>{raf=0;update();});};
    window.addEventListener('scroll',schedule,{passive:true});
    window.addEventListener('resize',schedule,{passive:true});
    window.addEventListener('hashchange',()=>{navigationTargetId=null;schedule();});
    if('onscrollend'in window)window.addEventListener('scrollend',finishNavigation,{passive:true});
    nav.addEventListener('click',event=>{
      const link=event.target.closest('.outline-link');if(!link)return;
      const id=decodeURIComponent(link.hash.slice(1)),heading=headingById.get(id);if(!heading)return;
      event.preventDefault();
      navigationTargetId=id;
      markActive(id);
      const hash=`#${encodeURIComponent(id)}`;
      if(window.location.hash!==hash)history.pushState(null,'',hash);
      heading.scrollIntoView({behavior:'smooth',block:'start'});
      if(navigationTimer)clearTimeout(navigationTimer);
      navigationTimer=window.setTimeout(finishNavigation,1200);
    });
    requestAnimationFrame(()=>{drawRail();markActive(currentHeading().id);});
  };

  buildOutline();
}
