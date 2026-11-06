import {test} from 'node:test';
import assert from 'node:assert/strict';
import {mkdtemp,readdir,rm} from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import {createQuestionSource} from '../question-source.mjs';
// 自编题面夹具，检查多示例、约束、上下标和图片均不被摘要化。
const fullHTML='<p>给定测试数组，请按指定规则返回结果。</p><p><strong>示例 1：</strong></p><pre>输入：a = [2]\n输出：2</pre><p><strong>示例 2：</strong></p><pre>输入：a = []\n输出：0</pre><p>约束：</p><ul><li>0 ≤ n ≤ 10<sup>5</sup></li></ul><img src="https://assets.leetcode.com/test.png" alt="测试图">';
function upstream(overrides={}) {return {questionFrontendId:'1',title:'Test',translatedTitle:'测试题',titleSlug:'test-question',difficulty:'Easy',isPaidOnly:false,translatedContent:fullHTML,content:'<p>English fallback</p>',...overrides};}
test('官方题面不截断，重复请求合并，重启后直接用磁盘缓存',async()=>{
 const dir=await mkdtemp(path.join(os.tmpdir(),'quiz-question-source-'));let calls=0;
 try {
  const load=createQuestionSource({directory:dir,fetcher:async()=>{calls++;return {ok:true,json:async()=>({data:{question:upstream()}})};}});
  const [a,b]=await Promise.all([load('test-question'),load('test-question')]);
  assert.equal(a.content_html,fullHTML);assert.equal(b.content_html,fullHTML);assert.equal(calls,1);
  assert.equal(a.language,'zh-CN');assert.equal(a.source_url,'https://leetcode.cn/problems/test-question/');
  const cached=createQuestionSource({directory:dir,fetcher:async()=>{throw new Error('应当使用缓存');}});
  assert.equal((await cached('test-question')).content_html,fullHTML);
  assert.deepEqual((await readdir(dir)).filter(n=>n.endsWith('.json')),['test-question.json']);
 } finally {await rm(dir,{recursive:true,force:true});}
});
test('会员题、题号不匹配、无内容与不合法slug不能缓存为完整题面',async()=>{
 const dir=await mkdtemp(path.join(os.tmpdir(),'quiz-question-reject-'));
 try {
  for(const question of [upstream({isPaidOnly:true}),upstream({titleSlug:'another'}),upstream({translatedContent:'',content:''})]) {
   const load=createQuestionSource({directory:dir,fetcher:async()=>({ok:true,json:async()=>({data:{question}})})});
   await assert.rejects(load('test-question'));
  }
  const load=createQuestionSource({directory:dir,fetcher:async()=>{throw new Error('不应请求');}});
  await assert.rejects(load('../private'));
  assert.equal((await readdir(dir)).filter(n=>n.endsWith('.json')).length,0);
 } finally {await rm(dir,{recursive:true,force:true});}
});

test('总等待时间包含排队，快速切题不会累加等待所有旧题超时',async()=>{
 const dir=await mkdtemp(path.join(os.tmpdir(),'quiz-question-timeout-'));
 try {
  const load=createQuestionSource({directory:dir,timeoutMs:40,fetcher:async(_,options)=>new Promise((resolve,reject)=>{
   options.signal.addEventListener('abort',()=>{const error=new Error('aborted');error.name='AbortError';reject(error);},{once:true});
  })});
  const finished=[];
  await Promise.all(['first-question','second-question','third-question','fourth-question'].map(slug=>load(slug).catch(()=>finished.push(Date.now()))));
  assert(finished.at(-1)-finished[0]<80,'四道题应在各自总等待时限内失败，不能逐题累加超时');
 } finally {await rm(dir,{recursive:true,force:true});}
});

test('离开题目取消等待；同题另一个读者仍可获得完整内容',async()=>{
 const dir=await mkdtemp(path.join(os.tmpdir(),'quiz-question-cancel-'));
 try {
  let release;const gate=new Promise(resolve=>{release=resolve;});let calls=0;
  const load=createQuestionSource({directory:dir,fetcher:async()=>{calls++;await gate;return {ok:true,json:async()=>({data:{question:upstream()}})};}});
  const controller=new AbortController();
  const first=load('test-question',{signal:controller.signal});
  const rejected=assert.rejects(first,/取消/);
  const second=load('test-question');
  await new Promise(resolve=>setTimeout(resolve,5));controller.abort();release();
  await rejected;assert.equal((await second).content_html,fullHTML);assert.equal(calls,1);
 } finally {await rm(dir,{recursive:true,force:true});}
});
