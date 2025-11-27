#!/usr/bin/env python3
"""
Chat with My Agent
==================

Simple chat interface to interact with your trained personalized agent.
"""

import sys
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dreamscape.core.memory import MemoryManager
from dreamscape.core.agent_trainer import AgentTrainer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def chat_with_agent(agent_id: str):
    """Chat with your trained agent."""
    print("🤖 Dream.OS Agent Chat Interface")
    print("=" * 50)
    print(f"Agent: {agent_id}")
    print("Type 'quit' to exit, 'help' for commands")
    print("-" * 50)
    
    # Initialize trainer
    memory_manager = MemoryManager("dreamos_memory.db")
    trainer = AgentTrainer(memory_manager)
    
    # Load agent info
    agent_config = trainer.load_trained_agent(agent_id)
    if agent_config:
        print(f"✅ Agent loaded: {agent_config.get('name', 'Unknown')}")
        if 'personality' in agent_config:
            personality = agent_config['personality']
            print(f"🎭 Personality: {personality.get('communication_style', 'Unknown')} style")
            print(f"💡 Expertise: {', '.join(personality.get('expertise_domains', []))}")
    else:
        print(f"❌ Could not load agent: {agent_id}")
        return
    
    print("\n💬 Start chatting with your agent:")
    
    while True:
        try:
            # Get user input
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye! Your agent will be here when you return.")
                break
            elif user_input.lower() == 'help':
                print("\n📋 Available Commands:")
                print("  help - Show this help")
                print("  quit/exit/bye - Exit chat")
                print("  personality - Show agent personality")
                print("  skills - Show agent skills")
                print("  Any other text - Chat with your agent")
                continue
            elif user_input.lower() == 'personality':
                if agent_config and 'personality' in agent_config:
                    p = agent_config['personality']
                    print(f"\n🎭 Agent Personality:")
                    print(f"  Communication Style: {p.get('communication_style', 'Unknown')}")
                    print(f"  Problem Solving: {p.get('problem_solving_approach', 'Unknown')}")
                    print(f"  Helpfulness: {p.get('helpfulness', 0):.2f}")
                    print(f"  Technical Depth: {p.get('technical_depth', 0):.2f}")
                    print(f"  Creativity: {p.get('creativity', 0):.2f}")
                    print(f"  Expertise: {', '.join(p.get('expertise_domains', []))}")
                continue
            elif user_input.lower() == 'skills':
                if agent_config and 'skill_tree' in agent_config:
                    skills = agent_config['skill_tree'].get('root_skills', {})
                    print(f"\n🌳 Agent Skills:")
                    for skill_id, skill_info in skills.items():
                        print(f"  {skill_info['name']}: {skill_info['level']} (count: {skill_info['count']})")
                continue
            elif not user_input:
                continue
            
            # Get agent response
            print("🤖 Agent: ", end="", flush=True)
            response = trainer.query_agent(agent_id, user_input)
            
            # Clean up response for display
            if "Based on my training and knowledge base" in response:
                # Extract the actual response part
                lines = response.split('\n')
                for line in lines:
                    if line.strip() and not line.startswith('**') and not line.startswith('Based on'):
                        print(line.strip())
                        break
            else:
                print(response[:500] + "..." if len(response) > 500 else response)
                
        except KeyboardInterrupt:
            print("\n👋 Chat interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def list_available_agents():
    """List all available trained agents."""
    memory_manager = MemoryManager("dreamos_memory.db")
    trainer = AgentTrainer(memory_manager)
    
    agents = trainer.list_trained_agents()
    
    if not agents:
        print("❌ No trained agents found.")
        return None
    
    print("🤖 Available Trained Agents:")
    print("-" * 50)
    
    for i, agent in enumerate(agents, 1):
        agent_id = agent.get('agent_id', 'Unknown')
        name = agent.get('name', 'Unknown')
        print(f"{i}. {name}")
        print(f"   ID: {agent_id}")
        
        # Show personality if available
        if 'personality' in agent:
            p = agent['personality']
            style = p.get('communication_style', 'Unknown')
            domains = ', '.join(p.get('expertise_domains', [])[:3])
            print(f"   Style: {style}, Expertise: {domains}")
        print()
    
    return agents

def main():
    """Main function."""
    print("🎯 Dream.OS Agent Chat Interface")
    print("=" * 50)
    
    # List available agents
    agents = list_available_agents()
    
    if not agents:
        print("❌ No agents available. Train an agent first!")
        return
    
    # Let user select agent
    while True:
        try:
            choice = input(f"Select agent (1-{len(agents)}) or 'list' to see agents again: ").strip()
            
            if choice.lower() == 'list':
                agents = list_available_agents()
                continue
            elif choice.lower() in ['quit', 'exit']:
                print("👋 Goodbye!")
                return
            
            try:
                agent_index = int(choice) - 1
                if 0 <= agent_index < len(agents):
                    selected_agent = agents[agent_index]
                    agent_id = selected_agent.get('agent_id')
                    print(f"\n✅ Selected: {selected_agent.get('name', 'Unknown')}")
                    chat_with_agent(agent_id)
                    break
                else:
                    print(f"❌ Please enter a number between 1 and {len(agents)}")
            except ValueError:
                print("❌ Please enter a valid number")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break

if __name__ == "__main__":
    main() 