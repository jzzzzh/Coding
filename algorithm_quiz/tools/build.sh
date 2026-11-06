#!/bin/sh
# 从已抓取数据生成两个 CSV 和内置数据的离线 HTML，无包安装步骤。
set -eu
cd "$(dirname "$0")/.."
node tools/build.mjs --csv < question_bank.json > question_bank.csv.tmp
node tools/build.mjs --index-csv < leetcode_index.json > leetcode_public_index.csv.tmp
{
  cat question_bank.json
  printf '\n__TEMPLATE__\n'
  cat tools/page-template.html
  printf '\n__CORE__\n'
  cat tools/study-core.mjs
} | node tools/build.mjs --html > index.html.tmp
mv question_bank.csv.tmp question_bank.csv
mv leetcode_public_index.csv.tmp leetcode_public_index.csv
mv index.html.tmp index.html
