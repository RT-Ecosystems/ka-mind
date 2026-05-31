"""
KA-Mind: Goal-Driven Thinking Demo
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ka_mind.framework.model import KaModel
from ka_mind.agents.web_agent import WebAgent
from ka_mind.core.neocortex import Neocortex
from ka_mind.agents.goal_agent import GoalAgent

def run_test():
    print("="*60)
    print(" 🎯 KA-MIND: GOAL-DRIVEN AGENT (AUTONOMOUS LOOP) DEMO")
    print("="*60)
    
    model = KaModel(name="Chanakya_Autonomous")
    web_agent = WebAgent(model.memory)
    neocortex = Neocortex(model.memory)
    
    # Goal Agent तैयार करना
    goal_agent = GoalAgent(model.memory, web_agent, neocortex)
    
    # मॉडल को एक बड़ा टास्क (Goal) देना
    user_goal = "क्वांटम कंप्यूटिंग के बारे में रिसर्च करो और निष्कर्ष निकालो"
    
    # एजेंट खुद प्लान बनाएगा और एग्जीक्यूट करेगा
    goal_agent.execute_plan(user_goal)
    
    print("\n📊 Memory Status: सिस्टम ने अपनी प्रोग्रेस खुद सेव कर ली है!")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_test()
