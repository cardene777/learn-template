const dataEl=document.getElementById('category-editor-data');
if(dataEl){
  const state=JSON.parse(dataEl.textContent||'{}');
  const catalog=Array.isArray(state.catalog)?state.catalog:[];
  const domain=String(state.domain||'');
  const buildSha=String(state.buildSha||'');
  const byPath=new Map(catalog.map(item=>[item.sourcePath,item]));
  const dialog=document.getElementById('category-editor-dialog');
  const heading=document.getElementById('category-editor-heading');
  const title=document.getElementById('category-editor-title');
  const description=document.getElementById('category-editor-description');
  const order=document.getElementById('category-editor-order');
  const status=document.getElementById('category-editor-status');
  const target=document.getElementById('category-editor-target');
  const moveOrder=document.getElementById('category-editor-move-order');
  const destination=document.getElementById('category-editor-destination');
  const moveStatus=document.getElementById('category-editor-move-status');
  const moveSave=document.getElementById('category-editor-save-move');
  const lock=document.getElementById('category-editor-lock');
  const bodyTab=document.getElementById('category-editor-body-tab');
  const bodyTextarea=document.getElementById('category-editor-body');
  const bodyStatus=document.getElementById('category-editor-body-status');
  const bodySave=document.getElementById('category-editor-save-body');
  const deleteTitle=document.getElementById('category-editor-delete-title');
  const deleteDescription=document.getElementById('category-editor-delete-description');
  const deleteId=document.getElementById('category-editor-delete-id');
  const deleteConfirm=document.getElementById('category-editor-delete-confirm');
  const deleteStatus=document.getElementById('category-editor-delete-status');
  const deleteSave=document.getElementById('category-editor-delete-save');
  let current=null;
  let bodySourceSha='';
  let bodyLoadedPath='';

  async function post(path,payload){
    const response=await fetch(path,{method:'POST',credentials:'same-origin',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
    const body=await response.json().catch(()=>({}));
    if(!response.ok){const labels={github_token_not_configured:'サーバー側のGitHub Tokenが設定されていません。Cloudflare Worker SecretのGITHUB_TOKENを設定してください。',github_auth_failed:'サーバー側のGitHub Tokenの権限または有効期限を確認してください。',placement_locked:'配置ロック中です。先にロック解除してください。',directory_cross_collection_move:'フォルダは同じCollection内で移動してください。',directory_cycle:'自分自身または子フォルダ配下へは移動できません。',conflict_reload_and_retry:'mainが更新されました。再読み込みしてください。',destination_exists:'移動先Source fileは既に存在します。',source_exists:'フォルダMetadata fileは既に存在します。',route_exists:'同じURLが既に存在します。',directory_not_empty:'子Noteまたは子フォルダがあります。先に中身を移動または削除してください。',stale_build:'ページ表示後にmainが更新されています。安全のため再読み込みしてから削除してください。',stale_page_reload:'ページ表示後にmainが更新されています。安全のため再読み込みしてから削除してください。',confirmation_mismatch:'確認IDが一致しません。',invalid_delete_confirmation:'確認IDが一致しません。',source_changed_reload:'記事本文が別の更新で変更されています。ページを再読み込みしてから編集してください。',invalid_body:'本文を空にはできません。',body_too_large:'本文が大きすぎます。',not_note:'本文編集はNoteだけで利用できます。'};throw new Error(labels[body.error]||body.error||`操作に失敗しました (${response.status})`)}
    return body
  }

  const directories=catalog.filter(item=>item.type==='Directory');
  const roots=[];const rootKeys=new Set();
  for(const item of catalog){if(!item.domainId)continue;const key=`${item.domainId}|${item.collectionId||''}`;if(rootKeys.has(key))continue;rootKeys.add(key);roots.push({key,domainId:item.domainId,domainName:item.domainName,collectionId:item.collectionId||'',collectionName:item.collectionName||'',label:item.collectionId?`${item.domainName} / ${item.collectionName}`:`${item.domainName} / トップ`})}
  function option(value,label){const el=document.createElement('option');el.value=value;el.textContent=label;return el}
  function descendants(id){const out=new Set();function walk(parent){for(const child of directories.filter(item=>item.directoryId===parent)){if(!out.has(child.id)){out.add(child.id);walk(child.id)}}}walk(id);return out}
  function fillTargets(){
    if(!current||!target)return;
    target.replaceChildren();
    const rootGroup=document.createElement('optgroup');rootGroup.label='トップ / Collection root';
    for(const root of roots){if(current.type==='Directory'&&(root.domainId!==current.domainId||root.collectionId!==current.collectionId))continue;rootGroup.append(option(`root:${root.key}`,root.label))}
    target.append(rootGroup);
    const blocked=current.type==='Directory'?descendants(current.id):new Set();
    const dirGroup=document.createElement('optgroup');dirGroup.label='フォルダ';
    for(const dir of directories){if(dir.id===current.id||blocked.has(dir.id))continue;if(current.type==='Directory'&&(dir.domainId!==current.domainId||dir.collectionId!==current.collectionId))continue;dirGroup.append(option(`dir:${dir.sourcePath}`,`${dir.domainName} / ${dir.collectionName} / ${dir.title}`))}
    target.append(dirGroup);
    const value=current.directoryId?`dir:${directories.find(dir=>dir.id===current.directoryId)?.sourcePath||''}`:`root:${current.domainId}|${current.collectionId||''}`;
    target.value=value
  }
  function directChildren(){return current?.type==='Directory'?catalog.filter(item=>item.directoryId===current.id).length:0}
  function updateDeletePanel(){
    if(!current)return;
    const childCount=directChildren();const blockedByLock=current.type!=='Directory'&&current.placementLocked;const blockedByChildren=current.type==='Directory'&&childCount>0;
    deleteTitle.textContent=current.type==='Directory'?'フォルダを削除':'Noteを削除';
    deleteId.textContent=current.id;
    deleteDescription.textContent=blockedByChildren?`子要素が ${childCount} 件あります。空にしてから削除できます。`:blockedByLock?'配置ロックを解除してから削除できます。':current.type==='Directory'?'このフォルダのMetadataとAstro Routeを削除します。':'このNoteのMarkdownを削除します。';
    deleteConfirm.value='';deleteConfirm.disabled=blockedByChildren||blockedByLock;deleteSave.disabled=true;deleteStatus.textContent=''
  }
  function resetBody(){bodySourceSha='';bodyLoadedPath='';if(bodyTextarea)bodyTextarea.value='';if(bodyStatus)bodyStatus.textContent='';if(bodySave)bodySave.disabled=true}
  async function loadBody(){
    if(!current||current.type==='Directory'||!bodyTextarea||!bodyStatus||!bodySave)return;
    if(bodySourceSha&&bodyLoadedPath===current.sourcePath)return;
    try{bodyStatus.textContent='本文を読み込み中…';bodySave.disabled=true;const result=await post('/api/manage/body',{action:'read',path:current.sourcePath});bodyTextarea.value=String(result.body||'');bodySourceSha=String(result.source_sha||'');bodyLoadedPath=current.sourcePath;bodyStatus.textContent='元Markdown本文を読み込みました。';bodySave.disabled=!bodySourceSha||!bodyTextarea.value.trim()}
    catch(error){bodyStatus.textContent=error instanceof Error?error.message:'本文の読み込みに失敗しました。';bodySave.disabled=true}
  }
  function hydrate(){
    if(!current)return;
    heading.textContent=current.type==='Directory'?'フォルダを編集':'Noteを編集';title.value=current.title;description.value=current.description;order.value=String(current.order);moveOrder.value=String(current.order);destination.value=current.sourcePath;status.textContent='';moveStatus.textContent='';lock.hidden=!(current.type!=='Directory'&&current.placementLocked);moveSave.disabled=current.type!=='Directory'&&current.placementLocked;if(bodyTab)bodyTab.hidden=current.type==='Directory';fillTargets();updateDeletePanel();resetBody()
  }
  function openEditor(path){const item=byPath.get(path);if(!item||!dialog)return;current=item;hydrate();for(const button of document.querySelectorAll('[data-category-tab]'))button.classList.toggle('active',button.dataset.categoryTab==='meta');for(const panel of document.querySelectorAll('[data-category-panel]'))panel.hidden=panel.dataset.categoryPanel!=='meta';dialog.showModal()}
  document.addEventListener('click',event=>{const button=event.target.closest('[data-category-edit]');if(button){event.preventDefault();event.stopPropagation();openEditor(button.dataset.categoryEdit)}});
  document.getElementById('category-editor-close')?.addEventListener('click',()=>dialog.close());dialog?.addEventListener('click',event=>{if(event.target===dialog)dialog.close()});
  for(const tab of document.querySelectorAll('[data-category-tab]'))tab.addEventListener('click',()=>{if(tab.hidden)return;for(const button of document.querySelectorAll('[data-category-tab]'))button.classList.toggle('active',button===tab);for(const panel of document.querySelectorAll('[data-category-panel]'))panel.hidden=panel.dataset.categoryPanel!==tab.dataset.categoryTab;if(tab.dataset.categoryTab==='delete')updateDeletePanel();if(tab.dataset.categoryTab==='body')loadBody()});

  document.getElementById('category-editor-save-meta')?.addEventListener('click',async()=>{if(!current)return;try{status.textContent='保存中…';await post('/api/manage/metadata',{path:current.sourcePath,title:title.value.trim(),description:description.value.trim(),order:Number(order.value)});current.title=title.value.trim();current.description=description.value.trim();current.order=Number(order.value);status.textContent='保存しました。CI成功後に公開へ反映されます。'}catch(error){status.textContent=error instanceof Error?error.message:'保存失敗'}});
  bodyTextarea?.addEventListener('input',()=>{if(bodySave)bodySave.disabled=!bodySourceSha||!bodyTextarea.value.trim()});
  bodySave?.addEventListener('click',async()=>{if(!current||!bodySourceSha||!bodyTextarea.value.trim())return;try{bodySave.disabled=true;bodyStatus.textContent='本文の保存Commitを作成中…';await post('/api/manage/body',{action:'save',path:current.sourcePath,body:bodyTextarea.value,expectedSourceSha:bodySourceSha});bodyStatus.textContent='本文を保存しました。CI成功後にページを更新します。';setTimeout(()=>location.reload(),900)}catch(error){bodyStatus.textContent=error instanceof Error?error.message:'本文の保存に失敗しました。';bodySave.disabled=false}});
  document.getElementById('category-editor-unlock')?.addEventListener('click',async()=>{if(!current)return;try{await post('/api/manage/placement-lock',{path:current.sourcePath,locked:false});current.placementLocked=false;lock.hidden=true;moveSave.disabled=false;moveStatus.textContent='配置ロックを解除しました。';updateDeletePanel()}catch(error){moveStatus.textContent=error instanceof Error?error.message:'解除失敗'}});
  moveSave?.addEventListener('click',async()=>{if(!current)return;const value=target.value;const payload={path:current.sourcePath,order:Number(moveOrder.value),destinationPath:destination.value.trim()};if(current.type==='Directory')payload.forbiddenTargetPaths=[...descendants(current.id)].map(id=>directories.find(dir=>dir.id===id)?.sourcePath).filter(Boolean);if(value.startsWith('dir:'))payload.targetDirectoryPath=value.slice(4);else{const root=roots.find(entry=>entry.key===value.slice(5));if(!root){moveStatus.textContent='移動先を選択してください。';return}payload.root={domainId:root.domainId,domainName:root.domainName,collectionId:root.collectionId||null,collectionName:root.collectionName||null}}try{moveStatus.textContent='移動Commitを作成中…';const result=await post('/api/manage/move',payload);current.sourcePath=result.destination_path||current.sourcePath;resetBody();moveStatus.textContent='移動しました。CI成功後に公開へ反映されます。'}catch(error){moveStatus.textContent=error instanceof Error?error.message:'移動失敗'}});

  deleteConfirm?.addEventListener('input',()=>{deleteSave.disabled=!current||deleteConfirm.disabled||deleteConfirm.value!==current.id});
  deleteSave?.addEventListener('click',async()=>{if(!current||deleteConfirm.value!==current.id)return;try{deleteStatus.textContent='削除Commitを作成中…';await post('/api/manage/delete',{path:current.sourcePath,confirmId:deleteConfirm.value,buildSha,expectedChildCount:current.type==='Directory'?0:undefined});deleteStatus.textContent='削除しました。CI成功後に公開へ反映されます。';for(const shell of document.querySelectorAll('[data-category-source]')){if(shell.dataset.categorySource===current.sourcePath){const panel=shell.closest('.library-collection');shell.remove();const meta=panel?.querySelector('.library-collection-meta');if(meta)meta.textContent=`${panel.querySelectorAll('.library-collection-entry').length} 項目`;break}}const count=document.getElementById('notes-count');if(count)count.textContent=`${document.querySelectorAll('.library-collection:not([hidden]) .library-collection-entry').length} 項目`;setTimeout(()=>dialog.close(),600)}catch(error){deleteStatus.textContent=error instanceof Error?error.message:'削除に失敗しました。'}});

  const createDialog=document.getElementById('category-editor-create-dialog');const createLocation=document.getElementById('category-editor-create-location');const createId=document.getElementById('category-editor-create-id');const createTitle=document.getElementById('category-editor-create-title');const createDescription=document.getElementById('category-editor-create-description');const createOrder=document.getElementById('category-editor-create-order');const createPermalink=document.getElementById('category-editor-create-permalink');const createSource=document.getElementById('category-editor-create-source');const createStatus=document.getElementById('category-editor-create-status');const createSave=document.getElementById('category-editor-create-save');
  function fillCreateLocations(){createLocation.replaceChildren();const rootGroup=document.createElement('optgroup');rootGroup.label='Collection root';for(const root of roots.filter(item=>item.domainId===domain&&item.collectionId))rootGroup.append(option(`root:${root.key}`,root.label));createLocation.append(rootGroup);const dirGroup=document.createElement('optgroup');dirGroup.label='既存フォルダの配下';for(const dir of directories.filter(item=>item.domainId===domain))dirGroup.append(option(`dir:${dir.sourcePath}`,`${dir.collectionName} / ${dir.title}`));createLocation.append(dirGroup)}
  function selectedCreateLocation(){const value=createLocation.value;if(value.startsWith('dir:'))return{dir:byPath.get(value.slice(4))};return{root:roots.find(item=>item.key===value.slice(5))}}
  function createValid(){const id=createId.value.trim(),orderValue=Number(createOrder.value),permalink=createPermalink.value.trim(),source=createSource.value.trim();return Boolean(createLocation.value)&&/^[A-Za-z0-9][A-Za-z0-9._-]*$/.test(id)&&Boolean(createTitle.value.trim())&&Boolean(createDescription.value.trim())&&createOrder.value!==''&&Number.isInteger(orderValue)&&orderValue>=0&&orderValue<=999999&&/^\/[A-Za-z0-9._/-]+\/$/.test(permalink)&&!permalink.includes('..')&&!permalink.includes('//')&&/^contents\/[A-Za-z0-9._/-]+\.md$/.test(source)&&!source.includes('..')&&!source.includes('//')}
  function updateCreateValidity(){if(createSave)createSave.disabled=!createValid()}
  function suggest(){const id=createId.value.trim(),location=selectedCreateLocation();if(!id||(!location.dir&&!location.root)){createPermalink.value='';createSource.value='';updateCreateValidity();return}if(location.dir){createPermalink.value=`${location.dir.permalink.replace(/\/$/,'')}/${id}/`;createSource.value=`${location.dir.sourcePath.split('/').slice(0,-1).join('/')}/${id}-directory.md`}else{createPermalink.value=`/${location.root.domainId}/${location.root.collectionId}/${id}/`;createSource.value=`contents/${location.root.domainId}/${location.root.collectionId}/${id}-directory.md`}updateCreateValidity()}
  createLocation?.addEventListener('change',suggest);createId?.addEventListener('input',suggest);for(const el of [createTitle,createDescription,createOrder,createPermalink,createSource])el?.addEventListener('input',updateCreateValidity);
  document.getElementById('category-editor-create-folder')?.addEventListener('click',()=>{createId.value='';createTitle.value='';createDescription.value='';createOrder.value='10';createPermalink.value='';createSource.value='';createStatus.textContent='';fillCreateLocations();suggest();updateCreateValidity();createDialog.showModal()});
  document.getElementById('category-editor-create-close')?.addEventListener('click',()=>createDialog.close());createDialog?.addEventListener('click',event=>{if(event.target===createDialog)createDialog.close()});
  createSave?.addEventListener('click',async()=>{if(createSave.disabled)return;const location=selectedCreateLocation();const payload={id:createId.value.trim(),title:createTitle.value.trim(),description:createDescription.value.trim(),order:Number(createOrder.value),permalink:createPermalink.value.trim(),sourcePath:createSource.value.trim()};if(location.dir)payload.parentDirectoryPath=location.dir.sourcePath;else if(location.root)Object.assign(payload,{domainId:location.root.domainId,domainName:location.root.domainName,collectionId:location.root.collectionId,collectionName:location.root.collectionName});else{createStatus.textContent='作成位置を選択してください。';updateCreateValidity();return}try{createSave.disabled=true;createStatus.textContent='フォルダ作成Commitを作成中…';await post('/api/manage/create-directory',payload);createStatus.textContent='フォルダを作成しました。CI成功後に表示されます。'}catch(error){createStatus.textContent=error instanceof Error?error.message:'作成失敗';updateCreateValidity()}});
  fillCreateLocations();updateCreateValidity();
}
