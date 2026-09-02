from pathlib import Path

runtime = Path('src/scripts/article-runtime.js')
text = runtime.read_text(encoding='utf-8')
start = text.index('function closeExpandedDiagram()')
end = text.index('function sectionNodes', start)
replacement = r'''let mermaidBlueprintSerial=0;
const mermaidBlueprintCss=`
svg.mermaid-svg-blueprint{overflow:visible;background:transparent}
svg.mermaid-svg-blueprint text,svg.mermaid-svg-blueprint tspan,svg.mermaid-svg-blueprint .label,svg.mermaid-svg-blueprint .nodeLabel,svg.mermaid-svg-blueprint .edgeLabel,svg.mermaid-svg-blueprint .messageText,svg.mermaid-svg-blueprint .loopText,svg.mermaid-svg-blueprint .noteText,svg.mermaid-svg-blueprint .classTitle,svg.mermaid-svg-blueprint .entityLabel{font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI","Hiragino Sans","Yu Gothic",Meiryo,sans-serif!important;fill:#1c343c!important;color:#1c343c!important;font-weight:650}
svg.mermaid-svg-blueprint .node rect,svg.mermaid-svg-blueprint rect.actor,svg.mermaid-svg-blueprint rect.actor-top,svg.mermaid-svg-blueprint rect.actor-bottom,svg.mermaid-svg-blueprint rect.note,svg.mermaid-svg-blueprint .classGroup rect,svg.mermaid-svg-blueprint rect.entityBox,svg.mermaid-svg-blueprint .statediagram-state rect,svg.mermaid-svg-blueprint .stateGroup rect,svg.mermaid-svg-blueprint .mindmap-node rect,svg.mermaid-svg-blueprint .timeline-node rect,svg.mermaid-svg-blueprint .kanban-item rect,svg.mermaid-svg-blueprint .block rect{fill:#fbfefe!important;stroke:#85aab2!important;stroke-width:1.5px!important}
svg.mermaid-svg-blueprint .node polygon,svg.mermaid-svg-blueprint .node circle,svg.mermaid-svg-blueprint .node ellipse,svg.mermaid-svg-blueprint .node path,svg.mermaid-svg-blueprint .statediagram-state circle,svg.mermaid-svg-blueprint .state-start,svg.mermaid-svg-blueprint .state-end{stroke:#85aab2!important;stroke-width:1.5px!important}
svg.mermaid-svg-blueprint .cluster rect,svg.mermaid-svg-blueprint .cluster polygon,svg.mermaid-svg-blueprint .cluster path{fill:#f4fafb!important;stroke:#b8d1d6!important;stroke-width:1.2px!important;stroke-dasharray:6 5}
svg.mermaid-svg-blueprint .flowchart-link,svg.mermaid-svg-blueprint .edgePath .path,svg.mermaid-svg-blueprint .relation,svg.mermaid-svg-blueprint .relationshipLine,svg.mermaid-svg-blueprint .actor-line,svg.mermaid-svg-blueprint .messageLine0,svg.mermaid-svg-blueprint .messageLine1,svg.mermaid-svg-blueprint .loopLine,svg.mermaid-svg-blueprint .transition,svg.mermaid-svg-blueprint .timeline-line{stroke:#4d7b84!important;stroke-width:1.9px!important;stroke-linecap:round;stroke-linejoin:round}
svg.mermaid-svg-blueprint marker path,svg.mermaid-svg-blueprint .marker{fill:#4d7b84!important;stroke:#4d7b84!important}
svg.mermaid-svg-blueprint .edgeLabel rect,svg.mermaid-svg-blueprint .labelBkg{fill:#f9fcfd!important;stroke:#c9dade!important;opacity:.97!important}
svg.mermaid-svg-blueprint rect.note{fill:#eaf5f7!important;stroke:#85aab2!important}
svg.mermaid-svg-blueprint .activation0,svg.mermaid-svg-blueprint .activation1,svg.mermaid-svg-blueprint .activation2{fill:#dceff2!important;stroke:#286b78!important}
svg.mermaid-svg-blueprint .attributeBoxEven,svg.mermaid-svg-blueprint .attributeBoxOdd{fill:#f4fafb!important;stroke:#c9dade!important}
svg.mermaid-svg-blueprint .task{stroke:#286b78!important;stroke-width:1.2px!important}
svg.mermaid-svg-blueprint .section0,svg.mermaid-svg-blueprint .section2{fill:#eaf5f7!important}
svg.mermaid-svg-blueprint .section1,svg.mermaid-svg-blueprint .section3{fill:#f4fafb!important}
svg.mermaid-svg-blueprint .grid .tick line,svg.mermaid-svg-blueprint .tick line{stroke:#c9dade!important}
svg.mermaid-svg-blueprint .pieTitleText,svg.mermaid-svg-blueprint .legend text{fill:#1c343c!important}
svg.mermaid-svg-blueprint .pieCircle{stroke:#f9fcfd!important;stroke-width:3px!important}
svg.mermaid-svg-blueprint foreignObject>div{color:#1c343c!important;line-height:1.35}
`;
function applyMermaidBlueprint(svg,kind){
  if(!svg||svg.dataset.learnBlueprint==='1')return;
  svg.dataset.learnBlueprint='1';
  const slug=String(kind||'diagram').toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');
  svg.classList.add('mermaid-svg-blueprint',`mermaid-svg-${slug||'diagram'}`);
  svg.setAttribute('preserveAspectRatio','xMidYMid meet');
  const ns='http://www.w3.org/2000/svg';
  let defs=svg.querySelector(':scope > defs');
  if(!defs){defs=document.createElementNS(ns,'defs');svg.insertBefore(defs,svg.firstChild)}
  const style=document.createElementNS(ns,'style');style.textContent=mermaidBlueprintCss;defs.appendChild(style);
  const filterId=`learn-mermaid-shadow-${++mermaidBlueprintSerial}`;
  const filter=document.createElementNS(ns,'filter');filter.id=filterId;filter.setAttribute('x','-20%');filter.setAttribute('y','-20%');filter.setAttribute('width','140%');filter.setAttribute('height','150%');
  const shadow=document.createElementNS(ns,'feDropShadow');shadow.setAttribute('dx','0');shadow.setAttribute('dy','3');shadow.setAttribute('stdDeviation','3');shadow.setAttribute('flood-color','#204852');shadow.setAttribute('flood-opacity','.09');filter.appendChild(shadow);defs.appendChild(filter);
  const radius={FLOWCHART:14,CLASS:13,STATE:16,SEQUENCE:11,ER:13,GANTT:7,MINDMAP:16,TIMELINE:13,JOURNEY:11,'GIT GRAPH':9,QUADRANT:10,'XY CHART':9,SANKEY:9,BLOCK:13,PACKET:9,ARCHITECTURE:14,KANBAN:13,REQUIREMENT:13,C4:13,DIAGRAM:12}[kind]||12;
  for(const rect of svg.querySelectorAll('rect')){
    if(rect.closest('defs'))continue;
    const className=rect.getAttribute('class')||'';
    const parentClass=rect.parentElement?.getAttribute('class')||'';
    const labelRect=rect.closest('.edgeLabel')||className.includes('labelBkg');
    const background=/background|grid/i.test(`${className} ${parentClass}`)&&(Number(rect.getAttribute('x')||0)===0&&Number(rect.getAttribute('y')||0)===0);
    if(background)continue;
    const r=labelRect?8:radius;
    rect.setAttribute('rx',String(r));rect.setAttribute('ry',String(r));
  }
  const nodeShapes=svg.querySelectorAll('.node rect,.node polygon,.node circle,.node ellipse,.node path,rect.actor,rect.note,.classGroup rect,rect.entityBox,.statediagram-state rect,.stateGroup rect,.mindmap-node rect,.timeline-node rect,.kanban-item rect,.block rect');
  for(const shape of nodeShapes)shape.setAttribute('filter',`url(#${filterId})`);
  if(kind==='FLOWCHART')for(const rect of svg.querySelectorAll('.node rect')){rect.setAttribute('rx','14');rect.setAttribute('ry','14')}
  if(kind==='CLASS')for(const rect of svg.querySelectorAll('.node rect,.classGroup rect')){rect.setAttribute('rx','13');rect.setAttribute('ry','13')}
  if(kind==='STATE')for(const rect of svg.querySelectorAll('.node rect,.statediagram-state rect,.stateGroup rect')){rect.setAttribute('rx','16');rect.setAttribute('ry','16')}
  if(kind==='SEQUENCE')for(const rect of svg.querySelectorAll('rect.actor,rect.note,rect[class*="activation"]')){rect.setAttribute('rx','11');rect.setAttribute('ry','11')}
  if(kind==='ER')for(const rect of svg.querySelectorAll('rect.entityBox,.node rect')){rect.setAttribute('rx','13');rect.setAttribute('ry','13')}
  if(kind==='PIE'){
    const palette=['#286b78','#5d8f77','#a37b4e','#85aab2','#8a6f9b','#b36d6a','#648a9a','#a9a268'];
    [...svg.querySelectorAll('.pieCircle')].forEach((slice,index)=>{slice.style.setProperty('fill',palette[index%palette.length],'important');slice.style.setProperty('stroke','#f9fcfd','important');slice.style.setProperty('stroke-width','3px','important')});
  }
}
function closeExpandedDiagram(){const box=document.querySelector('.mermaid-wrap.is-expanded');if(!box)return;box.classList.remove('is-expanded');box.querySelector('.mermaid-expand')?.setAttribute('aria-label','図を拡大');document.body.classList.remove('diagram-expanded')}
document.addEventListener('click',event=>{const button=event.target.closest('.mermaid-expand');if(!button)return;const box=button.closest('.mermaid-wrap');if(!box)return;const opening=!box.classList.contains('is-expanded');closeExpandedDiagram();if(opening){box.classList.add('is-expanded');button.setAttribute('aria-label','拡大表示を閉じる');document.body.classList.add('diagram-expanded')}});
document.addEventListener('keydown',event=>{if(event.key==='Escape')closeExpandedDiagram()});
async function renderMermaid(root){if(!root)return;const codes=[...root.querySelectorAll('code.language-mermaid')];for(const code of codes){const pre=code.closest('pre'),wrap=pre?.closest('.highlighter-rouge')||pre;if(!wrap)continue;const source=code.textContent||'',kind=mermaidKind(source),box=document.createElement('div'),head=document.createElement('div'),kicker=document.createElement('span'),type=document.createElement('span'),expand=document.createElement('button'),stage=document.createElement('div'),graph=document.createElement('div');box.className='mermaid-wrap mermaid-blueprint';box.dataset.diagramType=kind;head.className='mermaid-frame-head';kicker.className='mermaid-frame-kicker';kicker.textContent='BLUEPRINT';type.className='mermaid-frame-kind';type.textContent=kind;expand.className='mermaid-expand';expand.type='button';expand.setAttribute('aria-label','図を拡大');expand.textContent='⛶';stage.className='mermaid-stage';graph.className='mermaid';graph.textContent=source;head.append(kicker,type,expand);stage.appendChild(graph);box.append(head,stage);wrap.replaceWith(box)}const mermaid=await getMermaid();const nodes=[...root.querySelectorAll('.mermaid:not([data-processed])')];if(nodes.length)await mermaid.run({nodes});for(const box of root.querySelectorAll('.mermaid-wrap')){const svg=box.querySelector('svg');if(!svg)continue;svg.removeAttribute('height');svg.setAttribute('role','img');svg.setAttribute('aria-label',`${box.dataset.diagramType||'Diagram'} diagram`);applyMermaidBlueprint(svg,box.dataset.diagramType||'DIAGRAM')}}
'''
runtime.write_text(text[:start] + replacement + text[end:], encoding='utf-8')

css = Path('assets/article-overrides.css')
ctext = css.read_text(encoding='utf-8')
marker = '/* Mermaid Blueprint renderer v2 */'
if marker not in ctext:
    ctext += r'''

/* Mermaid Blueprint renderer v2 */
.mermaid-wrap.mermaid-blueprint{border-color:#b8d1d6!important;border-radius:18px!important;box-shadow:0 10px 28px rgba(32,72,82,.075)!important}
.mermaid-frame-head{min-height:50px!important;padding:8px 10px 8px 16px!important;background:rgba(249,252,253,.98)!important}
.mermaid-frame-kicker{font-size:10px!important;letter-spacing:.14em!important}
.mermaid-frame-kind{padding:5px 8px!important;border-color:#b8d1d6!important;background:#e5f2f4!important;color:#466b73!important}
.mermaid-stage{min-height:250px!important;padding:28px!important;background-color:#f3f9fa!important;background-image:radial-gradient(circle,#bfd8dd 1.05px,transparent 1.2px)!important;background-size:18px 18px!important}
.mermaid-wrap .mermaid svg{min-height:180px!important;overflow:visible!important}
.mermaid-wrap .mermaid svg .node rect,.mermaid-wrap .mermaid svg rect.actor,.mermaid-wrap .mermaid svg rect.note,.mermaid-wrap .mermaid svg .classGroup rect,.mermaid-wrap .mermaid svg rect.entityBox,.mermaid-wrap .mermaid svg .statediagram-state rect,.mermaid-wrap .mermaid svg .stateGroup rect{transition:filter .16s ease,stroke-color .16s ease,fill .16s ease}
.mermaid-wrap .mermaid svg .node:hover rect,.mermaid-wrap .mermaid svg .classGroup:hover rect,.mermaid-wrap .mermaid svg .statediagram-state:hover rect,.mermaid-wrap .mermaid svg .stateGroup:hover rect{fill:#f2fbfc!important;stroke:#5b9aa6!important}
@media(max-width:980px){.mermaid-stage{min-height:210px!important;padding:18px!important;background-size:16px 16px!important}.mermaid-wrap .mermaid svg{min-height:140px!important}}
'''
css.write_text(ctext, encoding='utf-8')
