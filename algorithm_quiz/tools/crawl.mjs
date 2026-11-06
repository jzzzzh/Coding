// 无第三方依赖：使用运行时原生 fetch、JSON、进程输出；目录内模块仅保存人工整理的题目配置。
// 运行：node tools/crawl.mjs > question_bank.json
import {catalog, groups} from './catalog.mjs';

const endpoint = 'https://leetcode.cn/graphql/';
const query = `query QuizQuestion($slug: String!) {
  question(titleSlug: $slug) {
    questionFrontendId title translatedTitle titleSlug difficulty isPaidOnly
    content translatedContent exampleTestcases topicTags { name translatedName slug }
  }
}`;
export const categories = groups.map(([name]) => name);
const mappedTags = {
  'hash-table': ['前缀和/哈希'], 'prefix-sum': ['前缀和/哈希'],
  'two-pointers': ['双指针', '归并/归并排序'], 'sliding-window': ['滑动窗口'],
  'binary-search': ['二分查找'], 'dynamic-programming': ['动态规划'], 'greedy': ['贪心'],
  'monotonic-stack': ['单调栈'], 'heap-priority-queue': ['堆/Top-K'],
  'breadth-first-search': ['BFS'], 'depth-first-search': ['DFS'], 'backtracking': ['回溯'],
  'quickselect': ['快排/快速选择'], 'sorting': ['快排/快速选择', '归并/归并排序'],
  'merge-sort': ['归并/归并排序'], 'divide-and-conquer': ['快排/快速选择', '归并/归并排序'],
  'string-matching': ['KMP'], 'string': ['KMP']
};
const pause = ms => new Promise(resolve => setTimeout(resolve, ms));
function shuffle(items) {
  const result = [...items];
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]];
  }
  return result;
}
export function makeOptions(seed, tags) {
  // 排除官方标签提示的其他常见解法，减少四选一的歧义。
  const excluded = new Set([seed.category]);
  for (const tag of tags) for (const category of mappedTags[tag.slug] || []) excluded.add(category);
  if (seed.category === 'BFS' || seed.category === 'DFS') {
    excluded.add('BFS'); excluded.add('DFS'); excluded.add('回溯');
  }
  if (seed.category === '单调栈') excluded.add('贪心');
  if (seed.category === '贪心') {excluded.add('堆/Top-K'); excluded.add('单调栈');}
  if (seed.category === '堆/Top-K') excluded.add('贪心');
  if (seed.category === 'BFS') excluded.add('堆/Top-K');
  if (seed.category === '回溯') {excluded.add('DFS'); excluded.add('BFS');}
  if (seed.category === 'KMP') excluded.add('前缀和/哈希');
  if (seed.category === '归并/归并排序' || seed.category === '快排/快速选择') {
    excluded.add('双指针'); excluded.add('堆/Top-K');
    excluded.add('归并/归并排序'); excluded.add('快排/快速选择');
  }
  const distractors = shuffle(categories.filter(c => !excluded.has(c))).slice(0, 3);
  if (distractors.length !== 3) throw new Error(`无法为 ${seed.slug} 生成无重复选项`);
  return shuffle([seed.category, ...distractors]);
}
export async function fetchQuestion(seed, {fetcher=fetch}={}) {
  for (let attempt = 0; attempt < 3; attempt++) {
    try {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 25000);
      let response;
      try {
        response = await fetcher(endpoint, {
          method: 'POST', signal: controller.signal,
          headers: {'Content-Type': 'application/json', 'User-Agent': 'AlgorithmStudyQuiz/1.0', 'Referer': 'https://leetcode.cn/'},
          body: JSON.stringify({query, variables: {slug: seed.slug}})
        });
      } finally { clearTimeout(timeout); }
      if (!response.ok) {
        // 不绕过登录或访问限制；限流时先退避，其他访问拒绝交给用户处理。
        if (response.status === 429 || response.status >= 500) throw new Error(`临时 HTTP ${response.status}`);
        throw new Error(`访问被拒绝 HTTP ${response.status}`);
      }
      const payload = await response.json();
      const q = payload.data?.question;
      if (!q || payload.errors) throw new Error(`无有效题目：${JSON.stringify(payload.errors || [])}`);
      if (q.isPaidOnly || !(q.translatedContent || q.content)) throw new Error('题目不是可用的公开题面');
      if (q.titleSlug !== seed.slug) throw new Error('返回题目与请求不一致');
      if(seed.sourceTag&&!q.topicTags.some(t=>t.slug===seed.sourceTag)) {
        const error=new Error('官方算法标签已变化，跳过该训练标注');error.permanent=true;throw error;
      }
      const options = makeOptions(seed, q.topicTags);
      const sourceExample = seed.example_input ? null : extractExample(q.translatedContent || q.content);
      if (!seed.example_input && !sourceExample) throw new Error('未提取到完整输入输出示例');
      return {
        id: String(q.questionFrontendId), slug: seed.slug,
        title: q.translatedTitle || q.title, difficulty: q.difficulty,
        statement: seed.statement, example_input: seed.example_input || sourceExample.input, example_output: seed.example_output || sourceExample.output,
        example_note: seed.example_input ? '自编示例；多解问题所列输出仅为一种。' : '输入输出取自力扣公开示例；题意为人工整理摘要。',
        option_a: options[0], option_b: options[1], option_c: options[2], option_d: options[3],
        answer: 'ABCD'[options.indexOf(seed.category)], category: seed.category,
        explanation: seed.explanation || reasons[seed.category],
        source_url: `https://leetcode.cn/problems/${seed.slug}/`,
        source_tags: q.topicTags.map(t => t.translatedName || t.name).join('、'),
        source_tag_slugs: q.topicTags.map(t=>t.slug),
        source_content_chars: (q.translatedContent || q.content).length,
        fetched_at: new Date().toISOString(), content_note: '根据力扣公开题面整理的中文摘要；分类及解析为本题库训练标注。'
      };
    } catch (error) {
      if (error.permanent || /访问被拒绝|未提取到完整输入输出示例|题目不是可用的公开题面/.test(error.message) || attempt === 2) throw new Error(`${seed.slug}: ${error.message}`);
      await pause(1500 * (attempt + 1));
    }
  }
}
const reasons = {
  '前缀和/哈希':'适合记录累计量、频次或已出现的键值关系，把重复扫描转换为预处理和快速查询。',
  '双指针':'按题目要求维护两个读取、写入或快慢位置，利用有序性或链表位置关系减少重复遍历。',
  '滑动窗口':'关键对象是连续区间，可随右端扩展和左端收缩增量维护区间约束或计数。',
  '二分查找':'有序性或可行性具有单调关系，可以依据中间候选排除一半范围。',
  '动态规划':'子问题存在重叠，定义前缀、区间、容量等状态，保存最优值或方案数并按依赖转移。',
  '贪心':'根据排序或局部边界做当前最优选择，避免枚举全部组合；具体选择规则应结合题目证明。',
  '单调栈':'通过维护候选值的单调次序，找到相邻的更大或更小边界，或在弹出候选时结算贡献。',
  '堆/Top-K':'需要反复获取当前极值或维护前 K 个候选，使用堆能高效更新动态候选集合。',
  'BFS':'按层或到达距离扩展，用队列保存下一批状态；无权图最短步数由首次到达确定。',
  'DFS':'沿分支深入访问，递归或显式栈汇总子树信息、标记连通区域或记录遍历路径。',
  '回溯':'需要枚举不同选择路径，做选择后递归探索，再撤销选择，并用约束剪枝去重。',
  '快排/快速选择':'按基准值划分候选，依据目标选择继续处理的区间，或递归完成原地排序。',
  '归并/归并排序':'利用有序子区间合并，合并过程中还可统计跨区间的配对或次序关系。',
  'KMP':'预处理相等真前后缀长度，使字符串匹配失配时复用先前信息，保持线性扫描。'
};
function decode(text) {
  return text.replace(/<br\s*\/?\s*>/gi, '\n').replace(/<[^>]*>/g, '')
    .replace(/&nbsp;/g, ' ').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"').replace(/&#39;|&apos;/g, "'").replace(/&amp;/g, '&')
    .replace(/&#(\d+);/g, (_, code) => String.fromCodePoint(Number(code))).trim();
}
export function extractExample(content) {
  const blocks = [...content.matchAll(/<pre[^>]*>([\s\S]*?)<\/pre>/gi),
    ...content.matchAll(/<div\s+class=["']example-block["'][^>]*>([\s\S]*?)<\/div>/gi)];
  for (const match of blocks) {
    const plain = decode(match[1]);
    const parts = plain.match(/(?:输入|Input)\s*[:：]?\s*([\s\S]*?)(?:输出|Output)\s*[:：]?\s*([\s\S]*?)(?=(?:解释|Explanation|说明|注意)\s*[:：]?|$)/i);
    if (parts && parts[1].trim() && parts[2].trim()) return {input:parts[1].trim(), output:parts[2].trim()};
  }
  return null;
}
if (process.argv[1]?.endsWith('/crawl.mjs')) {
const questions = [];
// 顺序请求并限速，避免大量并发访问。
for (const seed of catalog) {
  const q = await fetchQuestion(seed);
  questions.push(q);
  console.error(`[${questions.length}/${catalog.length}] ${q.id}. ${q.title}`);
  await pause(200);
}
console.log(JSON.stringify({version: 1, source: endpoint, categories, question_count: questions.length, questions}, null, 2));
}
