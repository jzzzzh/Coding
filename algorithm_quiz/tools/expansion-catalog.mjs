// 只选择已核实公开目录中的题目；宽泛的 String/Sorting 标签不直接推断为 KMP/快排。
export const TAG_CATEGORY = {
 'merge-sort':'归并/归并排序','quickselect':'快排/快速选择','monotonic-stack':'单调栈',
 'sliding-window':'滑动窗口','backtracking':'回溯','dynamic-programming':'动态规划',
 'binary-search':'二分查找','heap-priority-queue':'堆/Top-K','breadth-first-search':'BFS',
 'depth-first-search':'DFS','greedy':'贪心','prefix-sum':'前缀和/哈希','hash-table':'前缀和/哈希','two-pointers':'双指针'
};
// 这些模式匹配题可用 KMP 的前后缀/失配跳转方案；不把所有字符串题都标为 KMP。
const KMP_IDS=new Set(['796','1408','1668','1764','3006','3008','3029','3031','3034','3036','3407','3455','3529']);
const FEATURES={
 '前缀和/哈希':'记录累积量、键值关系或频次，将重复扫描变成快速查询。',
 '双指针':'维护两个位置协同扫描，利用顺序或位置关系减少重复枚举。',
 '滑动窗口':'围绕连续区间维护数量或边界条件，通过扩展与收缩增量更新。',
 '二分查找':'利用有序性或可行性的单调关系，在候选值范围中缩小搜索区间。',
 '动态规划':'保存重叠子问题的状态，按依赖顺序转移最优值或方案数。',
 '贪心':'根据问题性质选择当前最有利的候选，并用边界或交换关系保证整体结果。',
 '单调栈':'维持候选的单调顺序，在破坏顺序时寻找边界或结算贡献。',
 '堆/Top-K':'反复选择动态极值，或维护数量有限的最优候选。',
 'BFS':'按层扩展状态；在无权或等代价转换中，首次到达可确定最短步数。',
 'DFS':'沿分支深入访问状态或子树，回到父节点时汇总信息。',
 '回溯':'枚举选择路径并撤销选择，用合法性判断、去重和剪枝减少无效分支。',
 '快排/快速选择':'按基准划分候选区间，仅继续处理目标排名所在的一侧。',
 '归并/归并排序':'将子区间变为有序段，在合并过程中维护顺序或统计跨段贡献。',
 'KMP':'预处理相等真前后缀，在匹配失败时复用已有信息，或利用前后缀关系处理周期与模式匹配。'
};
export function buildExpansionCandidates(index,existing) {
 const ids=new Set(existing.map(q=>q.id)),slugs=new Set(existing.map(q=>q.slug));
 const rare=[],buckets=new Map();
 for(const row of index.questions) {
  if(row.paid||ids.has(row.id)||slugs.has(row.slug)||!/^\d+$/.test(row.id)||!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(row.slug))continue;
  const tags=new Set(row.tags.map(t=>t.slug));
  const supported=[...new Set(row.tags.map(t=>TAG_CATEGORY[t.slug]).filter(Boolean))];
  let category,sourceTag,curated=false;
  if(KMP_IDS.has(row.id)&&tags.has('string-matching')){category='KMP';sourceTag='string-matching';curated=true;}
  else if(tags.has('merge-sort')){category='归并/归并排序';sourceTag='merge-sort';curated=true;}
  else if(tags.has('quickselect')){category='快排/快速选择';sourceTag='quickselect';curated=true;}
  else if(supported.length===1){category=supported[0];sourceTag=row.tags.find(t=>TAG_CATEGORY[t.slug]===category).slug;}
  else continue;
  // 映射/二分/DFS 可能只是别的核心结构的辅助步骤；这些混合题先留待人工整理。
  const unsupportedCore={
   '前缀和/哈希':['trie','stack','recursion','tree','binary-tree','binary-search-tree','union-find','segment-tree','binary-indexed-tree','suffix-array','topological-sort','eulerian-path','eulerian-circuit'],
   '二分查找':['segment-tree','binary-indexed-tree','sweep-line','sparse-table','trie','suffix-array'],
   'DFS':['trie','segment-tree','binary-indexed-tree','heavy-light-decomposition','suffix-array']
  };
  if(!curated&&(unsupportedCore[category]||[]).some(tag=>tags.has(tag)))continue;
  if(!curated&&category==='DFS'&&tags.has('stack')&&!tags.has('tree')&&!tags.has('graph')&&!tags.has('binary-tree'))continue;
  const sourceName=row.tags.find(t=>t.slug===sourceTag)?.name||sourceTag;
  const seed={id:row.id,slug:row.slug,category,sourceTag,
   statement:`原题：${row.title}。请阅读官方完整题面中的任务、全部示例与约束；本条为索引提示，不代替完整题面。`,
   explanation:`本题官方算法标签包含「${sourceName}」。在本轮给定选项中按${category}方案识别：${FEATURES[category]}原题可能还支持其他解法。`,
   classification_source:curated?'official-tag-with-reviewed-training-direction':'single-supported-official-category'};
  if(curated)rare.push(seed);
  else {if(!buckets.has(category))buckets.set(category,[]);buckets.get(category).push(seed);}
 }
 const byNumber=(a,b)=>Number(a.id)-Number(b.id);
 rare.sort(byNumber);for(const values of buckets.values())values.sort(byNumber);
 // 先补少量专门算法，再按分类轮流取题，避免新增题几乎全是某一大类。
 const result=[...rare];
 while([...buckets.values()].some(values=>values.length))for(const values of buckets.values())if(values.length)result.push(values.shift());
 return result;
}
export function planExpansion(index,existing) {
 const reviewed=new Map(buildExpansionCandidates(index,[]).map(q=>[q.id,q]));
 const automatic=new Set(['single-supported-official-category','official-tag-with-reviewed-training-direction']);
 return {
  // 已有记录必须保留；目录和筛选规则的变化只能产生待复核提醒，不能删掉错题对应的题目。
  questions:existing.map(q=>({...q})),
  candidates:buildExpansionCandidates(index,existing),
  reviewNotes:existing.filter(q=>automatic.has(q.classification_source)&&reviewed.get(q.id)?.category!==q.category).map(q=>({id:q.id,reason:'当前目录或自动筛选规则已变化，保留原题，建议人工复核分类。'}))
 };
}
