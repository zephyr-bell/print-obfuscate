```markdown
# HTML Print Obfuscator

注入打印混淆脚本，防止 HTML 被随意打印传播。

## 功能

- 中文位移编码：源文件中文乱码，不可直接阅读
- 打印混淆：中文乱序 + 英文单词乱序 + 公式 ROT13 + 图片隐藏
- 图片自动 Base64 内嵌
- 自动恢复：打印后恢复原样

## 使用

```bash
python disPrint.py
# 输入 HTML 文件路径
```

输出 `xxx_PC.html` 和 `xxx_mobile.html`。