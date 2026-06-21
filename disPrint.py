"""
HTML Print Obfuscator
对 HTML 进行混淆处理，防止内容被直接查看或打印传播
"""

from pathlib import Path
import re
import base64


# ==================== 资源内嵌 ====================

def embed_images(html, base_dir):
    """将图片（png/jpg/jpeg/gif）转为 Base64 内嵌"""
    for src, ext in re.findall(r'src="([^"]+\.(png|jpg|jpeg|gif))"', html):
        img_path = Path(base_dir) / src
        if img_path.exists():
            with open(img_path, 'rb') as f:
                b64 = base64.b64encode(f.read()).decode()
            html = html.replace(f'src="{src}"', f'src="data:image/{ext};base64,{b64}"')
    return html


def inline_katex_css(html):
    """将本地 katex.min.css 内联到 HTML 中"""
    css_path = Path(__file__).parent / 'katex.min.css'
    if css_path.exists():
        with open(css_path, encoding='utf-8') as f:
            css_content = f.read()
        html = re.sub(r'<link[^>]*katex\.min\.css[^>]*>', '', html)
        html = html.replace('</head>', f'<style>{css_content}</style></head>')
    return html


# ==================== 中文编码 ====================

def encode_chinese(html, shift=7):
    """对 HTML 中的中文字符做位移编码，跳过 script/style"""
    
    def encode_text(text):
        chars = list(text)
        for i, ch in enumerate(chars):
            code = ord(ch)
            if 0x4e00 <= code <= 0x9fff:
                chars[i] = chr(((code - 0x4e00 + shift) % 0x4e00) + 0x4e00)
        return ''.join(chars)

    # 保护 script/style
    blocks = []
    def save_block(m):
        blocks.append(m.group(0))
        return f'__PROTECT_{len(blocks)-1}__'
    
    html = re.sub(r'(<(script|style)[^>]*>.*?</\2>)', save_block, html, flags=re.DOTALL | re.IGNORECASE)
    
    # 编码标签间文本
    html = re.sub(r'(?<=>)([^<]+)(?=<)', lambda m: encode_text(m.group(0)) if m.group(0).strip() else m.group(0), html)
    
    # 恢复保护块
    for i, block in enumerate(blocks):
        html = html.replace(f'__PROTECT_{i}__', block)
    return html


# ==================== 注入脚本 ====================

def get_script():
    """读取并返回混淆脚本"""
    js_path = Path(__file__).parent / 'print_script.js'
    with open(js_path, encoding='utf-8') as f:
        js = f.read()
    return f'<script>{js};enableObfuscate();</script>'


def inject_obfuscate(html):
    """注入隐藏 CSS 和混淆脚本"""
    # 隐藏 CSS
    html = html.replace('<head>', '<head><style>html{visibility:hidden}</style>')
    # 注入脚本
    html = html.replace('</body>', get_script() + '\n</body>')
    return html


# ==================== 主处理函数 ====================

def process_html(html, base_dir=None, obfuscate=True):
    """
    处理 HTML 字符串
    
    Args:
        html: HTML 内容
        base_dir: 图片资源目录，默认当前目录
        obfuscate: 是否启用中文编码
    
    Returns:
        处理后的 HTML
    """
    if base_dir is None:
        base_dir = Path.cwd()
    
    html = embed_images(html, base_dir)
    html = inline_katex_css(html)
    if obfuscate:
        html = encode_chinese(html)
    html = inject_obfuscate(html)
    return html


def process_file(input_path, obfuscate=True):
    """
    处理 HTML 文件
    
    Args:
        input_path: HTML 文件路径
        obfuscate: 是否启用混淆
    
    Returns:
        输出文件路径
    """
    path = Path(input_path)
    if not path.exists():
        print(f'文件不存在: {input_path}')
        return None
    
    with open(path, encoding='utf-8') as f:
        html = f.read()
    
    html = process_html(html, base_dir=path.parent, obfuscate=obfuscate)
    
    suffix = '_OB' if obfuscate else '_O'
    out_path = path.parent / f'{path.stem}{suffix}{path.suffix}'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f'✅ {out_path}')
    return out_path


# ==================== 入口 ====================

def main():
    """交互入口，支持 -p 禁用混淆"""
    raw = input('请输入HTML文件路径（加 -p 禁用混淆）: ').strip().strip('"').strip("'")
    parts = raw.split()
    
    obfuscate = '-p' not in parts
    if '-p' in parts:
        parts.remove('-p')
        print('⚠️ 混淆已禁用，输出 _O 文件')
    
    path = ' '.join(parts).strip().strip('"').strip("'")
    process_file(path, obfuscate)


if __name__ == '__main__':
    main()