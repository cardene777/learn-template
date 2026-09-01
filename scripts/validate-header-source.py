#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path('.')
errors: list[str] = []


def require(path: str, needles: list[str]) -> str:
    p = ROOT / path
    if not p.exists():
        errors.append(f'Missing required Astro source file: {path}')
        return ''
    text = p.read_text(encoding='utf-8')
    for needle in needles:
        if needle not in text:
            errors.append(f'{path}: missing {needle!r}')
    return text

article_header = require('src/components/ArticleHeader.astro', ['class="article-library-header"','href="/"','href="/commerce/"','href="/identity/"','href="/payments/"','class="article-library-github-link"','href="https://github.com/__LEARN_REPOSITORY__"','aria-label="GitHub repository"'])
library_header = require('src/components/LibraryHeader.astro', ['class="library-header"','href="/"','href="/commerce/"','href="/identity/"','href="/payments/"','class="library-github-link"','href="https://github.com/__LEARN_REPOSITORY__"','aria-label="GitHub repository"'])
for path, text in [('ArticleHeader.astro', article_header), ('LibraryHeader.astro', library_header)]:
    if '/manage/' in text or '>管理<' in text:
        errors.append(f'{path}: standalone management navigation must not return')

category_page = require('src/components/CategoryPage.astro', ["import CategoryContentEditor from './CategoryContentEditor.astro'",'data-category-edit=','data-category-body-edit','?edit=body','本文編集','タイトル編集'])
category_editor = require('src/components/CategoryContentEditor.astro', ['id="category-editor-create-folder"','data-category-panel="meta"','data-category-panel="move"','data-category-panel="delete"','class="category-editor-required"','id="category-editor-create-save" type="button" disabled'])
if 'data-category-panel="body"' in category_editor or 'data-category-tab="body"' in category_editor:
    errors.append('CategoryContentEditor.astro: body editing must not live in the metadata modal')

content_editor = require('src/components/ContentEditor.astro', ['id="content-editor-open"','タイトル編集','id="article-edit-mode"','本文編集','data-editor-panel="meta"','data-editor-panel="move"','class="content-editor-required"'])
if 'data-editor-panel="body"' in content_editor or 'data-editor-tab="body"' in content_editor:
    errors.append('ContentEditor.astro: body editing must not live in the metadata modal')

require('src/components/ArticleBodyEditor.astro', ['id="article-body-editor"','id="article-body-editor-textarea"','data-md-tool="h2"','data-md-tool="bold"','data-md-tool="link"',"import '../scripts/article-body-editor.js'"])
article_body_script = require('src/scripts/article-body-editor.js', ["fetch('/api/manage/body'",'expectedSourceSha','article-body-editing','本文編集中','data-md-tool','edit'])
body_css = require('src/styles/article-body-editor.css', ['.article-body-editor{','.article-body-editing #article-rendered-body{display:none!important}','@media print'])
if '.article-body-editing #content{display:none!important}' in body_css:
    errors.append('article-body-editor.css: body editing must keep #content in place rather than hiding the article container')
worker = require('src/index.js', ["'/api/manage/body':manageBody","action==='read'","action==='save'",'source_changed_reload','env.GITHUB_TOKEN','github_token_not_configured'])
if 'X-GitHub-Token' in worker:
    errors.append('src/index.js: browser-provided GitHub tokens must not be accepted')
require('src/manage-content.js', ['export function extractBodySource','export function updateBodySource'])
layout = require('src/layouts/ArticleLayout.astro', ["import ArticleBodyEditor from '../components/ArticleBodyEditor.astro'",'<article class="content" id="content"><ArticleBodyEditor entry={entry} /><div id="article-rendered-body"><slot /></div></article>','id="article-pdf-export"'])
if '<ArticleBodyEditor entry={entry} /><article class="content"' in layout:
    errors.append('ArticleLayout.astro: body editor must live inside the article content region')
category_script = require('src/scripts/category-content-editor.js', ["post('/api/manage/metadata'","post('/api/manage/move'","post('/api/manage/delete'","post('/api/manage/create-directory'",'function updateCreateValidity()'])
content_script = require('src/scripts/content-editor.js', ["post('/api/manage/metadata'","post('/api/manage/move'",'function updateCreateValidity()'])
for path, text in [('src/scripts/article-body-editor.js', article_body_script), ('src/scripts/category-content-editor.js', category_script), ('src/scripts/content-editor.js', content_script)]:
    for forbidden in ['X-GitHub-Token','learn-github-token','Fine-grained Token','sessionStorage']:
        if forbidden in text:
            errors.append(f'{path}: browser GitHub token handling must be removed: {forbidden}')

legacy_paths = ['_config.yml','_layouts','Gemfile','Gemfile.lock','.ruby-version','index.html','commerce.html','identity.html','payments.html','notes.html','src/pages/manage','src/scripts/manage.js','src/styles/manage.css']
for legacy in legacy_paths:
    if (ROOT / legacy).exists():
        errors.append(f'legacy or standalone management source must be removed: {legacy}')

front_re = re.compile(r'^---\n(.*?)\n---(?:\n|$)', re.DOTALL)
for path in sorted((ROOT / 'contents').rglob('*.md')):
    text = path.read_text(encoding='utf-8')
    match = front_re.match(text)
    if match and re.search(r'^layout\s*:', match.group(1), re.MULTILINE):
        errors.append(f'legacy Jekyll layout metadata must be removed: {path}')

workflow = require('.github/workflows/deploy-cloudflare.yml', ['npm run build','Category inline management smoke test','node --check src/scripts/article-body-editor.js','Deploy exactly the verified _site to Cloudflare'])
for forbidden in ['ruby/setup-ruby','bundle install','bundle exec','jekyll','src/scripts/manage.js']:
    if forbidden in workflow:
        errors.append(f'deploy workflow contains removed dependency: {forbidden}')

if errors:
    raise RuntimeError('Astro source global header contract failed:\n- ' + '\n- '.join(errors))

print('Astro source contract OK: GitHub links remain in both headers, GitHub write credentials remain server-side, タイトル編集 stays modal-based, 本文編集 replaces the rendered article body in place, folder required-field gating is present, and standalone management/Jekyll sources are absent.')
