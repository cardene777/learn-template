const el=document.getElementById('article-library-deploy-status');
const text=el?.querySelector('.article-library-deploy-text');
if(el&&text){
  const endpoint='https://api.github.com/repos/__LEARN_REPOSITORY__/actions/workflows/deploy-cloudflare.yml/runs?branch=main&per_page=1';
  const active=new Set(['queued','in_progress','waiting','requested','pending']);
  const render=run=>{
    el.classList.remove('success','failed','updating');
    if(run?.html_url)el.href=run.html_url;
    if(run&&active.has(run.status)){el.classList.add('updating');text.textContent='更新中';return;}
    if(run?.status==='completed'&&run.conclusion==='success'){el.classList.add('success');text.textContent='反映済み';return;}
    if(run?.status==='completed'&&run.conclusion&&!['cancelled','skipped'].includes(run.conclusion)){el.classList.add('failed');text.textContent='更新失敗';return;}
    text.textContent='状態確認';
  };
  fetch(endpoint,{headers:{Accept:'application/vnd.github+json'}})
    .then(r=>{if(!r.ok)throw new Error(String(r.status));return r.json();})
    .then(data=>render(Array.isArray(data.workflow_runs)?data.workflow_runs[0]:null))
    .catch(()=>{text.textContent='状態確認';});
}
