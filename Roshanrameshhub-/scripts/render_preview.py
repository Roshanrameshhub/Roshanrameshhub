import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README_PATH = os.path.join(BASE_DIR, "README.md")
HTML_PATH = os.path.join(BASE_DIR, "preview.html")

with open(README_PATH, "r", encoding="utf-8") as f:
    text = f.read()

# Replace relative paths in src and srcset with absolute file:// URIs for local browser rendering
def fix_src(m):
    rel = m.group(1)
    abs_path = os.path.join(BASE_DIR, rel).replace("\\", "/")
    return f'src="file:///{abs_path}"'

def fix_srcset(m):
    rel = m.group(1)
    abs_path = os.path.join(BASE_DIR, rel).replace("\\", "/")
    return f'srcset="file:///{abs_path}"'

text = re.sub(r'src=["\'](assets/[^"\']+)["\']', fix_src, text)
text = re.sub(r'srcset=["\'](assets/[^"\']+)["\']', fix_srcset, text)

# Convert headers
text = re.sub(r'^### (.*)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
text = re.sub(r'^#### (.*)$', r'<h4>\1</h4>', text, flags=re.MULTILINE)
text = re.sub(r'^---$', r'<hr>', text, flags=re.MULTILINE)
text = re.sub(r'^> (.*)$', r'<blockquote>\1</blockquote>', text, flags=re.MULTILINE)

# Convert code blocks
def code_sub(m):
    return f'<pre><code>{m.group(1)}</code></pre>'
text = re.sub(r'```(.*?)```', code_sub, text, flags=re.DOTALL)

# Convert bold and inline code
text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)

# Convert links
text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', text)

html_page = f"""<!DOCTYPE html>
<html lang="en" data-color-mode="dark" data-dark-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Roshan R // GitHub Profile Preview</title>
  <style>
    body {{
      background-color: #0d1117;
      color: #c9d1d9;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
      font-size: 14px;
      line-height: 1.6;
      padding: 30px 20px;
      margin: 0;
      display: flex;
      justify-content: center;
    }}
    .markdown-body {{
      max-width: 890px;
      width: 100%;
    }}
    a {{
      color: #58a6ff;
      text-decoration: none;
    }}
    a:hover {{
      text-decoration: underline;
    }}
    hr {{
      height: 1px;
      padding: 0;
      margin: 28px 0;
      background-color: #21262d;
      border: 0;
    }}
    h1, h2, h3, h4, h5, h6 {{
      margin-top: 24px;
      margin-bottom: 16px;
      font-weight: 600;
      line-height: 1.25;
      color: #f0f6fc;
    }}
    h3 {{
      font-size: 16px;
      letter-spacing: 0.5px;
      border-bottom: 1px solid #21262d;
      padding-bottom: 8px;
    }}
    h4 {{
      font-size: 14px;
      margin-top: 14px;
      margin-bottom: 8px;
    }}
    table {{
      border-spacing: 0;
      border-collapse: collapse;
      width: 100%;
      margin-top: 10px;
      margin-bottom: 16px;
    }}
    table th, table td {{
      padding: 12px 14px;
      border: 1px solid #30363d;
      vertical-align: top;
    }}
    table tr {{
      background-color: #0d1117;
    }}
    table tr:nth-child(2n) {{
      background-color: #161b22;
    }}
    blockquote {{
      padding: 0 1em;
      color: #8b949e;
      border-left: 0.25em solid #30363d;
      margin: 0 0 16px 0;
    }}
    pre {{
      padding: 14px;
      overflow: auto;
      font-size: 85%;
      line-height: 1.45;
      background-color: #161b22;
      border-radius: 6px;
      border: 1px solid #30363d;
      color: #e6edf3;
    }}
    code {{
      padding: 0.2em 0.4em;
      margin: 0;
      font-size: 85%;
      background-color: rgba(110,118,129,0.25);
      border-radius: 6px;
      font-family: ui-monospace,SFMono-Regular,SF Mono,Menlo,Consolas,Liberation Mono,monospace;
    }}
    pre code {{
      padding: 0;
      background-color: transparent;
    }}
    img {{
      max-width: 100%;
      box-sizing: border-box;
      display: block;
    }}
    ul, ol {{
      padding-left: 20px;
      margin-top: 6px;
      margin-bottom: 12px;
    }}
    li {{
      margin-bottom: 4px;
    }}
  </style>
</head>
<body>
  <div class="markdown-body">
    {text}
  </div>
</body>
</html>
"""

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html_page)

print(f"Generated {HTML_PATH}")
