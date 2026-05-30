"""
KA-Mind: Main CLI Interface
यहाँ से यूजर KA-Mind के साथ सीधा इंटरैक्ट करेगा।
"""
from ka_mind.core.graph_memory import GraphMemory
from ka_mind.teacher.master_teacher import MasterTeacher
from ka_mind.agents.web_agent import WebAgent
from ka_mind.agents.code_agent import CodeAgent

def print_banner():
    print("\n" + "="*60)
    print(" 🧠 Welcome to KA-Mind (Knowledge Atom Intelligence System)")
    print(" 🛡️ Type 'exit' or 'quit' to close the terminal.")
    print("="*60 + "\n")

def main():
    print("[System]: Booting Neural Graph Memory...")
    memory = GraphMemory()
    
    print("[System]: Initializing Agents...")
    web_agent = WebAgent(memory)
    code_agent = CodeAgent()
    
    print("[System]: Waking up Master Teacher...")
    teacher = MasterTeacher(memory, web_agent, code_agent)
    
    print_banner()
    
    while True:
        try:
            user_input = input("👤 You: ").strip()
            if user_input.lower() in ['exit', 'quit']:
                print("🧠 KA-Mind: अलविदा! मेमोरी सेव की जा रही है... Shutting down.")
                break
            
            if not user_input:
                continue
                
            print("\n🤖 KA-Mind Processing...")
            print("-" * 50)
            
            # सवाल सीधा मास्टर टीचर को भेजा जाता है
            response = teacher.process_request(user_input)
            
            print(response)
            print("-" * 50 + "\n")
            
        except KeyboardInterrupt:
            print("\n🧠 KA-Mind: Emergency Shutdown Activated. Goodbye!")
            break

if __name__ == "__main__":
    main()
