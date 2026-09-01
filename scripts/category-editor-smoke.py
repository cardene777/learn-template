#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import re
import shutil
import socket
import subprocess
import sys
import time

ROOT = Path('_site')
PORT = 8768
DOMAINS = ('commerce', 'identity', 'payments')


def find_chrome() -> str:
    for name in ('google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser'):
        path = shutil.which(name)
        if path:
            return path
    raise RuntimeError('Chrome/Chromium is required for category editor smoke testing')


def wait_for_server() -> None:
    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            with socket.create_connection(('127.0.0.1', PORT), timeout=0.25):
                return
        except OSError:
            time.sleep(0.1)
    raise RuntimeError('Local _site server did not start')


def find_targets() -> tuple[str, str, Path]:
    for domain in DOMAINS:
        category_path = ROOT / domain / 'index.html'
        if not category_path.exists():
            continue
        text = category_path.read_text(encoding='utf-8', errors='replace')
        match = re.search(r'<a(?=[^>]*\bdata-category-body-edit\b)(?=[^>]*\bhref="([^"]+)")[^>]*>', text)
        if not match:
            continue
        article_url = match.group(1).split('?', 1)[0]
        rel = article_url.lstrip('/')
        article_path = ROOT / (rel + 'index.html' if article_url.endswith('/') else rel)
        if article_path.exists():
            return f'/{domain}/', article_url, article_path
    raise RuntimeError('No category Note with body editing was found')


def harness_html(category_url: str, article_url: str) -> str:
    category = json.dumps(category_url, ensure_ascii=False)
    article = json.dumps(article_url, ensure_ascii=False)
    return r'''<!doctype html><meta charset="utf-8"><pre id="result">RUNNING</pre><script>
const CATEGORY=__CATEGORY__,ARTICLE=__ARTICLE__,failures=[];const sleep=ms=>new Promise(r=>setTimeout(r,ms));
function fail(msg){failures.push(msg)}
async function frame(path){const iframe=document.createElement('iframe');iframe.style.cssText='width:1280px;height:800px;border:0';document.body.appendChild(iframe);await new Promise((resolve,reject)=>{const t=setTimeout(()=>reject(new Error(`load timeout ${path}`)),5000);iframe.onload=()=>{clearTimeout(t);resolve()};iframe.src=path}).catch(e=>fail(e.message));await sleep(140);return iframe}
function input(doc,id,value){const el=doc.getElementById(id);if(!el){fail(`missing ${id}`);return null}el.value=value;el.dispatchEvent(new Event('input',{bubbles:true}));return el}
(async()=>{
  const categoryFrame=await frame(CATEGORY);const doc=categoryFrame.contentDocument;
  if(!doc){fail('category document unavailable')}else{
    const noteShell=[...doc.querySelectorAll('.library-entry-shell')].find(shell=>shell.querySelector('.library-collection-note'));
    const bodyEdit=noteShell?.querySelector('[data-category-body-edit]');if(!bodyEdit)fail('category Note 本文編集 link missing');else{if(bodyEdit.textContent.trim()!=='本文編集')fail('category body edit label must be 本文編集');if(!String(bodyEdit.getAttribute('href')||'').includes('?edit=body'))fail('category body edit link does not enter article edit mode')}
    const action=noteShell?.querySelector('[data-category-edit]');if(!action)fail('category Note タイトル編集 button missing');else{if(action.textContent.trim()!=='タイトル編集')fail('category metadata button label must be タイトル編集');action.click();await sleep(40);const dialog=doc.getElementById('category-editor-dialog');if(!dialog?.open)fail('metadata editor dialog did not open');const tabs=[...doc.querySelectorAll('[data-category-tab]')].filter(b=>!b.hidden).map(b=>b.dataset.categoryTab);for(const tab of ['meta','move','delete'])if(!tabs.includes(tab))fail(`missing ${tab} tab`);if(tabs.includes('body')||doc.querySelector('[data-category-panel="body"]'))fail('body editing remains inside category modal');dialog?.close()}
    const create=doc.getElementById('category-editor-create-folder');if(!create)fail('category フォルダ作成 button missing');else{create.click();await sleep(30);const createDialog=doc.getElementById('category-editor-create-dialog');if(!createDialog?.open)fail('folder create dialog did not open');if(createDialog?.querySelectorAll('.category-editor-required').length<7)fail('category folder create required marks missing');const save=doc.getElementById('category-editor-create-save');if(!save?.disabled)fail('category folder create button must start disabled');input(doc,'category-editor-create-id','smoke-folder');input(doc,'category-editor-create-title','Smoke Folder');input(doc,'category-editor-create-description','Smoke test folder');await sleep(30);if(save?.disabled)fail('category folder create button did not enable after all required fields were filled');createDialog?.close()}
  }
  categoryFrame.remove();

  const articleFrame=await frame(ARTICLE);const articleDoc=articleFrame.contentDocument;
  if(!articleDoc){fail('article document unavailable')}else{
    const meta=articleDoc.getElementById('content-editor-open'),bodyButton=articleDoc.getElementById('article-edit-mode');
    if(!meta)fail('article タイトル編集 button missing');else if(meta.textContent.trim()!=='タイトル編集')fail('article metadata button label must be タイトル編集');
    if(!bodyButton)fail('article 本文編集 button missing');else if(bodyButton.textContent.trim()!=='本文編集')fail('article body button label must be 本文編集');
    meta?.click();await sleep(30);const dialog=articleDoc.getElementById('content-editor-dialog');if(!dialog?.open)fail('article metadata modal did not open');if(articleDoc.querySelector('[data-editor-tab="body"]')||articleDoc.querySelector('[data-editor-panel="body"]'))fail('body editing remains inside article modal');dialog?.close();
    bodyButton?.click();await sleep(60);const panel=articleDoc.getElementById('article-body-editor'),content=articleDoc.getElementById('content'),rendered=articleDoc.getElementById('article-rendered-body');
    if(!panel||panel.hidden)fail('inline body editor did not open');if(panel?.closest('#content')!==content)fail('body editor is not inside the displayed article content area');if(content&&getComputedStyle(content).display==='none')fail('article content container must remain in place during body editing');if(rendered&&getComputedStyle(rendered).display!=='none')fail('rendered body must be replaced by editor in the same area');if(dialog?.open)fail('body edit opened metadata modal');if(articleDoc.querySelectorAll('[data-md-tool]').length<8)fail('Markdown editing toolbar is incomplete');if(bodyButton?.getAttribute('aria-pressed')!=='true')fail('body edit button state was not updated');if(bodyButton?.textContent.trim()!=='本文編集中')fail('body edit button must show 本文編集中 while active');
  }
  articleFrame.remove();

  const queryFrame=await frame(ARTICLE+'?edit=body');const queryDoc=queryFrame.contentDocument;if(!queryDoc?.body.classList.contains('article-body-editing'))fail('edit=body did not automatically enter article body editing');if(queryDoc?.getElementById('article-body-editor')?.closest('#content')!==queryDoc?.getElementById('content'))fail('query body editor is not inline in content');queryFrame.remove();
  document.getElementById('result').textContent=failures.length?'CATEGORY_EDITOR_FAIL\n'+failures.join('\n'):'CATEGORY_EDITOR_PASS';
})();</script>'''.replace('__CATEGORY__', category).replace('__ARTICLE__', article)


def main() -> int:
    if not ROOT.exists():
        raise RuntimeError('_site does not exist; run npm run build first')

    for domain in DOMAINS:
        path = ROOT / domain / 'index.html'
        if not path.exists():
            raise RuntimeError(f'missing category page: {path}')
        text = path.read_text(encoding='utf-8', errors='replace')
        for required in ('data-category-edit=', 'data-category-body-edit', '本文編集', 'タイトル編集', 'id="category-editor-create-folder"', 'category-editor-required'):
            if required not in text:
                raise RuntimeError(f'{path}: missing category management UI {required}')
        if 'data-category-panel="body"' in text:
            raise RuntimeError(f'{path}: body editor must not remain in metadata modal')

    category_url, article_url, article_path = find_targets()
    article_text = article_path.read_text(encoding='utf-8', errors='replace')
    for required in ('>タイトル編集<', '>本文編集<', 'id="article-edit-mode"', 'id="article-body-editor"', 'id="article-rendered-body"', 'id="article-body-editor-textarea"', 'data-md-tool="bold"'):
        if required not in article_text:
            raise RuntimeError(f'{article_path}: article inline body editing UI missing: {required}')
    if 'data-editor-tab="body"' in article_text:
        raise RuntimeError(f'{article_path}: article metadata modal still contains body tab')

    harness = ROOT / '__category-editor-smoke.html'
    harness.write_text(harness_html(category_url, article_url), encoding='utf-8')
    chrome = find_chrome()
    server = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT), '--bind', '127.0.0.1', '--directory', str(ROOT)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        wait_for_server()
        result = subprocess.run([chrome, '--headless=new', '--no-sandbox', '--disable-gpu', '--window-size=1440,1000', '--virtual-time-budget=12000', '--dump-dom', f'http://127.0.0.1:{PORT}/__category-editor-smoke.html'], capture_output=True, text=True, timeout=35, check=False)
        if result.returncode != 0 or 'CATEGORY_EDITOR_PASS' not in result.stdout:
            match = re.search(r'CATEGORY_EDITOR_FAIL.*?</pre>', result.stdout, re.S)
            raise RuntimeError('Category editor browser smoke failed:\n' + (match.group(0) if match else result.stderr[-4000:]))
    finally:
        harness.unlink(missing_ok=True)
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()
    print(f'Category editor smoke OK: {category_url} and {article_url} verified without content-specific paths.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
