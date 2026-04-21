"""
Test the Research Agent
"""
from agents.research_agent import ResearchAgent

# Create the agent
agent = ResearchAgent()

# Run an autonomous research task
task = "Find recent papers about transformers in NLP"

print("Starting autonomous research task...")
result = agent.run(task)

print("\n" + "="*60)
print("RESULTS:")
print("="*60)
print(f"Status: {result['status']}")
print(f"Papers found: {result['papers_found']}")
print(f"\nAnalysis:\n{result['analysis']}")