// 原生 JavaScript 构建工具：从标准输入读取，不依赖任何库。
// CSV: node tools/build.mjs --csv < question_bank.json > question_bank.csv
// HTML: 由 build.sh 把题库 JSON 与页面模板通过标准输入传入。
let input = '';
// 让运行时跨数据块解码 UTF-8，防止中文字符恰好被拆开时产生替换字符。
process.stdin.setEncoding('utf8');
for await (const chunk of process.stdin) input += chunk;
const marker = '\n__TEMPLATE__\n';
const mode = process.argv[2];
function csv(rows, fields) {
  const cell = value => {
    let text = String(value ?? '');
    const probe = text.trimStart();
    if (/^[=+@-]/.test(probe) && !/^-\d+(?:\.\d+)?(?:[eE][+-]?\d+)?$/.test(probe)) text = "'" + text;
    return '"' + text.replace(/"/g, '""') + '"';
  };
  return '\uFEFF' + [fields, ...rows.map(row => fields.map(field => row[field]))].map(row => row.map(cell).join(',')).join('\r\n') + '\r\n';
}
if (mode === '--html') {
  const split = input.indexOf(marker);
  if (split < 0) throw new Error('缺少 HTML 模板分隔符');
  const bank = JSON.parse(input.slice(0, split));
  if (bank.questions.length !== bank.question_count || bank.questions.length < 20) throw new Error('题库数量无效');
  const remaining = input.slice(split + marker.length);
  const coreMarker='\n__CORE__\n', coreSplit=remaining.indexOf(coreMarker);
  if(coreSplit<0) throw new Error('缺少复习规则源码');
  const template=remaining.slice(0,coreSplit);
  const core=remaining.slice(coreSplit+coreMarker.length).replace(/^export /gm,'');
  // 避免题面字符串包含 </script> 时提前闭合内置 JSON。
  const safeJSON = JSON.stringify(bank).replace(/</g, '\\u003c').replace(/>/g, '\\u003e').replace(/&/g, '\\u0026');
  if (!template.includes('__BANK_JSON__')) throw new Error('模板缺少题库占位符');
  process.stdout.write(template.replace('__BANK_JSON__',()=>safeJSON).replace('__STUDY_CORE__',()=>core));
} else if (mode === '--csv') {
  const bank = JSON.parse(input);
  const fields = ['id','title','difficulty','statement','example_input','example_output','example_note','option_a','option_b','option_c','option_d','answer','category','explanation','source_url','source_tags','slug','fetched_at','content_note'];
  process.stdout.write(csv(bank.questions, fields));
} else if (mode === '--index-csv') {
  const data = JSON.parse(input);
  const rows = data.questions.filter(q => !q.paid).map(q => ({...q, tags:q.tags.map(t => t.name).join('、')}));
  process.stdout.write(csv(rows, ['id','title','english_title','slug','difficulty','tags','source_url']));
} else throw new Error('用法：build.mjs --html | --csv | --index-csv');
