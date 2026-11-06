// 本地存档服务：只使用 Node 内置模块，无 npm 依赖；仅监听本机回环地址。
import http from 'node:http';
import {readFile,writeFile,mkdir,rename,rm,stat} from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {randomBytes} from 'node:crypto';
import {emptyProfile,validateProfile,mergeProfiles} from './study-core.mjs';
import {createQuestionSource} from './question-source.mjs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
async function atomicJSON(directory,name,data) {
  const target=path.join(directory,name), temporary=target+'.'+randomBytes(8).toString('hex')+'.tmp';
  try {
    await writeFile(temporary,JSON.stringify(data,null,2)+'\n',{mode:0o600});
    await rename(temporary,target);
  } finally {await rm(temporary,{force:true});}
}
async function acquireWriter(directory) {
  await mkdir(directory,{recursive:true,mode:0o700});
  const lock=path.join(directory,'.writer-lock');
  for(let attempt=0;attempt<2;attempt++) {
    try {
      await mkdir(lock,{mode:0o700});
      try {await writeFile(path.join(lock,'owner.json'),JSON.stringify({pid:process.pid}),{mode:0o600});}
      catch(error) {await rm(lock,{recursive:true,force:true});throw error;}
      return ()=>rm(lock,{recursive:true,force:true});
    } catch(error) {
      if(error.code!=='EEXIST')throw error;
      let alive=true;
      try {
        const owner=JSON.parse(await readFile(path.join(lock,'owner.json'),'utf8'));
        if(!Number.isInteger(owner.pid)||owner.pid<=0)throw new Error('无效锁');
        try {process.kill(owner.pid,0);}catch(check){if(check.code==='ESRCH')alive=false;else alive=true;}
      } catch(check) {
        // 另一个刚启动的进程可能还没写完锁信息；不能把它的锁误删。
        alive=Date.now()-(await stat(lock)).mtimeMs<30000;
      }
      if(alive)throw new Error('题库已在运行，个人记录正在使用中。请使用已打开的题库窗口。');
      await rm(lock,{recursive:true,force:true});
    }
  }
  throw new Error('无法取得个人记录的独占写入权限，请稍后重试。');
}
async function persistProfile(directory,profile) {
  await mkdir(directory,{recursive:true,mode:0o700});
  const records=Object.values(profile.records);
  await atomicJSON(directory,'mistakes.json',{version:2,updatedAt:profile.updatedAt,questions:records.filter(q=>q.status==='wrong')});
  await atomicJSON(directory,'review_schedule.json',{version:2,updatedAt:profile.updatedAt,questions:records.filter(q=>q.status==='correct').map(q=>({...q,reviewAt:new Date(q.reviewAfter).toISOString()}))});
  await atomicJSON(directory,'history.json',{version:2,updatedAt:profile.updatedAt,attempts:profile.history});
  try {
    const old=await readFile(path.join(directory,'profile.json'),'utf8');
    validateProfile(JSON.parse(old));
    await atomicJSON(directory,'profile.json.bak',JSON.parse(old));
  } catch(error) {if(error.code!=='ENOENT')throw error;}
  // 完整存档最后原子替换，读取以此为准；派生文件可由此重新生成。
  await atomicJSON(directory,'profile.json',profile);
}
export async function startServer({port=8765,dataDirectory=path.join(root,'personal'),questionFetcher=fetch}={}) {
  const release=await acquireWriter(dataDirectory);
  try {
  let profile;
  try {profile=validateProfile(JSON.parse(await readFile(path.join(dataDirectory,'profile.json'),'utf8')));}
  catch(error) {
    if(error.code==='ENOENT')profile=emptyProfile();
    else throw new Error('个人存档无法读取，已停止以保护原文件。可检查 profile.json 或用 profile.json.bak 恢复。原因：'+error.message);
  }
  const token=randomBytes(32).toString('hex');
  const loadQuestion=createQuestionSource({directory:path.join(dataDirectory,'question_content'),fetcher:questionFetcher});
  let baseURL,writeQueue=Promise.resolve();
  const send=(res,status,body,type='application/json; charset=utf-8')=>{
    res.writeHead(status,{'Content-Type':type,'Cache-Control':'no-store','X-Content-Type-Options':'nosniff','X-Frame-Options':'DENY'});
    res.end(typeof body==='string'||Buffer.isBuffer(body)?body:JSON.stringify(body));
  };
  const server=http.createServer(async(req,res)=>{
    try {
      if(req.headers.host!==new URL(baseURL).host || (req.headers.origin&&req.headers.origin!==baseURL)) return send(res,403,{error:'仅允许本机页面访问'});
      const url=new URL(req.url,baseURL);
      if(url.pathname.startsWith('/api/question/')) {
        if(req.headers['x-profile-token']!==token)return send(res,403,{error:'本地页面凭证无效，请刷新页面'});
        if(req.method!=='GET')return send(res,405,{error:'不支持此请求方法'});
        const controller=new AbortController();
        const disconnected=()=>{if(!res.writableEnded)controller.abort();};
        res.once('close',disconnected);
        try {
          const question=await loadQuestion(url.pathname.slice('/api/question/'.length),{signal:controller.signal});
          if(!res.destroyed)return send(res,200,{question});
        } catch(error) {if(!res.destroyed)return send(res,error.status||502,{error:error.message});}
        finally {res.removeListener('close',disconnected);}
        return;
      }
      if(url.pathname==='/api/profile') {
        if(req.headers['x-profile-token']!==token) return send(res,403,{error:'本地页面凭证无效，请刷新页面'});
        if(req.method==='GET') {await writeQueue.catch(()=>{});return send(res,200,{profile});}
        if(req.method!=='POST')return send(res,405,{error:'不支持此请求方法'});
        if(!(req.headers['content-type']||'').startsWith('application/json'))return send(res,415,{error:'只接受 JSON 记录'});
        let bytes=0;const chunks=[];
        for await(const chunk of req) {bytes+=chunk.length;if(bytes>20*1024*1024)return send(res,413,{error:'记录超过 20 MB'});chunks.push(chunk);}
        let incoming;
        try {incoming=validateProfile(JSON.parse(Buffer.concat(chunks).toString('utf8')));}
        catch(error) {return send(res,400,{error:error.message});}
        const operation=writeQueue.catch(()=>{}).then(async()=>{
          const merged=mergeProfiles(profile,incoming);
          await persistProfile(dataDirectory,merged);profile=merged;
        });
        writeQueue=operation;
        await operation;
        return send(res,200,{profile});
      }
      if(req.method!=='GET')return send(res,405,{error:'不支持此请求方法'});
      const files={'/':'index.html','/index.html':'index.html','/question_bank.csv':'question_bank.csv','/leetcode_public_index.csv':'leetcode_public_index.csv','/README.md':'README.md'};
      const name=Object.hasOwn(files,url.pathname)?files[url.pathname]:null;
      if(!name)return send(res,404,{error:'文件不存在'});
      let content=await readFile(path.join(root,name));
      if(name==='index.html')content=content.toString('utf8').replace('<head>',`<head><meta name="profile-token" content="${token}">`);
      return send(res,200,content,name.endsWith('.html')?'text/html; charset=utf-8':name.endsWith('.csv')?'text/csv; charset=utf-8':'text/plain; charset=utf-8');
    } catch(error) {if(!res.headersSent)send(res,500,{error:'本地存档操作失败：'+error.message});else res.end();}
  });
  await new Promise((resolve,reject)=>{server.once('error',reject);server.listen(port,'127.0.0.1',resolve);});
  baseURL=`http://127.0.0.1:${server.address().port}`;
  try {await persistProfile(dataDirectory,profile);}
  catch(error) {await new Promise(resolve=>server.close(resolve));throw error;}
  return {server,url:baseURL,dataDirectory,close:async()=>{
    await new Promise((resolve,reject)=>server.close(error=>error?reject(error):resolve()));
    await writeQueue.catch(()=>{});await release();
  }};
  } catch(error) {await release();throw error;}
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)) {
  try {
    const app=await startServer();
    console.log(`识题已启动：${app.url}\n个人记录：${app.dataDirectory}\n保持此窗口打开；按 Control+C 停止。`);
    if(!process.argv.includes('--no-open')) {
      const {spawn}=await import('node:child_process');
      if(process.platform==='darwin')spawn('open',[app.url],{stdio:'ignore'}).on('error',()=>{});
    }
    process.once('SIGINT',async()=>{await app.close();process.exit(0);});
    process.once('SIGTERM',async()=>{await app.close();process.exit(0);});
  } catch(error) {console.error(error.message);process.exitCode=1;}
}
