import sys
from pathlib import Path
import re
import base64

def get_script(mode='pc'):
    js_path = Path(__file__).parent / 'print_script.js'
    js = open(js_path, encoding='utf-8').read()
    
    if mode == 'mobile':
        return f'<script>{js};enableObfuscate();cleanOnly();</script>'
    else:
        return f'<script>{js};enableObfuscate();</script>'

def embed_images(html, base_dir):
    for src in re.findall(r'src="([^"]+\.(png|jpg|jpeg|gif))"', html):
        img_path = Path(base_dir) / src[0]
        if img_path.exists():
            b64 = base64.b64encode(open(img_path, 'rb').read()).decode()
            html = html.replace(f'src="{src[0]}"', f'src="data:image/{src[1]};base64,{b64}"')
    return html

def process(input_path):
    path = Path(input_path)
    if not path.exists():
        print(f'文件不存在: {input_path}')
        return
    
    html = open(path, encoding='utf-8').read()
    html = embed_images(html, path.parent)
    
    # 添加隐藏保护 CSS（JS 不执行时页面不可见）
    hidden_css = '<style>html{visibility:hidden}</style>'
    if '<head>' in html:
        html = html.replace('<head>', '<head>' + hidden_css)
    else:
        html = '<head>' + hidden_css + '</head>' + html
    
    # 生成电脑版
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