window.$=(selector)=>document.querySelector(selector);
window.$$=(selector)=>[...document.querySelectorAll(selector)];
window.show=(selector,value)=>{const el=$(selector);if(el)el.textContent=String(value)};
window.safe=(value)=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
window.downloadText=(name,text,type='text/plain')=>{const a=document.createElement('a');const url=URL.createObjectURL(new Blob([text],{type}));a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)};
