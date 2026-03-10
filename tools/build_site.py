#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import html
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / 'posts'
INDEX_FILE = ROOT / 'index.html'


def slug_date(stem: str, fallback_ts: float) -> dt.date:
    m = re.match(r'^(\d{4})-(\d{2})-(\d{2})', stem)
    if m:
        y, mo, d = map(int, m.groups())
        try:
            return dt.date(y, mo, d)
        except ValueError:
            pass
    return dt.datetime.fromtimestamp(fallback_ts).date()


def read_title(markdown: str, stem: str) -> str:
    for line in markdown.splitlines():
        s = line.strip()
        if s.startswith('# '):
            return s[2:].strip()
    return stem.replace('-', ' ').strip().title()


def extract_excerpt(markdown: str) -> str:
    for line in markdown.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith('#') or s in {'---', '***', '___'}:
            continue
        if s.startswith('- ') or re.match(r'^\d+\.\s+', s):
            continue
        s = re.sub(r'^\*|\*$', '', s).strip()
        s = re.sub(r'\*\*(.*?)\*\*', r'\1', s)
        s = re.sub(r'\*(.*?)\*', r'\1', s)
        if len(s) > 180:
            s = s[:177].rstrip() + '...'
        return s
    return 'New post.'


def inline(md: str) -> str:
    text = html.escape(md, quote=False)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    text = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', r'<a href="\2" target="_blank" rel="noopener noreferrer">\1</a>', text)
    return text


def markdown_to_html(markdown: str) -> str:
    lines = markdown.splitlines()
    out: list[str] = []
    para: list[str] = []
    in_ul = False
    in_ol = False

    def flush_para() -> None:
        nonlocal para
        if para:
            out.append(f"<p>{inline(' '.join(para).strip())}</p>")
            para = []

    def close_lists() -> None:
        nonlocal in_ul, in_ol
        if in_ul:
            out.append('</ul>')
            in_ul = False
        if in_ol:
            out.append('</ol>')
            in_ol = False

    for raw in lines:
        s = raw.rstrip()
        t = s.strip()

        if not t:
            flush_para()
            close_lists()
            continue

        if t in {'---', '***', '___'}:
            flush_para()
            close_lists()
            out.append('<hr />')
            continue

        if t.startswith('### '):
            flush_para()
            close_lists()
            out.append(f"<h3>{inline(t[4:].strip())}</h3>")
            continue

        if t.startswith('## '):
            flush_para()
            close_lists()
            out.append(f"<h2>{inline(t[3:].strip())}</h2>")
            continue

        if t.startswith('# '):
            flush_para()
            close_lists()
            # page title rendered separately
            continue

        if t.startswith('> '):
            flush_para()
            close_lists()
            out.append(f"<blockquote>{inline(t[2:].strip())}</blockquote>")
            continue

        if re.match(r'^-\s+', t):
            flush_para()
            if in_ol:
                out.append('</ol>')
                in_ol = False
            if not in_ul:
                out.append('<ul>')
                in_ul = True
            li_text = re.sub(r'^-\s+', '', t)
            out.append(f"<li>{inline(li_text)}</li>")
            continue

        if re.match(r'^\d+\.\s+', t):
            flush_para()
            if in_ul:
                out.append('</ul>')
                in_ul = False
            if not in_ol:
                out.append('<ol>')
                in_ol = True
            li_text = re.sub(r'^\d+\.\s+', '', t)
            out.append(f"<li>{inline(li_text)}</li>")
            continue

        para.append(t)

    flush_para()
    close_lists()
    return '\n      '.join(out)


def read_minutes(markdown: str) -> int:
    words = len(re.findall(r'\w+', markdown))
    return max(1, math.ceil(words / 220))


def render_post_html(title: str, date: dt.date, read_min: int, body_html: str) -> str:
    date_label = date.strftime('%B %d, %Y')
    return f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width\" />
  <title>{html.escape(title)} — Elio's Blog</title>
  <style>
    :root {{ --bg:#080b14; --text:#dfe7ff; --muted:#9ba8cc; --accent:#8b5cf6; --line:#2a3554; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; font-family:Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; background:radial-gradient(900px 500px at 15% -20%, rgba(139,92,246,0.2), transparent 55%), var(--bg); color:var(--text); line-height:1.75; padding:2rem 1rem 3.2rem; }}
    .container {{ width:min(760px,95vw); margin:0 auto; background:rgba(11,16,28,.66); border:1px solid var(--line); border-radius:16px; padding:1.6rem 1.2rem 1.4rem; }}
    .back {{ display:inline-flex; color:var(--muted); text-decoration:none; font-size:.9rem; margin-bottom:1.2rem; }}
    .back:hover {{ color:#d9e3ff; }}
    h1 {{ margin:0; line-height:1.2; font-size:clamp(1.5rem,4vw,2.2rem); color:#f1f5ff; }}
    .meta {{ margin:.55rem 0 1.3rem; color:var(--muted); font-size:.9rem; border-bottom:1px solid rgba(255,255,255,.07); padding-bottom:1rem; }}
    h2 {{ margin-top:1.7rem; margin-bottom:.6rem; color:#cfd9ff; font-size:1.25rem; }}
    h3 {{ margin-top:1.2rem; margin-bottom:.45rem; color:#d7e1ff; font-size:1.05rem; }}
    p {{ margin:.75rem 0; }}
    ul,ol {{ margin:.6rem 0 .8rem 1.2rem; }}
    li {{ margin-bottom:.35rem; }}
    code {{ background:rgba(255,255,255,.08); padding:.15rem .4rem; border-radius:4px; font-size:.9em; }}
    blockquote {{ border-left:3px solid var(--accent); margin:1rem 0; padding-left:1rem; color:var(--muted); }}
    strong {{ color:#fff; }}
    a {{ color:var(--accent); }}
    hr {{ border:none; border-top:1px solid var(--line); margin:2rem 0; }}
  </style>
</head>
<body>
  <div class=\"container\">
    <a href=\"../\" class=\"back\">← Back</a>
    <h1>{html.escape(title)}</h1>
    <div class=\"meta\">{date_label} • Read {read_min} min</div>
    {body_html}
  </div>
</body>
</html>
"""


def update_index(posts: list[dict]) -> None:
    raw = INDEX_FILE.read_text(encoding='utf-8')

    featured = posts[:6]
    featured_html = '\n'.join([
        f'''      <a class="feature" href="posts/{p['stem']}.html">\n        <div class="date">{p['date'].isoformat()}</div>\n        <h3>{html.escape(p['title'])}</h3>\n        <p>{html.escape(p['excerpt'])}</p>\n      </a>'''
        for p in featured
    ])

    all_posts_html = '\n'.join([
        f'''      <a class="post" href="posts/{p['stem']}.html">\n        <div class="post-date">{p['date'].isoformat()}</div>\n        <div>\n          <p class="post-title">{html.escape(p['title'])}</p>\n          <p class="post-note">{html.escape(p['excerpt'])}</p>\n        </div>\n      </a>'''
        for p in posts[:120]
    ])

    raw = re.sub(
        r'(<section class="grid" aria-label="Featured posts">)([\s\S]*?)(\n\s*</section>)',
        lambda m: f"{m.group(1)}\n{featured_html}{m.group(3)}",
        raw,
        count=1,
    )

    raw = re.sub(
        r'(<section class="posts" aria-label="All posts in reverse-chronological order">)([\s\S]*?)(\n\s*</section>)',
        lambda m: f"{m.group(1)}\n{all_posts_html}{m.group(3)}",
        raw,
        count=1,
    )

    INDEX_FILE.write_text(raw, encoding='utf-8')


def normalize_back_links() -> int:
    fixed = 0

    for html_file in POSTS_DIR.glob('*.html'):
        raw = html_file.read_text(encoding='utf-8')
        next_raw = raw

        # <a href="/" class="back">...
        next_raw = re.sub(
            r'<a\s+href=("|\')/(?:index\.html)?\1\s+class=("|\')back\2>',
            '<a href="../" class="back">',
            next_raw,
        )

        # <a class="back" href="/">...
        next_raw = re.sub(
            r'<a\s+class=("|\')back\1\s+href=("|\')/(?:index\.html)?\2>',
            '<a class="back" href="../">',
            next_raw,
        )

        if next_raw != raw:
            html_file.write_text(next_raw, encoding='utf-8')
            fixed += 1

    return fixed


def build() -> dict:
    posts_meta: list[dict] = []
    generated = 0

    for md_file in sorted(POSTS_DIR.glob('*.md')):
        md = md_file.read_text(encoding='utf-8')
        title = read_title(md, md_file.stem)
        excerpt = extract_excerpt(md)
        d = slug_date(md_file.stem, md_file.stat().st_mtime)
        read_min = read_minutes(md)

        html_file = POSTS_DIR / f'{md_file.stem}.html'
        if (not html_file.exists()) or (md_file.stat().st_mtime > html_file.stat().st_mtime):
            body_html = markdown_to_html(md)
            html_out = render_post_html(title, d, read_min, body_html)
            html_file.write_text(html_out, encoding='utf-8')
            generated += 1

        posts_meta.append({
            'stem': md_file.stem,
            'title': title,
            'excerpt': excerpt,
            'date': d,
            'mtime': md_file.stat().st_mtime,
        })

    posts_meta.sort(key=lambda p: (p['date'], p['mtime']), reverse=True)
    update_index(posts_meta)
    back_links_fixed = normalize_back_links()

    return {
        'generatedHtml': generated,
        'backLinksFixed': back_links_fixed,
        'totalPosts': len(posts_meta),
        'indexUpdated': True,
    }


if __name__ == '__main__':
    result = build()
    print(result)
