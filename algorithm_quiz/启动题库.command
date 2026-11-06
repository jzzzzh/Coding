#!/bin/zsh -l
# 双击启动：仅本机访问；个人记录自动写入已被 Git 忽略的 personal/。
cd "$(dirname "$0")" || exit 1
if ! command -v node >/dev/null 2>&1; then
  for candidate in "$HOME"/.nvm/versions/node/*/bin/node(NOn); do
    export PATH="$(dirname "$candidate"):$PATH"
    break
  done
fi
if ! command -v node >/dev/null 2>&1; then
  print '未找到 Node.js，请安装 Node.js 22 或更新版本后重试。'
  read '?按回车关闭'
  exit 1
fi
node tools/server.mjs
if [[ $? -ne 0 ]]; then
  print '启动失败。若端口被占用，请检查之前打开的题库窗口。'
  read '?按回车关闭'
fi
