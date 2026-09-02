from pathlib import Path

runtime = Path('src/scripts/article-runtime.js')
text = runtime.read_text(encoding='utf-8')
start = text.index('async function getMermaid()')
end = text.index('function sectionNodes', start)
replacement = r'''const mermaidKinds=[[/^(flowchart|graph)\b/i,'FLOWCHART'],[/^sequenceDiagram\b/i,'SEQUENCE'],[/^stateDiagram(?:-v2)?\b/i,'STATE'],[/^classDiagram\b/i,'CLASS'],[/^erDiagram\b/i,'ER'],[/^gantt\b/i,'GANTT'],[/^pie\b/i,'PIE'],[/^mindmap\b/i,'MINDMAP'],[/^timeline\b/i,'TIMELINE'],[/^journey\b/i,'JOURNEY'],[/^gitGraph\b/i,'GIT GRAPH'],[/^quadrantChart\b/i,'QUADRANT'],[/^xychart(?:-beta)?\b/i,'XY CHART'],[/^sankey(?:-beta)?\b/i,'SANKEY'],[/^block(?:-beta)?\b/i,'BLOCK'],[/^packet(?:-beta)?\b/i,'PACKET'],[/^architecture(?:-beta)?\b/i,'ARCHITECTURE'],[/^kanban\b/i,'KANBAN'],[/^requirementDiagram\b/i,'REQUIREMENT'],[/^C4\w*\b/i,'C4']];
function mermaidKind(source){const first=String(source||'').split('\n').map(line=>line.trim()).find(line=>line&&!line.startsWith('%%'))||'';return mermaidKinds.find(([pattern])=>pattern.test(first))?.[1]||'DIAGRAM'}
async function getMermaid(){if(mermaidApi)return mermaidApi;const mod=await import('https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs');mermaidApi=mod.default;mermaidApi.initialize({startOnLoad:false,securityLevel:'strict',theme:'base',flowchart:{curve:'linear',htmlLabels:true,useMaxWidth:true,nodeSpacing:44,rankSpacing:54},sequence:{useMaxWidth:true,wrap:true,diagramMarginX:18,diagramMarginY:18,actorMargin:60,messageMargin:40},themeVariables:{fontFamily:'Inter,-apple-system,BlinkMacSystemFont,"Segoe UI","Hiragino Sans","Yu Gothic",Meiryo,sans-serif',fontSize:'16px',background:'#f4fafb',primaryColor:'#fbfefe',primaryTextColor:'#1c343c',primaryBorderColor:'#85aab2',secondaryColor:'#eaf5f7',secondaryTextColor:'#1c343c',secondaryBorderColor:'#85aab2',tertiaryColor:'#dceff2',tertiaryTextColor:'#1c343c',tertiaryBorderColor:'#286b78',textColor:'#1c343c',lineColor:'#4d7b84',mainBkg:'#fbfefe',nodeBorder:'#85aab2',clusterBkg:'#f4fafb',clusterBorder:'#c9dade',titleColor:'#1c343c',edgeLabelBackground:'#f9fcfd',actorBkg:'#fbfefe',actorBorder:'#85aab2',actorTextColor:'#1c343c',actorLineColor:'#9bb9bf',signalColor:'#4d7b84',signalTextColor:'#1c343c',labelBoxBkgColor:'#eaf5f7',labelBoxBorderColor:'#85aab2',labelTextColor:'#1c343c',loopTextColor:'#1c343c',noteBkgColor:'#eaf5f7',noteBorderColor:'#85aab2',noteTextColor:'#1c343c',activationBkgColor:'#dceff2',activationBorderColor:'#286b78',classText:'#1c343c',taskBkgColor:'#5b9aa6',taskBorderColor:'#286b78',taskTextColor:'#173a42',activeTaskBkgColor:'#286b78',activeTaskBorderColor:'#174b56',activeTaskTextColor:'#ffffff',doneTaskBkgColor:'#85aab2',doneTaskBorderColor:'#5b9aa6',doneTaskTextColor:'#173a42',critBkgColor:'#a37b4e',critBorderColor:'#79572f',critTextColor:'#ffffff',todayLineColor:'#286b78',sectionBkgColor:'#f4fafb',altSectionBkgColor:'#eaf5f7',gridColor:'#c9dade',pie1:'#286b78',pie2:'#5d8f77',pie3:'#a37b4e',pie4:'#85aab2',pie5:'#8a6f9b',pie6:'#b36d6a',pie7:'#648a9a',pie8:'#a9a268',pieStrokeColor:'#f9fcfd',pieStrokeWidth:'3px',pieOpacity:'0.96',pieTitleTextSize:'18px',pieLegendTextColor:'#1c343c',pieLegendTextSize:'14px',pieSectionTextColor:'#ffffff',pieSectionTextSize:'13px'}});return mermaidApi}
function closeExpandedDiagram(){const box=document.querySelector('.mermaid-wrap.is-expanded');if(!box)return;box.classList.remove('is-expanded');box.querySelector('.mermaid-expand')?.setAttribute('aria-label','図を拡大');document.body.classList.remove('diagram-expanded')}
document.addEventListener('click',event=>{const button=event.target.closest('.mermaid-expand');if(!button)return;const box=button.closest('.mermaid-wrap');if(!box)return;const opening=!box.classList.contains('is-expanded');closeExpandedDiagram();if(opening){box.classList.add('is-expanded');button.setAttribute('aria-label','拡大表示を閉じる');document.body.classList.add('diagram-expanded')}});
document.addEventListener('keydown',event=>{if(event.key==='Escape')closeExpandedDiagram()});
async function renderMermaid(root){if(!root)return;const codes=[...root.querySelectorAll('code.language-mermaid')];for(const code of codes){const pre=code.closest('pre'),wrap=pre?.closest('.highlighter-rouge')||pre;if(!wrap)continue;const source=code.textContent||'',kind=mermaidKind(source),box=document.createElement('div'),head=document.createElement('div'),kicker=document.createElement('span'),type=document.createElement('span'),expand=document.createElement('button'),stage=document.createElement('div'),graph=document.createElement('div');box.className='mermaid-wrap mermaid-blueprint';box.dataset.diagramType=kind;head.className='mermaid-frame-head';kicker.className='mermaid-frame-kicker';kicker.textContent='BLUEPRINT';type.className='mermaid-frame-kind';type.textContent=kind;expand.className='mermaid-expand';expand.type='button';expand.setAttribute('aria-label','図を拡大');expand.textContent='⛶';stage.className='mermaid-stage';graph.className='mermaid';graph.textContent=source;head.append(kicker,type,expand);stage.appendChild(graph);box.append(head,stage);wrap.replaceWith(box)}const mermaid=await getMermaid();const nodes=[...root.querySelectorAll('.mermaid:not([data-processed])')];if(nodes.length)await mermaid.run({nodes});for(const box of root.querySelectorAll('.mermaid-wrap')){const svg=box.querySelector('svg');if(!svg)continue;svg.removeAttribute('height');svg.setAttribute('role','img');svg.setAttribute('aria-label',`${box.dataset.diagramType||'Diagram'} diagram`)}}
'''
runtime.write_text(text[:start] + replacement + text[end:], encoding='utf-8')

css = Path('assets/article-overrides.css')
ctext = css.read_text(encoding='utf-8')
marker = '/* Mermaid Blueprint viewer */'
if marker not in ctext:
    ctext += r'''

/* Mermaid Blueprint viewer */
body.diagram-expanded{overflow:hidden}
.mermaid-wrap.mermaid-blueprint{margin:16px 0 22px!important;padding:0!important;border:1px solid #c9dade!important;border-radius:16px!important;background:#f9fcfd!important;box-shadow:0 8px 22px rgba(32,72,82,.06);overflow:hidden!important}
.mermaid-frame-head{display:flex;align-items:center;gap:9px;min-height:46px;padding:7px 9px 7px 14px;border-bottom:1px solid #c9dade;background:rgba(249,252,253,.96)}
.mermaid-frame-kicker{color:#286b78;font-size:10px;font-weight:900;letter-spacing:.12em}
.mermaid-frame-kind{padding:4px 7px;border:1px solid #c9dade;border-radius:999px;background:#eaf5f7;color:#55707a;font-size:9px;font-weight:900;letter-spacing:.06em}
.mermaid-expand{margin-left:auto;width:32px;height:32px;border:1px solid #c9dade;border-radius:8px;background:#fbfefe;color:#286b78;font-size:15px;font-weight:800;cursor:pointer;transition:border-color .15s ease,background-color .15s ease,transform .15s ease}
.mermaid-expand:hover{border-color:#85aab2;background:#eaf5f7;transform:translateY(-1px)}
.mermaid-expand:focus-visible{outline:2px solid rgba(40,107,120,.32);outline-offset:2px}
.mermaid-stage{position:relative;min-height:220px;padding:22px;overflow:auto;background-color:#f4fafb;background-image:radial-gradient(circle,#c7dde1 1px,transparent 1.15px);background-size:18px 18px}
.mermaid-wrap .mermaid{display:flex;justify-content:center;min-width:0}
.mermaid-wrap .mermaid svg{display:block!important;width:auto!important;max-width:100%!important;height:auto!important;min-height:150px;font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI","Hiragino Sans","Yu Gothic",Meiryo,sans-serif!important}
.mermaid-wrap .mermaid svg text,.mermaid-wrap .mermaid svg .label,.mermaid-wrap .mermaid svg .nodeLabel,.mermaid-wrap .mermaid svg .edgeLabel,.mermaid-wrap .mermaid svg foreignObject{color:#1c343c!important;fill:#1c343c!important}
.mermaid-wrap .mermaid svg .node rect,.mermaid-wrap .mermaid svg .node circle,.mermaid-wrap .mermaid svg .node ellipse,.mermaid-wrap .mermaid svg .node polygon,.mermaid-wrap .mermaid svg .node path{fill:#fbfefe!important;stroke:#85aab2!important;stroke-width:1.4px!important}
.mermaid-wrap .mermaid svg .cluster rect,.mermaid-wrap .mermaid svg .cluster polygon{fill:#f4fafb!important;stroke:#c9dade!important;stroke-width:1.2px!important;stroke-dasharray:5 5}
.mermaid-wrap .mermaid svg .flowchart-link,.mermaid-wrap .mermaid svg .edgePath .path,.mermaid-wrap .mermaid svg .relation,.mermaid-wrap .mermaid svg .relationshipLine{stroke:#4d7b84!important;stroke-width:1.8px!important}
.mermaid-wrap .mermaid svg marker path,.mermaid-wrap .mermaid svg .marker{fill:#4d7b84!important;stroke:#4d7b84!important}
.mermaid-wrap .mermaid svg .edgeLabel rect,.mermaid-wrap .mermaid svg .labelBkg{fill:#f9fcfd!important;opacity:.96!important;stroke:#c9dade!important}
.mermaid-wrap .mermaid svg .actor,.mermaid-wrap .mermaid svg .actor-top,.mermaid-wrap .mermaid svg .actor-bottom{fill:#fbfefe!important;stroke:#85aab2!important;stroke-width:1.4px!important}
.mermaid-wrap .mermaid svg .actor-line,.mermaid-wrap .mermaid svg .messageLine0,.mermaid-wrap .mermaid svg .messageLine1,.mermaid-wrap .mermaid svg .loopLine{stroke:#4d7b84!important}
.mermaid-wrap .mermaid svg .note{fill:#eaf5f7!important;stroke:#85aab2!important}
.mermaid-wrap .mermaid svg .activation0,.mermaid-wrap .mermaid svg .activation1,.mermaid-wrap .mermaid svg .activation2{fill:#dceff2!important;stroke:#286b78!important}
.mermaid-wrap .mermaid svg .classGroup rect,.mermaid-wrap .mermaid svg .entityBox{fill:#fbfefe!important;stroke:#85aab2!important}
.mermaid-wrap .mermaid svg .attributeBoxEven,.mermaid-wrap .mermaid svg .attributeBoxOdd{fill:#f4fafb!important;stroke:#c9dade!important}
.mermaid-wrap .mermaid svg .pieTitleText,.mermaid-wrap .mermaid svg .legend text{fill:#1c343c!important}
.mermaid-wrap .mermaid svg .pieCircle{stroke:#f9fcfd!important;stroke-width:3px!important}
.mermaid-wrap.is-expanded{position:fixed!important;z-index:500;inset:18px;margin:0!important;display:flex;flex-direction:column;border-radius:18px!important;box-shadow:0 28px 90px rgba(21,45,52,.28)}
.mermaid-wrap.is-expanded .mermaid-frame-head{flex:0 0 auto}
.mermaid-wrap.is-expanded .mermaid-stage{flex:1;display:flex;align-items:center;justify-content:center;min-height:0;padding:28px}
.mermaid-wrap.is-expanded .mermaid{width:100%;height:100%;align-items:center}
.mermaid-wrap.is-expanded .mermaid svg{max-width:100%!important;max-height:100%!important}
@media(max-width:980px){.mermaid-wrap.mermaid-blueprint{margin:13px 0 19px!important;border-radius:13px!important}.mermaid-frame-head{min-height:44px;padding-left:11px}.mermaid-stage{min-height:190px;padding:14px;background-size:16px 16px}.mermaid-wrap .mermaid svg{min-height:120px}.mermaid-wrap.is-expanded{inset:8px}.mermaid-wrap.is-expanded .mermaid-stage{padding:14px}}
@media(prefers-reduced-motion:reduce){.mermaid-expand{transition:none}}
'''
css.write_text(ctext, encoding='utf-8')
