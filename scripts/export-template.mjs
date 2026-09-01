import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const OUT = path.join(ROOT, '_template-repo');
const SOURCE_REPOSITORY = '__LEARN_REPOSITORY__';
const SOURCE_OWNER = 'template-owner';
const DISTRIBUTION_REPOSITORY_MARKER = '__LEARN_REPOSITORY__';

const COPY_PATHS = [
  '.github',
  '.codex/skills',
  'assets',
  'src',
  'scripts',
  'docs/authoring-workflow.md',
  'docs/technical-explanation-prompt-template.md',
  'docs/setup.md',
  '.gitignore',
  'astro.config.mjs',
  'package.json',
  'tsconfig.json',
  'wrangler.jsonc',
];

const TEXT_EXTENSIONS = new Set([
  '.astro', '.css', '.html', '.js', '.json', '.jsonc', '.md', '.mjs', '.py',
  '.sh', '.svg', '.txt', '.yaml', '.yml',
]);

function copy(relativePath) {
  const source = path.join(ROOT, relativePath);
  const target = path.join(OUT, relativePath);
  if (!fs.existsSync(source)) {
    throw new Error(`Template export source is missing: ${relativePath}`);
  }
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.cpSync(source, target, { recursive: true });
}

function stripContentSpecificDirectoryRoutes(directory) {
  if (!fs.existsSync(directory)) return 0;
  let removed = 0;
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const target = path.join(directory, entry.name);
    if (entry.isDirectory()) {
      removed += stripContentSpecificDirectoryRoutes(target);
      if (fs.readdirSync(target).length === 0) fs.rmdirSync(target);
      continue;
    }
    if (!entry.name.endsWith('.astro')) continue;
    const source = fs.readFileSync(target, 'utf8');
    if (source.includes('DirectoryRoute') && /<DirectoryRoute\s+id=["'][^"']+["']\s*\/>/.test(source)) {
      fs.rmSync(target);
      removed += 1;
    }
  }
  return removed;
}

function sanitizeDistributionIdentity(directory) {
  let changed = 0;
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const target = path.join(directory, entry.name);
    if (entry.isDirectory()) {
      changed += sanitizeDistributionIdentity(target);
      continue;
    }
    const extension = path.extname(entry.name).toLowerCase();
    if (!TEXT_EXTENSIONS.has(extension) && entry.name !== '.gitignore') continue;
    const source = fs.readFileSync(target, 'utf8');
    const sanitized = source
      .replaceAll(SOURCE_REPOSITORY, DISTRIBUTION_REPOSITORY_MARKER)
      .replaceAll(SOURCE_OWNER, 'template-owner');
    if (sanitized !== source) {
      fs.writeFileSync(target, sanitized, 'utf8');
      changed += 1;
    }
  }
  return changed;
}

fs.rmSync(OUT, { recursive: true, force: true });
fs.mkdirSync(OUT, { recursive: true });

for (const relativePath of COPY_PATHS) copy(relativePath);

fs.rmSync(path.join(OUT, '.github', 'workflows', 'publish-template.yml'), { force: true });

const removedDirectoryRoutes = stripContentSpecificDirectoryRoutes(path.join(OUT, 'src', 'pages'));

fs.copyFileSync(path.join(ROOT, 'template', 'README.md'), path.join(OUT, 'README.md'));
fs.mkdirSync(path.join(OUT, 'contents'), { recursive: true });
fs.cpSync(path.join(ROOT, 'template', 'contents'), path.join(OUT, 'contents'), { recursive: true });
fs.mkdirSync(path.join(OUT, '_data'), { recursive: true });
fs.writeFileSync(path.join(OUT, '_data', 'article_changes.yml'), '{}\n', 'utf8');
fs.mkdirSync(path.join(OUT, '.codex', 'research-runs'), { recursive: true });
fs.writeFileSync(path.join(OUT, '.codex', 'research-runs', '.gitkeep'), '', 'utf8');

const packagePath = path.join(OUT, 'package.json');
const packageJson = JSON.parse(fs.readFileSync(packagePath, 'utf8'));
delete packageJson.scripts?.['template:export'];
delete packageJson.scripts?.['template:check'];
fs.writeFileSync(packagePath, JSON.stringify(packageJson, null, 2) + '\n', 'utf8');

for (const relativePath of ['node_modules', 'dist', '_site', '.astro', '.astro-content', '_archive', 'template']) {
  fs.rmSync(path.join(OUT, relativePath), { recursive: true, force: true });
}

const sanitizedFiles = sanitizeDistributionIdentity(OUT);

console.log(`Distribution template exported to ${path.relative(ROOT, OUT)}/ (${removedDirectoryRoutes} private Directory routes removed, ${sanitizedFiles} identity-bearing files sanitized)`);
