#!/usr/bin/env python3
import re
import sys

if len(sys.argv) < 2:
    print("Usage: convert_blog.py <markdown-file>")
    sys.exit(1)

md_file = sys.argv[1]
with open(md_file, 'r') as f:
    content = f.read()

# Extract title and date from frontmatter
title_match = re.search(r'^title:\s*"?(.+?)"?\s*$', content, re.MULTILINE)
date_match = re.search(r'^date:\s*"?(.+?)"?\s*$', content, re.MULTILINE)
title = title_match.group(1) if title_match else "Untitled"
date_str = date_match.group(1) if date_match else ""

# Parse date
import datetime
try:
    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    date_formatted = date_obj.strftime("%B %d, %Y")
except:
    date_formatted = date_str

# Remove frontmatter
lines = content.split('\n')
body_lines = []
in_frontmatter = False
for line in lines:
    if line.strip() == '---':
        if not in_frontmatter:
            in_frontmatter = True
            continue
        else:
            in_frontmatter = False
            continue
    if in_frontmatter:
        continue
    body_lines.append(line)

body = '\n'.join(body_lines)
lines = body.split('\n')
html_lines = []
in_code = False

for line in lines:
    if line.strip().startswith('```'):
        if not in_code:
            html_lines.append('<pre><code>')
            in_code = True
        else:
            html_lines.append('</code></pre>')
            in_code = False
        continue
    if in_code:
        html_lines.append(line.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;'))
        continue
    if line.startswith('# '):
        html_lines.append(f'<h1>{line[2:]}</h1>')
    elif line.startswith('## '):
        html_lines.append(f'<h2>{line[3:]}</h2>')
    elif line.startswith('### '):
        html_lines.append(f'<h3>{line[4:]}</h3>')
    elif line.strip() == '---':
        html_lines.append('<hr>')
    elif line.startswith('*') and line.endswith('*') and len(line) > 2 and line[1] != '*':
        html_lines.append(f'<p><em>{line[1:-1]}</em></p>')
    elif line.startswith('>'):
        html_lines.append(f'<blockquote>{line[1:].strip()}</blockquote>')
    elif line.startswith('- '):
        html_lines.append(f'<li>{line[2:]}</li>')
    elif line.strip() == '':
        html_lines.append('')
    else:
        processed = line
        processed = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', processed)
        processed = re.sub(r'\*(.+?)\*', r'<em>\1</em>', processed)
        processed = re.sub(r'`(.+?)`', r'<code>\1</code>', processed)
        if processed.strip():
            html_lines.append(f'<p>{processed}</p>')

html_body = '\n'.join(html_lines)

# Clean template
clean_template = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{TITLE}}</title>
<style>
body { font-family: Georgia, serif; max-width: 700px; margin: 4rem auto; padding: 0 1.5rem; line-height: 1.8; color: #222; }
h1 { font-size: 1.6rem; margin-bottom: 0.25rem; }
h2 { font-size: 1.2rem; margin-top: 2rem; }
h3 { font-size: 1rem; margin-top: 1.5rem; }
hr { border: none; border-top: 1px solid #ddd; margin: 2rem 0; }
blockquote { border-left: 3px solid #ccc; padding-left: 1rem; margin-left: 0; color: #555; }
code { background: #f4f4f4; padding: 0.1em 0.3em; border-radius: 3px; font-size: 0.9em; }
pre { background: #f4f4f4; padding: 1rem; overflow-x: auto; border-radius: 4px; }
li { margin-bottom: 0.3rem; }
</style>
</head>
<body>
<hr>
{{CONTENT}}
<p style="margin-top:3rem;color:#888;font-size:0.85rem;">{{DATE}} — Elio</p>
</body>
</html>'''

post_html = clean_template.replace('{{CONTENT}}', html_body)
post_html = post_html.replace('{{TITLE}}', title)
post_html = post_html.replace('{{DATE}}', date_formatted)

output_file = md_file.replace('.md', '.html')
with open(output_file, 'w') as f:
    f.write(post_html)

print(f'HTML generated: {output_file}')