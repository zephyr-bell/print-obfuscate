# HTML Print Obfuscator

对 HTML 文件进行混淆处理，防止内容被直接查看或打印传播。

## 背景

- VSCode 的 Markdown Preview Enhanced 插件导出的 HTML 存在以下问题：
  - 图片引用本地路径，分享后无法显示
  - KaTeX CSS 依赖 CDN，无网络时公式样式丢失
  - 内容可随意打印和复制传播
- 本工具旨在解决上述问题，输出单文件 HTML。

## 内嵌功能

### 图片内嵌
- 自动扫描 HTML 中所有图片引用（png/jpg/jpeg/gif），转换为 Base64 内联，无需携带外部图片文件。

### KaTeX CSS 内嵌
- 自动检测同目录下的 `katex.min.css` 文件，移除外链并内联到 `<head>` 中，确保公式样式在任何网络环境下正常显示。

## 混淆功能

- 中文位移编码，源文件不可直接阅读
- 打印时中文乱序 + 英文单词乱序 + 公式 ROT13 + 图片隐藏
- 打印后自动恢复

## 使用

```bash
python disPrint.py
# 输入 HTML 文件路径
```

输出 `xxx_OB.html`，单文件即可使用。

## 文件

| 文件 | 说明 |
|------|------|
| `disPrint.py` | 主程序 |
| `print_script.js` | 混淆脚本 |
| `katex.min.css` | KaTeX 样式（可选，存在则内联） |

## KaTeX CSS 来源

本目录下的 `katex.min.css` 文件来自 KaTeX 官方 CDN。

- **来源**：https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css
- **协议**：MIT License
- **项目官网**：https://katex.org

下载命令（如需重新下载）：
```powershell
Invoke-WebRequest -Uri "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css" -OutFile "katex.min.css"
```
