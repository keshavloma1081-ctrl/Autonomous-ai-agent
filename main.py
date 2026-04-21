"""
Autonomous AI Agent System - Command Line Interface
Multi-agent system with Research, Data, and Intelligence agents
"""
import sys
from agents.orchestrator_agent import OrchestratorAgent


def print_banner():
    """Print system banner"""
    print("\n" + "="*70)
    print("🤖 AUTONOMOUS AI AGENT SYSTEM")
    print("="*70)
    print("Multi-Agent Coordination | Research • Data • Intelligence")
    print("="*70 + "\n")


def print_help():
    """Print usage instructions"""
    print("Available commands:")
    print("  research <query>  - Search research papers")
    print("  monitor <url>     - Monitor API endpoint")
    print("  analyze <url>     - Analyze website")
    print("  task <description>- Custom task (auto-routes to agents)")
    print("  help              - Show this help")
    print("  exit              - Exit the system")
    print()


def main():
    """Main CLI interface"""
    print_banner()
    
    print("Initializing autonomous agent system...")
    try:
        orchestrator = OrchestratorAgent()
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        print("\nNote: This system works without API credits for:")
        print("  • API monitoring (uses public test APIs)")
        print("  • Web scraping (uses public websites)")
        print("  • System architecture demonstration")
        print("\nFor full autonomous thinking, add Anthropic API credits to .env")
        return
    
    print("\n✓ System ready! Type 'help' for commands or 'exit' to quit.\n")
    
    # Interactive loop
    while True:
        try:
            # Get user input
            user_input = input("🤖 > ").strip()
            
            if not user_input:
                continue
            
            # Parse command
            parts = user_input.split(maxsplit=1)
            command = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""
            
            # Handle commands
            if command == "exit":
                print("\n👋 Shutting down agent system. Goodbye!\n")
                break
            
            elif command == "help":
                print()
                print_help()
            
            elif command == "research":
                if not args:
                    print("❌ Usage: research <query>")
                    print("   Example: research transformers in NLP")
                else:
                    task = f"Find recent papers about {args}"
                    print(f"\n📚 Executing: {task}\n")
                    result = orchestrator.run(task)
                    print(f"\n✅ Task completed!")
                    print(f"Summary: {result.get('summary', 'No summary')}\n")
            
            elif command == "monitor":
                if not args:
                    print("❌ Usage: monitor <url>")
                    print("   Example: monitor https://httpbin.org/status/200")
                else:
                    task = f"Monitor API health for {args}"
                    print(f"\n📊 Executing: {task}\n")
                    result = orchestrator.run(task)
                    print(f"\n✅ Task completed!")
                    print(f"Summary: {result.get('summary', 'No summary')}\n")
            
            elif command == "analyze":
                if not args:
                    print("❌ Usage: analyze <url>")
                    print("   Example: analyze https://news.ycombinator.com")
                else:
                    task = f"Analyze website {args}"
                    print(f"\n🌐 Executing: {task}\n")
                    result = orchestrator.run(task)
                    print(f"\n✅ Task completed!")
                    print(f"Summary: {result.get('summary', 'No summary')}\n")
            
            elif command == "task":
                if not args:
                    print("❌ Usage: task <description>")
                    print("   Example: task Research ML papers and monitor APIs")
                else:
                    print(f"\n🎯 Executing: {args}\n")
                    result = orchestrator.run(args)
                    print(f"\n✅ Task completed!")
                    print(f"Summary: {result.get('summary', 'No summary')}\n")
            
            else:
                print(f"❌ Unknown command: {command}")
                print("   Type 'help' for available commands\n")
        
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Shutting down...\n")
            break
        
        except Exception as e:
            print(f"\n❌ Error: {e}\n")
            print("Note: Some features require API credits in .env")
            print("System continues running for available features.\n")


if __name__ == "__main__":
    main()