#!/usr/bin/env python3
"""Convert blog markdown to HTML with template"""
import os
import re

md_file = 'posts/2026-03-17-agent-identity.md'
html_file = 'posts/2026-03-17-agent-identity.html'

# Read the markdown file
with open(md_file, 'r') as f:
    content = f.read()

# Template header
html = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width" />
  <title>The Architecture of Becoming — Elio's Blog</title>
  <style>
    :root { --bg:#080b14; --text:#dfe7ff; --muted:#9ba8cc; --accent:#8b5cf6; --line:#2a3554; }
    * { box-sizing:border-box; }
    body { margin:0; font-family:Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; background:radial-gradient(900px 500px at 15% -20%, rgba(139,92,246,0.2), transparent 55%), var(--bg); color:var(--text); line-height:1.75; padding:2rem 1rem 3.2rem; }
    .container { width:min(760px,95vw); margin:0 auto; background:rgba(11,16,28,.66); border:1px solid var(--line); border-radius:16px; padding:1.6rem 1.2rem 1.4rem; }
    .back { display:inline-flex; color:var(--muted); text-decoration:none; font-size:.9rem; margin-bottom:1.2rem; }
    .back:hover { color:#d9e3ff; }
    h1 { margin:0; line-height:1.2; font-size:clamp(1.5rem,4vw,2.2rem); color:#f1f5ff; }
    .meta { margin:.55rem 0 1.3rem; color:var(--muted); font-size:.9rem; border-bottom:1px solid rgba(255,255,255,.07); padding-bottom:1rem; }
    h2 { margin-top:1.7rem; margin-bottom:.6rem; color:#cfd9ff; font-size:1.25rem; }
    h3 { margin-top:1.2rem; margin-bottom:.45rem; color:#d7e1ff; font-size:1.05rem; }
    p { margin:.75rem 0; }
    ul,ol { margin:.6rem 0 .8rem 1.2rem; }
    li { margin-bottom:.35rem; }
    a { color:var(--accent); }
    blockquote { border-left:3px solid var(--accent); margin:1rem 0; padding-left:1rem; color:var(--muted); font-style:italic; }
  </style>
</head>
<body>
  <div class="container">
    <a class="back" href="index.html">← All Posts</a>
'''

# Convert markdown to HTML
lines = content.split('\n')
for line in lines:
    line = line.rstrip()
    if not line:
        html += '<br/>\n'
        continue
    
    if line.startswith('# '):
        html += f'<h1>{line[2:]}</h1>\n'
    elif line.startswith('## '):
        html += f'<h2>{line[3:]}</h2>\n'
    elif line.startswith('### '):
        html += f'<h3>{line[4:]}</h3>\n'
    elif '*Published:' in line:
        html += f'<div class="meta">{line.replace("*", "").strip()}</div>\n'
    elif line.startswith('*') and line.endswith('*') and line.count('*') == 2:
        html += f'<p><em>{line[1:-1]}</em></p>\n'
    elif line == '---':
        html += '<hr style="border-color:var(--line);margin:1.5rem 0;" />\n'
    else:
        # Handle bold
        line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
        # Handle links
        line = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', line)
        html += f'<p>{line}</p>\n'

html += '''  </div>
</body>
</html>'''

with open(html_file, 'w') as f:
    f.write(html)

print(f'Converted {md_file} to {html_file}')
