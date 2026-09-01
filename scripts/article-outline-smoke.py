#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import html,json,shutil,socket,subprocess,sys,time

ROOT=Path('_site'); PORT=8766
VIEWPORTS=[('desktop',1280,800),('mobile',390,844)]
PASSES=('cold','warm')

def chrome_path():
    for name in ('google-chrome','google-chrome-stable','chromium','chromium-browser'):
        path=shutil.which(name)
        if path:return path
    raise RuntimeError('Chrome/Chromium is required')

def wait_server():
    deadline=time.time()+10
    while time.time()<deadline:
        try:
            with socket.create_connection(('127.0.0.1',PORT),timeout=.25): return
        except OSError: time.sleep(.1)
    raise RuntimeError('Local server did not start')

def url_for(path:Path)->str:
    rel=path.relative_to(ROOT).as_posix()
    if rel=='index.html':return '/'
    if rel.endswith('/index.html'):return '/'+rel[:-len('index.html')]
    return '/'+rel

def article_urls():
    out=[]
    for path in sorted(ROOT.rglob('*.html')):
        text=path.read_text(encoding='utf-8',errors='replace')
        if 'class="content"' in text:out.append(url_for(path))
    if not out:raise RuntimeError('No article pages found')
    return out

def harness(paths):
    payload=json.dumps(paths,ensure_ascii=False)
    return '''<!doctype html><meta charset="utf-8"><pre id="result">RUNNING</pre><script>
const PATHS=__PATHS__,VPS=[['desktop',1280,800],['mobile',390,844]],PASSES=['cold','warm'],failures=[];
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const fail=(p,v,pass,m)=>failures.push(`${p} [${v[0]}/${pass}] ${m}`);
const visible=(el,w)=>{if(!el)return false;const s=w.getComputedStyle(el),r=el.getBoundingClientRect();return s.display!=='none'&&s.visibility!=='hidden'&&Number(s.opacity||1)>.05&&r.width>0&&r.height>0};
async function run(p,v,pass){const f=document.createElement('iframe');f.style.cssText=`position:absolute;left:-10000px;top:0;width:${v[1]}px;height:${v[2]}px;border:0`;document.body.appendChild(f);let loaded=true;await new Promise((res,rej)=>{const t=setTimeout(()=>rej(new Error('load timeout')),7000);f.onload=()=>{clearTimeout(t);res()};f.src=p}).catch(e=>{loaded=false;fail(p,v,pass,e.message)});if(!loaded){f.remove();return}await sleep(350);const d=f.contentDocument,w=f.contentWindow;if(!d||!w){fail(p,v,pass,'document unavailable');f.remove();return}const c=d.querySelector('.content'),n=d.querySelector('#side-nav'),s=d.querySelector('#side');if(!c||!n||!s){fail(p,v,pass,'outline anchors missing');f.remove();return}
const directLinks=[...n.querySelectorAll(':scope > a')];if(directLinks.length)fail(p,v,pass,`legacy flat sidebar writer won: ${directLinks.length} direct links`);
const h2=[...c.querySelectorAll('h2')],h3=[...c.querySelectorAll('h3')],n2=[...n.querySelectorAll('.outline-item-2')],n3=[...n.querySelectorAll('.outline-item-3')];if(n2.length!==h2.length)fail(p,v,pass,`H2 parity ${h2.length}/${n2.length}`);if(n3.length!==h3.length)fail(p,v,pass,`H3 parity ${h3.length}/${n3.length}`);const ht=h3.map(x=>x.textContent.trim()),nt=n3.map(x=>x.querySelector(':scope > .outline-link')?.textContent.trim()||'');if(JSON.stringify(ht)!==JSON.stringify(nt))fail(p,v,pass,'H3 order/text mismatch');for(const h of [...h2,...h3])if(!h.id)fail(p,v,pass,`heading id missing: ${h.textContent.trim()}`);
const rail=n.querySelector('.outline-rail:not(.outline-rail-active-cap-layer)'),base=n.querySelector('.outline-rail-base'),active=n.querySelector('.outline-rail-active'),capRail=n.querySelector('.outline-rail-active-cap-layer'),cap=n.querySelector('.outline-rail-active-cap');if(!rail||!base||!active||!capRail||!cap)fail(p,v,pass,'hierarchy rail or current-row elbow missing');else{const path=base.getAttribute('d')||'';if(!path)fail(p,v,pass,'hierarchy base path empty');if(h3.length&&!path.includes(' L '))fail(p,v,pass,'approved hierarchy rail lost its level transition');const rr=rail.getBoundingClientRect();if(rr.width<48||rr.width>56)fail(p,v,pass,`hierarchy rail width=${Math.round(rr.width)}`);if(v[0]==='desktop'&&!visible(rail,w))fail(p,v,pass,'hierarchy rail hidden on desktop');const rz=parseInt(w.getComputedStyle(n.querySelector('.outline-root')).zIndex||'0',10),cz=parseInt(w.getComputedStyle(capRail).zIndex||'0',10);if(!(cz>rz))fail(p,v,pass,`current-row elbow must render above highlight root=${rz} cap=${cz}`)}
if(n2.length&&n3.length){const l2=n2[0].querySelector(':scope > .outline-link')?.getBoundingClientRect(),l3=n3[0].querySelector(':scope > .outline-link')?.getBoundingClientRect();if(l2&&l3&&l3.left<l2.left+10)fail(p,v,pass,`H3 indentation collapsed: h2=${Math.round(l2.left)} h3=${Math.round(l3.left)}`)}
const initialItems=[...n.querySelectorAll('.outline-item')],initialTexts=initialItems.map(x=>x.querySelector(':scope > .outline-link')?.textContent||''),contentHeadings=[...h2,...h3],contentTexts=contentHeadings.map(x=>x.textContent||'');let childMutations=0;const mo=new w.MutationObserver(ms=>{for(const m of ms)if(m.type==='childList'&&(m.addedNodes.length||m.removedNodes.length))childMutations++});mo.observe(n,{childList:true,subtree:true});
const targets=[n3[0]||n2[0],n3[1]||n2[1]].filter(Boolean);for(const target of targets){const link=target.querySelector(':scope > .outline-link');if(!link)continue;link.click();await sleep(120);if(!target.isConnected)fail(p,v,pass,'clicked heading node was replaced during navigation');if(n.querySelector('.outline-item.is-active')!==target)fail(p,v,pass,'active heading changed during smooth navigation');const currentItems=[...n.querySelectorAll('.outline-item')];if(currentItems.length!==initialItems.length)fail(p,v,pass,`sidebar heading count changed during click ${initialItems.length}->${currentItems.length}`);if(initialItems.some((x,i)=>currentItems[i]!==x))fail(p,v,pass,'sidebar heading DOM nodes were replaced during click');if(JSON.stringify(currentItems.map(x=>x.querySelector(':scope > .outline-link')?.textContent||''))!==JSON.stringify(initialTexts))fail(p,v,pass,'sidebar heading text disappeared or changed during click');if(contentHeadings.some((x,i)=>!x.isConnected||(x.textContent||'')!==contentTexts[i]))fail(p,v,pass,'article heading disappeared or changed during sidebar click');await sleep(950)}mo.disconnect();if(childMutations)fail(p,v,pass,`sidebar DOM mutated after initial build: ${childMutations} childList mutation(s)`);
const target=targets[0];if(target&&cap){const link=target.querySelector(':scope > .outline-link');if(link){link.click();await sleep(70);if(n.querySelector('.outline-item.is-active')!==target)fail(p,v,pass,'clicked outline item did not become active');const cp=cap.getAttribute('d')||'';if(!cp)fail(p,v,pass,'current-row elbow path is empty');if(!cp.includes(' V ')||!cp.includes(' H ')||/[LCQAST]/.test(cp))fail(p,v,pass,`current-row elbow is not vertical-then-horizontal: ${cp}`);if(cp){const len=cap.getTotalLength(),start=cap.getPointAtLength(0),end=cap.getPointAtLength(len),nr=n.getBoundingClientRect(),lr=link.getBoundingClientRect(),pseudo=w.getComputedStyle(link,'::after'),dotLeft=parseFloat(pseudo.left),dotWidth=parseFloat(pseudo.width),expectedX=lr.left-nr.left+dotLeft+dotWidth/2,expectedY=lr.top-nr.top+lr.height/2,expectedTop=lr.top-nr.top;if(Math.abs(start.y-expectedTop)>1.5)fail(p,v,pass,`elbow does not start at current-row top start=${start.y.toFixed(1)} top=${expectedTop.toFixed(1)}`);if(Math.abs(end.x-expectedX)>1||Math.abs(end.y-expectedY)>1)fail(p,v,pass,`elbow misses current dot end=(${end.x.toFixed(1)},${end.y.toFixed(1)}) dot=(${expectedX.toFixed(1)},${expectedY.toFixed(1)})`);if(pseudo.content==='none'||Math.abs(dotWidth-5)>0.2)fail(p,v,pass,'current-location dot styling changed')}}}
if(v[0]==='mobile'){d.querySelector('#menu-btn')?.click();await sleep(80);if(!s.classList.contains('open'))fail(p,v,pass,'mobile sidebar did not open');if(rail&&!visible(rail,w))fail(p,v,pass,'hierarchy rail hidden on mobile')}f.remove()}
(async()=>{for(const v of VPS)for(const p of PATHS)for(const pass of PASSES)await run(p,v,pass);document.getElementById('result').textContent=failures.length?'OUTLINE_SMOKE_FAIL\n'+failures.join('\n'):'OUTLINE_SMOKE_PASS'})();
</script>'''.replace('__PATHS__',payload)

def main():
    chrome=chrome_path();paths=article_urls();page=ROOT/'__outline-smoke.html';page.write_text(harness(paths),encoding='utf-8')
    server=subprocess.Popen([sys.executable,'-m','http.server',str(PORT),'--bind','127.0.0.1','--directory',str(ROOT)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    try:
        wait_server();proc=subprocess.run([chrome,'--headless=new','--no-sandbox','--disable-gpu','--window-size=1440,1000','--virtual-time-budget=180000','--dump-dom',f'http://127.0.0.1:{PORT}/__outline-smoke.html'],capture_output=True,text=True,timeout=210,check=False)
        if 'OUTLINE_SMOKE_PASS' not in proc.stdout:
            start=proc.stdout.find('OUTLINE_SMOKE_FAIL');end=proc.stdout.find('</pre>',start);msg=proc.stdout[start:end] if start>=0 else proc.stderr[-5000:]
            raise RuntimeError('Article outline smoke failed. '+html.unescape(msg))
        print(f'Article outline smoke OK: {len(paths)} article pages x 2 viewports x 2 cache passes; stable heading DOM, click navigation lock and current-row elbow verified.')
    finally:
        server.terminate()
        try:server.wait(timeout=3)
        except subprocess.TimeoutExpired:server.kill()
        page.unlink(missing_ok=True)

if __name__=='__main__':
    try:main()
    except Exception as exc:
        print(f'error: {exc}',file=sys.stderr);raise SystemExit(1)
