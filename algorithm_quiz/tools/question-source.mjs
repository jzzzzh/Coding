// 按打开的题目读取官方公开题面，完整保留正文、示例与约束；缓存在个人目录。
// 使用 Node 内置文件接口和原生 fetch，不需要安装包。
import {readFile,writeFile,mkdir,rename,rm} from 'node:fs/promises';
import path from 'node:path';
import {randomBytes} from 'node:crypto';
const endpoint='https://leetcode.cn/graphql/';
const query=`query FullQuizQuestion($slug: String!) {
 question(titleSlug:$slug) {
  questionFrontendId title translatedTitle titleSlug difficulty isPaidOnly translatedContent content
 }
}`;
function sourceError(message,status=502) {const error=new Error(message);error.status=status;return error;}
function validContent(value,slug) {
 return value && value.version===1 && value.slug===slug && typeof value.id==='string' &&
  typeof value.content_html==='string' && value.content_html.trim().length>0 && value.content_html.length<=2_000_000 &&
  value.source_url===`https://leetcode.cn/problems/${slug}/` && ['zh-CN','en'].includes(value.language);
}
export function createQuestionSource({directory,fetcher=fetch,timeoutMs=15000}={}) {
 const inflight=new Map(), waiting=[];let running=false,lastStarted=0;
 async function cached(slug) {
  try {const value=JSON.parse(await readFile(path.join(directory,slug+'.json'),'utf8'));return validContent(value,slug)?{...value,cache_saved:true}:null;}
  catch(error) {if(error.code==='ENOENT'||error instanceof SyntaxError)return null;throw sourceError('题面缓存读取失败：'+error.message,500);}
 }
 async function fetchAndCache(slug,signal) {
  const existing=await cached(slug);if(existing)return existing;
  const remaining=200-(Date.now()-lastStarted);if(remaining>0)await new Promise(resolve=>setTimeout(resolve,remaining));
  lastStarted=Date.now();
  if(signal.aborted)throw sourceError('已取消读取题面。',499);
  let payload;
  try {
   const response=await fetcher(endpoint,{method:'POST',signal,
    headers:{'Content-Type':'application/json','User-Agent':'AlgorithmStudyQuiz/1.0','Referer':'https://leetcode.cn/'},
    body:JSON.stringify({query,variables:{slug}})});
   if(!response.ok)throw sourceError(response.status===429?'力扣暂时限流，请稍后重试。':`官方题面暂不可用（HTTP ${response.status}）。`);
   payload=await response.json();
  } catch(error) {
   if(error.status)throw error;
   throw sourceError(signal.aborted?'已取消读取题面。':'完整题面获取失败：'+error.message,signal.aborted?499:502);
  }
  const question=payload.data?.question;
  if(payload.errors||!question)throw sourceError('官方接口未返回有效题面，请打开原题核对。');
  if(question.isPaidOnly)throw sourceError('该题面需要会员权限，请前往官方页面阅读。',403);
  if(question.titleSlug!==slug)throw sourceError('返回题目与请求不一致，未缓存。');
  const html=question.translatedContent?.trim()?question.translatedContent:question.content;
  const result={version:1,id:String(question.questionFrontendId),slug,title:question.translatedTitle||question.title,
   difficulty:question.difficulty,content_html:html,language:question.translatedContent?.trim()?'zh-CN':'en',
   source_url:`https://leetcode.cn/problems/${slug}/`,fetched_at:new Date().toISOString()};
  if(!validContent(result,slug))throw sourceError('未取得完整题面，未缓存空内容。');
  const temporary=path.join(directory,slug+'.'+randomBytes(8).toString('hex')+'.tmp');
  try {
   await mkdir(directory,{recursive:true,mode:0o700});
   await writeFile(temporary,JSON.stringify(result,null,2)+'\n',{mode:0o600});
   await rename(temporary,path.join(directory,slug+'.json'));
   return {...result,cache_saved:true};
  } catch(error) {return {...result,cache_saved:false,cache_error:'本次已显示完整题面，但缓存写入失败：'+error.message};}
  finally {await rm(temporary,{force:true}).catch(()=>{});}
 }
 // 每个访问者的总时限包含排队时间；离开题目后取消相应等待。
 function finish(task,waiter,error,value) {
  if(waiter.done)return;
  waiter.done=true;clearTimeout(waiter.timer);waiter.signal?.removeEventListener('abort',waiter.abort);
  task.waiters.delete(waiter);
  if(error)waiter.reject(error);else waiter.resolve(value);
  if(!task.completed&&!task.waiters.size) {
   task.controller.abort();
   const i=waiting.indexOf(task);if(i>=0)waiting.splice(i,1);
   if(inflight.get(task.slug)===task)inflight.delete(task.slug);
  }
 }
 function pump() {
  if(running)return;
  // 尚未开始的请求优先处理最近打开的题，避免陈旧请求阻塞当前题。
  let task;
  while(waiting.length&&!task){const next=waiting.pop();if(next.waiters.size&&!next.controller.signal.aborted)task=next;}
  if(!task)return;
  running=true;
  (async()=>{
   let value,error;
   try {value=await fetchAndCache(task.slug,task.controller.signal);}catch(problem){error=problem;}
   task.completed=true;
   for(const waiter of [...task.waiters])finish(task,waiter,error,value);
   if(inflight.get(task.slug)===task)inflight.delete(task.slug);
   running=false;pump();
  })();
 }
 return async function load(slug,{signal}={}) {
  const started=Date.now();
  if(typeof slug!=='string'||!slug||slug.length>160||!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(slug))throw sourceError('无效题目标识。',400);
  if(signal?.aborted)throw sourceError('已取消读取题面。',499);
  const existing=await cached(slug);if(existing)return existing;
  if(signal?.aborted)throw sourceError('已取消读取题面。',499);
  const remaining=timeoutMs-(Date.now()-started);
  if(remaining<=0)throw sourceError('完整题面读取超时，请重试或打开官方原题。',504);
  let task=inflight.get(slug);
  if(!task||task.controller.signal.aborted) {
   task={slug,controller:new AbortController(),waiters:new Set(),completed:false};
   inflight.set(slug,task);waiting.push(task);
  }
  return new Promise((resolve,reject)=>{
   const waiter={resolve,reject,signal,done:false};
   waiter.abort=()=>finish(task,waiter,sourceError('已取消读取题面。',499));
   waiter.timer=setTimeout(()=>finish(task,waiter,sourceError('完整题面读取超时，请重试或打开官方原题。',504)),remaining);
   task.waiters.add(waiter);signal?.addEventListener('abort',waiter.abort,{once:true});
   pump();
  });
 };
}
