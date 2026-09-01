import fs from 'node:fs';
import path from 'node:path';
import { marked } from 'marked';

const ROOT = process.cwd();
const SOURCE = path.join(ROOT, 'contents');
const OUT = path.join(ROOT, '.astro-content');

fs.rmSync(OUT, { recursive: true, force: true });
fs.mkdirSync(OUT, { recursive: true });

const DETAIL_RE = /<details>\s*\n<summary>(?<summary>[^\n<>]+)<\/summary>\s*\n(?<body>[\s\S]*?)\n<\/details>/g;
const DEFINITION_ITEM_RE = /<li>\s*<(strong|code)>([\s\S]*?)<\/\1>\s*:\s*([\s\S]*?)<\/li>/g;

let files = 0;
let details = 0;

function compileDetails(source, rel) {
  return source.replace(DETAIL_RE, (...args) => {
    const groups = args.at(-1);
    if (!groups?.summary) throw new Error(`${rel}: unsupported details block`);
    details += 1;
    const summary = groups.summary.trim()
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;');
    let html = marked.parse(groups.body, { gfm: true, breaks: false });
    html = html.replace(DEFINITION_ITEM_RE, (_m, tag, label, description) => (
      `<li class="details-definition"><${tag}>${label}</${tag}><span class="details-definition-description">${description}</span></li>`
    ));
    return `<details>\n<summary>${summary}</summary>\n${html.trim()}\n</details>`;
  });
}

function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const abs = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      walk(abs);
      continue;
    }
    if (!entry.name.endsWith('.md') || entry.name === 'README.md') continue;
    const rel = path.relative(SOURCE, abs);
    const target = path.join(OUT, rel);
    fs.mkdirSync(path.dirname(target), { recursive: true });
    const source = fs.readFileSync(abs, 'utf8');
    fs.writeFileSync(target, compileDetails(source, rel), 'utf8');
    files += 1;
  }
}

walk(SOURCE);
console.log(`Prepared Astro content: ${files} Markdown files / ${details} details blocks.`);
