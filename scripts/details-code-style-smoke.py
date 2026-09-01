#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path('_site')
PORT = 8768


def chrome_path() -> str:
    for name in ('google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser'):
        path = shutil.which(name)
        if path:
            return path
    raise RuntimeError('Chrome/Chromium is required')


def wait_server() -> None:
    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            with socket.create_connection(('127.0.0.1', PORT), timeout=.25):
                return
        except OSError:
            time.sleep(.1)
    raise RuntimeError('Local server did not start')


def url_for(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == 'index.html':
        return '/'
    if rel.endswith('/index.html'):
        return '/' + rel[:-len('index.html')]
    return '/' + rel


def article_urls() -> list[str]:
    urls = []
    for path in sorted(ROOT.rglob('*.html')):
        text = path.read_text(encoding='utf-8', errors='replace')
        if 'class="content"' in text and '<details' in text and '<pre' in text:
            urls.append(url_for(path))
    return urls


def harness(paths: list[str]) -> str:
    payload = json.dumps(paths, ensure_ascii=False)
    return '''<!doctype html><meta charset="utf-8"><pre id="result">RUNNING</pre><script>
const PATHS=__PATHS__,VPS=[['desktop',1280,800],['mobile',390,844]],failures=[];
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const fail=(p,v,m)=>failures.push(`${p} [${v[0]}] ${m}`);
async function run(p,v){
  const f=document.createElement('iframe');
  f.style.cssText=`position:absolute;left:-10000px;top:0;width:${v[1]}px;height:${v[2]}px;border:0`;
  document.body.appendChild(f);
  let loaded=true;
  await new Promise((res,rej)=>{const t=setTimeout(()=>rej(new Error('load timeout')),7000);f.onload=()=>{clearTimeout(t);res()};f.src=p}).catch(e=>{loaded=false;fail(p,v,e.message)});
  if(!loaded){f.remove();return}
  await sleep(100);
  const d=f.contentDocument,w=f.contentWindow;
  if(!d||!w){fail(p,v,'document unavailable');f.remove();return}
  for(const details of d.querySelectorAll('.content details'))details.open=true;
  await sleep(20);
  const codes=[...d.querySelectorAll('.content details pre code')];
  for(const [i,code] of codes.entries()){
    const s=w.getComputedStyle(code),bg=s.backgroundColor.replace(/\s+/g,'');
    const transparent=bg==='rgba(0,0,0,0)'||bg==='transparent';
    if(!transparent)fail(p,v,`details code#${i} background=${s.backgroundColor}`);
    if(parseFloat(s.paddingTop)>0.1||parseFloat(s.paddingRight)>0.1||parseFloat(s.paddingBottom)>0.1||parseFloat(s.paddingLeft)>0.1)fail(p,v,`details code#${i} padding=${s.padding}`);
  }
  f.remove();
}
(async()=>{for(const v of VPS)for(const p of PATHS)await run(p,v);document.getElementById('result').textContent=failures.length?'DETAILS_CODE_STYLE_FAIL\\n'+failures.join('\\n'):'DETAILS_CODE_STYLE_PASS'})();
</script>'''.replace('__PATHS__', payload)


def main() -> None:
    chrome = chrome_path()
    paths = article_urls()
    page = ROOT / '__details-code-style-smoke.html'
    page.write_text(harness(paths), encoding='utf-8')
    server = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT), '--bind', '127.0.0.1', '--directory', str(ROOT)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        wait_server()
        proc = subprocess.run([chrome, '--headless=new', '--no-sandbox', '--disable-gpu', '--window-size=1440,1000', '--virtual-time-budget=120000', '--dump-dom', f'http://127.0.0.1:{PORT}/__details-code-style-smoke.html'], capture_output=True, text=True, timeout=150, check=False)
        if 'DETAILS_CODE_STYLE_PASS' not in proc.stdout:
            start = proc.stdout.find('DETAILS_CODE_STYLE_FAIL')
            end = proc.stdout.find('</pre>', start)
            reason = html.unescape(proc.stdout[start:end]) if start >= 0 else proc.stderr[-5000:]
            raise RuntimeError('Details code style smoke failed. ' + reason)
        print(f'Details code style smoke OK: {len(paths)} article pages with details/code blocks x 2 viewports; code backgrounds are transparent.')
    finally:
        server.terminate()
        try:
            server.wait(timeout=3)
        except subprocess.TimeoutExpired:
            server.kill()
        page.unlink(missing_ok=True)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f'error: {exc}', file=sys.stderr)
        raise SystemExit(1)
