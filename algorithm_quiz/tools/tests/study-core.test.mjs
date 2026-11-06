// 使用 Node 原生测试接口；题库和页面不依赖测试库。
import {test} from 'node:test';
import assert from 'node:assert/strict';
import {emptyProfile, recordResult, eligibleQuestions, drawStudyRound, mergeProfiles, validateProfile, WEEK} from '../study-core.mjs';
const q = id => ({id:String(id),category:'DFS',option_a:'DFS',option_b:'BFS',option_c:'KMP',option_d:'贪心'});
const bank = Array.from({length:30},(_,i)=>q(i));
const now = 1793930400000;
test('错题持续可抽；答对从提交时起七天后才能再次出现',()=>{
 const p=emptyProfile();
 recordResult(p,q(0),'BFS',now,'wrong');
 assert.equal(p.records['0'].status,'wrong');
 assert(eligibleQuestions(bank,p,now+WEEK*3).some(q=>q.id==='0'));
 recordResult(p,q(0),'DFS',now+1000,'right');
 assert.equal(p.records['0'].wrongCount,1);
 assert.equal(p.records['0'].correctCount,1);
 assert(!eligibleQuestions(bank,p,now+1000).some(q=>q.id==='0'));
 assert(!eligibleQuestions(bank,p,now+1000+WEEK-1).some(q=>q.id==='0'));
 assert(eligibleQuestions(bank,p,now+1000+WEEK).some(q=>q.id==='0'));
});
test('每次提交只计一次；后续再次答错会撤销冷却',()=>{
 const p=emptyProfile();recordResult(p,q(0),'DFS',now,'one');recordResult(p,q(0),'DFS',now,'one');
 assert.equal(p.history.length,1);assert.equal(p.records['0'].correctCount,1);
 recordResult(p,q(0),'KMP',now+1,'two');assert.equal(p.records['0'].status,'wrong');
 assert(eligibleQuestions(bank,p,now+2).some(q=>q.id==='0'));
});
test('错题优先、最多20道不重复，冷却题不拿来补足20题',()=>{
 const p=emptyProfile();recordResult(p,q(2),'BFS',now,'w');recordResult(p,q(0),'DFS',now,'c');
 const round=drawStudyRound(bank,p,now,()=>0.5);
 assert.equal(round.entries.length,20);assert.equal(round.entries[0].id,'2');
 assert.equal(new Set(round.entries.map(e=>e.id)).size,20);assert(!round.entries.some(e=>e.id==='0'));
 assert(round.entries.every(e=>new Set(e.options).size===4&&!e.checked));
 for(let i=1;i<30;i++)recordResult(p,q(i),'DFS',now,'c'+i);
 assert.equal(drawStudyRound(bank,p,now).entries.length,0);
});
test('不足20道可用题时只出实际可用题',()=>{
 const r=drawStudyRound(bank.slice(0,3),emptyProfile(),now);
 assert.equal(r.entries.length,3);
});
test('JSON往返后错题和冷却仍有效；损坏记录拒绝读取',()=>{
 const p=emptyProfile();recordResult(p,q(1),'KMP',now,'a');recordResult(p,q(2),'DFS',now,'b');
 const restored=validateProfile(JSON.parse(JSON.stringify(p)));
 assert.equal(restored.records['1'].status,'wrong');assert.equal(restored.records['2'].reviewAfter,now+WEEK);
 assert.throws(()=>validateProfile({version:2,history:[{id:'x'}]}));
 assert.throws(()=>validateProfile({version:2,history:'broken'}));
});
test('合并浏览器与磁盘记录不重复，较新结果决定冷却和错题状态',()=>{
 const a=emptyProfile(),b=emptyProfile();
 recordResult(a,q(0),'BFS',now,'a');recordResult(b,q(0),'DFS',now+100,'b');
 a.session={updatedAt:now};b.session={updatedAt:now+1};
 const merged=mergeProfiles(a,b);
 assert.equal(merged.history.length,2);assert.equal(merged.records['0'].status,'correct');
 assert.equal(merged.session.updatedAt,now+1);
 assert.equal(mergeProfiles(merged,b).history.length,2);
});
