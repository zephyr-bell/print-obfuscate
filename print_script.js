// ============================================================
// 打印混淆脚本（精简版）
// ============================================================

// ============ 配置 ============
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

// ============ 清洁功能 ============
function cleanOnly() {
    var style = document.createElement('style');
    style.textContent = '.katex .katex-html { display: none; } .katex .katex-mathml { display: inline-block; }';
    document.head.appendChild(style);
}

// ============ 混淆功能 ============
function enableObfuscate() {
    (function() {
        var originalHTML = null;

        function shuffleArray(arr) {
            for (var i = arr.length - 1; i > 0; i--) {
                var j = Math.floor(Math.random() * (i + 1));
                var temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
            }
            return arr;
        }

        function shuffleChinese(str) {
            var chars = str.split('');
            var cnIndices = [];
            var cnChars = [];
            for (var i = 0; i < chars.length; i++) {
                var code = chars[i].charCodeAt(0);
                if (code >= 0x4e00 && code <= 0x9fff) {
                    cnIndices.push(i);
                    cnChars.push(chars[i]);
                }
            }
            if (cnChars.length <= 1) return str;
            shuffleArray(cnChars);
            var result = chars.slice();
            for (var i = 0; i < cnIndices.length; i++) {
                result[cnIndices[i]] = cnChars[i];
            }
            return result.join('');
        }

        function shuffleEnglish(str) {
            var parts = str.match(/([a-zA-Z]+)|([^a-zA-Z]+)/g);
            if (!parts) return str;
            var wordIndices = [];
            var words = [];
            for (var i = 0; i < parts.length; i++) {
                if (/[a-zA-Z]/.test(parts[i])) {
                    wordIndices.push(i);
                    words.push(parts[i]);
                }
            }
            if (words.length <= 1) return str;
            shuffleArray(words);
            var result = parts.slice();
            for (var i = 0; i < wordIndices.length; i++) {
                result[wordIndices[i]] = words[i];
            }
            return result.join('');
        }

        function scrambleText(node) {
            if (node.nodeType === 3) {
                if (node.textContent.trim()) {
                    var text = node.textContent;
                    text = shuffleChinese(text);
                    text = shuffleEnglish(text);
                    node.textContent = text;
                }
            } else if (node.nodeType === 1 && node.tagName !== 'SCRIPT' && node.tagName !== 'STYLE') {
                for (var i = 0; i < node.childNodes.length; i++) {
                    scrambleText(node.childNodes[i]);
                }
            }
        }

        function obfuscateFormula(node) {
            if (node.nodeType === 1) {
                if (node.classList && node.classList.contains('katex')) {
                    var walker = document.createTreeWalker(node, NodeFilter.SHOW_TEXT, null, false);
                    var textNodes = [];
                    while (walker.nextNode()) textNodes.push(walker.currentNode);
                    for (var i = 0; i < textNodes.length; i++) {
                        var tn = textNodes[i];
                        tn.textContent = tn.textContent.replace(/[a-zA-Z]/g, function(c) {
                            var code = c.charCodeAt(0);
                            var isUpper = (code >= 65 && code <= 90);
                            var base = isUpper ? 65 : 97;
                            return String.fromCharCode(base + ((code - base + 13) % 26));
                        });
                    }
                    return;
                }
                for (var i = 0; i < node.childNodes.length; i++) {
                    obfuscateFormula(node.childNodes[i]);
                }
            }
        }

        function hideImages(node) {
            if (node.nodeType === 1) {
                if (node.tagName === 'IMG') {
                    node.style.display = 'none';
                } else {
                    for (var i = 0; i < node.childNodes.length; i++) {
                        hideImages(node.childNodes[i]);
                    }
                }
            }
        }

        function getContainer() {
            var selectors = ['.content', 'main', 'article', '.review-content', 'body'];
            for (var i = 0; i < selectors.length; i++) {
                var el = document.querySelector(selectors[i]);
                if (el) return el;
            }
            return document.body;
        }

        window.addEventListener('beforeprint', function() {
            var container = getContainer();
            if (container && !originalHTML) {
                originalHTML = container.innerHTML;
                var clone = container.cloneNode(true);
                obfuscateFormula(clone);
                hideImages(clone);
                scrambleText(clone);
                container.innerHTML = clone.innerHTML;
            }
        });

        window.addEventListener('afterprint', function() {
            var container = getContainer();
            if (container && originalHTML) {
                container.innerHTML = originalHTML;
                originalHTML = null;
            }
        });
    })();
}

// ============ 移动版 ============
function enableObfuscateMobile() {
    cleanOnly();
    enableObfuscate();
}

// ============ 页面加载解码 ============
function init() {
    decodeChinese(document.documentElement);
    document.documentElement.style.visibility = 'visible';
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}