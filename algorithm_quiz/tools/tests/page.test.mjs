import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import vm from 'node:vm';
const html=await readFile(new URL('../../index.html',import.meta.url),'utf8');
const data=html.match(/<script id="bank-data" type="application\/json">([\s\S]*?)<\/script>/)[1];
class Element {
 constructor(tag='div'){this.tagName=tag.toUpperCase();this.children=[];this.value='';this.textContent='';this.hidden=false;this.disabled=false;this.attributes={};this.style={};this.events={};this.classList={toggle:()=>{}};this.checked=false;this.open=false;}
 append(...items){this.children.push(...items);} replaceChildren(...items){this.children=[...items];} add(item){this.append(item);} get options(){return this.children;}
 setAttribute(key,value){this.attributes[key]=value;} addEventListener(event,fn){this.events[event]=fn;}
 querySelectorAll(tag){return this.children.flatMap(c=>[...(c.tagName===tag.toUpperCase()?[c]:[]),...(c.querySelectorAll?c.querySelectorAll(tag):[])]);}
 focus(){} scrollIntoView(){} remove(){} click(){this.events.click?.({target:this});} showModal(){this.open=true;} close(){this.open=false;}
}
async function fixture(store=new Map(),network=null) {
 const elements=new Map([...html.matchAll(/id="([^"]+)"/g)].map(m=>[m[1],new Element()]));
 elements.get('bank-data').textContent=data;elements.get('difficulty-filter').children=['','Easy','Medium','Hard'].map(value=>({value}));
 const document={getElementById:id=>elements.get(id),querySelector:()=>network?{content:'test-token'}:null,createElement:tag=>new Element(tag),createTextNode:text=>({textContent:text}),body:new Element('body'),addEventListener(){}};
 const FixedDate=class extends Date {static now(){return 1793930400000;}};
 const context={document,window:{},Option:function(text,value){this.textContent=text;this.value=value;},localStorage:{setItem:(k,v)=>store.set(k,v),getItem:k=>store.get(k)||null},console,Blob,URL,AbortController,setTimeout:fn=>{fn();return 1;},Date:network?FixedDate:Date,Math,fetch:network};
 vm.createContext(context);
 const scripts=[...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)].slice(1).map(m=>m[1]);
 vm.runInContext(scripts.join('\n')+`\nwindow.testAPI={grade,choose,submitQuestion,retryQuestion,goTo,startRound,importFile,importProfileFile,pool,flush:()=>remoteQueue,getRound:()=>round,getProfile:()=>profile,getQuestion:()=>byId.get(round.entries[round.current].id)};`,context);
 await context.window.QuizReady;
 return {elements,store,api:context.window.testAPI,core:context.window.QuizCore};
}
test('未选择不提交；逐题提交立即显示原因并持久保存错题，重复点击不重复计数',async()=>{
 const f=await fixture(),{api,elements}=f;
 api.submitQuestion();assert.equal(api.getProfile().history.length,0);assert.equal(elements.get('feedback-dialog').open,false);
 const q=api.getQuestion(),wrong=api.getRound().entries[0].options.find(o=>o!==q.category);
 api.choose(wrong);assert.equal(api.getProfile().history.length,0);
 api.submitQuestion();assert.equal(api.getProfile().history.length,1);assert.equal(elements.get('feedback-dialog').open,true);
 assert.match(elements.get('feedback-title').textContent,/不正确/);assert(elements.get('feedback-reason').textContent.includes(q.explanation));
 api.submitQuestion();assert.equal(api.getProfile().history.length,1);
 const restored=await fixture(f.store);assert.equal(restored.api.getProfile().records[q.id].status,'wrong');
 assert.equal(restored.api.getRound().entries[0].checked,true);assert.equal(restored.elements.get('explanation').hidden,false);
 restored.api.retryQuestion();restored.api.choose(q.category);restored.api.submitQuestion();
 assert.match(restored.elements.get('feedback-title').textContent,/回答正确/);
 assert.equal(restored.api.getProfile().records[q.id].wrongCount,1);
 assert.equal(restored.api.getProfile().records[q.id].correctCount,1);
 assert(!restored.api.pool().some(row=>row.id===q.id));
 const again=await fixture(f.store);assert.notEqual(again.api.getQuestion().id,q.id);
});
test('20题逐一提交评分，刷新后开启新轮并排除全部刚答对题',async()=>{
 const f=await fixture();const ids=new Set(f.api.getRound().entries.map(e=>e.id));
 for(let i=0;i<20;i++){f.api.goTo(i);f.api.choose(f.api.getQuestion().category);f.api.submitQuestion();f.elements.get('feedback-dialog').close();}
 assert.equal(f.api.grade().score,100);assert.equal(f.elements.get('result').hidden,false);
 const next=await fixture(f.store);assert.equal(next.api.getRound().entries.length,20);
 assert(next.api.getRound().entries.every(e=>!ids.has(e.id)));
});
test('少于20题的筛选能恢复；CSV保持兼容；坏记录导入不改变学习状态',async()=>{
 const f=await fixture();
 f.elements.get('category-filter').value='KMP';f.api.startRound();const expected=Math.min(20,JSON.parse(data).questions.filter(q=>q.category==='KMP').length);assert.equal(f.api.getRound().entries.length,expected);
 const id=f.api.getQuestion().id;f.api.choose(f.api.getQuestion().category);f.api.submitQuestion();
 const restored=await fixture(f.store);assert.equal(restored.api.getRound().entries.length,expected);assert.notEqual(restored.api.getQuestion().id,id);
 const bank=JSON.parse(data).questions, csv=f.core.toCSV(bank);assert.equal(f.core.validateBank(f.core.parseCSV(csv)).length,bank.length);
 const before=f.api.getProfile().history.length;
 await f.api.importProfileFile({size:10,text:async()=>'{bad json'});
 assert.equal(f.api.getProfile().history.length,before);assert.match(f.elements.get('status').textContent,/恢复失败/);
});

test('延迟返回的文件保存响应不能覆盖后来提交的答案，即使在同一毫秒操作',async()=>{
 const pending=[];
 const network=async(url,options)=>{
  if(!options.method)return {ok:true,json:async()=>({profile:{version:2,history:[],session:null}})};
  return new Promise(resolve=>pending.push({snapshot:JSON.parse(options.body),resolve}));
 };
 const wait=()=>new Promise(resolve=>setImmediate(resolve));
 const finish=async()=>{
  while(!pending.length)await wait();
  const request=pending.shift();request.resolve({ok:true,json:async()=>({profile:request.snapshot})});
  await wait();
 };
 const f=await fixture(new Map(),network);
 await finish();await f.api.flush();
 f.api.choose(f.api.getRound().entries[0].options.find(c=>c!==f.api.getQuestion().category));
 f.api.submitQuestion();
 await finish();
 assert.equal(f.api.getProfile().session.round.entries[0].checked,true,'较早的未提交快照不能回滚当前提交');
 await finish();await f.api.flush();
 const stored=JSON.parse(f.store.get('algorithm-quiz-personal-v2'));
 assert.equal(stored.session.round.entries[0].checked,true);
 assert.equal(stored.history.length,1);
});

test('扩充题库导致版本指纹改变时，错题与7天复习时间不丢失',async()=>{
 const f=await fixture(),wrongQuestion=f.api.getQuestion();
 f.api.choose(f.api.getRound().entries[0].options.find(c=>c!==wrongQuestion.category));f.api.submitQuestion();
 f.elements.get('feedback-dialog').close();f.api.goTo(1);
 const correctQuestion=f.api.getQuestion();f.api.choose(correctQuestion.category);f.api.submitQuestion();
 const raw=JSON.parse(f.store.get('algorithm-quiz-personal-v2'));
 raw.session.fingerprint='previous-bank-version';
 f.store.set('algorithm-quiz-personal-v2',JSON.stringify(raw));
 const next=await fixture(f.store),profile=next.api.getProfile();
 assert.equal(profile.history.length,2);
 assert.equal(profile.records[wrongQuestion.id].status,'wrong');
 assert.equal(profile.records[correctQuestion.id].status,'correct');
 assert.equal(profile.records[correctQuestion.id].reviewAfter,raw.records[correctQuestion.id].reviewAfter);
 assert(next.api.getRound().entries.some(e=>e.id===wrongQuestion.id));
 assert(!next.api.getRound().entries.some(e=>e.id===correctQuestion.id));
});
