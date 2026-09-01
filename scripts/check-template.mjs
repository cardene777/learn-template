import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

const ROOT = process.cwd();
const OUT = path.join(ROOT, '_template-repo');

function run(command, args, cwd = ROOT, env = process.env) {
  const result = spawnSync(command, args, {
    cwd,
    env,
    stdio: 'inherit',
    shell: false,
  });
  if (result.status !== 0) {
    throw new Error(`${command} ${args.join(' ')} failed with status ${result.status}`);
  }
}

function filesUnder(directory) {
  const files = [];
  if (!fs.existsSync(directory)) return files;
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const target = path.join(directory, entry.name);
    if (entry.isDirectory()) files.push(...filesUnder(target));
    else files.push(target);
  }
  return files;
}

run(process.execPath, ['scripts/export-template.mjs']);

for (const forbidden of [
  '_archive',
  'template',
  '.codex/research-runs/ap2.json',
  '.github/workflows/publish-template.yml',
  'docs/fork-deployment.md',
  '.env',
  '.dev.vars',
  '.wrangler',
]) {
  if (fs.existsSync(path.join(OUT, forbidden))) {
    throw new Error(`Distribution template contains forbidden source data: ${forbidden}`);
  }
}

for (const required of [
  'README.md',
  'docs/setup.md',
  '.github/workflows/deploy-cloudflare.yml',
  '.codex/skills/skill-creator/SKILL.md',
  '.codex/skills/learn-deployer/SKILL.md',
  '.codex/skills/learn-deployer/references/troubleshooting.md',
  '.codex/skills/learn-deployer/evals/evals.json',
]) {
  if (!fs.existsSync(path.join(OUT, required))) {
    throw new Error(`Distribution template is missing required file: ${required}`);
  }
}

const exportedFiles = filesUnder(OUT);
for (const file of exportedFiles) {
  const relative = path.relative(OUT, file);
  const basename = path.basename(file);
  if ((basename === '.env' || basename.startsWith('.env.')) && basename !== '.env.example') {
    throw new Error(`Distribution template contains environment file: ${relative}`);
  }
  if (basename === '.dev.vars' || basename.startsWith('.dev.vars.')) {
    throw new Error(`Distribution template contains Wrangler local secret file: ${relative}`);
  }
}

const secretPatterns = [
  ['source owner identity', /template-owner/i],
  ['GitHub fine-grained token', /\bgithub_pat_[A-Za-z0-9_]{20,}\b/],
  ['GitHub token', /\bgh[pousr]_[A-Za-z0-9]{20,}\b/],
  ['AWS access key', /\bAKIA[0-9A-Z]{16}\b/],
  ['private key', /-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/],
];
for (const file of exportedFiles) {
  const relative = path.relative(OUT, file);
  const text = fs.readFileSync(file).toString('utf8');
  for (const [label, pattern] of secretPatterns) {
    if (pattern.test(text)) {
      throw new Error(`Distribution template public-safety scan found ${label}: ${relative}`);
    }
  }
}

const gitignore = fs.readFileSync(path.join(OUT, '.gitignore'), 'utf8');
for (const required of ['.env', '.dev.vars', '.wrangler/', '*.secrets.json']) {
  if (!gitignore.split(/\r?\n/).includes(required)) {
    throw new Error(`Distribution .gitignore must protect local secrets: ${required}`);
  }
}

const deployerSkill = fs.readFileSync(path.join(OUT, '.codex/skills/learn-deployer/SKILL.md'), 'utf8');
for (const required of [
  'name: learn-deployer',
  'docs/setup.md',
  'references/troubleshooting.md',
  'Secret値をチャットへ貼らせない',
  'E2E Verification',
]) {
  if (!deployerSkill.includes(required)) {
    throw new Error(`learn-deployer contract is missing: ${required}`);
  }
}

const deployerEvals = JSON.parse(fs.readFileSync(path.join(OUT, '.codex/skills/learn-deployer/evals/evals.json'), 'utf8'));
if (deployerEvals.skill_name !== 'learn-deployer') {
  throw new Error('learn-deployer evals use the wrong skill_name');
}
if (!Array.isArray(deployerEvals.evals) || deployerEvals.evals.length < 4) {
  throw new Error('learn-deployer must keep bootstrap, resume, existing-secret, and secret-safety eval coverage');
}

for (const page of filesUnder(path.join(OUT, 'src', 'pages')).filter((file) => file.endsWith('.astro'))) {
  const source = fs.readFileSync(page, 'utf8');
  if (source.includes('DirectoryRoute') && /<DirectoryRoute\s+id=["'][^"']+["']\s*\/>/.test(source)) {
    throw new Error(`Private content-specific Directory route leaked into distribution: ${path.relative(OUT, page)}`);
  }
}

const packageJson = JSON.parse(fs.readFileSync(path.join(OUT, 'package.json'), 'utf8'));
for (const command of ['template:export', 'template:check']) {
  if (packageJson.scripts?.[command]) {
    throw new Error(`Source-only npm command leaked into distribution package.json: ${command}`);
  }
}

const markdown = [];
function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const target = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(target);
    else if (entry.name.endsWith('.md')) markdown.push(target);
  }
}
walk(path.join(OUT, 'contents'));
if (markdown.length !== 3) {
  throw new Error(`Expected exactly 3 sample notes, found ${markdown.length}`);
}
if (!markdown.every((file) => path.basename(path.dirname(file)) === 'sample')) {
  throw new Error('Template contents must contain only sample notes');
}

const changes = fs.readFileSync(path.join(OUT, '_data', 'article_changes.yml'), 'utf8').trim();
if (changes !== '{}') {
  throw new Error('Template article_changes.yml must be empty');
}

const nodeModules = path.join(OUT, 'node_modules');
fs.rmSync(nodeModules, { recursive: true, force: true });
fs.symlinkSync(path.relative(OUT, path.join(ROOT, 'node_modules')), nodeModules, 'dir');

try {
  const env = {
    ...process.env,
    PUBLIC_BUILD_SHA: 'template-check',
    PUBLIC_SOURCE_REPOSITORY: 'example/learn',
  };
  run('npm', ['run', 'build'], OUT, env);
  run('python3', ['scripts/validate-content-metadata.py'], OUT, env);
  run('python3', ['scripts/validate-directories.py'], OUT, env);
  run('python3', ['scripts/validate-output-contract.py'], OUT, env);
  run('python3', ['scripts/validate-directory-ui.py'], OUT, env);
  run('python3', ['scripts/validate-term-toggles.py'], OUT, env);
} finally {
  fs.rmSync(nodeModules, { recursive: true, force: true });
}

console.log('Distribution template check OK: sanitized sample repository passes public-safety scan, builds, and validates successfully.');
