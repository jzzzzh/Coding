// 浏览器与本地存档服务共享的纯 JavaScript 规则；不导入任何库。
export const WEEK = 7 * 24 * 60 * 60 * 1000;
export function emptyProfile() {
  return {version:2, updatedAt:0, records:Object.create(null), history:[], session:null};
}
function checkEvent(event) {
  if (!event || typeof event.attemptId !== 'string' || !event.attemptId || event.attemptId.length > 160 ||
      typeof event.questionId !== 'string' || !event.questionId || event.questionId.length > 80 ||
      typeof event.category !== 'string' || !event.category || typeof event.selected !== 'string' || !event.selected ||
      !Number.isSafeInteger(event.at) || event.at < 0 || event.at > 8640000000000000-WEEK) throw new Error('答题历史格式损坏，未覆盖原有记录。');
  return {attemptId:event.attemptId, questionId:event.questionId, category:event.category,
    selected:event.selected, at:event.at, correct:event.selected===event.category,
    question:event.question && typeof event.question==='object' && !Array.isArray(event.question) ? {...event.question} : {id:event.questionId}};
}
function rebuild(history, session=null) {
  const profile=emptyProfile();
  const unique=new Map();
  for (const raw of history) {
    const event=checkEvent(raw);
    if (unique.has(event.attemptId) && JSON.stringify(unique.get(event.attemptId))!==JSON.stringify(event)) throw new Error('答题历史编号冲突，未覆盖原有记录。');
    unique.set(event.attemptId,event);
  }
  profile.history=[...unique.values()].sort((a,b)=>a.at-b.at||a.attemptId.localeCompare(b.attemptId));
  for (const event of profile.history) {
    const prior=profile.records[event.questionId];
    profile.records[event.questionId]={id:event.questionId, question:event.question, status:event.correct?'correct':'wrong',
      selected:event.selected, category:event.category, lastAnsweredAt:event.at,
      reviewAfter:event.correct ? event.at+WEEK : 0,
      wrongCount:(prior?.wrongCount||0)+(event.correct?0:1), correctCount:(prior?.correctCount||0)+(event.correct?1:0)};
    profile.updatedAt=Math.max(profile.updatedAt,event.at);
  }
  profile.session=session && typeof session==='object' && !Array.isArray(session) ? session : null;
  profile.updatedAt=Math.max(profile.updatedAt,Number.isSafeInteger(session?.updatedAt)?session.updatedAt:0);
  return profile;
}
export function validateProfile(value) {
  if (!value || value.version!==2 || !Array.isArray(value.history)) throw new Error('个人记录格式不兼容，未覆盖原有记录。');
  return rebuild(value.history,value.session);
}
export function mergeProfiles(a,b) {
  const left=validateProfile(a),right=validateProfile(b);
  const session=(left.session?.updatedAt||0)>(right.session?.updatedAt||0)?left.session:right.session;
  return rebuild([...left.history,...right.history],session);
}
export function recordResult(profile,question,selected,at=Date.now(),attemptId=`${at}-${Math.random().toString(36).slice(2)}`) {
  if (profile.history.some(e=>e.attemptId===attemptId)) return profile.records[String(question.id)];
  // 同一毫秒内重答时仍保持提交顺序，避免合并记录后较早的错误覆盖新答案。
  at=Math.max(at,(profile.records[String(question.id)]?.lastAnsweredAt??-1)+1);
  const snapshot={};
  for (const key of ['id','title','category','statement','example_input','example_output','explanation','source_url']) snapshot[key]=String(question[key]??'');
  const event=checkEvent({attemptId,questionId:String(question.id),category:question.category,selected,at,question:snapshot});
  const next=rebuild([...profile.history,event],profile.session);
  Object.assign(profile,next);
  return profile.records[String(question.id)];
}
export function eligibleQuestions(questions,profile,now=Date.now()) {
  return questions.filter(q=>!profile.records[q.id] || profile.records[q.id].status==='wrong' || profile.records[q.id].reviewAfter<=now);
}
function studyShuffle(values,random) {
  const result=[...values];
  for (let i=result.length-1;i>0;i--) {const j=Math.floor(random()*(i+1));[result[i],result[j]]=[result[j],result[i]];}
  return result;
}
export function drawStudyRound(questions,profile,now=Date.now(),random=Math.random) {
  const ready=eligibleQuestions(questions,profile,now);
  const wrong=studyShuffle(ready.filter(q=>profile.records[q.id]?.status==='wrong'),random);
  const rest=studyShuffle(ready.filter(q=>profile.records[q.id]?.status!=='wrong'),random);
  return {entries:[...wrong,...rest].slice(0,20).map(q=>({id:q.id,
    options:studyShuffle([q.option_a,q.option_b,q.option_c,q.option_d],random),selected:null,checked:false,attemptId:null})),
    current:0,submitted:false,onlyErrors:false,startedAt:now};
}
