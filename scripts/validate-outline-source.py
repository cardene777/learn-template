#!/usr/bin/env python3
from pathlib import Path

layout = Path('src/layouts/ArticleLayout.astro').read_text(encoding='utf-8')
workflow = Path('.github/workflows/deploy-cloudflare.yml').read_text(encoding='utf-8')
outline_js = Path('assets/article-outline.js').read_text(encoding='utf-8')
outline_css = Path('assets/article-outline.css').read_text(encoding='utf-8')

errors=[]
for required in ["../../assets/article-outline.css", "../../assets/article-outline.js", 'id="side-nav"', 'id="content"', 'class="hero"']:
    if required not in layout: errors.append(f'ArticleLayout.astro missing {required}')
for required in ["content.querySelectorAll('h2,h3')",'outline-item-${level}','outline-rail-base','outline-rail-active',"sideTitle.textContent='このページ'","document.querySelector('#toc ul')"]:
    if required not in outline_js: errors.append(f'article-outline.js missing {required}')
for required in ['.outline-level-3','.outline-rail-base','.outline-rail-active']:
    if required not in outline_css: errors.append(f'article-outline.css missing {required}')
if "document.getElementById('side-nav').innerHTML" in layout:
    errors.append('ArticleLayout.astro contains a legacy sidebar writer')
if "document.querySelector('#toc ul').innerHTML" in layout:
    errors.append('ArticleLayout.astro contains a legacy TOC writer')
for forbidden in ['side.scrollTop=', 'side.scrollTop+=', 'side.scrollTop -=']:
    if forbidden in outline_js: errors.append(f'article-outline.js must not move sidebar scroll position: {forbidden}')
for forbidden in ['fix-article-outline.py','patch-outline-scroll.py','postprocess-library.py','version-library-assets.py','build-cloudflare.sh']:
    if forbidden in workflow: errors.append(f'workflow still uses legacy outline/build processing: {forbidden}')
if Path('scripts/version-library-assets.py').exists():
    errors.append('scripts/version-library-assets.py must be removed; Astro/Vite owns asset fingerprinting')
if errors:
    raise RuntimeError('Astro article outline source contract failed:\n- '+'\n- '.join(errors))
print('Astro article outline source contract OK: article-outline.js is the single owner of heading ids, TOC and sidebar outline.')
