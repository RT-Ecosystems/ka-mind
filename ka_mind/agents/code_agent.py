"""
KA-Mind Code Agent v3.0 — Multi-language code generation with self-debugging.
Supports: Python, मंत्र (Mantra), JavaScript, C++, HTML/CSS.
"""
import re, subprocess, tempfile, os


class CodeAgent:
    # ── Multi-language templates ─────────────────────
    TEMPLATES = {
        # Python
        "python_sort":      "sorted_list = sorted(my_list)",
        "python_reverse":   "reversed_list = my_list[::-1]",
        "python_sum":       "total = sum(my_list)",
        "python_read":      "with open(filename, 'r', encoding='utf-8') as f:\n    content = f.read()",
        "python_write":     "with open(filename, 'w', encoding='utf-8') as f:\n    f.write(content)",
        "python_web":       "import requests\nresp = requests.get(url)\nprint(resp.text)",
        "python_api":       "from fastapi import FastAPI\napp = FastAPI()\n\n@app.get('/')\ndef home():\n    return {'status': 'ok'}",
        "python_class":     "class MyClass:\n    def __init__(self, name):\n        self.name = name\n    def greet(self):\n        return f'Hello, {self.name}'",
        "python_ml":        "from sklearn.linear_model import LinearRegression\nmodel = LinearRegression()\nmodel.fit(X_train, y_train)\npredictions = model.predict(X_test)",
        "python_loop":      "for i in range(10):\n    print(f'Item {i}: {data[i]}')",

        # मंत्र (Mantra)
        "mantra_print":     'dikhao "नमस्ते दुनिया!"',
        "mantra_var":       'rakho x = 10\nrakho y = 20\ndikhao x + y',
        "mantra_if":        'rakho age = 18\nagar age >= 18 tab\n    dikhao "वयस्क"\nwarna\n    dikhao "बच्चा"',
        "mantra_loop":      'rakho i = 0\nbaarbaar i < 5\n    dikhao i\n    rakho i = i + 1',
        "mantra_func":      'kaam jodo(a, b)\n    wapas a + b\ndikhao jodo(5, 3)',
        "mantra_sikho":     'sikho("नई दिल्ली भारत की राजधानी है")\ndikhao puchho("राजधानी")',
        "mantra_hash":      'rakho h = hash("नमस्ते")\ndikhao h',

        # JavaScript
        "js_sort":          "const sorted = arr.sort((a, b) => a - b);",
        "js_fetch":         "fetch(url)\n  .then(res => res.json())\n  .then(data => console.log(data));",
        "js_func":          "function add(a, b) {\n    return a + b;\n}\nconsole.log(add(5, 3));",

        # C++
        "cpp_hello":        '#include <iostream>\nint main() {\n    std::cout << "Hello World!" << std::endl;\n    return 0;\n}',
        "cpp_vector":       "#include <vector>\nstd::vector<int> v = {1, 2, 3};\nfor (int x : v) std::cout << x << ' ';",

        # HTML/CSS
        "html_page":        "<!DOCTYPE html>\n<html>\n<head><title>My Page</title></head>\n<body>\n    <h1>Hello!</h1>\n</body>\n</html>",
        "css_style":        "body { font-family: Arial; margin: 20px; background: #f0f0f0; }\n.button { padding: 10px 20px; background: blue; color: white; border: none; border-radius: 5px; }",
    }

    # ── Language detection ──────────────────────────
    LANG_KEYWORDS = {
        "mantra":   ["dikhao", "rakho", "agar", "warna", "baarbaar", "kaam", "wapas", "sikho", "puchho", "hash", "beej", "gyan"],
        "python":   ["def ", "import ", "print(", "class ", "with ", "for ", "if __name__"],
        "javascript": ["function ", "const ", "let ", "=>", "console.log", "fetch("],
        "cpp":      ["#include", "int main", "std::", "cout", "vector"],
    }

    def solve_task(self, task: str, language: str = "auto") -> str:
        """Solve a coding task. Auto-detects language if not specified."""
        tl = task.lower()
        
        # Auto-detect language
        if language == "auto":
            language = self._detect_lang(task)
        
        # Check templates
        for key, code in self.TEMPLATES.items():
            if key.startswith(language + "_") and any(kw in tl for kw in key.split("_")[1:]):
                return f"```{language}
{code}
```"
            elif key.split("_")[0] == language and key.split("_")[1] in tl:
                return f"```{language}
{code}
```"
        
        # Generate custom code based on description
        return self._generate_code(task, language)

    def _detect_lang(self, task: str) -> str:
        """Detect programming language from task description."""
        tl = task.lower()
        scores = {}
        for lang, keywords in self.LANG_KEYWORDS.items():
            scores[lang] = sum(1 for kw in keywords if kw.lower() in tl)
        
        if "मंत्र" in task or "mantra" in tl or "हिंदी" in task:
            return "mantra"
        if "python" in tl or "पायथन" in task:
            return "python"
        if "javascript" in tl or "js" in tl:
            return "javascript"
        if "c++" in tl or "cpp" in tl:
            return "cpp"
        
        best = max(scores, key=scores.get)
        return best if scores[best] > 0 else "python"

    def _generate_code(self, task: str, language: str) -> str:
        """Generate code based on natural language description."""
        tl = task.lower()
        
        if language == "mantra":
            if "प्रिंट" in task or "दिखाओ" in task or "print" in tl:
                return f'```mantra
dikhao "नमस्ते दुनिया!"
```'
            return f'```mantra
# {task}
rakho x = 10
dikhao x
```'
        
        elif language == "python":
            if "sort" in tl: return "```python
sorted_list = sorted(my_list)
```"
            if "api" in tl or "server" in tl:
                return "```python
from fastapi import FastAPI
app = FastAPI()

@app.get('/')
def home():
    return {'status': 'ok'}
```"
            return f"```python
# {task}
def solution():
    # TODO: implement
    pass
```"
        
        elif language == "javascript":
            return f"```javascript
// {task}
function solution() {{
    // TODO: implement
}}
```"
        
        elif language == "cpp":
            return f"```cpp
// {task}
#include <iostream>
int main() {{
    // TODO: implement
    return 0;
}}
```"
        
        return f"```{language}
# {task}
# Code generation for this task is being developed.
```"

    def execute_safe(self, code: str, language: str = "python") -> str:
        """Safely execute code and return output. Supports Python only for now."""
        if language != "python":
            return f"[Execution for {language} not yet supported. Use Python for testing.]"
        
        # Security check
        blocked = ['import os', 'import sys', '__import__', 'exec(', 'eval(', 'open(', 'subprocess', 'shutil', 'os.system']
        if any(b in code for b in blocked):
            return "🚫 Blocked: unsafe code detected."
        
        # Limit code length
        if len(code) > 5000:
            return "🚫 Code too long. Max 5000 characters."
        
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                f.flush()
                result = subprocess.run(['python', f.name], capture_output=True, text=True, timeout=10)
            os.unlink(f.name)
            
            output = result.stdout.strip()
            if result.stderr.strip():
                output += "
[Errors]:
" + result.stderr.strip()
            return output if output else "[No output]"
        except subprocess.TimeoutExpired:
            return "⏱️ Execution timed out (10s limit)."
        except Exception as e:
            return f"❌ Execution error: {e}"

    def debug_and_fix(self, code: str, error_msg: str, language: str = "python") -> str:
        """Try to debug and fix broken code based on error message."""
        if language != "python":
            return "[Auto-debug only supports Python for now.]"
        
        fixes = []
        
        # Common fixes
        if "NameError" in error_msg:
            var_match = re.search(r"name '(\w+)' is not defined", error_msg)
            if var_match:
                var_name = var_match.group(1)
                fixes.append(f"# Fixed: defined '{var_name}'
{var_name} = None  # TODO: set proper value
{code}")
        
        if "IndentationError" in error_msg:
            # Try to fix indentation
            lines = code.split('
')
            fixed_lines = []
            for line in lines:
                fixed_lines.append(line.replace('	', '    '))
            fixes.append('
'.join(fixed_lines))
        
        if "SyntaxError" in error_msg:
            # Check for missing colons
            if 'if ' in code and ':
' not in code and '):
' not in code:
                fixed = code.replace('if ', 'if ').rstrip() + ':'
                fixes.append(fixed)
        
        if fixes:
            return f"[Auto-fix attempt]:
```python
{fixes[0]}
```"
        
        return f"[Could not auto-fix. Error]: {error_msg[:200]}"

    @property
    def supported_languages(self) -> list:
        return list(self.LANG_KEYWORDS.keys()) + ["html/css"]
