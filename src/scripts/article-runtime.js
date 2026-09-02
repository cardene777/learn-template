const content=document.getElementById('content');const side=document.getElementById('side');const menuBtn=document.getElementById('menu-btn');const sideClose=document.getElementById('side-close');const backdrop=document.getElementById('side-backdrop');function setMenu(open){side.classList.toggle('open',open);backdrop.classList.toggle('open',open);document.body.classList.toggle('nav-open',open)}menuBtn?.addEventListener('click',()=>setMenu(!side.classList.contains('open')));sideClose?.addEventListener('click',()=>setMenu(false));backdrop?.addEventListener('click',()=>setMenu(false));
const headings=[...content.querySelectorAll('h2')];
const escapeHtml=v=>String(v??'').replace(/[&<>"']/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));const articlePath=JSON.parse(document.getElementById('article-meta-json')?.textContent||'{}').path||'';let marked=null;let currentPatch='';let mermaidApi=null;const updatesEl=document.getElementById('article-updates-json');const updates=updatesEl?JSON.parse(updatesEl.textContent):[];const modalBackdrop=document.getElementById('revision-modal-backdrop');const modalBody=document.getElementById('revision-modal-body');
const mermaidKinds=[
  [/^(flowchart|graph)\b/i,'FLOWCHART'],[/^swimlane-beta\b/i,'SWIMLANE'],[/^sequenceDiagram\b/i,'SEQUENCE'],[/^classDiagram\b/i,'CLASS'],[/^stateDiagram(?:-v2)?\b/i,'STATE'],[/^erDiagram\b/i,'ER'],[/^journey\b/i,'JOURNEY'],[/^gantt\b/i,'GANTT'],[/^pie\b/i,'PIE'],[/^quadrantChart\b/i,'QUADRANT'],[/^requirementDiagram\b/i,'REQUIREMENT'],[/^gitGraph\b/i,'GIT GRAPH'],[/^C4\w*\b/i,'C4'],[/^mindmap\b/i,'MINDMAP'],[/^timeline\b/i,'TIMELINE'],[/^zenuml\b/i,'ZENUML'],[/^sankey(?:-beta)?\b/i,'SANKEY'],[/^xychart(?:-beta)?\b/i,'XY CHART'],[/^block(?:-beta)?\b/i,'BLOCK'],[/^packet(?:-beta)?\b/i,'PACKET'],[/^kanban\b/i,'KANBAN'],[/^architecture(?:-beta)?\b/i,'ARCHITECTURE'],[/^radar(?:-beta)?\b/i,'RADAR'],[/^eventmodeling\b/i,'EVENT MODELING'],[/^treemap(?:-beta)?\b/i,'TREEMAP'],[/^venn(?:-beta)?\b/i,'VENN'],[/^ishikawa(?:-beta)?\b/i,'ISHIKAWA'],[/^wardley(?:-beta)?\b/i,'WARDLEY'],[/^cynefin(?:-beta)?\b/i,'CYNEFIN'],[/^treeView(?:-beta)?\b/i,'TREEVIEW']
];
function mermaidKind(source){const first=String(source||'').split('\n').map(line=>line.trim()).find(line=>line&&!line.startsWith('%%')&&!line.startsWith('---'))||'';return mermaidKinds.find(([pattern])=>pattern.test(first))?.[1]||'DIAGRAM'}
const mermaidPalette=['#286b78','#65806e','#a27b54','#7a678f','#b36d6a','#648a9a','#a9a268','#85aab2'];
async function getMermaid(){
  if(mermaidApi)return mermaidApi;
  const mod=await import('https://cdn.jsdelivr.net/npm/mermaid@11.17.2/dist/mermaid.esm.min.mjs');
  mermaidApi=mod.default;
  try{
    const zenuml=await import('https://cdn.jsdelivr.net/npm/@mermaid-js/mermaid-zenuml@0.1.0/dist/mermaid-zenuml.esm.min.mjs');
    await mermaidApi.registerExternalDiagrams([zenuml.default]);
  }catch(error){console.warn('ZenUML plugin could not be registered',error)}
  mermaidApi.initialize({
    startOnLoad:false,securityLevel:'strict',theme:'base',
    flowchart:{curve:'basis',htmlLabels:true,useMaxWidth:false,nodeSpacing:56,rankSpacing:64,padding:20},
    sequence:{useMaxWidth:true,wrap:true,diagramMarginX:24,diagramMarginY:20,actorMargin:70,messageMargin:42},
    architecture:{seed:1,randomize:false},cynefin:{seed:1},
    themeVariables:{
      fontFamily:'Inter,-apple-system,BlinkMacSystemFont,"Segoe UI","Hiragino Sans","Yu Gothic",Meiryo,sans-serif',fontSize:'15px',background:'#f4fafb',
      primaryColor:'#fbfefe',primaryTextColor:'#1c343c',primaryBorderColor:'#8fb3ba',secondaryColor:'#eef7f8',secondaryTextColor:'#1c343c',secondaryBorderColor:'#8fb3ba',tertiaryColor:'#dceff2',tertiaryTextColor:'#1c343c',tertiaryBorderColor:'#286b78',
      textColor:'#1c343c',lineColor:'#587c84',mainBkg:'#fbfefe',nodeBorder:'#8fb3ba',clusterBkg:'#f4fafb',clusterBorder:'#c8dade',titleColor:'#1c343c',edgeLabelBackground:'#f9fcfd',
      actorBkg:'#fbfefe',actorBorder:'#8fb3ba',actorTextColor:'#1c343c',actorLineColor:'#adc3c7',signalColor:'#587c84',signalTextColor:'#1c343c',labelBoxBkgColor:'#eef7f8',labelBoxBorderColor:'#c8dade',labelTextColor:'#1c343c',loopTextColor:'#1c343c',noteBkgColor:'#eef7f8',noteBorderColor:'#8fb3ba',noteTextColor:'#1c343c',activationBkgColor:'#dceff2',activationBorderColor:'#286b78',
      classText:'#1c343c',taskBkgColor:'#286b78',taskBorderColor:'#286b78',taskTextColor:'#ffffff',activeTaskBkgColor:'#65806e',activeTaskBorderColor:'#52705c',activeTaskTextColor:'#ffffff',doneTaskBkgColor:'#85aab2',doneTaskBorderColor:'#648a9a',doneTaskTextColor:'#173a42',critBkgColor:'#a27b54',critBorderColor:'#79572f',critTextColor:'#ffffff',todayLineColor:'#286b78',sectionBkgColor:'#f4fafb',altSectionBkgColor:'#eef7f8',gridColor:'#c8dade',
      pie1:mermaidPalette[0],pie2:mermaidPalette[1],pie3:mermaidPalette[2],pie4:mermaidPalette[3],pie5:mermaidPalette[4],pie6:mermaidPalette[5],pie7:mermaidPalette[6],pie8:mermaidPalette[7],pieStrokeColor:'#f9fcfd',pieStrokeWidth:'3px',pieOpacity:'0.96',pieTitleTextSize:'18px',pieLegendTextColor:'#1c343c',pieLegendTextSize:'14px',pieSectionTextColor:'#ffffff',pieSectionTextSize:'13px',
      cScale0:mermaidPalette[0],cScale1:mermaidPalette[1],cScale2:mermaidPalette[2],cScale3:mermaidPalette[3],cScale4:mermaidPalette[4],cScale5:mermaidPalette[5],cScale6:mermaidPalette[6],cScale7:mermaidPalette[7],
      radar:{axisColor:'#8fb3ba',graticuleColor:'#c8dade',curveOpacity:0.20,curveStrokeWidth:2,graticuleOpacity:0.7},
      treeView:{labelColor:'#1c343c',lineColor:'#8fb3ba',descriptionColor:'#60767d',highlightBg:'rgba(40,107,120,.10)',highlightStroke:'#286b78'}
    }
  });
  return mermaidApi;
}
let mermaidBlueprintSerial=0;
const svgNS='http://www.w3.org/2000/svg';
const mermaidProfiles={
  FLOWCHART:{radius:16},SWIMLANE:{radius:16,badge:'STEP'},SEQUENCE:{radius:13,badge:'PARTICIPANT'},CLASS:{radius:16,badge:'CLASS'},STATE:{radius:16,badge:'STATE'},ER:{radius:16,badge:'ENTITY'},JOURNEY:{radius:12},GANTT:{radius:12},PIE:{radius:0},QUADRANT:{radius:12},REQUIREMENT:{radius:16,badge:'REQUIREMENT'},'GIT GRAPH':{radius:10},C4:{radius:16,badge:'CONTAINER'},MINDMAP:{radius:16,badge:'TOPIC'},TIMELINE:{radius:14,badge:'EVENT'},ZENUML:{radius:13,badge:'PARTICIPANT'},SANKEY:{radius:8},'XY CHART':{radius:8},BLOCK:{radius:16,badge:'BLOCK'},PACKET:{radius:9},KANBAN:{radius:16,badge:'CARD'},ARCHITECTURE:{radius:16,badge:'SERVICE'},RADAR:{radius:0},'EVENT MODELING':{radius:14,badge:'EVENT'},TREEMAP:{radius:10},VENN:{radius:0},ISHIKAWA:{radius:10},WARDLEY:{radius:10},CYNEFIN:{radius:12},TREEVIEW:{radius:10},DIAGRAM:{radius:14}
};
const mermaidBlueprintCss=`
svg.mermaid-svg-blueprint{overflow:visible;background:transparent}
svg.mermaid-svg-blueprint text,svg.mermaid-svg-blueprint tspan,svg.mermaid-svg-blueprint .label,svg.mermaid-svg-blueprint .nodeLabel,svg.mermaid-svg-blueprint .edgeLabel,svg.mermaid-svg-blueprint .messageText,svg.mermaid-svg-blueprint .loopText,svg.mermaid-svg-blueprint .noteText,svg.mermaid-svg-blueprint .classTitle,svg.mermaid-svg-blueprint .entityLabel{font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI","Hiragino Sans","Yu Gothic",Meiryo,sans-serif!important;fill:#1c343c!important;color:#1c343c!important;font-weight:650}
svg.mermaid-svg-blueprint .node rect,svg.mermaid-svg-blueprint rect.actor,svg.mermaid-svg-blueprint rect.actor-top,svg.mermaid-svg-blueprint rect.actor-bottom,svg.mermaid-svg-blueprint rect.note,svg.mermaid-svg-blueprint .classGroup rect,svg.mermaid-svg-blueprint rect.entityBox,svg.mermaid-svg-blueprint .statediagram-state rect,svg.mermaid-svg-blueprint .stateGroup rect,svg.mermaid-svg-blueprint .mindmap-node rect,svg.mermaid-svg-blueprint .timeline-node rect,svg.mermaid-svg-blueprint .kanban-item rect,svg.mermaid-svg-blueprint .block rect{fill:#fbfefe!important;stroke:#8fb3ba!important;stroke-width:1.4px!important}
svg.mermaid-svg-blueprint .node polygon,svg.mermaid-svg-blueprint .node circle,svg.mermaid-svg-blueprint .node ellipse,svg.mermaid-svg-blueprint .node path,svg.mermaid-svg-blueprint .statediagram-state circle,svg.mermaid-svg-blueprint .state-start,svg.mermaid-svg-blueprint .state-end{stroke:#8fb3ba!important;stroke-width:1.4px!important}
svg.mermaid-svg-blueprint .cluster rect,svg.mermaid-svg-blueprint .cluster polygon,svg.mermaid-svg-blueprint .cluster path{fill:#f4fafb!important;stroke:#b8d1d6!important;stroke-width:1.15px!important;stroke-dasharray:6 5}
svg.mermaid-svg-blueprint .flowchart-link,svg.mermaid-svg-blueprint .edgePath .path,svg.mermaid-svg-blueprint .relation,svg.mermaid-svg-blueprint .relationshipLine,svg.mermaid-svg-blueprint .actor-line,svg.mermaid-svg-blueprint .messageLine0,svg.mermaid-svg-blueprint .messageLine1,svg.mermaid-svg-blueprint .loopLine,svg.mermaid-svg-blueprint .transition,svg.mermaid-svg-blueprint .timeline-line{stroke:#587c84!important;stroke-width:1.9px!important;stroke-linecap:round;stroke-linejoin:round}
svg.mermaid-svg-blueprint marker path,svg.mermaid-svg-blueprint .marker{fill:#587c84!important;stroke:#587c84!important}
svg.mermaid-svg-blueprint .edgeLabel rect,svg.mermaid-svg-blueprint .labelBkg{fill:#f9fcfd!important;stroke:#c8dade!important;opacity:.98!important}
svg.mermaid-svg-blueprint rect.note{fill:#eef7f8!important;stroke:#8fb3ba!important}
svg.mermaid-svg-blueprint .activation0,svg.mermaid-svg-blueprint .activation1,svg.mermaid-svg-blueprint .activation2{fill:#dceff2!important;stroke:#286b78!important}
svg.mermaid-svg-blueprint .attributeBoxEven,svg.mermaid-svg-blueprint .attributeBoxOdd{fill:#f4fafb!important;stroke:#c8dade!important}
svg.mermaid-svg-blueprint .task{stroke-width:1.2px!important}
svg.mermaid-svg-blueprint .section0,svg.mermaid-svg-blueprint .section2{fill:#eef7f8!important}
svg.mermaid-svg-blueprint .section1,svg.mermaid-svg-blueprint .section3{fill:#f4fafb!important}
svg.mermaid-svg-blueprint .grid .tick line,svg.mermaid-svg-blueprint .tick line{stroke:#c8dade!important}
svg.mermaid-svg-blueprint .learn-bp-badge-bg{fill:#edf6f7!important;stroke:#c5dcdf!important;stroke-width:1!important}
svg.mermaid-svg-blueprint .learn-bp-badge-dot{fill:#286b78!important}
svg.mermaid-svg-blueprint .learn-bp-badge-text{font:800 7.5px Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif!important;letter-spacing:.08em!important;fill:#60767d!important;pointer-events:none}
svg.mermaid-svg-blueprint .learn-bp-pie-hole{fill:#f4fafb!important;stroke:#f9fcfd!important;stroke-width:2.5px!important}
svg.mermaid-svg-blueprint .learn-bp-pie-total{font:900 16px Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif!important;fill:#1c343c!important}
svg.mermaid-svg-blueprint .learn-bp-pie-caption{font:800 7px Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif!important;letter-spacing:.08em!important;fill:#60767d!important}
svg.mermaid-svg-blueprint foreignObject>div{color:#1c343c!important;line-height:1.35}
`;
function svgEl(name,attrs={}){const el=document.createElementNS(svgNS,name);for(const [key,value] of Object.entries(attrs))el.setAttribute(key,String(value));return el}
function numberAttr(el,name,fallback=0){const value=parseFloat(el?.getAttribute(name)||'');return Number.isFinite(value)?value:fallback}
function isBackgroundRect(rect){const cls=`${rect.getAttribute('class')||''} ${rect.parentElement?.getAttribute('class')||''}`;const width=numberAttr(rect,'width'),height=numberAttr(rect,'height');return /background|grid|plot/i.test(cls)&&(width>300||height>220)}
function largestRect(group){const rects=[...group.querySelectorAll(':scope > rect,rect')].filter(rect=>!rect.closest('defs')&&!isBackgroundRect(rect));return rects.sort((a,b)=>numberAttr(b,'width')*numberAttr(b,'height')-numberAttr(a,'width')*numberAttr(a,'height'))[0]||null}
function addBadge(group,rect,label){if(!group||!rect||group.querySelector(':scope > .learn-bp-badge'))return;const x=numberAttr(rect,'x'),y=numberAttr(rect,'y'),width=numberAttr(rect,'width');if(width<54)return;const badgeWidth=Math.max(38,Math.min(78,label.length*5.2+18));const g=svgEl('g',{class:'learn-bp-badge','aria-hidden':'true'});const bg=svgEl('rect',{class:'learn-bp-badge-bg',x:x+10,y:y-7,width:badgeWidth,height:16,rx:8,ry:8});const dot=svgEl('circle',{class:'learn-bp-badge-dot',cx:x+18,cy:y+1,r:2.6});const text=svgEl('text',{class:'learn-bp-badge-text',x:x+25,y:y+4});text.textContent=label;g.append(bg,dot,text);group.appendChild(g)}
function addShadow(svg){const id=`learn-mermaid-shadow-${++mermaidBlueprintSerial}`;let defs=svg.querySelector(':scope > defs');if(!defs){defs=svgEl('defs');svg.insertBefore(defs,svg.firstChild)}const filter=svgEl('filter',{id,x:'-20%',y:'-20%',width:'140%',height:'150%'});const shadow=svgEl('feDropShadow',{dx:0,dy:3,stdDeviation:3,'flood-color':'#204852','flood-opacity':'.09'});filter.appendChild(shadow);defs.appendChild(filter);return id}
function applyRadius(svg,radius){if(!radius)return;for(const rect of svg.querySelectorAll('rect')){if(rect.closest('defs')||isBackgroundRect(rect))continue;const cls=`${rect.getAttribute('class')||''} ${rect.parentElement?.getAttribute('class')||''}`;const r=/edgeLabel|labelBkg/i.test(cls)?8:radius;rect.setAttribute('rx',String(r));rect.setAttribute('ry',String(r))}}
function applyNodeBadges(svg,kind,badge){if(!badge)return;let groups=[];if(kind==='SEQUENCE'||kind==='ZENUML'){for(const rect of svg.querySelectorAll('rect.actor,rect.actor-top,rect.actor-bottom'))addBadge(rect.parentElement||svg,rect,badge);return}
  if(kind==='ER'){for(const rect of svg.querySelectorAll('rect.entityBox'))addBadge(rect.parentElement||svg,rect,badge);return}
  if(kind==='CLASS'){groups=[...svg.querySelectorAll('g.node,g.classGroup')]}else if(kind==='STATE'){groups=[...svg.querySelectorAll('g.node,g.statediagram-state,g.stateGroup')]}else if(kind==='MINDMAP'){groups=[...svg.querySelectorAll('g.mindmap-node,g.node')]}else if(kind==='TIMELINE'){groups=[...svg.querySelectorAll('g.timeline-node,g.node')]}else if(kind==='KANBAN'){groups=[...svg.querySelectorAll('g.kanban-item,g.node')]}else if(kind==='ARCHITECTURE'){groups=[...svg.querySelectorAll('g.service,g.node')]}else groups=[...svg.querySelectorAll('g.node')];
  for(const group of groups){const rect=largestRect(group);if(rect)addBadge(group,rect,badge)}
}
function decoratePie(svg){const slices=[...svg.querySelectorAll('.pieCircle')];if(!slices.length)return;slices.forEach((slice,index)=>{slice.style.setProperty('fill',mermaidPalette[index%mermaidPalette.length],'important');slice.style.setProperty('stroke','#f9fcfd','important');slice.style.setProperty('stroke-width','3px','important')});let boxes=[];for(const slice of slices){try{boxes.push(slice.getBBox())}catch{}}if(!boxes.length)return;const minX=Math.min(...boxes.map(b=>b.x)),minY=Math.min(...boxes.map(b=>b.y)),maxX=Math.max(...boxes.map(b=>b.x+b.width)),maxY=Math.max(...boxes.map(b=>b.y+b.height));const cx=(minX+maxX)/2,cy=(minY+maxY)/2,r=Math.min(maxX-minX,maxY-minY)*.22;const parent=slices[0].parentElement||svg;if(parent.querySelector('.learn-bp-pie-hole'))return;const hole=svgEl('circle',{class:'learn-bp-pie-hole',cx,cy,r});const total=svgEl('text',{class:'learn-bp-pie-total',x:cx,y:cy-1,'text-anchor':'middle'});total.textContent='100%';const caption=svgEl('text',{class:'learn-bp-pie-caption',x:cx,y:cy+14,'text-anchor':'middle'});caption.textContent='TOTAL';parent.append(hole,total,caption)}
function decorateChartPalette(svg,kind){if(kind==='RADAR'){const polygons=[...svg.querySelectorAll('polygon,path')].filter(el=>!el.closest('defs'));polygons.forEach((el,index)=>{if(index<mermaidPalette.length){el.style.setProperty('stroke',mermaidPalette[index%mermaidPalette.length],'important')}})}
  if(kind==='VENN'){const shapes=[...svg.querySelectorAll('circle,path')].filter(el=>!el.closest('defs'));shapes.forEach((el,index)=>{el.style.setProperty('fill',mermaidPalette[index%4],'important');el.style.setProperty('fill-opacity','.18','important');el.style.setProperty('stroke',mermaidPalette[index%4],'important');el.style.setProperty('stroke-width','2px','important')})}
  if(kind==='TREEMAP'){[...svg.querySelectorAll('rect')].filter(r=>!isBackgroundRect(r)).forEach((rect,index)=>{rect.style.setProperty('fill',mermaidPalette[index%mermaidPalette.length],'important');rect.style.setProperty('fill-opacity',index<2?'.20':'.76','important');rect.style.setProperty('stroke','#f9fcfd','important');rect.style.setProperty('stroke-width','2px','important')})}
  if(kind==='SANKEY'){[...svg.querySelectorAll('rect')].forEach((rect,index)=>{rect.style.setProperty('fill',mermaidPalette[index%4],'important');rect.setAttribute('rx','8');rect.setAttribute('ry','8')});[...svg.querySelectorAll('path')].filter(p=>!p.closest('defs')).forEach(path=>path.style.setProperty('opacity','.38','important'))}
}
function addFlowAccent(svg){
  for(const group of svg.querySelectorAll('.node')){
    const rect=largestRect(group);
    if(!rect)continue;
    const width=numberAttr(rect,'width'),height=numberAttr(rect,'height'),x=numberAttr(rect,'x'),y=numberAttr(rect,'y');
    if(width<54||height<38||group.querySelector(':scope > .learn-bp-flow-accent'))continue;
    const accent=svgEl('rect',{class:'learn-bp-flow-accent',x:x+12,y:y+8,width:Math.min(30,Math.max(18,width-24)),height:3,rx:1.5,ry:1.5,'aria-hidden':'true'});
    group.appendChild(accent);
  }
}
async function reflowWideFlowchart(box,mermaid){
  if(!box||box.dataset.diagramType!=='FLOWCHART')return box?.querySelector('svg')||null;
  const source=String(box._learnMermaidSource||'');
  const match=source.match(/^(\s*(?:flowchart|graph)\s+)(LR|RL)\b/im);
  const svg=box.querySelector('svg'),stage=box.querySelector('.mermaid-stage');
  const viewBox=svg?.viewBox?.baseVal;
  if(!match||!svg||!stage||!viewBox?.width)return svg;
  const available=Math.max(320,stage.clientWidth-12);
  if(viewBox.width<=available*1.05)return svg;
  const verticalSource=source.replace(/^(\s*(?:flowchart|graph)\s+)(LR|RL)\b/im,'$1TB');
  const graph=box.querySelector('.mermaid');
  if(!graph)return svg;
  try{
    const id=`learn-mermaid-reflow-${++mermaidBlueprintSerial}`;
    const rendered=await mermaid.render(id,verticalSource);
    graph.innerHTML=rendered.svg;
    rendered.bindFunctions?.(graph);
    const next=graph.querySelector('svg');
    if(!next)return svg;
    box.dataset.layoutMode='reflow';
    box.dataset.originalDirection=match[2].toUpperCase();
    box.classList.remove('mermaid-readable-wide');
    next.classList.remove('mermaid-svg-readable-wide');
    next.style.removeProperty('--learn-mermaid-natural-width');
    return next;
  }catch(error){
    console.error('Mermaid adaptive flow reflow failed',error);
    return svg;
  }
}
function stabilizeMermaidLayout(box,svg,kind){
  if(box?.dataset.layoutMode==='reflow'){box.classList.remove('mermaid-readable-wide');svg?.classList.remove('mermaid-svg-readable-wide');svg?.style.removeProperty('--learn-mermaid-natural-width');return;}
  const stage=box?.querySelector('.mermaid-stage'),viewBox=svg?.viewBox?.baseVal;
  if(!stage||!viewBox||!viewBox.width||!viewBox.height)return;
  const ratio=viewBox.width/viewBox.height;
  const readableWide=kind==='FLOWCHART'&&ratio>=4;
  box.classList.toggle('mermaid-readable-wide',readableWide);
  svg.classList.toggle('mermaid-svg-readable-wide',readableWide);
  if(readableWide){
    svg.style.setProperty('--learn-mermaid-natural-width',`${Math.ceil(viewBox.width)}px`);
    box.dataset.layoutMode='scroll';
  }else{
    svg.style.removeProperty('--learn-mermaid-natural-width');
    delete box.dataset.layoutMode;
  }
}
function applyMermaidBlueprint(svg,kind){if(!svg||svg.dataset.learnBlueprint==='3')return;svg.dataset.learnBlueprint='3';const profile=mermaidProfiles[kind]||mermaidProfiles.DIAGRAM;const slug=String(kind||'diagram').toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');svg.classList.add('mermaid-svg-blueprint',`mermaid-svg-${slug||'diagram'}`);svg.setAttribute('preserveAspectRatio','xMidYMid meet');let defs=svg.querySelector(':scope > defs');if(!defs){defs=svgEl('defs');svg.insertBefore(defs,svg.firstChild)}const style=svgEl('style');style.textContent=mermaidBlueprintCss;defs.appendChild(style);const shadowId=addShadow(svg);applyRadius(svg,profile.radius);applyNodeBadges(svg,kind,profile.badge);if(kind==='FLOWCHART')addFlowAccent(svg);
  const shadowSelectors='.node rect,rect.actor,rect.note,.classGroup rect,rect.entityBox,.statediagram-state rect,.stateGroup rect,.mindmap-node rect,.timeline-node rect,.kanban-item rect,.block rect';for(const shape of svg.querySelectorAll(shadowSelectors)){if(!shape.closest('defs'))shape.setAttribute('filter',`url(#${shadowId})`)}
  if(kind==='FLOWCHART'||kind==='SWIMLANE'){for(const rect of svg.querySelectorAll('.node rect')){rect.setAttribute('rx','16');rect.setAttribute('ry','16')}}
  if(kind==='STATE'){for(const rect of svg.querySelectorAll('.node rect,.statediagram-state rect,.stateGroup rect')){rect.setAttribute('rx','16');rect.setAttribute('ry','16')}}
  if(kind==='CLASS'){for(const rect of svg.querySelectorAll('.node rect,.classGroup rect')){rect.setAttribute('rx','16');rect.setAttribute('ry','16')}}
  if(kind==='ER'){for(const rect of svg.querySelectorAll('rect.entityBox,.node rect')){rect.setAttribute('rx','16');rect.setAttribute('ry','16')}}
  if(kind==='SEQUENCE'||kind==='ZENUML'){for(const rect of svg.querySelectorAll('rect.actor,rect.note,rect[class*="activation"]')){rect.setAttribute('rx','13');rect.setAttribute('ry','13')}}
  if(kind==='GANTT'){for(const rect of svg.querySelectorAll('.task,rect.task,rect[class*="task"]')){rect.setAttribute('rx','12');rect.setAttribute('ry','12')}}
  if(kind==='PIE')decoratePie(svg);decorateChartPalette(svg,kind);
}
function closeExpandedDiagram(){const box=document.querySelector('.mermaid-wrap.is-expanded');if(!box)return;box.classList.remove('is-expanded');box.querySelector('.mermaid-expand')?.setAttribute('aria-label','図を拡大');document.body.classList.remove('diagram-expanded')}
document.addEventListener('click',event=>{const button=event.target.closest('.mermaid-expand');if(!button)return;const box=button.closest('.mermaid-wrap');if(!box)return;const opening=!box.classList.contains('is-expanded');closeExpandedDiagram();if(opening){box.classList.add('is-expanded');button.setAttribute('aria-label','拡大表示を閉じる');document.body.classList.add('diagram-expanded')}});
document.addEventListener('keydown',event=>{if(event.key==='Escape')closeExpandedDiagram()});
async function renderMermaid(root){if(!root)return;const codes=[...root.querySelectorAll('code.language-mermaid')];for(const code of codes){const pre=code.closest('pre'),wrap=pre?.closest('.highlighter-rouge')||pre;if(!wrap)continue;const source=code.textContent||'',kind=mermaidKind(source),box=document.createElement('div'),head=document.createElement('div'),kicker=document.createElement('span'),type=document.createElement('span'),expand=document.createElement('button'),stage=document.createElement('div'),graph=document.createElement('div');box.className='mermaid-wrap mermaid-blueprint';box.dataset.diagramType=kind;box._learnMermaidSource=source;head.className='mermaid-frame-head';kicker.className='mermaid-frame-kicker';kicker.textContent='BLUEPRINT';type.className='mermaid-frame-kind';type.textContent=kind;expand.className='mermaid-expand';expand.type='button';expand.setAttribute('aria-label','図を拡大');expand.textContent='⛶';stage.className='mermaid-stage';graph.className='mermaid';graph.textContent=source;head.append(kicker,type,expand);stage.appendChild(graph);box.append(head,stage);wrap.replaceWith(box)}const mermaid=await getMermaid();for(const box of root.querySelectorAll('.mermaid-wrap')){const graph=box.querySelector('.mermaid:not([data-processed])');if(graph){try{await mermaid.run({nodes:[graph]})}catch(error){box.classList.add('mermaid-render-error');graph.textContent='Mermaid diagram could not be rendered.';console.error(`Mermaid ${box.dataset.diagramType||'DIAGRAM'} render failed`,error);continue}}let svg=box.querySelector('svg');if(!svg)continue;const kind=box.dataset.diagramType||'DIAGRAM';svg=await reflowWideFlowchart(box,mermaid)||svg;svg.removeAttribute('height');svg.setAttribute('role','img');svg.setAttribute('aria-label',`${kind||'Diagram'} diagram`);applyMermaidBlueprint(svg,kind);stabilizeMermaidLayout(box,svg,kind)}}
function sectionNodes(name){const h=headings.find(x=>x.textContent.trim()===name);if(!h)return[];const nodes=[h];let n=h.nextElementSibling;while(n&&n.tagName!=='H2'){nodes.push(n);n=n.nextElementSibling}return nodes}function closeModal(){modalBackdrop?.classList.remove('open');modalBackdrop?.setAttribute('aria-hidden','true');document.body.classList.remove('modal-open')}document.getElementById('revision-modal-close')?.addEventListener('click',closeModal);modalBackdrop?.addEventListener('click',e=>{if(e.target===modalBackdrop)closeModal()});document.addEventListener('keydown',e=>{if(e.key==='Escape'&&modalBackdrop?.classList.contains('open'))closeModal()});
async function getMarked(){if(marked)return marked;const mod=await import('https://cdn.jsdelivr.net/npm/marked@15/+esm');marked=mod.marked;return marked}async function fetchRevisionMarkdown(commit){const url=`https://raw.githubusercontent.com/__LEARN_REPOSITORY__/${commit}/${articlePath.split('/').map(encodeURIComponent).join('/')}`;const res=await fetch(url);if(!res.ok)throw new Error(`raw ${res.status}`);return await res.text()}async function fetchPatch(commit){const res=await fetch(`https://api.github.com/repos/__LEARN_REPOSITORY__/commits/${commit}`,{headers:{Accept:'application/vnd.github+json'}});if(!res.ok)throw new Error(`commit ${res.status}`);const data=await res.json();return(data.files||[]).find(f=>f.filename===articlePath)?.patch||''}function extractSectionMarkdown(md,heading){const lines=md.split('\n');const target=`## ${heading}`;const start=lines.findIndex(l=>l.trim()===target);if(start<0)return'';let end=lines.length;for(let i=start+1;i<lines.length;i++){if(/^##\s+/.test(lines[i])){end=i;break}}return lines.slice(start,end).join('\n').trim()}function extractSectionDiff(patch,heading){if(!patch)return'';const lines=patch.split('\n');const marker=`## ${heading}`;let start=lines.findIndex(l=>l.replace(/^[ +\-]/,'').trim()===marker);if(start<0)return'';while(start>0&&!lines[start].startsWith('@@'))start--;let end=lines.length;for(let i=start+1;i<lines.length;i++){const plain=lines[i].replace(/^[ +\-]/,'').trim();if(/^##\s+/.test(plain)&&plain!==marker){end=i;break}if(i>start+1&&lines[i].startsWith('@@')){end=i;break}}return lines.slice(start,end).join('\n')}function classifyChange(diff,heading){const lines=diff.split('\n');const added=lines.some(l=>l.startsWith('+')&&l.slice(1).trim()===`## ${heading}`);const removed=lines.some(l=>l.startsWith('-')&&l.slice(1).trim()===`## ${heading}`);return added&&!removed?'added':'changed'}function renderDiff(patch){if(!patch)return'<div class="diff-note">この項目のText差分を取得できませんでした。</div>';return patch.split('\n').map(line=>{let cls='';if(line.startsWith('+')&&!line.startsWith('+++'))cls='diff-add';else if(line.startsWith('-')&&!line.startsWith('---'))cls='diff-del';else if(line.startsWith('@@'))cls='diff-meta';return`<span class="diff-line ${cls}">${escapeHtml(line)}</span>`}).join('')}
async function openRevision(index){const update=updates[index];if(!update)return;modalBackdrop.classList.add('open');modalBackdrop.setAttribute('aria-hidden','false');document.body.classList.add('modal-open');document.getElementById('revision-modal-date').textContent=update.date||'';document.getElementById('revision-modal-title').textContent=update.title||'';document.getElementById('revision-modal-summary').textContent=update.summary||'';modalBody.innerHTML='<div class="modal-loading">変更内容を読み込んでいます…</div>';try{const[md,patch,parser]=await Promise.all([fetchRevisionMarkdown(update.commit),fetchPatch(update.commit),getMarked()]);currentPatch=patch;const parts=[];for(const change of update.changes||[]){const sectionMd=extractSectionMarkdown(md,change.heading);const itemDiff=extractSectionDiff(patch,change.heading);const kind=classifyChange(itemDiff,change.heading);parts.push(`<article class="modal-change" data-heading="${escapeHtml(change.heading)}"><div class="modal-change-head"><div><div class="modal-change-title">${escapeHtml(change.heading)} <span class="modal-kind ${kind}">${kind==='added'?'追加':'変更'}</span></div><div class="modal-change-label">${escapeHtml(change.label||'')}</div></div></div><div class="snapshot ${kind}">${sectionMd?parser.parse(sectionMd):'<p>この更新時点のセクションを取得できませんでした。</p>'}</div><div class="change-actions"><button class="change-jump" type="button">記事の該当箇所へ</button><button class="item-diff-toggle" type="button">この項目の差分を見る</button></div><div class="diff-box item-diff">${renderDiff(itemDiff)}</div></article>`)}parts.push(`<div class="modal-footer"><div class="modal-footer-row"><button class="full-diff-toggle" type="button">この更新の全差分を見る</button><a href="https://github.com/__LEARN_REPOSITORY__/commit/${encodeURIComponent(update.commit)}" target="_blank" rel="noopener">GitHubでCommitを見る</a></div><div class="diff-box full-diff">${renderDiff(patch)}</div></div>`);modalBody.innerHTML=parts.join('');await renderMermaid(modalBody)}catch(error){modalBody.innerHTML='<div class="modal-error">変更内容を取得できませんでした。GitHubのCommitから確認してください。</div>'}}
for(const row of document.querySelectorAll('.revision-row'))row.addEventListener('click',()=>openRevision(Number(row.dataset.revision)));modalBody?.addEventListener('click',e=>{const change=e.target.closest('.modal-change');if(e.target.closest('.change-jump')&&change){const nodes=sectionNodes(change.dataset.heading);closeModal();if(nodes.length){nodes[0].classList.add('change-focus');nodes[0].scrollIntoView({behavior:'smooth',block:'start'});setTimeout(()=>nodes[0].classList.remove('change-focus'),3200)}}const itemBtn=e.target.closest('.item-diff-toggle');if(itemBtn&&change){const box=change.querySelector('.item-diff');box.classList.toggle('open');itemBtn.textContent=box.classList.contains('open')?'差分を閉じる':'この項目の差分を見る'}const fullBtn=e.target.closest('.full-diff-toggle');if(fullBtn){const box=modalBody.querySelector('.full-diff');box.classList.toggle('open');fullBtn.textContent=box.classList.contains('open')?'全差分を閉じる':'この更新の全差分を見る'}});
const languageMeta={javascript:['JavaScript','#f1e05a'],js:['JavaScript','#f1e05a'],typescript:['TypeScript','#3178c6'],ts:['TypeScript','#3178c6'],jsx:['React / JSX','#61dafb'],tsx:['React / TSX','#61dafb'],solidity:['Solidity','#6f7fa8'],rust:['Rust','#dea584'],go:['Go','#00add8'],python:['Python','#3776ab'],json:['JSON','#d4a72c'],yaml:['YAML','#cb171e'],yml:['YAML','#cb171e'],bash:['Bash','#4eaa25'],sh:['Shell','#4eaa25'],html:['HTML','#e34c26'],css:['CSS','#563d7c'],sql:['SQL','#e38c00'],text:['Text','#8b949e']};function detectLanguage(pre){for(const node of[pre,pre.querySelector('code')].filter(Boolean))for(const cls of node.classList||[])if(cls.startsWith('language-'))return cls.slice(9).toLowerCase();return'text'}for(const pre of content.querySelectorAll('pre')){const lang=detectLanguage(pre);if(lang==='mermaid')continue;const meta=languageMeta[lang]||[lang,'#8b949e'],wrap=pre.closest('.highlighter-rouge')||pre;wrap.classList.add('code-block');wrap.dataset.language=meta[0];wrap.style.setProperty('--code-accent',meta[1])}await renderMermaid(content)
