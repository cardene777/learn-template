(() => {
  const el = document.getElementById('library-deploy-status');
  const text = el?.querySelector('.library-deploy-text');
  if (!el || !text) return;

  const endpoint = '/deploy-status.json';
  const active = new Set(['queued','in_progress','waiting','requested','pending']);
  const storageKey = 'learn-deploy-status-v5';
  let timer;

  function setState(kind, label, href, persist = true) {
    el.classList.remove('success','failed','updating');
    if (kind) el.classList.add(kind);
    text.textContent = label;
    if (href) el.href = href;

    if (persist) {
      try {
        localStorage.setItem(storageKey, JSON.stringify({
          kind,
          label,
          href: href || '',
          savedAt: Date.now(),
        }));
      } catch (_) {}
    }
  }

  function restoreState() {
    try {
      const cached = JSON.parse(localStorage.getItem(storageKey) || 'null');
      if (!cached) return false;
      setState(cached.kind || '', cached.label || '更新確認中…', cached.href || undefined, false);
      return true;
    } catch (_) {
      return false;
    }
  }

  function schedule(ms) {
    clearTimeout(timer);
    timer = setTimeout(refresh, ms);
  }

  async function refresh() {
    try {
      const response = await fetch(`${endpoint}?_=${Date.now()}`, {
        cache: 'no-store',
        headers: { Accept: 'application/json' },
      });

      if (!response.ok) throw new Error(`status request failed: ${response.status}`);

      const run = await response.json();
      if (!run?.ok) throw new Error(run?.error || 'status unavailable');

      if (active.has(run.status)) {
        setState('updating', run.status === 'queued' ? '更新待ち…' : '更新中…', run.html_url);
        schedule(5000);
        return;
      }

      if (run.status === 'completed' && run.conclusion === 'success') {
        setState('success', '最新反映済み', run.html_url);
        schedule(30000);
        return;
      }

      if (run.status === 'completed' && run.conclusion === 'cancelled') {
        setState('updating', '再更新待ち…', run.html_url);
        schedule(10000);
        return;
      }

      if (run.status === 'completed') {
        setState('failed', '更新失敗', run.html_url);
        schedule(30000);
        return;
      }

      setState('updating', '更新確認中…', run.html_url);
      schedule(10000);
    } catch (_) {
      setState('', '状態確認不可', undefined, false);
      schedule(30000);
    }
  }

  if (!restoreState()) {
    setState('updating', '更新確認中…', undefined, false);
  }

  refresh();
})();
