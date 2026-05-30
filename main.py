"""
KA-Mind: Main CLI Interface with Vision Agent
"""
from ka_mind.core.graph_memory import GraphMemory
from ka_mind.teacher.master_teacher import MasterTeacher
from ka_mind.agents.web_agent import WebAgent
from ka_mind.agents.code_agent import CodeAgent
from ka_mind.agents.vision_agent import VisionAgent

def main():
    memory = GraphMemory()
    web_agent = WebAgent(memory)
    code_agent = CodeAgent()
    vision_agent = VisionAgent(memory)
    
    teacher = MasterTeacher(memory, web_agent, code_agent, vision_agent)
    
    print("="*60)
    print(" 🧠 Welcome to KA-Mind (Now with Multimodal Vision!)")
    print("="*60)
    
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            if user_input.lower() in ['exit', 'quit']:
                break
            if not user_input: continue
            
            print("\n🤖 KA-Mind Processing...")
            print("-" * 50)
            print(teacher.process_request(user_input))
            print("-" * 50)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
