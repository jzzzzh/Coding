// 抓取公开题目索引；无第三方依赖。只请求公开元数据，不访问会员题面。
const questions = [];
let total = 1;
for (let skip = 0; skip < total; skip += 100) {
  const query = `query { problemsetQuestionList(categorySlug: "", skip: ${skip}, limit: 100, filters: {}) { total questions { titleSlug } } }`;
  const response = await fetch('https://leetcode.cn/graphql/', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({query})});
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  const data = await response.json();
  const page = data.data?.problemsetQuestionList;
  if (!page || data.errors || !page.questions.length) throw new Error('目录分页失败：' + JSON.stringify(data.errors));
  total = page.total;
  questions.push(...page.questions);
  console.error(`目录 ${questions.length}/${total}`);
  await new Promise(resolve => setTimeout(resolve, 200));
}
const unique = [...new Map(questions.map(q => [q.titleSlug, q])).values()];
console.log(JSON.stringify({fetched_at: new Date().toISOString(), total, questions: unique.map(q => ({id: q.frontendQuestionId, title: q.titleCn || q.title, english_title:q.title, slug:q.titleSlug, difficulty:q.difficulty, paid:q.paidOnly, tags:q.topicTags.map(t => ({slug:t.slug, name:t.nameTranslated || t.name})), source_url:`https://leetcode.cn/problems/${q.titleSlug}/`}))}, null, 2));
