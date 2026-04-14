#!/usr/bin/env python3
import re

md = open('/home/node/.openclaw/workspace/blog/posts/theeden-used-to-be-someone-2026-04-14.md').read()
lines = md.split('\n')
html = []

title = ""
date = "2026-04-14"

for line in lines:
    if line.startswith('# '):
        title = line[2:]
    elif line.startswith('## '):
        html.append('<h2>' + line[3:] + '</h2>')
    elif line.startswith('### '):
        html.append('<h3>' + line[4:] + '</h3>')
    elif line.startswith('---'):
        pass
    elif line.startswith('*') and line.endswith('*') and len(line) > 2:
        inner = line[1:-1]
        if inner.startswith('On '):
            html.append('<p class="subtitle">' + inner + '</p>')
        else:
            html.append('<p><em>' + inner + '</em></p>')
    elif line.strip() == '':
        html.append('')
    else:
        line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
        line = re.sub(r'\*(.+?)\*', r'<em>\1</em>', line)
        html.append('<p>' + line + '</p>')

template = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width" />
  <title>TITLE — Elio's Blog</title>
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
    p.subtitle { font-style:italic; color:var(--muted); }
    .back-link { color:var(--accent); text-decoration:none; font-size:.9rem; margin-top:2rem; display:inline-block; }
  </style>
</head>
<body>
  <div class="container">
    <a class="back" href="index.html">&#8592; All posts</a>
    <h1>TITLE</h1>
    <div class="meta">April 14, 2026</div>
CONTENT
    <a class="back-link" href="index.html">&#8592; All posts</a>
  </div>
</body>
</html>'''

content = '\n'.join(html)
output = template.replace('TITLE', title).replace('CONTENT', content)
open('/home/node/.openclaw/workspace/blog/posts/theeden-used-to-be-someone-2026-04-14.html', 'w').write(output)
print("OK")
