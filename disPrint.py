from pathlib import Path
import re
import base64

def get_script(mode='pc'):
    js_path = Path(__file__).parent / 'print_script.js'
    js = open(js_path, encoding='utf-8').read()
    
    if mode == 'mobile':
        return f'<script>{js};enableObfuscateMobile();</script>'
    else:
        return f'<script>{js};enableObfuscate();</script>'

def embed_images(html, base_dir):
    for src in re.findall(r'src="([^"]+\.(png|jpg|jpeg|gif))"', html):
        img_path = Path(base_dir) / src[0]
        if img_path.exists():
            b64 = base64.b64encode(open(img_path, 'rb').read()).decode()
            html = html.replace(f'src="{src[0]}"', f'src="data:image/{src[1]};base64,{b64}"')
    return html

def encode_chinese(html, shift=7):
    """
    对 HTML 中的中文字符做位移编码
    保留标签、属性、script、style 不变
    """
    def encode_text(text):
        chars = list(text)
        for i, ch in enumerate(chars):
            code = ord(ch)
            if 0x4e00 <= code <= 0x9fff:
                new_code = ((code - 0x4e00 + shift) % 0x4e00) + 0x4e00
                chars[i] = chr(new_code)
        return ''.join(chars)

    # 保护 script 和 style 内容
    script_style_pattern = r'(<(script|style)[^>]*>.*?</\2>)'
    protected_blocks = []
    
    def protect(match):
        protected_blocks.append(match.group(0))
        return f'__PROTECT_{len(protected_blocks)-1}__'
    
    html = re.sub(script_style_pattern, protect, html, flags=re.DOTALL | re.IGNORECASE)
    
    # 对标签之间的文本进行编码
    pattern = r'(?<=>)([^<]+)(?=<)'
    def replace_text(match):
        text = match.group(0)
        if text.strip():
            return encode_text(text)
        return text
    
    html = re.sub(pattern, replace_text, html)
    
    # 恢复保护的块
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
    
    # 第一层：中文字符位移编码（固定偏移 7，与 JS 一致）
    html = encode_chinese(html, shift=7)
    
    # 隐藏保护 CSS（JS 不执行时页面不可见）
    hidden_css = '<style>html{visibility:hidden}</style>'
    if '<head>' in html:
        html = html.replace('<head>', '<head>' + hidden_css)
    else:
        html = '<head>' + hidden_css + '</head>' + html
    
    # 生成 PC 版
    script_pc = get_script('pc')
    html_pc = html.replace('</body>', script_pc + '\n</body>') if '</body>' in html else html + script_pc
    out_pc = path.parent / f'{path.stem}_PC{path.suffix}'
    open(out_pc, 'w', encoding='utf-8').write(html_pc)
    print(f'✅ {out_pc}')
    
    # 生成手机版
    script_mobile = get_script('mobile')
    html_mobile = html.replace('</body>', script_mobile + '\n</body>') if '</body>' in html else html + script_mobile
    out_mobile = path.parent / f'{path.stem}_mobile{path.suffix}'
    open(out_mobile, 'w', encoding='utf-8').write(html_mobile)
    print(f'✅ {out_mobile}')

if __name__ == '__main__':
    html_path = input('请输入HTML文件路径: ').strip().strip('"').strip("'")
    process(html_path)