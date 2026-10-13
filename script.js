'use strict';
const $=(selector,root=document)=>root.querySelector(selector);
const $$=(selector,root=document)=>Array.from(root.querySelectorAll(selector));
const projects={
 identity:{number:'001',eyebrow:'ENTERPRISE / IDENTITY',label:'IDENTITY',title:'Identity in motion',subtitle:'Identity & Access Management · TCS Digital / Westpac engagement',description:'Supporting enterprise access management operations where security, governance, and user experience intersect. This chapter is about ensuring access requests are handled carefully, consistently, and in line with established policy.',points:['Support access provisioning and identity-related service requests through ServiceNow.','Help resolve access-related support issues and maintain operational continuity.','Work within documented access governance and approval procedures.','Coordinate with stakeholders to support clear, controlled request handling.'],tags:['IAM','Access Provisioning','Access Control','ServiceNow','Governance'],disclaimer:'Professional responsibilities are described at a high level. No client data, internal systems, or confidential workflows are disclosed.',art:'radial-gradient(circle at 45% 48%,#587b3c,#13271a)'},
 servicenow:{number:'002',eyebrow:'ENTERPRISE / WORKFLOWS',label:'EAR / CATALOG',title:'The workflow edit',subtitle:'ServiceNow Service Catalog · EAR activities',description:'A technical practice built around improving enterprise request experiences. Beyond IAM support, I configure, script and refine ServiceNow catalog experiences as part of EAR activities, creating and adapting the building blocks that connect users to services.',points:['Design and build templates used in ServiceNow catalog activities.','Configure existing catalog forms, fields, data, and request behavior.','Modify scripting and workflow logic to support evolving requirements.','Validate changes in development and test environments before approved release processes.','Collaborate with BAOs and automation colleagues on testing and implementation.'],tags:['ServiceNow','Service Catalog','EAR','Scripting','Workflow Logic','Configuration'],disclaimer:'EAR is an internal activity name. Examples are intentionally generalized to protect client confidentiality.',art:'linear-gradient(130deg,#425e50,#0c2425)'},
 vapt:{number:'003',eyebrow:'SECURITY / RESEARCH',label:'VAPT',title:'Think like the threat',subtitle:'Vulnerability Assessment and Penetration Testing · Academic / internship project',description:'A security assessment project exploring how to identify weaknesses, understand potential impacts, document findings and develop recommendations for improving defensive posture.',points:['Studied vulnerability assessment methods and attack surfaces.','Explored application security testing and DAST concepts in a project context.','Documented findings, risks and potential mitigation approaches.','Developed a security-first way of examining application behavior.'],tags:['VAPT','DAST','Application Security','Risk Assessment','Documentation'],disclaimer:'This is a learning/project showcase, not a claim of authorized testing on live third-party systems.',art:'radial-gradient(circle at 48% 42%,#8a3a2c,#21120f)'},
 mitm:{number:'004',eyebrow:'SECURITY / NETWORKS',label:'MITM',title:'Between the packets',subtitle:'Man-in-the-Middle attack research · Academic project',description:'An exploration of man-in-the-middle attack concepts and the importance of trusting what happens between endpoints. The project examined network security risks and protective principles in controlled learning scenarios.',points:['Researched interception and spoofing techniques including ARP and DNS concepts.','Explored how insecure communication can affect confidentiality and integrity.','Reviewed encryption and defensive strategies for reducing MITM risks.','Documented observations and the importance of secure networking practice.'],tags:['Networking','MITM','Cybersecurity','Encryption','Defensive Research'],disclaimer:'Research and educational simulation only; no real-world unauthorized network testing is implied.',art:'linear-gradient(130deg,#285378,#0d1b2b)'},
 placement:{number:'005',eyebrow:'SIDE QUEST / FULL STACK',label:'FLASK',title:'Where careers connect',subtitle:'Placement Portal · Python, Flask, SQLite',description:'A multi-role web application designed to manage campus placement workflows in one place, from companies and recruitment drives to student applications and approvals.',points:['Created role-based dashboards for administrators, companies, and students.','Implemented registration, approvals, drive creation, and applications.','Designed relational models using Flask and SQLite.','Built résumé upload handling, search, pagination, and JSON API endpoints.'],tags:['Python','Flask','SQLAlchemy','SQLite','RBAC','REST APIs'],disclaimer:'An academic software project. Not connected to any live enterprise client systems.',art:'linear-gradient(120deg,#51428d,#1c1935)'},
 hospital:{number:'006',eyebrow:'SIDE QUEST / FULL STACK',label:'FLASK',title:'Care, coordinated',subtitle:'Hospital Management System · Python, Flask, SQLite',description:'A role-aware healthcare management web app prototype focused on giving administrators, doctors, and patients clear journeys through common hospital workflows.',points:['Designed separate application roles for admin, doctor, and patient.','Used Flask, Jinja2 templates, and SQLite for app and data flow.','Explored application architecture, models, and role-specific pages.','Practiced practical backend and template-driven interface development.'],tags:['Python','Flask','Jinja2','SQLite','Role-based Access'],disclaimer:'Academic prototype only; not a production healthcare or patient-record service.',art:'radial-gradient(circle at center,#237668,#10272b)'}
};
const order=Object.keys(projects);
const modal=$('#projectModal');const modalArt=$('#modalArt');let currentProject='identity';let lastFocus=null;
function setBodyLock(){document.body.classList.toggle('no-scroll',!modal.hidden||!$('#palette').hidden)}
function openProject(key){const p=projects[key];if(!p)return;lastFocus=document.activeElement;currentProject=key;$('#modalEyebrow').textContent=p.eyebrow;$('#modalNumber').textContent=p.number;$('#modalArt').textContent=p.label;$('#modalArt').style.background=p.art;$('#modalTitle').textContent=p.title;$('#modalSubtitle').textContent=p.subtitle;$('#modalDescription').textContent=p.description;$('#modalPoints').replaceChildren(...p.points.map(s=>{let li=document.createElement('li');li.textContent=s;return li}));$('#modalTags').replaceChildren(...p.tags.map(s=>{let tag=document.createElement('span');tag.textContent=s;return tag}));$('#modalDisclaimer').textContent=p.disclaimer;modal.hidden=false;setBodyLock();$('.modal-content').scrollTop=0;$('.modal-close').focus()}
function closeProject(){modal.hidden=true;setBodyLock();if(lastFocus&&lastFocus.isConnected)lastFocus.focus()}
$$('[data-project]').forEach(el=>el.addEventListener('click',()=>openProject(el.dataset.project)));
$$('[data-close]').forEach(el=>el.addEventListener('click',closeProject));
$('#modalNext').addEventListener('click',()=>openProject(order[(order.indexOf(currentProject)+1)%order.length]));
$('#randomProject').addEventListener('click',()=>openProject(order[Math.floor(Math.random()*order.length)]));
$$('.filter').forEach(el=>el.addEventListener('click',()=>{$$('.filter').forEach(b=>{let active=b===el;b.classList.toggle('active',active);b.setAttribute('aria-pressed',String(active))});$$('.poster-card').forEach(card=>{card.hidden=el.dataset.filter!=='all'&&card.dataset.category!==el.dataset.filter})}));
$('#watchStory').addEventListener('click',()=>document.querySelector('#journey').scrollIntoView({behavior:'smooth'}));
$('#tryTerminal').addEventListener('click',()=>{document.querySelector('#terminalInput').focus();runCommand('help')});
const commands={help:'Available commands: help · about · radio · work · skills · experience · contact · linkedin · whoami · date · coffee · secret · clear',about:'I\'m Sharanya Pal — a System Engineer at TCS Digital, supporting IAM operations and ServiceNow catalog / EAR development.',radio:'Signal Radio is waiting. Opening your listening room now...',work:'Six files available in the collection. Opening the first one now...',skills:'IAM · ServiceNow Service Catalog · Scripting · Workflow Logic · Python · Flask · SQL · Security',experience:'TCS Digital → Westpac engagement | IAM Support Analyst + ServiceNow EAR activities. Previously explored app security, IT and design.',contact:'Let\'s talk: sharanyapal856@gmail.com',linkedin:'Opening the professional universe in a new tab...',whoami:'visitor@sharanya: curious human with excellent taste in websites',date:()=>new Date().toLocaleString(undefined,{dateStyle:'full',timeStyle:'short'}),coffee:'☕ Coffee.exe loaded. Conversations are better over coffee.',secret:'Achievement unlocked: you found the secret command. Keep exploring; the best bugs are the ones we fix. ✳'};
function appendTerminal(message,type=''){let p=document.createElement('p');if(type)p.className=type;p.textContent=message;$('#terminalOutput').appendChild(p);$('#terminalOutput').scrollTop=$('#terminalOutput').scrollHeight}
function runCommand(raw){let command=raw.trim().toLowerCase();if(!command)return;appendTerminal('visitor@sharanya:~$ '+raw,'term-command');if(command==='clear'){$('#terminalOutput').replaceChildren();return}let response=commands[command];if(response){appendTerminal(typeof response==='function'?response():response,'term-accent');if(command==='work')setTimeout(()=>openProject('identity'),220);if(command==='radio')$('#radio').scrollIntoView({behavior:'smooth'});if(command==='linkedin')window.open('https://www.linkedin.com/in/sharanya-pal-a9a637187/','_blank','noopener,noreferrer')}else appendTerminal(`Unknown command: ${raw}. Try 'help'.`,'term-error')}
$('#terminalForm').addEventListener('submit',e=>{e.preventDefault();const input=$('#terminalInput');runCommand(input.value);input.value=''});
let toastTimeout;function showToast(message){const el=$('#toast');el.textContent=message;el.classList.add('show');clearTimeout(toastTimeout);toastTimeout=setTimeout(()=>el.classList.remove('show'),3100)}
$('#copyEmail').addEventListener('click',async()=>{try{await navigator.clipboard.writeText('sharanyapal856@gmail.com');showToast('EMAIL COPIED TO CLIPBOARD ✓')}catch{showToast('EMAIL: sharanyapal856@gmail.com')}});
$('#backToTop').addEventListener('click',()=>window.scrollTo({top:0,behavior:'smooth'}));$('#year').textContent=new Date().getFullYear();
const menu=$('#mobileMenu');$('#menuToggle').addEventListener('click',()=>{menu.hidden=!menu.hidden;$('#menuToggle').setAttribute('aria-expanded',String(!menu.hidden))});$$('.mobile-menu a').forEach(a=>a.addEventListener('click',()=>{menu.hidden=true;$('#menuToggle').setAttribute('aria-expanded','false')}));
const palette=$('#palette');const navigation=[{label:'Home / Feature presentation',dest:'#home',shortcut:'01'},{label:'The Collection / Work',dest:'#work',shortcut:'02'},{label:'Signal Radio / Soundtrack',dest:'#radio',shortcut:'♫'},{label:'Work Experience & Education',dest:'#journey',shortcut:'03'},{label:'About Me',dest:'#experience',shortcut:'↗'},{label:'Loadout / Skills',dest:'#stack',shortcut:'04'},{label:'Terminal / Easter egg',dest:'#terminal',shortcut:'05'},{label:'Contact / Say hello',dest:'#contact',shortcut:'06'},...order.map(key=>({label:'Project / '+projects[key].title,dest:key,shortcut:'↗'}))];let selectedPalette=0;let paletteItems=[];
function drawPalette(){let q=$('#paletteInput').value.toLowerCase().trim();paletteItems=navigation.filter(item=>item.label.toLowerCase().includes(q));selectedPalette=0;const results=$('#paletteResults');results.replaceChildren();if(!paletteItems.length){let p=document.createElement('p');p.className='palette-empty';p.textContent='No matching files found.';results.appendChild(p)}paletteItems.forEach((item,i)=>{const b=document.createElement('button');b.type='button';b.className='palette-result'+(i===0?' selected':'');b.textContent=item.label;const small=document.createElement('small');small.textContent=item.shortcut;b.appendChild(small);b.addEventListener('click',()=>activatePalette(item));results.appendChild(b)})}
function activatePalette(item){closePalette();if(item.dest.startsWith('#'))document.querySelector(item.dest).scrollIntoView({behavior:'smooth'});else openProject(item.dest)}
function openPalette(){if(!modal.hidden)closeProject();palette.hidden=false;setBodyLock();$('#paletteInput').value='';drawPalette();$('#paletteInput').focus()}
function closePalette(){palette.hidden=true;setBodyLock()}
$('#searchTrigger').addEventListener('click',openPalette);$('[data-palette-close]').addEventListener('click',closePalette);$('#paletteInput').addEventListener('input',drawPalette);$('#paletteInput').addEventListener('keydown',e=>{if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();if(!paletteItems.length)return;selectedPalette=(selectedPalette+(e.key==='ArrowDown'?1:-1)+paletteItems.length)%paletteItems.length;$$('.palette-result').forEach((el,i)=>el.classList.toggle('selected',i===selectedPalette))}if(e.key==='Enter'){e.preventDefault();if(paletteItems[selectedPalette])activatePalette(paletteItems[selectedPalette])}});
document.addEventListener('keydown',e=>{if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='k'){e.preventDefault();palette.hidden?openPalette():closePalette()}if(e.key==='Escape'){if(!modal.hidden)closeProject();if(!palette.hidden)closePalette();if(!menu.hidden){menu.hidden=true;$('#menuToggle').setAttribute('aria-expanded','false')}}});
const revealObserver=('IntersectionObserver'in window)?new IntersectionObserver(entries=>{entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('is-visible');revealObserver.unobserve(entry.target)}})},{threshold:.07,rootMargin:'0px 0px -24px 0px'}):null;$$('.reveal').forEach(el=>revealObserver?revealObserver.observe(el):el.classList.add('is-visible'));
function handleScroll(){const max=document.documentElement.scrollHeight-innerHeight;$('#scrollProgress').style.transform=`scaleX(${max>0?scrollY/max:0})`;$('#header').classList.toggle('scrolled',scrollY>30)}window.addEventListener('scroll',handleScroll,{passive:true});handleScroll();

/* Signal Radio: optional, locally synthesized musical loops; no streaming service or external audio. */
const radioTracks=[
 {title:'Secure Frequencies',sub:'The identity chapter · minimal analog pulses',color:'#d9ff89',word:'SECURE',symbol:'◈',label:'IDENTITY',duration:42,project:'identity',root:45,notes:[0,7,12,7,3,7,10,7],wave:'sine'},
 {title:'Catalog Dreams',sub:'The workflow chapter · soft electric sequences',color:'#9dece0',word:'DESIGN',symbol:'⌘',label:'CATALOG',duration:48,project:'servicenow',root:48,notes:[0,4,7,11,12,11,7,4],wave:'triangle'},
 {title:'Packet Noir',sub:'The security chapter · dark digital atmosphere',color:'#f0aeaa',word:'DECODE',symbol:'⟁',label:'SECURITY',duration:40,project:'mitm',root:40,notes:[0,1,7,6,0,-2,5,1],wave:'sine'},
 {title:'Weekend Frames',sub:'The human chapter · dreamy evening textures',color:'#dfc4ff',word:'WANDER',symbol:'✳',label:'EXPLORE',duration:52,project:null,root:52,notes:[0,4,7,12,9,7,4,2],wave:'triangle'}
];
let radioIndex=0,radioPlaying=false,radioSeconds=0,radioStep=0,radioLastTime=0,radioCtx=null,radioOutput=null,radioAudioTimer=null,radioUiTimer=null,radioInView=true,radioDismissed=false;
const radioDeck=$('#radioDeck');
function radioFormat(seconds){const n=Math.max(0,Math.floor(seconds));return `${Math.floor(n/60)}:${String(n%60).padStart(2,'0')}`}
function radioHz(midi){return 440*Math.pow(2,(midi-69)/12)}
function radioNote(freq,at,length,level,type='sine'){
 if(!radioCtx||!radioOutput||radioCtx.state!=='running')return;
 const osc=radioCtx.createOscillator(),env=radioCtx.createGain();
 osc.type=type;osc.frequency.setValueAtTime(freq,at);env.gain.setValueAtTime(0.0001,at);env.gain.exponentialRampToValueAtTime(Math.max(.0002,level),at+.035);env.gain.exponentialRampToValueAtTime(.0001,at+length);
 osc.connect(env);env.connect(radioOutput);osc.start(at);osc.stop(at+length+.025);
}
function radioToneStep(){if(!radioPlaying||!radioCtx||radioCtx.state!=='running')return;const t=radioTracks[radioIndex],at=radioCtx.currentTime+.01;let k=radioStep%t.notes.length;
 radioNote(radioHz(t.root+t.notes[k]+12),at,.24,.16,t.wave);
 if(radioStep%4===0){radioNote(radioHz(t.root-12),at,.72,.21,'sine');radioNote(radioHz(t.root+7),at,1.12,.08,'triangle')}
 radioStep++;
}
function radioIsSupported(){return !!(window.AudioContext||window.webkitAudioContext)}
async function radioBegin(){
 if(!radioIsSupported()){showToast('AUDIO ENGINE UNAVAILABLE IN THIS BROWSER');return}
 try{
   if(!radioCtx){radioCtx=new (window.AudioContext||window.webkitAudioContext)();radioOutput=radioCtx.createGain();radioOutput.gain.value=Number($('#radioVolume').value)/100*.38;radioOutput.connect(radioCtx.destination)}
   await radioCtx.resume();radioPlaying=true;radioDismissed=false;radioLastTime=performance.now();
   if(!radioAudioTimer){radioToneStep();radioAudioTimer=setInterval(radioToneStep,285)}
   if(!radioUiTimer)radioUiTimer=setInterval(radioTick,120);
   radioRender();
 }catch(e){radioPlaying=false;showToast('AUDIO COULD NOT START — CHECK BROWSER PERMISSIONS');console.warn('Signal Radio audio failed:',e)}
}
function radioPause(){
 if(radioPlaying){radioTick();radioPlaying=false}
 clearInterval(radioAudioTimer);radioAudioTimer=null;clearInterval(radioUiTimer);radioUiTimer=null;
 if(radioCtx&&radioCtx.state==='running')radioCtx.suspend().catch(()=>{});
 radioRender();
}
function radioTick(){if(!radioPlaying)return;let now=performance.now();radioSeconds+=(now-radioLastTime)/1000;radioLastTime=now;let t=radioTracks[radioIndex];if(radioSeconds>=t.duration){radioChoose((radioIndex+1)%radioTracks.length);return}radioSetProgress()}
function radioSetProgress(){const t=radioTracks[radioIndex];const progress=Math.max(0,Math.min(100,100*radioSeconds/t.duration));$('#radioTime').textContent=radioFormat(radioSeconds);$('#radioDuration').textContent=radioFormat(t.duration);$('#radioProgress').value=String(progress);$('#miniProgress').style.width=`${progress}%`}
function radioChoose(index){radioIndex=(index+radioTracks.length)%radioTracks.length;radioSeconds=0;radioStep=0;radioLastTime=performance.now();radioRender()}
function radioRender(){let t=radioTracks[radioIndex];radioDeck.style.setProperty('--radio-accent',t.color);radioDeck.classList.toggle('is-playing',radioPlaying);
 $('#radioCurrentTitle').textContent=t.title;$('#radioCurrentSub').textContent=t.sub;$('#radioSequence').textContent=String(radioIndex+1).padStart(2,'0')+' / 04';$('#radioVinylText').textContent=t.label;$('#radioAmbientWord').textContent=t.word;
 $('#radioOpenProject').textContent=t.project?'CASE FILE ↗':'MY STORY ↗';$('#radioOpenProject').setAttribute('aria-label',t.project?'Open related project case study':'Go to my story');
 $('#radioPlay').textContent=radioPlaying?'Ⅱ':'▶';$('#radioPlay').setAttribute('aria-label',radioPlaying?'Pause soundscape':'Play soundscape');$('#radioPlay').setAttribute('aria-pressed',String(radioPlaying));
 $('#miniPause').textContent=radioPlaying?'Ⅱ':'▶';$('#miniPause').setAttribute('aria-label',radioPlaying?'Pause soundscape':'Play soundscape');$('#miniTitle').textContent=t.title;$('#miniCover').textContent=t.symbol;$('#miniCover').style.background=t.color;
 $$('.radio-track').forEach((b,i)=>{let selected=i===radioIndex;b.classList.toggle('selected',selected);b.setAttribute('aria-pressed',String(selected));let n=$('.radio-track-number',b);n.textContent=selected&&radioPlaying?'♫':String(i+1).padStart(2,'0')});
 radioSetProgress();radioShowMini();
}
function radioShowMini(){$('#miniRadio').hidden=!radioPlaying||radioInView||radioDismissed}
$('#radioPlay').addEventListener('click',()=>radioPlaying?radioPause():radioBegin());
$('#radioPrevious').addEventListener('click',()=>radioChoose(radioIndex-1));$('#radioNext').addEventListener('click',()=>radioChoose(radioIndex+1));
$$('.radio-track').forEach(b=>b.addEventListener('click',()=>radioChoose(Number(b.dataset.track))));
$('#radioProgress').addEventListener('input',e=>{radioSeconds=Number(e.target.value)/100*radioTracks[radioIndex].duration;radioStep=Math.floor(radioSeconds/.285);radioLastTime=performance.now();radioSetProgress()});
$('#radioVolume').addEventListener('input',e=>{let vol=Number(e.target.value);$('#radioVolumeLabel').textContent=vol+'%';if(radioOutput&&radioCtx)radioOutput.gain.setTargetAtTime(vol/100*.38,radioCtx.currentTime,.035)});
$('#radioOpenProject').addEventListener('click',()=>{let t=radioTracks[radioIndex];if(t.project)openProject(t.project);else $('#experience').scrollIntoView({behavior:'smooth'})});
$('#miniPause').addEventListener('click',()=>radioPlaying?radioPause():radioBegin());$('#miniNext').addEventListener('click',()=>radioChoose(radioIndex+1));
$('#miniClose').addEventListener('click',()=>{radioDismissed=true;radioPause()});
if('IntersectionObserver' in window){new IntersectionObserver(entries=>{radioInView=entries[0].isIntersecting;radioShowMini()},{threshold:.15}).observe($('#radio'))}
radioRender();

/* Edition 02: background filter, hero/player affordance */
$$('[data-journey-filter]').forEach(button=>button.addEventListener('click',()=>{const filter=button.dataset.journeyFilter;$$('[data-journey-filter]').forEach(el=>{const isActive=el===button;el.classList.toggle('active',isActive);el.setAttribute('aria-pressed',String(isActive))});$$('[data-journey]').forEach(card=>{card.hidden=filter!=='all'&&card.dataset.journey!==filter})}));
function revealRadioLauncher(){$('#radioLauncher').hidden=radioPlaying}
const initialRadioRender=radioRender;
radioRender=function(){initialRadioRender();revealRadioLauncher()};
const quickRadioPlay=()=>{if(radioPlaying){document.querySelector('#radio').scrollIntoView({behavior:'smooth'});return}radioBegin()};
$('#radioLauncher').addEventListener('click',quickRadioPlay);
$('#heroPlayRadio').addEventListener('click',quickRadioPlay);
$('#modePlayRadio').addEventListener('click',quickRadioPlay);
revealRadioLauncher();
