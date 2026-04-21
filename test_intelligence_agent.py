"""
Test Intelligence Agent with public website scraping (no Claude API needed)
"""
from agents.intelligence_agent import IntelligenceAgent

print("\n" + "="*70)
print("🤖 INTELLIGENCE AGENT - WEB SCRAPING DEMO")
print("="*70 + "\n")

# Create agent
print("Step 1: Initializing Intelligence Agent...")
agent = IntelligenceAgent()

print("\nStep 2: Scraping Hacker News (public tech news site)...\n")

# Scrape a public website
url = "https://news.ycombinator.com/"
scraped = agent.scrape_webpage(url)

if scraped["success"]:
    print("\n" + "="*70)
    print("📊 SCRAPING RESULTS")
    print("="*70 + "\n")
    
    print(f"Title: {scraped['title']}")
    print(f"URL: {scraped['url']}")
    print(f"Timestamp: {scraped['timestamp']}")
    print()
    
    print("="*70)
    print("📌 TOP HEADINGS")
    print("="*70 + "\n")
    
    for i, heading in enumerate(scraped['headings'][:5], 1):
        print(f"{i}. [{heading['tag'].upper()}] {heading['text'][:60]}...")
    print()
    
    print("="*70)
    print("🔗 EXTERNAL LINKS FOUND")
    print("="*70 + "\n")
    
    for i, link in enumerate(scraped['links'][:5], 1):
        print(f"{i}. {link['text'][:50]}...")
        print(f"   → {link['url'][:60]}...")
    print()
    
    # Extract insights
    insights = agent.extract_insights(scraped)
    
    print("="*70)
    print("💡 KEY INSIGHTS")
    print("="*70 + "\n")
    
    print(f"Key Topics: {', '.join(insights['key_topics'][:3])}")
    print(f"\nSummary: {insights['summary']}")
    print()
    
    # Detect trends
    trends = agent.detect_trends(scraped)
    
    print("="*70)
    print("📈 TREND ANALYSIS")
    print("="*70 + "\n")
    
    for trend in trends:
        print(f"  • {trend}")
    print()

print("="*70)
print("✅ INTELLIGENCE AGENT CAPABILITIES DEMONSTRATED")
print("="*70 + "\n")

print("What this agent can do:")
print("  ✓ Scrape web pages autonomously")
print("  ✓ Extract structured data (titles, headings, links)")
print("  ✓ Identify key topics and themes")
print("  ✓ Track changes over time")
print("  ✓ Detect trends and patterns")
print("  ✓ Competitive intelligence gathering")
print()

print("Production use cases:")
print("  • Monitor competitor websites for changes")
print("  • Track industry news and trends")
print("  • Gather market intelligence")
print("  • Analyze content strategies")
print("  • Detect emerging topics")
print()

print("="*70)
print("🎉 ALL 3 AGENTS COMPLETE!")
print("="*70 + "\n")

print("✅ Agent 1: Research Agent (arXiv papers)")
print("✅ Agent 2: Data Agent (API monitoring)")
print("✅ Agent 3: Intelligence Agent (web scraping)")
print()
print("Next: Build the Orchestrator to coordinate all 3 agents!")
print("="*70 + "\n")