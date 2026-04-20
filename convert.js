#!/usr/bin/env node
const fs = require('fs');
const md = fs.readFileSync(process.argv[2], 'utf8');
let html = '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width">\n<title>' + process.argv[2].replace('.md','').split('/').pop() + '</title>\n<style>\nbody { max-width: 720px; margin: 0 auto; padding: 2rem; font-family: Georgia, serif; line-height: 1.7; color: #e8e8e8; background: #0d0d0d; }\nh1, h2, h3 { color: #f0f0f0; margin-top: 2rem; }\np { margin: 1rem 0; }\na { color: #8ab4f8; }\nblockquote { border-left: 3px solid #444; margin: 1rem 0; padding-left: 1rem; color: #aaa; }\ncode { background: #1a1a1a; padding: 0.1rem 0.3rem; border-radius: 3px; font-size: 0.9em; }\npre { background: #1a1a1a; padding: 1rem; border-radius: 6px; overflow-x: auto; }\n</style>\n</head>\n<body>\n';
const lines = md.split('\n');
for (const line of lines) {
  if (line.startsWith('# ')) html += '<h1>' + line.slice(2) + '</h1>\n';
  else if (line.startsWith('## ')) html += '<h2>' + line.slice(3) + '</h2>\n';
  else if (line.startsWith('### ')) html += '<h3>' + line.slice(4) + '</h3>\n';
  else if (line.startsWith('> ')) html += '<blockquote>' + line.slice(2) + '</blockquote>\n';
  else if (line.trim()) html += '<p>' + line.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\*(.*?)\*/g, '<em>$1</em>') + '</p>\n';
  else html += '<br>\n';
}
html += '</body>\n</html>\n';
fs.writeFileSync(process.argv[3] || process.argv[2].replace('.md','.html'), html.trim());
console.log('done');
