import {test} from 'node:test';
import assert from 'node:assert/strict';
import {fetchQuestion} from '../crawl.mjs';
const seed={id:'99',slug:'example-question',category:'动态规划',sourceTag:'dynamic-programming',statement:'自编测试提示'};
const payload=(changes={})=>({data:{question:{questionFrontendId:'99',title:'Example',translatedTitle:'示例题',titleSlug:'example-question',difficulty:'Easy',isPaidOnly:false,translatedContent:'<p>自编题面。</p><pre>输入：n = 2\n输出：3</pre>',topicTags:[{slug:'dynamic-programming',name:'Dynamic Programming',translatedName:'动态规划'}],...changes}}});
test('扩展记录来自实时官方标签，保留示例并生成唯一四选一答案',async()=>{
 const q=await fetchQuestion(seed,{fetcher:async()=>({ok:true,json:async()=>payload()})});
 assert.equal(q.id,'99');assert.deepEqual(q.source_tag_slugs,['dynamic-programming']);
 assert.equal(q.example_input,'n = 2');assert.equal(q.example_output,'3');
 const options=[q.option_a,q.option_b,q.option_c,q.option_d];
 assert.equal(new Set(options).size,4);assert.equal(options['ABCD'.indexOf(q.answer)],'动态规划');
});
test('标签漂移或示例缺失立即跳过，不能伪造题目或反复请求',async()=>{
 for(const change of [{topicTags:[{slug:'array',name:'Array'}]},{translatedContent:'<p>没有输入输出示例。</p>'}]) {
  let calls=0;
  await assert.rejects(fetchQuestion(seed,{fetcher:async()=>{calls++;return {ok:true,json:async()=>payload(change)};}}));
  assert.equal(calls,1);
 }
});
