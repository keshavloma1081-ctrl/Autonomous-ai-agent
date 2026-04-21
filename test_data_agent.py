"""
Test Data Agent with mock monitoring (no Claude API needed)
Demonstrates autonomous API monitoring and anomaly detection
"""
from agents.data_agent import DataAgent

print("\n" + "="*70)
print("🤖 DATA AGENT - API MONITORING DEMO")
print("="*70 + "\n")

# Create the Data Agent
print("Step 1: Initializing Data Agent...")
agent = DataAgent()

print("\nStep 2: Monitoring a public test API (httpbin.org)...\n")

# Monitor a real public API (no auth needed)
print("="*70)
print("Starting 3 monitoring checks with 2-second intervals...")
print("="*70 + "\n")

results = []
for i in range(3):
    print(f"Check {i+1}/3:")
    metrics = agent.monitor_api("https://httpbin.org/status/200")
    results.append(metrics)
    
    if i < 2:
        import time
        time.sleep(2)
    print()

# Display summary
print("="*70)
print("📊 MONITORING SUMMARY")
print("="*70 + "\n")

successful_checks = sum(1 for r in results if r["success"])
total_checks = len(results)
avg_time = sum(r["response_time_ms"] for r in results if r["response_time_ms"]) / total_checks

print(f"Total Checks: {total_checks}")
print(f"Successful: {successful_checks}/{total_checks}")
print(f"Average Response Time: {avg_time:.2f}ms")
print(f"Anomalies Detected: {len(agent.anomalies_detected)}")
print()

# Show individual check details
print("="*70)
print("📋 DETAILED RESULTS")
print("="*70 + "\n")

for i, result in enumerate(results, 1):
    print(f"Check {i}:")
    print(f"  Status: {'✓ Success' if result['success'] else '❌ Failed'}")
    print(f"  Status Code: {result['status_code']}")
    print(f"  Response Time: {result['response_time_ms']}ms")
    print(f"  Timestamp: {result['timestamp']}")
    if result.get('error'):
        print(f"  Error: {result['error']}")
    print()

# Show anomalies if any
if agent.anomalies_detected:
    print("="*70)
    print("⚠️  ANOMALIES DETECTED")
    print("="*70 + "\n")
    
    for anomaly in agent.anomalies_detected:
        print(f"Timestamp: {anomaly['timestamp']}")
        print(f"Issue: {anomaly['anomaly']}")
        print()
else:
    print("="*70)
    print("✓ No anomalies detected - API is healthy!")
    print("="*70 + "\n")

print("="*70)
print("✅ DATA AGENT CAPABILITIES DEMONSTRATED")
print("="*70 + "\n")

print("What this agent can do:")
print("  ✓ Monitor API endpoints autonomously")
print("  ✓ Track response times and status codes")
print("  ✓ Detect anomalies (slow responses, errors, status changes)")
print("  ✓ Build historical baseline for comparison")
print("  ✓ Multiple checks for pattern detection")
print("  ✓ Structured metric collection")
print()

print("Production use cases:")
print("  • Monitor critical API health 24/7")
print("  • Alert on performance degradation")
print("  • Track SLA compliance")
print("  • Detect outages before users report them")
print("  • Analyze API response patterns")
print()

print("="*70)
print("🎓 WHAT YOU'VE BUILT SO FAR")
print("="*70 + "\n")

print("Agent 1: ✅ Research Agent (arXiv paper search & analysis)")
print("Agent 2: ✅ Data Agent (API monitoring & anomaly detection)")
print("Agent 3: ⏳ Intelligence Agent (web scraping & trends)")
print("Orchestrator: ⏳ Coordinates all agents")
print()

print("Next: Build the Intelligence Agent for competitive intelligence!")
print("="*70 + "\n")