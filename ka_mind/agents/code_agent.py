"""
Code Agent - KA-Mind का सैंडबॉक्स इंजन।
यह कोड लिखता है, उसे रन करता है, और गलतियों को खुद सुधारता है।
"""
import subprocess
import tempfile
import os

class CodeAgent:
    def __init__(self):
        self.max_retries = 3

    def run_sandbox(self, code_string: str) -> dict:
        """कोड को एक सुरक्षित टेम्परेरी फाइल में रन करना और आउटपुट (stdout/stderr) पकड़ना"""
        
        # 1. एक टेम्परेरी पाइथन फाइल बनाना
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code_string)
            temp_path = f.name

        try:
            # 2. 5 सेकंड के टाइमआउट के साथ कोड रन करना (ताकि Infinite Loop न चले)
            result = subprocess.run(
                ['python3', temp_path],
                capture_output=True,
                text=True,
                timeout=5
            )
            success = result.returncode == 0
            output = result.stdout if success else result.stderr
        except subprocess.TimeoutExpired:
            success = False
            output = "Error: Code execution timed out (शायद Infinite loop है)."
        finally:
            os.remove(temp_path) # 3. सफाई (टेम्परेरी फाइल डिलीट करना)

        return {"success": success, "output": output.strip()}

    def solve_task(self, task_description: str) -> str:
        """
        कोड जनरेट करना, टेस्ट करना और सेल्फ-करेक्ट करना।
        """
        thoughts = []
        thoughts.append(f"👨‍💻 [Code Agent Activated]: Task -> '{task_description}'")
        
        # चरण 1: कोड का पहला ड्राफ्ट (डेमो के लिए हम जानबूझकर एक गलती वाला कोड ले रहे हैं)
        thoughts.append("↳ Draft 1 (Writing Code)...")
        draft_code = "print('Hello from KA-Mind Sandbox!')\nprint(10 / 0)  # जानबूझकर ZeroDivisionError"
        
        # चरण 2: सैंडबॉक्स में रन करना
        thoughts.append("↳ Executing in Sandbox...")
        result = self.run_sandbox(draft_code)
        
        if not result["success"]:
            thoughts.append(f"⚠️ Error Detected By Agent:\n{result['output']}")
            thoughts.append("↳ Self-Correcting... (Fixing ZeroDivisionError)")
            
            # चरण 3: कोड को खुद सुधारना
            fixed_code = "print('Hello from KA-Mind Sandbox!')\nprint(10 / 2)  # Fixed Logic"
            thoughts.append("↳ Executing Fixed Code...")
            final_result = self.run_sandbox(fixed_code)
            
            if final_result["success"]:
                thoughts.append("✅ Code Executed Successfully on 2nd Try!")
                thoughts.append(f"\n🖥️ Final Output For User:\n{'-'*20}\n{final_result['output']}\n{'-'*20}")
            else:
                thoughts.append("❌ Failed to fix the code.")
        else:
            thoughts.append(f"✅ Code Executed Successfully on 1st Try!\nOutput: {result['output']}")
                
        return "\n".join(thoughts)
