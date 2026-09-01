const content=document.getElementById('content');
const pdfButton=document.getElementById('article-pdf-export');
const side=document.getElementById('side');
const backdrop=document.getElementById('side-backdrop');
const modalBackdrop=document.getElementById('revision-modal-backdrop');
let printDetailStates=null;

function prepareArticlePrint(){
  if(!content||printDetailStates)return;
  printDetailStates=[...content.querySelectorAll('details')].map(detail=>[detail,detail.open]);
  for(const[detail]of printDetailStates)detail.open=true;
  side?.classList.remove('open');
  backdrop?.classList.remove('open');
  modalBackdrop?.classList.remove('open');
  modalBackdrop?.setAttribute('aria-hidden','true');
  document.body.classList.remove('nav-open','modal-open');
}

function restoreArticlePrint(){
  if(!printDetailStates)return;
  for(const[detail,wasOpen]of printDetailStates)detail.open=wasOpen;
  printDetailStates=null;
}

window.addEventListener('beforeprint',prepareArticlePrint);
window.addEventListener('afterprint',restoreArticlePrint);
pdfButton?.addEventListener('click',()=>{
  prepareArticlePrint();
  requestAnimationFrame(()=>window.print());
});
