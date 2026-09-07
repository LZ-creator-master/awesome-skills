/* Local-only reader controls. No analytics, network requests, or persistence. */
document.querySelectorAll('input[name="reading-level"]').forEach(control=>{
  control.addEventListener('change',()=>{document.body.dataset.reading=control.value;
    const notice=document.getElementById('reading-notice');
    if(notice)notice.textContent=control.value==='basic'?'基础版：先读直观解释与结果，公式推导和源码已收起。':'进阶版：已展开公式推导与源码对应。';
  });
});
document.querySelectorAll('form[data-quiz]').forEach(form=>{
  form.addEventListener('submit',event=>{event.preventDefault();let score=0,answered=0;
    form.querySelectorAll('fieldset[data-answer]').forEach(field=>{
      const selected=field.querySelector('input:checked');if(selected)answered++;
      const correct=!!selected&&selected.value===field.dataset.answer;if(correct)score++;
      const feedback=field.querySelector('.quiz-feedback');feedback.hidden=false;
      feedback.textContent=(correct?'答对了。':selected?'再想一下。':'尚未作答。')+field.dataset.explanation;
    });
    form.querySelector('[data-score]').textContent=`答对 ${score} / ${form.querySelectorAll('fieldset').length} 题，已作答 ${answered} 题。这是学习自测，不是能力评级。`;
  });
  form.addEventListener('reset',()=>{form.querySelectorAll('.quiz-feedback').forEach(x=>x.hidden=true);form.querySelector('[data-score]').textContent='';});
});
document.querySelectorAll('[data-copy-target]').forEach(button=>button.addEventListener('click',async()=>{
  const text=document.getElementById(button.dataset.copyTarget).textContent;const status=button.nextElementSibling;
  try{await navigator.clipboard.writeText(text);status.textContent='已复制';}catch{status.textContent='请选中内容手动复制';}
}));
