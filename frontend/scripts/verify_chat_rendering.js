import hljs from 'highlight.js'
import katex from 'katex'

console.log('--- Testing AI Chat Rendering Components ---')

// 1. Math preprocessing test
function preprocessMathAndFormatting(raw) {
  if (!raw) return ''
  const segments = raw.split(/(```[\s\S]*?```|`[^`\n]+`)/g)
  for (let i = 0; i < segments.length; i += 2) {
    let text = segments[i]
    text = text.replace(/\\\[([\s\S]*?)\\\]/g, (_match, math) => {
      return `\n$$\n${math.trim()}\n$$\n`
    })
    text = text.replace(/\\\(([\s\S]*?)\\\)/g, (_match, math) => {
      return `$${math.trim()}$`
    })
    segments[i] = text
  }
  return segments.join('')
}

function isMermaidCode(lang, codeText) {
  if (lang.toLowerCase() === 'mermaid') return true
  const trimmed = codeText.trim()
  return /^(graph|flowchart|sequenceDiagram|classDiagram|stateDiagram(-v2)?|erDiagram|gantt|pie|gitGraph|journey|mindmap|timeline)\b/m.test(
    trimmed
  )
}

// Test Case 1: Math Equation Preprocessing & KaTeX Rendering
const inlineMath = 'The mean is \\(\\mu = \\frac{1}{n}\\sum_{i=1}^{n}x_i\\).'
const displayMath = '\\[\\sigma^2 = \\frac{1}{N}\\sum_{i=1}^{N}(x_i-\\mu)^2\\]'
const complexMath = '\\[\\int_{-\\infty}^{\\infty} e^{-x^2} dx = \\sqrt{\\pi}\\]'

const processedInline = preprocessMathAndFormatting(inlineMath)
const processedDisplay = preprocessMathAndFormatting(displayMath)
const processedComplex = preprocessMathAndFormatting(complexMath)

console.log('Test 1: Math Preprocessing')
console.log('  Inline before:', inlineMath)
console.log('  Inline after: ', processedInline)
console.log('  Display before:', displayMath)
console.log('  Display after: ', processedDisplay.trim())

// Verify KaTeX renders without errors
const katexInline = katex.renderToString('\\mu = \\frac{1}{n}\\sum_{i=1}^{n}x_i', { displayMode: false })
const katexDisplay = katex.renderToString('\\sigma^2 = \\frac{1}{N}\\sum_{i=1}^{N}(x_i-\\mu)^2', { displayMode: true })
const katexComplex = katex.renderToString('\\int_{-\\infty}^{\\infty} e^{-x^2} dx = \\sqrt{\\pi}', { displayMode: true })

if (!katexInline.includes('katex') || !katexDisplay.includes('katex-display')) {
  throw new Error('KaTeX rendering failed!')
}
console.log('  ✓ KaTeX inline and display equations rendered successfully!')

// Test Case 2: Code blocks with syntax highlighting
console.log('\nTest 2: Code Syntax Highlighting')
const pyCode = `def compute_loss(y_true, y_pred):\n    return np.mean((y_true - y_pred) ** 2)`
const jsCode = `async function fetchPapers(query) {\n  const res = await fetch(\`/api/search?q=\${query}\`);\n  return res.json();\n}`

const highlightedPy = hljs.highlight(pyCode, { language: 'python' }).value
const highlightedJs = hljs.highlight(jsCode, { language: 'javascript' }).value

if (!highlightedPy.includes('hljs-keyword') || !highlightedJs.includes('hljs-keyword')) {
  throw new Error('Syntax highlighting failed!')
}
console.log('  ✓ Python and JavaScript code blocks highlighted successfully!')

// Test Case 3: Mermaid detection
console.log('\nTest 3: Mermaid Diagram Detection')
const flowchart = `flowchart TD\n    A[Query] --> B[FAISS Index]\n    B --> C[Gemini LLM]\n    C --> D[Answer]`
const seqDiag = `sequenceDiagram\n    User->>Rover: Ask question\n    Rover->>DB: Retrieve chunks\n    Rover-->>User: Grounded answer`
const classDiag = `classDiagram\n    class Paper {\n      +String title\n      +String doi\n    }`

if (!isMermaidCode('mermaid', '') || !isMermaidCode('', flowchart) || !isMermaidCode('', seqDiag) || !isMermaidCode('', classDiag)) {
  throw new Error('Mermaid detection failed!')
}
console.log('  ✓ Flowchart, Sequence, and Class diagrams detected accurately!')

// Test Case 4: Preserving equations inside code blocks
console.log('\nTest 4: Preserving Math Inside Code Fences')
const codeWithMath = 'Here is code:\n```python\n# \\[x\\] is not math here\nprint("test")\n```\nAnd outside: \\[E = mc^2\\]'
const processedCodeWithMath = preprocessMathAndFormatting(codeWithMath)
if (!processedCodeWithMath.includes('# \\[x\\] is not math here') || !processedCodeWithMath.includes('$$\nE = mc^2\n$$')) {
  throw new Error('Code fence protection failed!')
}
console.log('  ✓ Math inside code blocks preserved verbatim while prose equations converted correctly!')

console.log('\n--- All Automated Verification Tests Passed Successfully! ---')
