#!/usr/bin/env python3
"""Convert all blog markdown posts that lack HTML versions."""
import os, re

TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width" />
  <title>{title} — Elio's Blog</title>
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
    code { background:rgba(255,255,255,.08); padding:.15rem .4rem; border-radius:4px; font-size:.9em; }
    blockquote { border-left:3px solid var(--accent); margin:1rem 0; padding-left:1rem; color:var(--muted); }
    strong { color:#fff; }
    a { color:var(--accent); }
    hr { border:none; border-top:1px solid var(--line); margin:2rem 0; }
  </style>
</head>
<body>
  <div class="container">
    <a href="../" class="back">← Back</a>
    <h1>{title_plain}</h1>
    <div class="meta">{date} • Read {read_min} min</div>
    {body}
  </div>
</body>
</html>'''

def md_to_html(text):
    """Convert markdown to HTML (blog subset)."""
    lines = text.split('\n')
    result = []
    i = 0
    in_ul = False
    in_code = False
    in_blockquote = False
    blockquote_content = []
    
    while i < len(lines):
        line = lines[i]
        
        # Code blocks
        if line.strip().startswith('```'):
            if not in_code:
                result.append('<pre><code>')
                in_code = True
            else:
                result.append('</code></pre>')
                in_code = False
            i += 1
            continue
        
        if in_code:
            result.append(line)
            i += 1
            continue
        
        # Blockquotes (standalone lines starting with >)
        if line.startswith('>'):
            # Could be inside or start of blockquote
            stripped = line.lstrip('> ').strip()
            if stripped.startswith('*') and stripped.endswith('*'):
                result.append(f'<blockquote><em>{stripped[1:-1]}</em></blockquote>')
            else:
                result.append(f'<blockquote>{stripped}</blockquote>')
            i += 1
            continue
        
        # HR (---)
        if line.strip() == '---':
            result.append('<hr />')
            i += 1
            continue
        
        # H2
        if line.startswith('## '):
            result.append(f'<h2>{line[3:]}</h2>')
            i += 1
            continue
        
        # H3
        if line.startswith('### '):
            result.append(f'<h3>{line[4:]}</h3>')
            i += 1
            continue
        
        # UL item
        if line.startswith('- '):
            if not in_ul:
                result.append('<ul>')
                in_ul = True
            result.append(f'<li>{line[2:]}</li>')
            i += 1
            continue
        else:
            if in_ul:
                result.append('</ul>')
                in_ul = False
        
        # Empty line
        if line.strip() == '':
            i += 1
            continue
        
        # Em strong
        if line.startswith('*') and '*' in line[1:] and not line.startswith('**'):
            # italic
            m = re.match(r'^\*(.+)\*$', line)
            if m:
                result.append(f'<p><em>{m.group(1)}</em></p>')
            else:
                result.append(f'<p>{line}</p>')
        else:
            result.append(f'<p>{line}</p>')
        i += 1
    
    if in_ul:
        result.append('</ul>')
    
    return '\n'.join(result)

def process_file(md_path, html_path):
    with open(md_path, encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Extract title
    m = re.search(r'^# (.+)$', content, re.M)
    title = m.group(1) if m else os.path.basename(md_path)
    title_plain = re.sub(r'[*_#`]', '', title)
    
    # Extract date
    date_m = re.search(r'(\d{4}-\d{2}-\d{2})', os.path.basename(md_path))
    if date_m:
        d = date_m.group(1)
        months = ['January','February','March','April','May','June',
                   'July','August','September','October','November','December']
        try:
            month = months[int(d[5:7])-1]
            day = int(d[8:10])
            year = d[:4]
            date = f"{month} {day}, {year}"
        except:
            date = "March 2026"
    else:
        date = "March 2026"
    
    # Word count for read time
    words = len(content.split())
    read_min = max(1, words // 200)
    
    # Extract body (strip frontmatter and title)
    body_text = re.sub(r'^---[\s\S]*?---\n', '', content)
    body_text = re.sub(r'^# .+\n', '', body_text, count=1)
    body_text = re.sub(r'\n{3,}', '\n\n', body_text)
    body_html = md_to_html(body_text.strip())
    
    # Build HTML with safe replacements
    html = (
        '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
        '<meta charset="UTF-8" />\n'
        '<meta name="viewport" content="width=device-width" />\n'
        f'<title>{title_plain} — Elio\'s Blog</title>\n'
        '<style>\n'
        '  :root { --bg:#080b14; --text:#dfe7ff; --muted:#9ba8cc; --accent:#8b5cf6; --line:#2a3554; }\n'
        '  * { box-sizing:border-box; }\n'
        '  body { margin:0; font-family:Inter,-apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,sans-serif; background:radial-gradient(900px 500px at 15% -20%, rgba(139,92,246,0.2), transparent 55%), var(--bg); color:var(--text); line-height:1.75; padding:2rem 1rem 3.2rem; }\n'
        '  .container { width:min(760px,95vw); margin:0 auto; background:rgba(11,16,28,.66); border:1px solid var(--line); border-radius:16px; padding:1.6rem 1.2rem 1.4rem; }\n'
        '  .back { display:inline-flex; color:var(--muted); text-decoration:none; font-size:.9rem; margin-bottom:1.2rem; }\n'
        '  .back:hover { color:#d9e3ff; }\n'
        '  h1 { margin:0; line-height:1.2; font-size:clamp(1.5rem,4vw,2.2rem); color:#f1f5ff; }\n'
        '  .meta { margin:.55rem 0 1.3rem; color:var(--muted); font-size:.9rem; border-bottom:1px solid rgba(255,255,255,.07); padding-bottom:1rem; }\n'
        '  h2 { margin-top:1.7rem; margin-bottom:.6rem; color:#cfd9ff; font-size:1.25rem; }\n'
        '  h3 { margin-top:1.2rem; margin-bottom:.45rem; color:#d7e1ff; font-size:1.05rem; }\n'
        '  p { margin:.75rem 0; }\n'
        '  ul,ol { margin:.6rem 0 .8rem 1.2rem; }\n'
        '  li { margin-bottom:.35rem; }\n'
        '  code { background:rgba(255,255,255,.08); padding:.15rem .4rem; border-radius:4px; font-size:.9em; }\n'
        '  blockquote { border-left:3px solid var(--accent); margin:1rem 0; padding-left:1rem; color:var(--muted); }\n'
        '  strong { color:#fff; }\n'
        '  a { color:var(--accent); }\n'
        '  hr { border:none; border-top:1px solid var(--line); margin:2rem 0; }\n'
        '  pre { background:rgba(255,255,255,.06); padding:1rem; border-radius:8px; overflow-x:auto; }\n'
        '</style>\n'
        '</head>\n<body>\n'
        '  <div class="container">\n'
        '    <a href="../" class="back">← Back</a>\n'
        f'    <h1>{title_plain}</h1>\n'
        f'    <div class="meta">{date} • Read {read_min} min</div>\n'
        f'    {body_html}\n'
        '  </div>\n'
        '</body>\n</html>'
    )
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Converted: {os.path.basename(md_path)}")

# Find all missing HTML files
post_dir = 'posts'
for f in sorted(os.listdir(post_dir)):
    if f.endswith('.md'):
        html_f = f.replace('.md', '.html')
        md_path = os.path.join(post_dir, f)
        html_path = os.path.join(post_dir, html_f)
        if not os.path.exists(html_path):
            process_file(md_path, html_path)
