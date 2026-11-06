import {test} from 'node:test';
import assert from 'node:assert/strict';
import {buildExpansionCandidates} from '../expansion-catalog.mjs';
const question=(id,tags,more={})=>({id:String(id),slug:'question-'+id,title:'测试题',paid:false,tags:tags.map(slug=>({slug,name:slug})),...more});
test('扩充不重复旧题，不纳入会员题或宽泛标签推断题',()=>{
 const old=question(1,['dynamic-programming']);
 const index={questions:[old,question(2,['dynamic-programming']),question(3,['string']),question(4,['sorting']),question(5,['greedy'],{paid:true}),question(6,['dynamic-programming','binary-search'])]};
 const seeds=buildExpansionCandidates(index,[old]);
 assert.deepEqual(seeds.map(q=>q.id),['2']);assert.equal(seeds[0].category,'动态规划');
});
test('专门算法按精确标签或核实的模式匹配题选择，常见分类交替扩充',()=>{
 const index={questions:[question(10,['merge-sort','binary-search']),question(11,['quickselect','heap-priority-queue']),question(796,['string-matching','string']),question(12,['string-matching']),question(20,['dynamic-programming']),question(21,['dynamic-programming']),question(22,['greedy'])]};
 const seeds=buildExpansionCandidates(index,[]);
 assert.deepEqual(seeds.slice(0,3).map(q=>q.category),['归并/归并排序','快排/快速选择','KMP']);
 assert.deepEqual(seeds.slice(3).map(q=>q.category),['动态规划','贪心','动态规划']);
 assert(!seeds.some(q=>q.id==='12'));
});

test('不把字典树、线段树、并查集或解析栈中的辅助操作误标成现有主分类',()=>{
 const index={questions:[question(208,['trie','hash-table']),question(736,['stack','recursion','hash-table']),question(952,['union-find','hash-table']),question(1157,['segment-tree','binary-search']),question(3515,['depth-first-search','binary-indexed-tree']),question(212,['trie','backtracking'])]};
 const seeds=buildExpansionCandidates(index,[]);
 assert.deepEqual(seeds.map(q=>q.id),['212']);assert.equal(seeds[0].category,'回溯');
});

test('树构造中的辅助哈希和非树图解析步骤不自动推断分类',()=>{
 const index={questions:[question(889,['array','tree','hash-table','divide-and-conquer','binary-tree']),question(211,['design','trie','depth-first-search']),question(385,['stack','string','depth-first-search']),question(94,['tree','binary-tree','stack','depth-first-search'])]};
 assert.deepEqual(buildExpansionCandidates(index,[]).map(q=>q.id),['94']);
});
test('目录暂缺或筛选规则变化只能提示复核，不能删除已收录题目',async()=>{
 const {planExpansion}=await import('../expansion-catalog.mjs');
 const old=[{...question(796,['string-matching']),category:'KMP',classification_source:'official-tag-with-reviewed-training-direction'}];
 const plan=planExpansion({questions:[]},old);
 assert.deepEqual(plan.questions,old);assert.equal(plan.reviewNotes[0].id,'796');assert.deepEqual(plan.candidates,[]);
});
