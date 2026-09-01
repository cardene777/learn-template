const dataEl=document.getElementById('content-editor-data');
if(dataEl){
  const state=JSON.parse(dataEl.textContent||'{}');
  const current=state.current;
  const catalog=state.catalog||[];
  const directChildren=Number(state.directChildren||0);
  const buildSha=String(state.buildSha||'');
  const dialog=document.getElementById('content-editor-dialog');
  const open=document.getElementById('content-editor-open');
  const close=document.getElementById('content-editor-close');
  const title=document.getElementById('content-editor-title');
  const description=document.getElementById('content-editor-description');
  const order=document.getElementById('content-editor-order');
  const status=document.getElementById('content-editor-status');
  const target=document.getElementById('content-editor-target');
  const moveOrder=document.getElementById('content-editor-move-order');
  const destination=document.getElementById('content-editor-destination');
  const moveStatus=document.getElementById('content-editor-move-status');
  const moveSave=document.getElementById('content-editor-save-move');
  const lock=document.getElementById('content-editor-lock');
  const bodyTextarea=document.getElementById('content-editor-body');
  const bodyStatus=document.getElementById('content-editor-body-status');
  const bodySave=document.getElementById('content-editor-save-body');
  let bodySourceSha='';

  async function post(path,payload){
    const r=await fetch(path,{method:'POST',credentials:'same-origin',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
    const responseBody=await r.json().catch(()=>({}));
    if(!r.ok){
      const labels={github_token_not_configured:'サーバー側のGitHub Tokenが設定されていません。Cloudflare Worker SecretのGITHUB_TOKENを設定してください。',github_auth_failed:'サーバー側のGitHub Tokenの権限または有効期限を確認してください。',placement_locked:'配置ロック中です。先にロック解除してください。',directory_cross_collection_move:'フォルダは現在同じCollection内で移動できます。',destination_exists:'移動先Source fileは既に存在します。',directory_cycle:'自分自身または子フォルダの配下へは移動できません。',route_exists:'同じURLのフォルダが既に存在します。',source_exists:'同じMetadata fileが既に存在します。',directory_not_empty:'子要素があるフォルダは削除できません。中身を移動または削除してください。',invalid_delete_confirmation:'確認IDが一致しません。',directory_route_missing:'対応するRouteが見つからないため削除を中止しました。',stale_page_reload:'この画面の生成後にmainが更新されています。再読み込みしてから削除してください。',source_changed_reload:'記事本文が別の更新で変更されています。ページを再読み込みしてから編集してください。',invalid_body:'本文を空にはできません。',body_too_large:'本文が大きすぎます。',not_note:'本文編集はNoteだけで利用できます。'};
      throw new Error(labels[responseBody.error]||responseBody.error||`操作に失敗しました (${r.status})`)
    }
    return responseBody
  }

  const descendants=new Set();
  function collect(id){for(const item of catalog.filter(x=>x.directoryId===id)){if(item.type==='Directory'&&!descendants.has(item.id)){descendants.add(item.id);collect(item.id)}}}
  if(current?.type==='Directory')collect(current.id);
  function opt(value,label){const o=document.createElement('option');o.value=value;o.textContent=label;return o}
  function fillTargets(){
    if(!target||!current)return;
    target.replaceChildren();
    const roots=[];const seen=new Set();
    for(const item of catalog){if(!item.domainId)continue;const key=`${item.domainId}|${item.collectionId||''}`;if(seen.has(key))continue;seen.add(key);roots.push({key,domainId:item.domainId,domainName:item.domainName,collectionId:item.collectionId||'',collectionName:item.collectionName||''})}
    const rg=document.createElement('optgroup');rg.label='トップ / Collection root';
    for(const r of roots){if(current.type==='Directory'&&(r.domainId!==current.domainId||r.collectionId!==current.collectionId))continue;rg.append(opt(`root:${r.key}`,r.collectionId?`${r.domainName} / ${r.collectionName}`:`${r.domainName} / トップ`))}
    target.append(rg);
    const dg=document.createElement('optgroup');dg.label='フォルダ';
    for(const d of catalog.filter(x=>x.type==='Directory')){if(d.id===current.id||descendants.has(d.id))continue;if(current.type==='Directory'&&(d.domainId!==current.domainId||d.collectionId!==current.collectionId))continue;dg.append(opt(`dir:${d.sourcePath}`,`${d.domainName} / ${d.collectionName} / ${d.title}`))}
    target.append(dg);
    const currentValue=current.directoryId?`dir:${catalog.find(x=>x.id===current.directoryId)?.sourcePath||''}`:`root:${current.domainId}|${current.collectionId||''}`;
    target.value=currentValue
  }

  const deleteOpen=document.getElementById('content-editor-delete-open');
  function resetBody(){bodySourceSha='';if(bodyTextarea)bodyTextarea.value='';if(bodyStatus)bodyStatus.textContent='';if(bodySave)bodySave.disabled=true}
  async function loadBody(){
    if(!current||current.type==='Directory'||!bodyTextarea||!bodyStatus||!bodySave)return;
    if(bodySourceSha)return;
    try{bodyStatus.textContent='本文を読み込み中…';bodySave.disabled=true;const result=await post('/api/manage/body',{action:'read',path:current.sourcePath});bodyTextarea.value=String(result.body||'');bodySourceSha=String(result.source_sha||'');bodyStatus.textContent='元Markdown本文を読み込みました。';bodySave.disabled=!bodySourceSha||!bodyTextarea.value.trim()}
    catch(e){bodyStatus.textContent=e instanceof Error?e.message:'本文の読み込みに失敗しました。';bodySave.disabled=true}
  }
  function hydrate(){
    if(!current)return;
    title.value=current.title;description.value=current.description;order.value=String(current.order);moveOrder.value=String(current.order);destination.value=current.sourcePath;lock.hidden=!(current.type!=='Directory'&&current.placementLocked);moveSave.disabled=current.type!=='Directory'&&current.placementLocked;if(deleteOpen)deleteOpen.disabled=(current.type==='Directory'&&directChildren>0)||(current.type!=='Directory'&&current.placementLocked);fillTargets();resetBody()
  }
  open?.addEventListener('click',()=>{hydrate();dialog.showModal()});
  close?.addEventListener('click',()=>dialog.close());
  dialog?.addEventListener('click',e=>{if(e.target===dialog)dialog.close()});
  for(const tab of document.querySelectorAll('[data-editor-tab]'))tab.addEventListener('click',()=>{for(const b of document.querySelectorAll('[data-editor-tab]'))b.classList.toggle('active',b===tab);for(const p of document.querySelectorAll('[data-editor-panel]'))p.hidden=p.dataset.editorPanel!==tab.dataset.editorTab;if(tab.dataset.editorTab==='body')loadBody()});

  document.getElementById('content-editor-save-meta')?.addEventListener('click',async()=>{try{status.textContent='保存中…';await post('/api/manage/metadata',{path:current.sourcePath,title:title.value.trim(),description:description.value.trim(),order:Number(order.value)});status.textContent='保存しました。CI反映後にページが更新されます。';setTimeout(()=>location.reload(),900)}catch(e){status.textContent=e instanceof Error?e.message:'保存に失敗しました。'}});
  bodyTextarea?.addEventListener('input',()=>{if(bodySave)bodySave.disabled=!bodySourceSha||!bodyTextarea.value.trim()});
  bodySave?.addEventListener('click',async()=>{if(!bodySourceSha||!bodyTextarea.value.trim())return;try{bodySave.disabled=true;bodyStatus.textContent='本文の保存Commitを作成中…';await post('/api/manage/body',{action:'save',path:current.sourcePath,body:bodyTextarea.value,expectedSourceSha:bodySourceSha});bodyStatus.textContent='本文を保存しました。CI反映後にページを更新します。';setTimeout(()=>location.reload(),900)}catch(e){bodyStatus.textContent=e instanceof Error?e.message:'本文の保存に失敗しました。';bodySave.disabled=false}});
  document.getElementById('content-editor-unlock')?.addEventListener('click',async()=>{try{moveStatus.textContent='ロック解除中…';await post('/api/manage/placement-lock',{path:current.sourcePath,locked:false});current.placementLocked=false;lock.hidden=true;moveSave.disabled=false;if(deleteOpen)deleteOpen.disabled=false;moveStatus.textContent='解除しました。移動・削除は次のCommitとして実行できます。'}catch(e){moveStatus.textContent=e instanceof Error?e.message:'解除に失敗しました。'}});
  moveSave?.addEventListener('click',async()=>{const value=target.value;const payload={path:current.sourcePath,order:Number(moveOrder.value),destinationPath:destination.value.trim()};if(value.startsWith('dir:'))payload.targetDirectoryPath=value.slice(4);else{const [domainId,collectionId='']=value.slice(5).split('|');const ref=catalog.find(x=>x.domainId===domainId&&(x.collectionId||'')===collectionId);payload.root={domainId,domainName:ref?.domainName||domainId,collectionId:collectionId||null,collectionName:ref?.collectionName||null}}try{moveStatus.textContent='移動Commitを作成中…';await post('/api/manage/move',payload);moveStatus.textContent='移動しました。CI反映後に再読み込みします。';setTimeout(()=>location.reload(),1000)}catch(e){moveStatus.textContent=e instanceof Error?e.message:'移動に失敗しました。'}});

  const deleteDialog=document.getElementById('content-editor-delete-dialog');const deleteClose=document.getElementById('content-editor-delete-close');const deleteConfirm=document.getElementById('content-editor-delete-confirm');const deleteSave=document.getElementById('content-editor-delete-save');const deleteStatus=document.getElementById('content-editor-delete-status');
  deleteOpen?.addEventListener('click',()=>{if(deleteOpen.disabled)return;deleteConfirm.value='';deleteSave.disabled=true;deleteStatus.textContent='';deleteDialog.showModal();setTimeout(()=>deleteConfirm.focus(),0)});deleteClose?.addEventListener('click',()=>deleteDialog.close());deleteDialog?.addEventListener('click',e=>{if(e.target===deleteDialog)deleteDialog.close()});deleteConfirm?.addEventListener('input',()=>{deleteSave.disabled=deleteConfirm.value.trim()!==current.id});
  deleteSave?.addEventListener('click',async()=>{if(deleteConfirm.value.trim()!==current.id)return;try{deleteSave.disabled=true;deleteStatus.textContent='削除Commitを作成中…';await post('/api/manage/delete',{path:current.sourcePath,confirmId:current.id,expectedChildCount:directChildren,buildSha});deleteStatus.textContent='削除しました。CI反映後に一覧へ戻ります。';const parent=current.directoryId?catalog.find(x=>x.id===current.directoryId):null;const href=parent?.permalink||`/${current.domainId}/`;setTimeout(()=>location.assign(href),900)}catch(e){deleteStatus.textContent=e instanceof Error?e.message:'削除に失敗しました。';deleteSave.disabled=false}});

  const createDialog=document.getElementById('content-editor-create-dialog');const createOpen=document.getElementById('content-editor-create-child');const createClose=document.getElementById('content-editor-create-close');const cid=document.getElementById('content-editor-create-id');const ctitle=document.getElementById('content-editor-create-title');const cdesc=document.getElementById('content-editor-create-description');const corder=document.getElementById('content-editor-create-order');const cpermalink=document.getElementById('content-editor-create-permalink');const csource=document.getElementById('content-editor-create-source');const cstatus=document.getElementById('content-editor-create-status');const createSave=document.getElementById('content-editor-create-save');
  function createValid(){if(!cid||!ctitle||!cdesc||!corder||!cpermalink||!csource)return false;const id=cid.value.trim(),orderValue=Number(corder.value),permalink=cpermalink.value.trim(),source=csource.value.trim();return /^[A-Za-z0-9][A-Za-z0-9._-]*$/.test(id)&&Boolean(ctitle.value.trim())&&Boolean(cdesc.value.trim())&&corder.value!==''&&Number.isInteger(orderValue)&&orderValue>=0&&orderValue<=999999&&/^\/[A-Za-z0-9._/-]+\/$/.test(permalink)&&!permalink.includes('..')&&!permalink.includes('//')&&/^contents\/[A-Za-z0-9._/-]+\.md$/.test(source)&&!source.includes('..')&&!source.includes('//')}
  function updateCreateValidity(){if(createSave)createSave.disabled=!createValid()}
  function suggest(){if(!current||!cid)return;const id=cid.value.trim();if(!id){cpermalink.value='';csource.value='';updateCreateValidity();return}cpermalink.value=`${current.permalink.replace(/\/$/,'')}/${id}/`;csource.value=`${current.sourcePath.split('/').slice(0,-1).join('/')}/${id}-directory.md`;updateCreateValidity()}
  createOpen?.addEventListener('click',()=>{cid.value='';ctitle.value='';cdesc.value='';corder.value='10';cpermalink.value='';csource.value='';cstatus.textContent='';updateCreateValidity();createDialog.showModal()});
  createClose?.addEventListener('click',()=>createDialog.close());
  createDialog?.addEventListener('click',e=>{if(e.target===createDialog)createDialog.close()});
  cid?.addEventListener('input',suggest);
  for(const el of [ctitle,cdesc,corder,cpermalink,csource])el?.addEventListener('input',updateCreateValidity);
  createSave?.addEventListener('click',async()=>{if(createSave.disabled)return;try{createSave.disabled=true;cstatus.textContent='作成中…';await post('/api/manage/create-directory',{parentDirectoryPath:current.sourcePath,id:cid.value.trim(),title:ctitle.value.trim(),description:cdesc.value.trim(),order:Number(corder.value),permalink:cpermalink.value.trim(),sourcePath:csource.value.trim()});cstatus.textContent='作成しました。CI反映後に表示されます。';setTimeout(()=>location.reload(),1000)}catch(e){cstatus.textContent=e instanceof Error?e.message:'作成に失敗しました。';updateCreateValidity()}})
}
