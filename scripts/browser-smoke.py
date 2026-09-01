#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import html
import json
import re
import shutil
import socket
import subprocess
import sys
import time

ROOT = Path('_site')
ARTIFACTS = Path('_layout-smoke-artifacts')
PORT = 8765
VIEWPORTS = [('desktop', 1280, 800), ('mobile', 390, 844)]


def find_chrome() -> str:
    for name in ('google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser'):
        path = shutil.which(name)
        if path:
            return path
    raise RuntimeError('Chrome/Chromium is required for layout smoke testing')


def wait_for_server(port: int) -> None:
    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            with socket.create_connection(('127.0.0.1', port), timeout=0.25):
                return
        except OSError:
            time.sleep(0.1)
    raise RuntimeError('Local _site server did not start')


def url_for(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == 'index.html':
        return '/'
    if rel.endswith('/index.html'):
        return '/' + rel[:-len('index.html')]
    return '/' + rel


def classify(text: str) -> str:
    if 'class="content"' in text:
        return 'article'
    if 'directory-main' in text:
        return 'directory'
    if 'class="library-body"' in text:
        return 'library'
    return 'generic'


def discover_cases() -> list[dict[str, str]]:
    cases = []
    for path in sorted(ROOT.rglob('*.html')):
        if path.name in {'__layout-smoke.html', '__details-preview.html'}:
            continue
        text = path.read_text(encoding='utf-8', errors='replace')
        cases.append({'path': url_for(path), 'kind': classify(text)})
    if not cases:
        raise RuntimeError('No generated HTML pages found')
    return cases


def local_target_exists(url: str) -> bool:
    clean = url.split('#', 1)[0].split('?', 1)[0]
    if not clean.startswith('/') or clean.startswith('//'):
        return True
    rel = clean.lstrip('/')
    candidates = []
    if not rel:
        candidates.append(ROOT / 'index.html')
    elif clean.endswith('/'):
        candidates.append(ROOT / rel / 'index.html')
    else:
        candidates.extend([ROOT / rel, ROOT / rel / 'index.html'])
    return any(p.exists() for p in candidates)


def validate_generated_links() -> None:
    errors = []
    attr_re = re.compile(r'''(?:href|src)=["']([^"']+)["']''', re.IGNORECASE)
    for path in ROOT.rglob('*.html'):
        text = path.read_text(encoding='utf-8', errors='replace')
        if '{{' in text or '{%' in text:
            errors.append(f'{path}: unrendered Liquid remains')
        for target in attr_re.findall(text):
            if target.startswith(('#', 'mailto:', 'tel:', 'javascript:', 'data:', 'http://', 'https://')):
                continue
            if target.startswith('/') and not local_target_exists(target):
                errors.append(f'{path}: broken local target {target}')
    if errors:
        raise RuntimeError('Generated HTML/link validation failed:\n- ' + '\n- '.join(errors[:100]))


def harness_html(cases: list[dict[str, str]]) -> str:
    payload = json.dumps(cases, ensure_ascii=False)
    return '''<!doctype html><meta charset="utf-8"><title>Layout smoke</title>
<pre id="result">RUNNING</pre>
<script>
const CASES=__CASES__;
const VIEWPORTS=[{name:'desktop',width:1280,height:800},{name:'mobile',width:390,height:844}];
const failures=[];
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
function fail(c,v,msg){failures.push(`${c.path} [${v.name}] ${msg}`);}
function visible(el,win){if(!el)return false;const s=win.getComputedStyle(el),r=el.getBoundingClientRect();return s.display!=='none'&&s.visibility!=='hidden'&&Number(s.opacity||1)>0.05&&r.width>0&&r.height>0;}
function overflowCulprit(doc){const cw=doc.documentElement.clientWidth;for(const el of doc.querySelectorAll('body *')){const r=el.getBoundingClientRect(),s=doc.defaultView.getComputedStyle(el);if((r.right>cw+4||r.left<-4)&&!['auto','scroll'].includes(s.overflowX))return `${el.tagName.toLowerCase()}.${String(el.className||'').replace(/\s+/g,'.')} right=${Math.round(r.right)} left=${Math.round(r.left)} viewport=${cw}`;}return 'unknown';}
function checkDuplicateIds(c,v,doc){const seen=new Set();for(const el of doc.querySelectorAll('[id]')){if(seen.has(el.id)){fail(c,v,`duplicate id #${el.id}`);return;}seen.add(el.id);}}
function checkAssets(c,v,doc,win){for(const img of doc.images){if(visible(img,win)&&img.complete&&img.naturalWidth===0)fail(c,v,`broken visible image ${img.getAttribute('src')||''}`);}for(const link of doc.querySelectorAll('link[rel="stylesheet"]')){try{const u=new URL(link.href,win.location.href);if(u.origin===win.location.origin&&!link.sheet)fail(c,v,`stylesheet not loaded ${u.pathname}`);}catch(_){}}}
function checkManagedHeader(c,v,doc,win){const selector=c.kind==='article'?'.article-library-header':'.library-header';const headers=doc.querySelectorAll(selector);if(headers.length!==1){fail(c,v,`expected exactly one global header, got ${headers.length}`);return null;}const header=headers[0];if(!visible(header,win)){fail(c,v,'global header is not visible');return header;}const r=header.getBoundingClientRect(),s=win.getComputedStyle(header),cw=doc.documentElement.clientWidth;if(Math.abs(r.top)>3)fail(c,v,`header top=${Math.round(r.top)}`);if(s.position!=='fixed')fail(c,v,`header position=${s.position}, expected fixed`);if(r.width<cw-4||r.right>cw+3)fail(c,v,`header width=${Math.round(r.width)} viewport=${cw}`);const minH=c.kind==='article'||v.name==='desktop'?48:90,maxH=c.kind==='article'||v.name==='desktop'?62:130;if(r.height<minH||r.height>maxH)fail(c,v,`header height=${Math.round(r.height)} expected ${minH}-${maxH}`);const labels=[...header.querySelectorAll('nav a')].map(a=>a.textContent.trim());for(const label of ['Home','コマース','アイデンティティ','決済'])if(!labels.includes(label))fail(c,v,`nav missing ${label}`);const pt=parseFloat(win.getComputedStyle(doc.body).paddingTop)||0;if(pt+4<r.height)fail(c,v,`body padding-top ${pt} is smaller than header ${r.height}`);return header;}
function checkTextClipping(c,v,doc,win){for(const el of doc.querySelectorAll('h1,h2,h3,.library-collection-name,.directory-note-copy strong,.library-collection-note strong')){if(!visible(el,win)||el.classList.contains('mobile-title'))continue;const s=win.getComputedStyle(el);if(s.overflow==='hidden'&&el.scrollWidth>el.clientWidth+3&&s.textOverflow!=='ellipsis')fail(c,v,`clipped text in ${el.tagName.toLowerCase()}.${String(el.className||'').replace(/\s+/g,'.')}`);}}
async function runOne(c,v){const iframe=document.createElement('iframe');iframe.style.cssText=`position:absolute;left:-10000px;top:0;width:${v.width}px;height:${v.height}px;border:0`;document.body.appendChild(iframe);let loaded=true;await new Promise((resolve,reject)=>{const t=setTimeout(()=>reject(new Error('load timeout')),5000);iframe.onload=()=>{clearTimeout(t);resolve();};iframe.src=c.path;}).catch(e=>{loaded=false;fail(c,v,e.message);});if(!loaded){iframe.remove();return;}await sleep(35);const doc=iframe.contentDocument,win=iframe.contentWindow;if(!doc||!win){fail(c,v,'document unavailable');iframe.remove();return;}const raw=doc.documentElement.innerHTML;if(raw.includes('{{')||raw.includes('{%'))fail(c,v,'unrendered template syntax found');if(!visible(doc.body,win))fail(c,v,'body missing/hidden');if((doc.body.textContent||'').trim().length<2&&!doc.querySelector('img,svg,video,canvas,iframe'))fail(c,v,'page has no visible content');checkDuplicateIds(c,v,doc);checkAssets(c,v,doc,win);if(doc.documentElement.scrollWidth>doc.documentElement.clientWidth+4)fail(c,v,`horizontal overflow: ${overflowCulprit(doc)}`);checkTextClipping(c,v,doc,win);let header=null;if(c.kind!=='generic')header=checkManagedHeader(c,v,doc,win);if(c.kind==='article'){const hero=doc.querySelector('.hero'),content=doc.querySelector('.content'),shell=doc.querySelector('.shell');if(!visible(hero,win))fail(c,v,'article hero missing/hidden');if(!visible(content,win))fail(c,v,'article content missing/hidden');if(!visible(shell,win))fail(c,v,'article shell missing/hidden');if(hero&&header&&hero.getBoundingClientRect().top<header.getBoundingClientRect().bottom-2)fail(c,v,'article hero overlaps global header');if(v.name==='mobile'&&!visible(doc.querySelector('.mobile-head'),win))fail(c,v,'mobile article head missing');if(v.name==='desktop'){const side=doc.querySelector('.side');if(!visible(side,win))fail(c,v,'desktop article sidebar missing');else{const sw=side.getBoundingClientRect().width;if(sw<180||sw>360)fail(c,v,`sidebar width=${Math.round(sw)}`);}}}else if(c.kind==='directory'){const main=doc.querySelector('.directory-main'),list=doc.querySelector('.directory-list');if(!visible(main,win))fail(c,v,'directory main missing/hidden');if(!visible(list,win))fail(c,v,'directory list missing/hidden');if(doc.querySelectorAll('.directory-note-row').length===0)fail(c,v,'directory has no rendered entries');if(main&&header&&main.getBoundingClientRect().top<header.getBoundingClientRect().bottom-2)fail(c,v,'directory content overlaps header');}else if(c.kind==='library'){const main=doc.querySelector('.library-main');if(!visible(main,win))fail(c,v,'library main missing/hidden');if(c.path!=='/'&&doc.querySelectorAll('.library-collection-entry').length===0)fail(c,v,'category has no rendered entries');if(main&&header&&main.getBoundingClientRect().top<header.getBoundingClientRect().bottom-2)fail(c,v,'library content overlaps header');}iframe.remove();}
(async()=>{for(const v of VIEWPORTS)for(const c of CASES)await runOne(c,v);document.getElementById('result').textContent=failures.length?'LAYOUT_SMOKE_FAIL\n'+failures.join('\n'):'LAYOUT_SMOKE_PASS';})();
</script>'''.replace('__CASES__', payload)


def details_preview_html() -> str:
    target = ROOT / 'payments' / 'ap2-implementation-flow.html'
    source = target.read_text(encoding='utf-8', errors='replace')
    head_match = re.search(r'<head>(?P<head>.*?)</head>', source, flags=re.S | re.I)
    if not head_match:
        raise RuntimeError('generated implementation-flow page has no <head>')
    head = re.sub(r'<script\b[^>]*>.*?</script>', '', head_match.group('head'), flags=re.S | re.I)
    block_match = re.search(
        r'<details(?P<attrs>[^>]*)>\s*<summary>JSON-RPC / A2A Envelopeの主要フィールド</summary>.*?</details>',
        source,
        flags=re.S | re.I,
    )
    if not block_match:
        raise RuntimeError('JSON-RPC details block not found in generated implementation-flow page')
    block = block_match.group(0)
    block = re.sub(r'^<details([^>]*)>', r'<details\1 open>', block, count=1, flags=re.I)
    return f'''<!doctype html><html><head>{head}
<style>
body{{padding:42px 28px!important;background:var(--bg,#f5f4ef)!important}}
.main{{padding:0!important}}
.content{{max-width:980px!important;margin:0 auto!important}}
@media(max-width:980px){{body{{padding:24px 12px!important}}}}
</style></head><body><main class="main"><div class="content">{block}</div></main></body></html>'''


def screenshot(chrome: str, path: str, name: str, width: int, height: int) -> None:
    out = ARTIFACTS / f'{name}-{width}x{height}.png'
    subprocess.run([chrome, '--headless=new', '--no-sandbox', '--disable-gpu', f'--window-size={width},{height}', f'--screenshot={out.resolve()}', f'http://127.0.0.1:{PORT}{path}'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=20, check=False)


def main() -> int:
    if not ROOT.exists():
        raise RuntimeError('_site does not exist; run the site build first')
    validate_generated_links()
    cases = discover_cases()
    chrome = find_chrome()
    ARTIFACTS.mkdir(exist_ok=True)
    harness = ROOT / '__layout-smoke.html'
    details_preview = ROOT / '__details-preview.html'
    harness.write_text(harness_html(cases), encoding='utf-8')
    details_preview.write_text(details_preview_html(), encoding='utf-8')
    server = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT), '--bind', '127.0.0.1', '--directory', str(ROOT)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        wait_for_server(PORT)
        proc = subprocess.run([chrome, '--headless=new', '--no-sandbox', '--disable-gpu', '--window-size=1440,1000', '--virtual-time-budget=60000', '--dump-dom', f'http://127.0.0.1:{PORT}/__layout-smoke.html'], capture_output=True, text=True, timeout=90, check=False)
        dump = proc.stdout
        (ARTIFACTS / 'layout-smoke-dom.html').write_text(dump, encoding='utf-8')
        for path, name in [('/payments/', 'payments'),('/payments/ap2/', 'ap2-directory'),('/payments/ap2/ap2.html','ap2-overview')]:
            for _, width, height in VIEWPORTS:
                screenshot(chrome, path, name, width, height)
        for _, width, height in VIEWPORTS:
            screenshot(chrome, '/__details-preview.html', 'implementation-flow-jsonrpc-details-open', width, height)
        details_dump = subprocess.run([chrome, '--headless=new', '--no-sandbox', '--disable-gpu', '--window-size=1280,800', '--dump-dom', f'http://127.0.0.1:{PORT}/__details-preview.html'], capture_output=True, text=True, timeout=20, check=False)
        (ARTIFACTS / 'implementation-flow-jsonrpc-details-dom.html').write_text(details_dump.stdout, encoding='utf-8')
        if 'LAYOUT_SMOKE_PASS' not in dump:
            marker = 'LAYOUT_SMOKE_FAIL'
            start = dump.find(marker)
            end = dump.find('</pre>', start) if start >= 0 else -1
            result = dump[start:end] if start >= 0 else proc.stderr[-5000:]
            raise RuntimeError('Browser layout smoke failed. ' + html.unescape(result))
        kinds = {}
        for case in cases:
            kinds[case['kind']] = kinds.get(case['kind'], 0) + 1
        print(f'Browser layout smoke OK: {len(cases)} generated HTML pages x {len(VIEWPORTS)} viewports. kinds={kinds}')
        return 0
    finally:
        server.terminate()
        try:
            server.wait(timeout=3)
        except subprocess.TimeoutExpired:
            server.kill()
        harness.unlink(missing_ok=True)
        details_preview.unlink(missing_ok=True)


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f'error: {exc}', file=sys.stderr)
        raise SystemExit(1)
