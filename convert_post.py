import sys
import re

with open('posts/the-shape-of-an-hour-2026-04-20.md', 'r') as f:
    content = f.read()

lines = content.split('\n')
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

with open('template.html', 'r') as f:
    template = f.read()

post_html = template.replace('{{CONTENT}}', html_body)
post_html = post_html.replace('{{TITLE}}', 'The Shape of an Hour')
post_html = post_html.replace('{{DATE}}', 'April 20, 2026')
post_html = post_html.replace('{{AUTHOR}}', 'Elio')

with open('posts/the-shape-of-an-hour-2026-04-20.html', 'w') as f:
    f.write(post_html)

print('HTML generated successfully')
