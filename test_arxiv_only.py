"""
Test arXiv search without Claude API - FREE
"""
from agents.research_agent import ResearchAgent

print("Creating Research Agent...")
agent = ResearchAgent()

print("\nSearching arXiv for papers about 'transformers in NLP'...\n")

# Direct search - bypasses Claude API
papers = agent.search_papers("transformers NLP", max_results=5)

print(f"\n{'='*60}")
print(f"RESULTS: Found {len(papers)} papers")
print(f"{'='*60}\n")

for i, paper in enumerate(papers, 1):
    print(f"📄 Paper {i}:")
    print(f"   Title: {paper['title']}")
    print(f"   Authors: {', '.join(paper['authors'][:3])}")
    print(f"   Published: {paper['published'][:10]}")
    print(f"   Link: {paper['link']}")
    print(f"   Summary: {paper['summary'][:150]}...")
    print()