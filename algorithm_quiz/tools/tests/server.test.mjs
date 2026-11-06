import {test} from 'node:test';
import assert from 'node:assert/strict';
import {mkdtemp,readFile,writeFile,rm} from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import {startServer} from '../server.mjs';
import {emptyProfile,recordResult,WEEK} from '../study-core.mjs';
const q={id:'1',title:'测试题',category:'DFS',statement:'测试摘要',explanation:'沿分支访问'};
async function connect(app) {
 const page=await (await fetch(app.url)).text();
 const token=page.match(/name="profile-token" content="([a-f0-9]+)"/)[1];
 const headers={'Content-Type':'application/json','X-Profile-Token':token};
 return {headers,post:profile=>fetch(app.url+'/api/profile',{method:'POST',headers,body:JSON.stringify(profile)}),get:()=>fetch(app.url+'/api/profile',{headers})};
}
test('本地文件持久化、重启恢复、并发合并、禁止直接读取私人文件',async()=>{
 const directory=await mkdtemp(path.join(os.tmpdir(),'quiz-profile-test-'));
 let app;
 try {
  app=await startServer({port:0,dataDirectory:directory});let client=await connect(app);
  const unauthorized=await fetch(app.url+'/api/profile');assert.equal(unauthorized.status,403);
  assert.equal((await fetch(app.url+'/personal/profile.json')).status,404);
  assert.equal((await fetch(app.url+'/api/profile',{headers:{...client.headers,Origin:'https://example.com'}})).status,403);
  const at=Date.now(),a=emptyProfile(),b=emptyProfile();
  recordResult(a,q,'BFS',at,'wrong');
  recordResult(b,{...q,id:'2'},'DFS',at,'right');
  const responses=await Promise.all([client.post(a),client.post(b)]);assert(responses.every(r=>r.ok));
  const current=(await(await client.get()).json()).profile;
  assert.equal(current.history.length,2);assert.equal(current.records['1'].status,'wrong');
  assert.equal(current.records['2'].reviewAfter,at+WEEK);
  const mistakes=JSON.parse(await readFile(path.join(directory,'mistakes.json'),'utf8'));
  const schedule=JSON.parse(await readFile(path.join(directory,'review_schedule.json'),'utf8'));
  const history=JSON.parse(await readFile(path.join(directory,'history.json'),'utf8'));
  assert.equal(mistakes.questions[0].id,'1');assert.equal(schedule.questions[0].id,'2');assert.equal(history.attempts.length,2);
  await app.close();app=await startServer({port:0,dataDirectory:directory});client=await connect(app);
  assert.equal((await(await client.get()).json()).profile.history.length,2);
  const correct=emptyProfile();recordResult(correct,q,'DFS',at+1,'correct');
  assert((await client.post(correct)).ok);
  assert.equal(JSON.parse(await readFile(path.join(directory,'mistakes.json'),'utf8')).questions.length,0);
  const before=await readFile(path.join(directory,'profile.json'),'utf8');
  const malformed=await fetch(app.url+'/api/profile',{method:'POST',headers:client.headers,body:'not json'});
  assert.equal(malformed.status,400);
  assert.equal(await readFile(path.join(directory,'profile.json'),'utf8'),before);
 } finally {if(app)await app.close();await rm(directory,{recursive:true,force:true});}
});
test('磁盘存档损坏时停止，不覆盖记录和备份',async()=>{
 const directory=await mkdtemp(path.join(os.tmpdir(),'quiz-corrupt-test-'));
 try {
  await writeFile(path.join(directory,'profile.json'),'{bad json');
  await writeFile(path.join(directory,'profile.json.bak'),'backup');
  await assert.rejects(startServer({port:0,dataDirectory:directory}),/停止以保护原文件/);
  assert.equal(await readFile(path.join(directory,'profile.json'),'utf8'),'{bad json');
  assert.equal(await readFile(path.join(directory,'profile.json.bak'),'utf8'),'backup');
 } finally {await rm(directory,{recursive:true,force:true});}
});

test('重复启动被拒绝，不能改写现有存档或干扰保存',async()=>{
 const {stat}=await import('node:fs/promises');
 const directory=await mkdtemp(path.join(os.tmpdir(),'quiz-double-start-'));
 let app;
 try {
  app=await startServer({port:0,dataDirectory:directory});const client=await connect(app);
  const before=await stat(path.join(directory,'profile.json'));
  await assert.rejects(startServer({port:Number(new URL(app.url).port),dataDirectory:directory}));
  const after=await stat(path.join(directory,'profile.json'));
  assert.equal(after.ino,before.ino,'失败的重复启动不得替换 profile.json');
  const p=emptyProfile();recordResult(p,q,'DFS',Date.now(),'after-duplicate');
  assert((await client.post(p)).ok);
  assert.equal(JSON.parse(await readFile(path.join(directory,'profile.json'),'utf8')).history.length,1);
 } finally {if(app)await app.close();await rm(directory,{recursive:true,force:true});}
});

test('完整题面接口带页面凭证，返回全部内容并写入个人缓存',async()=>{
 const directory=await mkdtemp(path.join(os.tmpdir(),'quiz-full-api-'));let app,calls=0;
 const html='<p>自编完整题面夹具。</p><pre>示例一</pre><pre>示例二</pre><ul><li>全部约束</li></ul>';
 try {
  app=await startServer({port:0,dataDirectory:directory,questionFetcher:async()=>{
   calls++;return {ok:true,json:async()=>({data:{question:{questionFrontendId:'1',title:'Test',translatedTitle:'测试',titleSlug:'test-question',difficulty:'Easy',isPaidOnly:false,translatedContent:html}}})};
  }});
  const client=await connect(app),url=app.url+'/api/question/test-question';
  assert.equal((await fetch(url)).status,403);assert.equal(calls,0);
  const result=await(await fetch(url,{headers:client.headers})).json();assert.equal(result.question.content_html,html);
  assert.equal((await(await fetch(url,{headers:client.headers})).json()).question.content_html,html);assert.equal(calls,1);
  const disk=JSON.parse(await readFile(path.join(directory,'question_content','test-question.json'),'utf8'));
  assert.equal(disk.content_html,html);
  assert.equal((await fetch(app.url+'/personal/question_content/test-question.json')).status,404);
 } finally {if(app)await app.close();await rm(directory,{recursive:true,force:true});}
});
