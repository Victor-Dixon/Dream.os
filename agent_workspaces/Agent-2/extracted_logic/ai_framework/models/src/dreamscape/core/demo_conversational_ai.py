#!/usr/bin/env python3
"""
Conversational AI Workflow Demo
===============================

Demonstrates the interactive "speaking" capabilities with ChatGPT using rich conversation context.
"""

import sys
import json
import time
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dreamscape.core.conversational_ai_workflow import ConversationalAIWorkflow

def demo_conversational_ai():
    """Demo the conversational AI workflow capabilities."""
    print("🤖 Conversational AI Workflow Demo")
    print("=" * 50)
    
    # Initialize the workflow
    workflow = ConversationalAIWorkflow()
    
    try:
        # Start a session
        print("🚀 Starting conversation session...")
        session_result = workflow.start_conversation_session()
        
        if not session_result.get('success'):
            print(f"❌ Failed to start session: {session_result.get('error')}")
            return
        
        print(f"✅ Session started: {session_result['session_id']}")
        
        # Display work patterns
        work_patterns = session_result.get('work_patterns', {})
        print(f"\n📊 Work Patterns Analyzed:")
        print(f"   - Topics: {len(work_patterns.get('topics', {}))}")
        print(f"   - Technologies: {len(work_patterns.get('technologies', {}))}")
        print(f"   - Project themes: {len(work_patterns.get('project_themes', []))}")
        
        # Demo 1: General conversation with context
        print(f"\n💬 Demo 1: General Conversation")
        print("-" * 30)
        
        message = "I'm working on improving the database performance of my application. What should I focus on?"
        print(f"👤 You: {message}")
        
        response = workflow.speak_to_workflow(message, context_type="general")
        
        if response.get('success'):
            print(f"🤖 AI: {response['ai_response'][:200]}...")
            print(f"   Context used: {response['context_used'].get('total_results', 0)} conversations")
        else:
            print(f"❌ Error: {response.get('error')}")
        
        # Demo 2: Coding-specific context
        print(f"\n💻 Demo 2: Coding Context")
        print("-" * 30)
        
        message = "I'm getting database locking errors in my SQLite application. How can I fix this?"
        print(f"👤 You: {message}")
        
        response = workflow.speak_to_workflow(message, context_type="coding")
        
        if response.get('success'):
            print(f"🤖 AI: {response['ai_response'][:200]}...")
            print(f"   Context used: {response['context_used'].get('total_results', 0)} conversations")
        else:
            print(f"❌ Error: {response.get('error')}")
        
        # Demo 3: Ask about work patterns
        print(f"\n❓ Demo 3: Work Pattern Analysis")
        print("-" * 30)
        
        question = "What are my main work patterns and how can I improve my development workflow?"
        print(f"👤 Question: {question}")
        
        analysis = workflow.ask_about_work(question)
        
        if analysis.get('success'):
            print(f"🤖 Analysis: {analysis['analysis'][:300]}...")
            if analysis.get('patterns_found'):
                print(f"   Patterns found: {len(analysis['patterns_found'])}")
        else:
            print(f"❌ Error: {analysis.get('error')}")
        
        # Demo 4: Workflow suggestions
        print(f"\n💡 Demo 4: Workflow Suggestions")
        print("-" * 30)
        
        task = "Improve my overall development workflow and productivity"
        print(f"👤 Task: {task}")
        
        suggestions = workflow.get_workflow_suggestions(task)
        
        if suggestions.get('success'):
            print(f"🤖 Suggestions: {suggestions['ai_analysis'][:300]}...")
            if suggestions.get('suggestions'):
                print(f"   Actionable suggestions: {len(suggestions['suggestions'])}")
        else:
            print(f"❌ Error: {suggestions.get('error')}")
        
        # Demo 5: Interactive conversation
        print(f"\n🔄 Demo 5: Interactive Conversation")
        print("-" * 30)
        
        conversation_messages = [
            "I've been working on a lot of Python projects lately. What patterns do you notice?",
            "Based on that, what should I focus on learning next?",
            "How can I apply those learnings to my current database optimization project?"
        ]
        
        for i, message in enumerate(conversation_messages, 1):
            print(f"\n👤 Message {i}: {message}")
            
            response = workflow.speak_to_workflow(message, context_type="general")
            
            if response.get('success'):
                print(f"🤖 AI: {response['ai_response'][:200]}...")
                time.sleep(1)  # Brief pause for readability
            else:
                print(f"❌ Error: {response.get('error')}")
        
        # Get session summary
        print(f"\n📋 Session Summary")
        print("-" * 30)
        
        summary = workflow.get_session_summary()
        print(f"   Session ID: {summary['session_id']}")
        print(f"   Conversations: {summary['conversation_count']}")
        print(f"   Work patterns: {len(summary['work_patterns'].get('topics', {}))} topics")
        
        # End session
        print(f"\n🏁 Ending session...")
        end_result = workflow.end_session()
        
        if end_result.get('success'):
            print(f"✅ Session ended successfully")
            print(f"   Insights saved to memory")
        else:
            print(f"❌ Failed to end session: {end_result.get('error')}")
        
        print(f"\n🎉 Demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

def demo_context_injection():
    """Demo the context injection capabilities."""
    print(f"\n🔍 Context Injection Demo")
    print("=" * 50)
    
    workflow = ConversationalAIWorkflow()
    
    try:
        # Start session
        session_result = workflow.start_conversation_session()
        if not session_result.get('success'):
            print(f"❌ Failed to start session: {session_result.get('error')}")
            return
        
        # Test different context types
        context_types = [
            ("general", "I need help with project planning"),
            ("coding", "How can I optimize my Python code?"),
            ("writing", "I need to write technical documentation"),
            ("analysis", "How should I analyze this dataset?"),
            ("planning", "What's the best way to structure this project?"),
            ("debugging", "I'm getting errors in my application")
        ]
        
        for context_type, message in context_types:
            print(f"\n🔧 Testing {context_type} context:")
            print(f"   Message: {message}")
            
            response = workflow.speak_to_workflow(message, context_type=context_type)
            
            if response.get('success'):
                context_used = response['context_used']
                print(f"   ✅ Success - Context: {context_used.get('total_results', 0)} conversations")
                print(f"   AI Response: {response['ai_response'][:100]}...")
            else:
                print(f"   ❌ Error: {response.get('error')}")
        
        workflow.end_session()
        
    except Exception as e:
        print(f"❌ Context injection demo failed: {e}")

def demo_work_pattern_analysis():
    """Demo work pattern analysis capabilities."""
    print(f"\n📊 Work Pattern Analysis Demo")
    print("=" * 50)
    
    workflow = ConversationalAIWorkflow()
    
    try:
        # Start session
        session_result = workflow.start_conversation_session()
        if not session_result.get('success'):
            print(f"❌ Failed to start session: {session_result.get('error')}")
            return
        
        # Analyze different aspects of work
        analysis_questions = [
            "What technologies do I use most frequently?",
            "What are my main project themes?",
            "How can I improve my development workflow?",
            "What patterns do you notice in my work style?",
            "What should I focus on learning next?"
        ]
        
        for question in analysis_questions:
            print(f"\n❓ Question: {question}")
            
            analysis = workflow.ask_about_work(question)
            
            if analysis.get('success'):
                print(f"🤖 Analysis: {analysis['analysis'][:200]}...")
                if analysis.get('patterns_found'):
                    print(f"   Patterns: {len(analysis['patterns_found'])} found")
            else:
                print(f"❌ Error: {analysis.get('error')}")
        
        workflow.end_session()
        
    except Exception as e:
        print(f"❌ Work pattern analysis demo failed: {e}")

if __name__ == "__main__":
    print("🚀 Starting Conversational AI Workflow Demos")
    print("=" * 60)
    
    # Run demos
    demo_conversational_ai()
    demo_context_injection()
    demo_work_pattern_analysis()
    
    print(f"\n🎉 All demos completed!")
    print(f"\n💡 Key Features Demonstrated:")
    print(f"   ✅ Context-aware conversations")
    print(f"   ✅ Work pattern analysis")
    print(f"   ✅ Workflow suggestions")
    print(f"   ✅ Interactive AI sessions")
    print(f"   ✅ Rich conversation history integration")
    print(f"   ✅ Personalized AI responses")
    
    print(f"\n🔧 To use in your workflow:")
    print(f"   1. Start a session with workflow.start_conversation_session()")
    print(f"   2. Send messages with workflow.speak_to_workflow()")
    print(f"   3. Ask about work with workflow.ask_about_work()")
    print(f"   4. Get suggestions with workflow.get_workflow_suggestions()")
    print(f"   5. End session with workflow.end_session()") 