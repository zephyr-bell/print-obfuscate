# HTML Print Obfuscator

注入打印混淆脚本到 HTML 文件中，让打印出来的内容乱序，防止文档被随意打印传播。

## 函数

### `obfuscate_html(html)`

注入打印混淆脚本到 HTML 中。

**参数：**
- `html` (str) - 原始 HTML 内容

**返回：**
- `str` - 注入脚本后的 HTML 内容

**依赖：**
- 需要在同目录下存在 `print_script.js` 文件，其中定义了 `enableObfuscate()` 函数

## 完整代码

```python
from pathlib import Path

def obfuscate_html(html):
    """
    注入打印混淆脚本到 HTML 中

    参数:
        html (str): 原始 HTML 内容

    返回:
        str: 注入脚本后的 HTML 内容
    """
    # 读取混淆脚本
    js_path = Path(__file__).parent / 'print_script.js'
    js = open(js_path, encoding='utf-8').read()
    script = f'<script>{js};enableObfuscate();</script>'

    # 注入到 </body> 前
    if '</body>' in html:
        return html.replace('</body>', script + '\n</body>')
    else:
        return html + script
