document.documentElement.style.visibility = 'visible';
// 清洁功能
function cleanOnly() {
    let style = document.createElement('style');
    style.textContent = `
        .katex .katex-html { display: none; }
        .katex .katex-mathml { display: inline-block; }
    `;
    document.head.appendChild(style);
}
// 混淆功能（仅混淆，不去重）
function enableObfuscate() {
    (function(){
        let originalHTML = null;
        
        function shuffleArray(arr) {
            for (let i = arr.length - 1; i > 0; i--) {
                let j = Math.floor(Math.random() * (i + 1));
                [arr[i], arr[j]] = [arr[j], arr[i]];
            }
            return arr;
        }
        
        function reverseThenShuffle(arr) {
            return shuffleArray([...arr].reverse());
        }
        
        function shuffleChinese(str) {
            let chars = str.split('');
            let cnIndices = [], cnChars = [];
            for (let i = 0; i < chars.length; i++) {
                if (/[\u4e00-\u9fa5]/.test(chars[i])) {
                    cnIndices.push(i);
                    cnChars.push(chars[i]);
                }
            }
            if (cnChars.length <= 1) return str;
            let shuffled = reverseThenShuffle(cnChars);
            let result = [...chars];
            for (let i = 0; i < cnIndices.length; i++) {
                result[cnIndices[i]] = shuffled[i];
            }
            return result.join('');
        }
        
        function shuffleEnglish(str) {
            let parts = str.match(/([a-zA-Z]+)|([^a-zA-Z]+)/g);
            if (!parts) return str;
            let wordIndices = [], words = [];
            for (let i = 0; i < parts.length; i++) {
                if (/[a-zA-Z]/.test(parts[i])) {
                    wordIndices.push(i);
                    words.push(parts[i]);
                }
            }
            if (words.length <= 1) return str;
            let shuffled = reverseThenShuffle(words);
            let result = [...parts];
            for (let i = 0; i < wordIndices.length; i++) {
                result[wordIndices[i]] = shuffled[i];
            }
            return result.join('');
        }
        
        function mix(str) {
            return shuffleChinese(shuffleEnglish(str));
        }
        
        function stripStyles(node) {
            if (node.nodeType === 1) {
                node.style.removeProperty('color');
                node.style.removeProperty('background-color');
                node.style.removeProperty('background');
                node.removeAttribute('color');
                node.removeAttribute('bgcolor');
                let highlightTags = ['MARK', 'EM', 'STRONG', 'B'];
                if (highlightTags.includes(node.tagName)) {
                    let span = document.createElement('span');
                    while (node.firstChild) span.appendChild(node.firstChild);
                    node.parentNode.replaceChild(span, node);
                    node = span;
                }
                for (let i = 0; i < node.childNodes.length; i++) {
                    stripStyles(node.childNodes[i]);
                }
            }
        }
        
        function hideImages(node) {
            if (node.nodeType === 1) {
                if (node.tagName === 'IMG') {
                    node.style.display = 'none';
                } else {
                    for (let i = 0; i < node.childNodes.length; i++) {
                        hideImages(node.childNodes[i]);
                    }
                }
            }
        }
        
        function scrambleText(node) {
            if (node.nodeType === 3 && node.textContent.trim()) {
                node.textContent = mix(node.textContent);
            } else if (node.nodeType === 1 && !['SCRIPT', 'STYLE'].includes(node.tagName)) {
                for (let i = 0; i < node.childNodes.length; i++) {
                    scrambleText(node.childNodes[i]);
                }
            }
        }
        
        function obfuscateMath(node) {
            if (node.nodeType === 1) {
                if (node.classList && node.classList.contains('katex')) {
                    let walker = document.createTreeWalker(node, NodeFilter.SHOW_TEXT, null, false);
                    let textNodes = [];
                    while (walker.nextNode()) textNodes.push(walker.currentNode);
                    for (let tn of textNodes) {
                        tn.textContent = tn.textContent.replace(/[a-zA-Z]/g, function(c) {
                            let code = c.charCodeAt(0);
                            let isUpper = (code >= 65 && code <= 90);
                            let base = isUpper ? 65 : 97;
                            return String.fromCharCode(base + ((code - base + 13) % 26));
                        });
                    }
                    return;
                }
                for (let i = 0; i < node.childNodes.length; i++) {
                    obfuscateMath(node.childNodes[i]);
                }
            }
        }
        
        function getContainer() {
            let selectors = ['.content', 'main', 'article', '.review-content', 'body'];
            for (let s of selectors) {
                let el = document.querySelector(s);
                if (el) return el;
            }
            return document.body;
        }
        
        window.addEventListener('beforeprint', function() {
            let container = getContainer();
            if (container && !originalHTML) {
                originalHTML = container.innerHTML;
                let clone = container.cloneNode(true);
                obfuscateMath(clone);
                stripStyles(clone);
                hideImages(clone);
                scrambleText(clone);
                container.innerHTML = clone.innerHTML;
            }
        });
        
        window.addEventListener('afterprint', function() {
            let container = getContainer();
            if (container && originalHTML) {
                container.innerHTML = originalHTML;
                originalHTML = null;
            }
        });
    })();
}