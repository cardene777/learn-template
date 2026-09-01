import fs from 'node:fs';
import YAML from 'yaml';

export const DOMAINS = {
  'example-a': { id: 'example-a', name: 'サンプルA', eyebrow: 'EXAMPLE A' },
  'example-b': { id: 'example-b', name: 'サンプルB', eyebrow: 'EXAMPLE B' },
  'example-c': { id: 'example-c', name: 'サンプルC', eyebrow: 'EXAMPLE C' },
} as const;

export function permalink(entry: any): string {
  return String(entry?.data?.permalink || '/');
}

export function routeParam(entry: any): string {
  const url = permalink(entry);
  const clean = url.replace(/^\/+/, '');
  if (clean.endsWith('.html')) return clean.slice(0, -5);
  const directory = clean.replace(/\/+$/, '');
  return directory ? `${directory}/index` : 'index';
}

export function orderOf(entry: any): number {
  const value = Number(entry?.data?.order);
  return Number.isFinite(value) ? value : 999999;
}

export function sortByOrder<T = any>(items: T[]): T[] {
  return [...items].sort((a: any, b: any) => orderOf(a) - orderOf(b) || String(a?.data?.title || '').localeCompare(String(b?.data?.title || ''), 'ja'));
}

export function noteKind(entry: any): string {
  if (entry?.data?.noteKind) return String(entry.data.noteKind);
  return String(entry?.data?.title || '').includes('仕組み') ? '仕組み' : '概要';
}

let changesCache: Record<string, any[]> | null = null;
export function articleChanges(): Record<string, any[]> {
  if (changesCache) return changesCache;
  const source = fs.readFileSync('_data/article_changes.yml', 'utf8');
  changesCache = YAML.parse(source) || {};
  return changesCache;
}

export function sourcePathFromEntry(entry: any): string {
  return `contents/${String(entry.id || '').replace(/^\/+/, '')}`;
}
