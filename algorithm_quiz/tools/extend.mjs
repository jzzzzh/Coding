// 扩展公开题面；先运行 fetch-index.mjs 和 crawl.mjs，再运行本文件。
// node tools/extend.mjs > expanded.json（验证成功后替换 question_bank.json）
import index from '../leetcode_index.json' with {type:'json'};
import base from '../question_bank.json' with {type:'json'};
import {extraCatalog} from './extra-catalog.mjs';
import {catalog} from './catalog.mjs';
import {fetchQuestion, categories} from './crawl.mjs';

const byId = new Map(index.questions.map(q => [q.id, q]));
// 后续增量扩充的记录也要保留，不能再按最初的人工清单裁剪。
const questions = base.questions.map(q=>({...q}));
// 人工样例的修正也同步到已有基础记录。
for (const q of questions) {
  const seed = catalog.find(s => s.slug === q.slug);
  if (seed) Object.assign(q, {example_input:seed.example_input, example_output:seed.example_output});
}
const ids = new Set(questions.map(q => q.id));
const skips = [];
let pending = extraCatalog.filter(q => !ids.has(q.id));
console.error(`扩展候选 ${pending.length}，已有 ${questions.length}`);
for (const seed of pending) {
  const source = byId.get(seed.id);
  if (!source || source.paid) {
    skips.push({id:seed.id, reason:!source ? '目录中不存在' : '会员题'});
    continue;
  }
  try {
    const q = await fetchQuestion({...seed, slug:source.slug});
    if (q.id !== seed.id) throw new Error('题号不一致');
    questions.push(q); ids.add(q.id);
    console.error(`[${questions.length}] ${q.id}. ${q.title}`);
  } catch (error) {
    skips.push({id:seed.id, reason:error.message});
    console.error(`跳过 ${seed.id}：${error.message}`);
  }
  await new Promise(resolve => setTimeout(resolve, 200));
}
console.log(JSON.stringify({version:1, source:'https://leetcode.cn/graphql/', categories,
  question_count:questions.length, index_total:index.total, public_index_count:index.questions.filter(q => !q.paid).length,
  scope_note:'索引覆盖当次返回的完整目录；可答题库为已整理摘要、核实公开题面并具有完整示例的候选题，非全部公开题目。',
  skipped:skips, questions}, null, 2));
