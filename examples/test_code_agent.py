"""
KA-Mind: Code Agent Test
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ka_mind.agents.code_agent import CodeAgent

def run_test():
    print("="*50)
    print("💻 KA-MIND: SELF-EXECUTING CODE AGENT DEMO")
    print("="*50)
    
    agent = CodeAgent()
    
    print("\n👤 USER: मेरे लिए एक कैलकुलेशन प्रोग्राम लिखो और रन करके आउटपुट दो।")
    
    # यह फंक्शन कोड लिखेगा, रन करेगा, एरर (ZeroDivision) पकड़ेगा, फिक्स करेगा और फाइनल आउटपुट देगा।
    output = agent.solve_task("Math Calculation Program")
    
    print("\n" + output)
    print("\n" + "="*50)

if __name__ == "__main__":
    run_test()
