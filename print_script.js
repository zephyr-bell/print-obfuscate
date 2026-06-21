// ============================================================
// 打印混淆脚本
// ============================================================

(function() {
    var SHIFT = 7;

    // ============ 解码中文 ============
    function decodeChinese(node) {
        if (node.nodeType === 3) {
            var text = node.textContent;
            if (text.trim()) {
                var chars = text.split('');
                for (var i = 0; i < chars.length; i++) {
                    var code = chars[i].charCodeAt(0);
                    if (code >= 0x4e00 && code <= 0x9fff) {
                        var newCode = code - SHIFT;
                        if (newCode < 0x4e00) newCode += 0x4e00;
                        chars[i] = String.fromCharCode(newCode);
                    }
                }
                node.textContent = chars.join('');
            }
        } else if (node.nodeType === 1 && node.tagName !== 'SCRIPT' && node.tagName !== 'STYLE') {
            for (var i = 0; i < node.childNodes.length; i++) {
                decodeChinese(node.childNodes[i]);
            }
        }
    }

    // ============ cleanOnly（移动端公式清理） ============
    function cleanOnly() {
        var style = document.createElement('style');
        style.textContent = `
            .katex .katex-html { display: none; }
            .katex .katex-mathml { display: inline-block; }
        `;
        document.head.appendChild(style);
    }

    // ============ 页面加载解码 ============
    function init() {
        decodeChinese(document.documentElement);  // 遍历整个文档
        document.documentElement.style.visibility = 'visible';
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    window.cleanOnly = cleanOnly;

})();