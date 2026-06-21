from pathlib import Path
import re
import base64

def get_script():
    js_path = Path(__file__).parent / 'print_script.js'
    js = open(js_path, encoding='utf-8').read()
    return f'<script>{js};enableObfuscate();</script>'

def embed_images(html, base_dir):
    for src in re.findall(r'src="([^"]+\.(png|jpg|jpeg|gif))"', html):
        img_path = Path(base_dir) / src[0]
        if img_path.exists():
            b64 = base64.b64encode(open(img_path, 'rb').read()).decode()
            html = html.replace(f'src="{src[0]}"', f'src="data:image/{src[1]};base64,{b64}"')
    return html

def inline_katex_css(html):
    css_path = Path(__file__).parent / 'katex.min.css'
    if css_path.exists():
        css_content = open(css_path, encoding='utf-8').read()
        html = re.sub(r'<link[^>]*katex\.min\.css[^>]*>', '', html)
        style_tag = f'<style>{css_content}</style>'
        html = html.replace('</head>', style_tag + '</head>')
    return html

def encode_chinese(html, shift=7):
    def encode_text(text):
        chars = list(text)
        for i, ch in enumerate(chars):
            code = ord(ch)
            if 0x4e00 <= code <= 0x9fff:
                new_code = ((code - 0x4e00 + shift) % 0x4e00) + 0x4e00
                chars[i] = chr(new_code)
        return ''.join(chars)

    script_style_pattern = r'(<(script|style)[^>]*>.*?</\2>)'
    protected_blocks = []
    
    def protect(match):
        protected_blocks.append(match.group(0))
        return f'__PROTECT_{len(protected_blocks)-1}__'
    
    html = re.sub(script_style_pattern, protect, html, flags=re.DOTALL | re.IGNORECASE)
    
    pattern = r'(?<=>)([^<]+)(?=<)'
    def replace_text(match):
        text = match.group(0)
        if text.strip():
            return encode_text(text)
        return text
    
    html = re.sub(pattern, replace_text, html)
    
    for i, block in enumerate(protected_blocks):
        html = html.replace(f'__PROTECT_{i}__', block)
    
    return html

def process(input_path):
    path = Path(input_path)
    if not path.exists():
        print(f'文件不存在: {input_path}')
        return
    
    html = open(path, encoding='utf-8').read()
    html = embed_images(html, path.parent)
    html = inline_katex_css(html)
    html = encode_chinese(html, shift=7)
    
    hidden_css = '<style>html{visibility:hidden}</style>'
    if '<head>' in html:
        html = html.replace('<head>', '<head>' + hidden_css)
    else:
        html = '<head>' + hidden_css + '</head>' + html
    
    script = get_script()
    html = html.replace('</body>', script + '\n</body>') if '</body>' in html else html + script
    
    out_path = path.parent / f'{path.stem}_OB{path.suffix}'
    open(out_path, 'w', encoding='utf-8').write(html)
    print(f'✅ {out_path}')

if __name__ == '__main__':
    html_path = input('请输入HTML文件路径: ').strip().strip('"').strip("'")
    process(html_path)