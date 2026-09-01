#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / ' _site'.strip()
CSS_PATH = ROOT / 'assets' / 'article-overrides.css'
PORT = 8767
errors: list[str] = []
checked_blocks = 0
checked_definition_rows = 0

DETAIL_RE = re.compile(r'<details(?:\s[^>]*)?>(?P<body>.*?)</details>', re.S | re.I)
DEFINITION_ROW_RE = re.compile(r'<li(?=[^>]*\bdetails-definition\b)[^>]*>(?P<body>.*?)</li>', re.S | re.I)


def selector_block(css: str, selector: str) -> str | None:
    match = re.search(re.escape(selector) + r'\s*\{(?P<body>.*?)\}', css, re.S)
    return match.group('body') if match else None


def validate_css_contract() -> None:
    css = CSS_PATH.read_text(encoding='utf-8')
    open_summary = selector_block(css, '.content details[open] > summary')
    if open_summary is None:
        errors.append('article-overrides.css: missing open summary rule')
    elif 'border-bottom' in open_summary:
        errors.append('article-overrides.css: open summary must not restore the separator line')
    details_list = selector_block(css, '.content details > ul')
    if details_list is None:
        errors.append('article-overrides.css: missing details list rule')
    elif not re.search(r'padding:\s*0\s+', details_list):
        errors.append('article-overrides.css: details list top padding must remain zero')
    desktop_definition = selector_block(css, '.content details > ul > li.details-definition')
    if desktop_definition is None or 'display: grid' not in desktop_definition:
        errors.append('article-overrides.css: details-definition must remain a grid on desktop')
    if desktop_definition is not None and 'grid-template-columns: minmax(120px, 200px) minmax(0, 1fr)' not in desktop_definition:
        errors.append('article-overrides.css: details-definition desktop two-column contract changed')
    if '.details-definition-description' not in css:
        errors.append('article-overrides.css: missing details-definition-description styling')
    mobile = re.search(r'@media\s*\(max-width:\s*980px\).*?\.content details > ul > li\.details-definition\s*\{(?P<body>.*?)\}', css, re.S)
    if not mobile or 'grid-template-columns: minmax(0, 1fr)' not in mobile.group('body'):
        errors.append('article-overrides.css: mobile details-definition must remain one column')


def summary_text(block: str) -> str | None:
    match = re.search(r'<summary(?:\s[^>]*)?>(?P<text>.*?)</summary>', block, re.S | re.I)
    if not match:
        return None
    return re.sub(r'<[^>]+>', '', html.unescape(match.group('text'))).strip()


def url_for(path: Path) -> str:
    rel = path.relative_to(SITE).as_posix()
    if rel == 'index.html':
        return '/'
    if rel.endswith('/index.html'):
        return '/' + rel[:-len('index.html')]
    return '/' + rel


def validate_rendered_structure() -> list[str]:
    global checked_blocks, checked_definition_rows
    pages: list[str] = []
    for path in sorted(SITE.rglob('*.html')):
        if path.name.startswith('__'):
            continue
        rendered = path.read_text(encoding='utf-8', errors='replace')
        if '<details' not in rendered.lower():
            continue
        pages.append(url_for(path))
        for match in DETAIL_RE.finditer(rendered):
            checked_blocks += 1
            block = match.group(0)
            body = match.group('body')
            summary = summary_text(block)
            if not summary:
                errors.append(f'{path.relative_to(ROOT)}: details has no readable summary')
            if re.search(r'(?:^|[>\n])\s*-\s+(?:\*\*|`)', body, re.M):
                errors.append(f'{path.relative_to(ROOT)}: raw Markdown leaked inside details {summary!r}')
            body_without_summary = re.sub(r'<summary(?:\s[^>]*)?>.*?</summary>', '', body, count=1, flags=re.S | re.I)
            plain = re.sub(r'<[^>]+>', '', html.unescape(body_without_summary)).strip()
            if not plain and not re.search(r'<(?:img|svg|video|canvas|table|pre)\b', body_without_summary, re.I):
                errors.append(f'{path.relative_to(ROOT)}: details {summary!r} has no rendered content')
            rows = list(DEFINITION_ROW_RE.finditer(body))
            checked_definition_rows += len(rows)
            for row in rows:
                row_body = row.group('body')
                if not re.match(r'\s*<(?:strong|code)>.*?</(?:strong|code)>', row_body, re.S | re.I):
                    errors.append(f'{path.relative_to(ROOT)}: details-definition row lost its label in {summary!r}')
                if not re.search(r'<span\s+class="details-definition-description">.*?</span>', row_body, re.S | re.I):
                    errors.append(f'{path.relative_to(ROOT)}: details-definition row lost its description in {summary!r}')
    if checked_blocks == 0:
        errors.append('no rendered details blocks were found')
    if checked_definition_rows == 0:
        errors.append('no rendered details-definition rows were found')
    return pages


def find_chrome() -> str:
    for name in ('google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser'):
        path = shutil.which(name)
        if path:
            return path
    raise RuntimeError('Chrome/Chromium is required for details regression testing')


def wait_for_server() -> None:
    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            with socket.create_connection(('127.0.0.1', PORT), timeout=0.25):
                return
        except OSError:
            time.sleep(0.1)
    raise RuntimeError('details regression server did not start')


def harness_html(paths: list[str]) -> str:
    payload = json.dumps(paths, ensure_ascii=False)
    return '''<!doctype html><meta charset="utf-8"><pre id="result">RUNNING</pre><script>
const PATHS=__PATHS__,VPS=[['desktop',1280,800],['mobile',390,844]],failures=[];
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const fail=(p,v,i,m)=>failures.push(`${p} [${v[0]} details#${i}] ${m}`);
const visible=(el,w)=>{if(!el)return false;const s=w.getComputedStyle(el),r=el.getBoundingClientRect();return s.display!=='none'&&s.visibility!=='hidden'&&Number(s.opacity||1)>.05&&r.width>0&&r.height>0};
async function run(p,v){const f=document.createElement('iframe');f.style.cssText=`position:absolute;left:-10000px;top:0;width:${v[1]}px;height:${v[2]}px;border:0`;document.body.appendChild(f);let loaded=true;await new Promise((res,rej)=>{const t=setTimeout(()=>rej(new Error('load timeout')),7000);f.onload=()=>{clearTimeout(t);res()};f.src=p}).catch(e=>{loaded=false;fail(p,v,-1,e.message)});if(!loaded){f.remove();return}await sleep(100);const d=f.contentDocument,w=f.contentWindow;if(!d||!w){fail(p,v,-1,'document unavailable');f.remove();return}const blocks=[...d.querySelectorAll('.content details')];if(!blocks.length)fail(p,v,-1,'no content details found');for(const [i,details] of blocks.entries()){const summary=details.querySelector(':scope > summary');if(!summary){fail(p,v,i,'summary missing');continue}details.open=false;summary.click();await sleep(12);if(!details.open){fail(p,v,i,'summary click did not open details');continue}const children=[...details.children].filter(el=>el!==summary&&!['SCRIPT','STYLE','TEMPLATE'].includes(el.tagName));if(!children.length){fail(p,v,i,'opened details has no content elements');continue}const shown=children.filter(el=>visible(el,w));if(!shown.length)fail(p,v,i,'opened details content is not visible');const dr=details.getBoundingClientRect(),sr=summary.getBoundingClientRect();if(dr.height<=sr.height+2)fail(p,v,i,`opened height=${Math.round(dr.height)} summary=${Math.round(sr.height)}`);const text=children.map(el=>el.textContent||'').join('').trim();if(!text&&!details.querySelector(':scope > img,:scope > svg,:scope > video,:scope > canvas,:scope > table,:scope > pre'))fail(p,v,i,'opened details has no visible content payload');if(dr.right>d.documentElement.clientWidth+4)fail(p,v,i,`details overflows viewport right=${Math.round(dr.right)} viewport=${d.documentElement.clientWidth}`);const rows=[...details.querySelectorAll(':scope > ul > li.details-definition')];if(rows.length){const list=details.querySelector(':scope > ul');if(parseFloat(w.getComputedStyle(summary).borderBottomWidth)>0.1)fail(p,v,i,'definition summary bottom separator returned');if(!list||parseFloat(w.getComputedStyle(list).paddingTop)>0.1)fail(p,v,i,'definition list top padding returned');for(const [j,row] of rows.entries()){const labelEl=row.querySelector(':scope > strong:first-child,:scope > code:first-child'),desc=row.querySelector(':scope > .details-definition-description');if(!labelEl||!desc){fail(p,v,i,`definition row ${j} missing label/description`);continue}const lr=labelEl.getBoundingClientRect(),xr=desc.getBoundingClientRect();if(v[0]==='mobile'){if(xr.top<lr.bottom-1)fail(p,v,i,`definition row ${j} mobile overlap`);if(Math.abs(xr.left-lr.left)>3)fail(p,v,i,`definition row ${j} mobile not stacked`)}else{if(xr.left<lr.right+4)fail(p,v,i,`definition row ${j} desktop overlap`)}}}}f.remove()}
(async()=>{for(const v of VPS)for(const p of PATHS)await run(p,v);document.getElementById('result').textContent=failures.length?'DETAILS_SMOKE_FAIL\\n'+failures.join('\\n'):'DETAILS_SMOKE_PASS'})();
</script>'''.replace('__PATHS__', payload)


def validate_browser_interaction(pages: list[str]) -> None:
    chrome = find_chrome()
    harness = SITE / '__details-smoke.html'
    harness.write_text(harness_html(pages), encoding='utf-8')
    server = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT), '--bind', '127.0.0.1', '--directory', str(SITE)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        wait_for_server()
        proc = subprocess.run([chrome, '--headless=new', '--no-sandbox', '--disable-gpu', '--window-size=1440,1000', '--virtual-time-budget=120000', '--dump-dom', f'http://127.0.0.1:{PORT}/__details-smoke.html'], capture_output=True, text=True, timeout=150, check=False)
        if 'DETAILS_SMOKE_PASS' not in proc.stdout:
            start = proc.stdout.find('DETAILS_SMOKE_FAIL')
            end = proc.stdout.find('</pre>', start)
            reason = html.unescape(proc.stdout[start:end]) if start >= 0 else proc.stderr[-5000:]
            errors.append('browser details interaction failed: ' + reason)
    finally:
        server.terminate()
        try:
            server.wait(timeout=3)
        except subprocess.TimeoutExpired:
            server.kill()
        harness.unlink(missing_ok=True)


def main() -> int:
    if not SITE.exists():
        raise RuntimeError('_site does not exist; run the site build first')
    validate_css_contract()
    pages = validate_rendered_structure()
    validate_browser_interaction(pages)
    if errors:
        print('Rendered details regression failed:', file=sys.stderr)
        for error in errors:
            print(f'- {error}', file=sys.stderr)
        return 1
    print(f'Rendered details regression OK: {len(pages)} pages / {checked_blocks} details blocks / {checked_definition_rows} definition rows opened and visible in desktop/mobile Chrome.')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f'error: {exc}', file=sys.stderr)
        raise SystemExit(1)
