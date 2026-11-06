// 增量扩充已存在的题库；保留全部旧题及原答案，不读写 personal/。
// node tools/expand.mjs --target 1000 > question_bank.next.json
import base from '../question_bank.json' with {type:'json'};
import index from '../leetcode_index.json' with {type:'json'};
import {planExpansion,TAG_CATEGORY} from './expansion-catalog.mjs';
import {fetchQuestion} from './crawl.mjs';
const argument=process.argv.indexOf('--target');
const target=argument>=0?Number(process.argv[argument+1]):1000;
if(!Number.isInteger(target)||target<base.questions.length)throw new Error('目标数量必须为不小于现有题库数量的整数');
const plan=planExpansion(index,base.questions),candidates=plan.candidates;
const questions=plan.questions,skipped=[];
const retained=questions.length;
const originalCount=base.original_question_count??(base.question_count-(base.expansion_added||0));
console.error(`当前 ${questions.length}，目标 ${target}，待核实候选 ${candidates.length}`);
for(const seed of candidates) {
 if(questions.length>=target)break;
 try {
  const q=await fetchQuestion(seed);
  if(q.id!==seed.id)throw new Error('返回题号不一致');
  if(seed.classification_source==='single-supported-official-category') {
   const liveCategories=[...new Set(q.source_tag_slugs.map(tag=>TAG_CATEGORY[tag]).filter(Boolean))];
   if(liveCategories.length!==1||liveCategories[0]!==seed.category)throw new Error('实时官方标签含多个可选训练分类，暂不收录');
  }
  q.classification_source=seed.classification_source;
  q.classification_tag=seed.sourceTag;
  q.content_note='扩展题：官方完整题面在答题页加载；CSV提供索引提示和官方示例；分类按核实的官方算法标签整理，不代表唯一解法。';
  questions.push(q);
  console.error(`[${questions.length}/${target}] ${q.id}. ${q.title} · ${q.category}`);
 } catch(error) {skipped.push({id:seed.id,reason:error.message});console.error(`跳过 ${seed.id}：${error.message}`);}
 await new Promise(resolve=>setTimeout(resolve,200));
}
if(questions.length<target)throw new Error(`有效题目仅 ${questions.length} 道，未写出不完整目标；可调整目标后重试`);
console.log(JSON.stringify({...base,question_count:questions.length,index_total:index.total,
 public_index_count:index.questions.filter(q=>!q.paid).length,
 expanded_at:new Date().toISOString(),
 original_question_count:originalCount,expansion_added:questions.length-originalCount,last_expansion_added:questions.length-retained,
 expansion_review:plan.reviewNotes,
 expansion_skipped:skipped,questions},null,2));
