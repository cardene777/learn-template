import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { marked } from 'marked';

const ROOT = process.cwd();
const SOURCE = path.join(ROOT, 'contents');
const OUT = path.join(ROOT, '.astro-content');
const REPOSITORY_MARKER = '__LEARN_REPOSITORY__';
const WRANGLER_VERSION = '4.127.1';

function run(command, args, options = {}) {
  const result = spawnSync(command, args, {
    cwd: ROOT,
    stdio: 'inherit',
    shell: false,
    env: options.env || process.env,
  });
  if (result.status !== 0) throw new Error(`${command} ${args.join(' ')} failed with status ${result.status}`);
}

function capture(command, args) {
  const result = spawnSync(command, args, { cwd: ROOT, encoding: 'utf8', shell: false });
  return result.status === 0 ? String(result.stdout || '').trim() : '';
}

function githubRepositoryFromRemote(remote) {
  for (const pattern of [
    /^https:\/\/github\.com\/([^/]+)\/([^/]+?)(?:\.git)?$/i,
    /^git@github\.com:([^/]+)\/([^/]+?)(?:\.git)?$/i,
    /^ssh:\/\/git@github\.com\/([^/]+)\/([^/]+?)(?:\.git)?$/i,
  ]) {
    const match = String(remote || '').trim().match(pattern);
    if (match) return `${match[1]}/${match[2]}`;
  }
  return '';
}

function directDeploy() {
  const repository = String(process.env.LEARN_REPOSITORY || '').trim()
    || githubRepositoryFromRemote(capture('git', ['config', '--get', 'remote.origin.url']));
  if (!/^[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+$/.test(repository)) {
    throw new Error('Could not determine GitHub repository. Set LEARN_REPOSITORY=owner/repository and retry.');
  }

  const workerName = String(process.env.LEARN_WORKER_NAME || '').trim();
  const originals = new Map();
  const targets = [
    'src/index.js',
    'src/components/ArticleHeader.astro',
    'src/components/LibraryHeader.astro',
  ];

  for (const relative of targets) {
    const source = fs.readFileSync(relative, 'utf8');
    originals.set(relative, source);
    if (!source.includes(REPOSITORY_MARKER)) throw new Error(`${relative}: repository marker missing`);
    fs.writeFileSync(relative, source.replaceAll(REPOSITORY_MARKER, repository), 'utf8');
  }

  if (workerName) {
    const relative = 'wrangler.jsonc';
    const source = fs.readFileSync(relative, 'utf8');
    originals.set(relative, source);
    const updated = source.replace(/("name"\s*:\s*")[^"]+("\s*,)/, `$1${workerName}$2`);
    if (updated === source) throw new Error('wrangler.jsonc: Worker name could not be updated');
    fs.writeFileSync(relative, updated, 'utf8');
  }

  try {
    const env = {
      ...process.env,
      PUBLIC_BUILD_SHA: capture('git', ['rev-parse', 'HEAD']) || 'direct-deploy',
      PUBLIC_SOURCE_REPOSITORY: repository,
    };
    console.log(`Deploying ${repository}${workerName ? ` as Worker ${workerName}` : ''}`);
    run('npm', ['run', 'build'], { env });
    const args = ['--yes', `wrangler@${WRANGLER_VERSION}`, 'deploy', '--config', 'wrangler.jsonc'];
    const secretsFile = String(process.env.LEARN_SECRETS_FILE || '').trim();
    if (secretsFile) args.push('--secrets-file', secretsFile);
    run('npx', args, { env });
  } finally {
    for (const [relative, source] of originals) fs.writeFileSync(relative, source, 'utf8');
  }
}

if (process.argv.includes('--deploy-cloudflare')) {
  directDeploy();
  process.exit(0);
}

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
