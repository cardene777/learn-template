const dataEl=document.getElementById('article-body-editor-data');
if(dataEl){
  const state=JSON.parse(dataEl.textContent||'{}');
  const path=String(state.path||'');
  const trigger=document.getElementById('article-edit-mode');
  const panel=document.getElementById('article-body-editor');
  const rendered=document.getElementById('article-rendered-body');
  const content=document.getElementById('content');
  const textarea=document.getElementById('article-body-editor-textarea');
  const status=document.getElementById('article-body-editor-status');
  const stateLabel=document.getElementById('article-body-editor-state');
  const save=document.getElementById('article-body-editor-save');
  const cancel=document.getElementById('article-body-editor-cancel');
  let sourceSha='';
  let originalBody='';
  let active=false;
  let loading=false;

  async function post(payload){
    const response=await fetch('/api/manage/body',{method:'POST',credentials:'same-origin',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
    const body=await response.json().catch(()=>({}));
    if(!response.ok){const labels={github_token_not_configured:'サーバー側のGitHub Tokenが設定されていません。Cloudflare Worker SecretのGITHUB_TOKENを設定してください。',github_auth_failed:'サーバー側のGitHub Tokenの権限または有効期限を確認してください。',source_changed_reload:'記事本文が別の更新で変更されています。ページを再読み込みしてから編集してください。',invalid_body:'本文を空にはできません。',body_too_large:'本文が大きすぎます。',not_note:'本文編集はNoteだけで利用できます。',source_not_found:'元Markdownが見つかりません。'};throw new Error(labels[body.error]||body.error||`操作に失敗しました (${response.status})`)}
    return body
  }
  function updateSave(){if(!save||!textarea)return;save.disabled=loading||!sourceSha||!textarea.value.trim()||textarea.value===originalBody}
  function setMode(enabled){
    active=enabled;
    document.body.classList.toggle('article-body-editing',enabled);
    if(panel)panel.hidden=!enabled;
    trigger?.setAttribute('aria-pressed',enabled?'true':'false');
    if(trigger)trigger.textContent=enabled?'本文編集中':'本文編集';
    if(enabled){content?.scrollIntoView({behavior:'smooth',block:'start'});setTimeout(()=>textarea?.focus(),100)}
  }
  async function enter(){
    if(active||loading||!path||!panel||!textarea)return;
    const renderedHeight=rendered?.getBoundingClientRect().height||0;
    if(renderedHeight>0)textarea.style.minHeight=`${Math.max(560,Math.min(Math.round(renderedHeight),1400))}px`;
    setMode(true);loading=true;sourceSha='';originalBody='';textarea.value='';textarea.disabled=true;if(status)status.textContent='元Markdown本文を読み込み中…';if(stateLabel)stateLabel.textContent='読込中';updateSave();
    try{const result=await post({action:'read',path});sourceSha=String(result.source_sha||'');originalBody=String(result.body||'');textarea.value=originalBody;textarea.disabled=false;if(status)status.textContent='この本文エリアでMarkdownを直接編集できます。⌘/Ctrl + Sでも保存できます。';if(stateLabel)stateLabel.textContent='編集中'}
    catch(error){textarea.disabled=true;if(status)status.textContent=error instanceof Error?error.message:'本文の読み込みに失敗しました。';if(stateLabel)stateLabel.textContent='読込失敗'}
    finally{loading=false;updateSave()}
  }
  function exit(){
    if(!active)return;
    if(textarea&&textarea.value!==originalBody&&!confirm('保存していない本文の変更を破棄しますか？'))return;
    setMode(false);sourceSha='';originalBody='';if(textarea){textarea.value='';textarea.disabled=false;textarea.style.minHeight=''}if(status)status.textContent='本文編集を開始すると元Markdownを読み込みます。';if(stateLabel)stateLabel.textContent='';updateSave()
  }
  function replaceSelection(before,after=before,placeholder='テキスト'){
    if(!textarea||textarea.disabled)return;
    const start=textarea.selectionStart,end=textarea.selectionEnd,selected=textarea.value.slice(start,end)||placeholder;
    textarea.setRangeText(before+selected+after,start,end,'select');textarea.selectionStart=start+before.length;textarea.selectionEnd=start+before.length+selected.length;textarea.focus();textarea.dispatchEvent(new Event('input',{bubbles:true}))
  }
  function prefixLines(prefix){
    if(!textarea||textarea.disabled)return;
    const value=textarea.value,start=textarea.selectionStart,end=textarea.selectionEnd,lineStart=value.lastIndexOf('\n',Math.max(0,start-1))+1,lineEnd=value.indexOf('\n',end)<0?value.length:value.indexOf('\n',end);
    const block=value.slice(lineStart,lineEnd).split('\n').map(line=>prefix+line).join('\n');textarea.setRangeText(block,lineStart,lineEnd,'select');textarea.focus();textarea.dispatchEvent(new Event('input',{bubbles:true}))
  }
  function heading(prefix){if(!textarea||textarea.disabled)return;const value=textarea.value,start=textarea.selectionStart,lineStart=value.lastIndexOf('\n',Math.max(0,start-1))+1;textarea.setRangeText(prefix,lineStart,lineStart,'end');textarea.focus();textarea.dispatchEvent(new Event('input',{bubbles:true}))}
  function tool(name){if(name==='h2')return heading('## ');if(name==='h3')return heading('### ');if(name==='bold')return replaceSelection('**','**','太字');if(name==='link')return replaceSelection('[','](https://)','リンクテキスト');if(name==='list')return prefixLines('- ');if(name==='quote')return prefixLines('> ');if(name==='code')return replaceSelection('`','`','code');if(name==='codeblock')return replaceSelection('```text\n','\n```','code')}

  trigger?.addEventListener('click',()=>active?exit():enter());
  cancel?.addEventListener('click',exit);
  textarea?.addEventListener('input',updateSave);
  textarea?.addEventListener('keydown',event=>{if((event.metaKey||event.ctrlKey)&&event.key.toLowerCase()==='s'){event.preventDefault();if(save&&!save.disabled)save.click()}else if(event.key==='Tab'){event.preventDefault();const start=textarea.selectionStart,end=textarea.selectionEnd;textarea.setRangeText('  ',start,end,'end');textarea.dispatchEvent(new Event('input',{bubbles:true}))}});
  for(const button of document.querySelectorAll('[data-md-tool]'))button.addEventListener('click',()=>tool(button.dataset.mdTool));
  save?.addEventListener('click',async()=>{if(save.disabled||!sourceSha||!textarea?.value.trim())return;try{loading=true;updateSave();if(status)status.textContent='本文の保存Commitを作成中…';if(stateLabel)stateLabel.textContent='保存中';const result=await post({action:'save',path,body:textarea.value,expectedSourceSha:sourceSha});originalBody=textarea.value;sourceSha='';if(status)status.textContent=`保存しました。公開反映後に再読み込みすると新しい本文になります。${result.commit_sha?' Commit '+String(result.commit_sha).slice(0,8):''}`;if(stateLabel)stateLabel.textContent='保存済み'}catch(error){if(status)status.textContent=error instanceof Error?error.message:'本文の保存に失敗しました。';if(stateLabel)stateLabel.textContent='保存失敗'}finally{loading=false;updateSave()}});

  if(new URLSearchParams(location.search).get('edit')==='body')enter();
}
