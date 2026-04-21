"""
Orchestrator Agent - Coordinates multiple specialized agents
"""
from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from agents.research_agent import ResearchAgent
from agents.data_agent import DataAgent
from agents.intelligence_agent import IntelligenceAgent


class OrchestratorAgent(BaseAgent):
    """
    Master agent that coordinates specialized agents:
    - Analyzes complex tasks
    - Delegates to appropriate agents
    - Aggregates results
    - Provides unified responses
    """
    
    def __init__(self):
        """Initialize the Orchestrator with all specialized agents"""
        super().__init__(
            name="Orchestrator Agent",
            role="Coordinate multiple agents to accomplish complex tasks"
        )
        
        # Initialize all specialized agents
        self.research_agent = ResearchAgent()
        self.data_agent = DataAgent()
        self.intelligence_agent = IntelligenceAgent()
        
        self.agents = {
            "research": self.research_agent,
            "data": self.data_agent,
            "intelligence": self.intelligence_agent
        }
        
        print(f"✓ Orchestrator initialized with {len(self.agents)} specialized agents")
    
    def analyze_task(self, task: str) -> Dict[str, Any]:
        """
        Analyze a task to determine which agents are needed
        
        Args:
            task: High-level task description
            
        Returns:
            Dictionary with task analysis and agent assignments
        """
        print(f"\n🔍 Analyzing task: {task}\n")
        
        analysis = {
            "task": task,
            "agents_needed": [],
            "reasoning": ""
        }
        
        # Simple keyword-based routing (in production, use LLM for this)
        task_lower = task.lower()
        
        # Check for research keywords
        if any(word in task_lower for word in ["paper", "research", "arxiv", "study", "ml", "ai", "sota"]):
            analysis["agents_needed"].append("research")
        
        # Check for data/monitoring keywords
        if any(word in task_lower for word in ["api", "monitor", "health", "performance", "endpoint", "status"]):
            analysis["agents_needed"].append("data")
        
        # Check for intelligence keywords
        if any(word in task_lower for word in ["website", "scrape", "competitor", "trend", "web", "analyze"]):
            analysis["agents_needed"].append("intelligence")
        
        # If no specific keywords, use all agents
        if not analysis["agents_needed"]:
            analysis["agents_needed"] = ["research", "data", "intelligence"]
            analysis["reasoning"] = "No specific agent identified - will use all agents for comprehensive analysis"
        else:
            agent_names = [self.agents[a].name for a in analysis["agents_needed"]]
            analysis["reasoning"] = f"Task requires: {', '.join(agent_names)}"
        
        print(f"📋 Analysis: {analysis['reasoning']}")
        print(f"🎯 Agents to use: {', '.join(analysis['agents_needed'])}\n")
        
        return analysis
    
    def delegate_task(self, agent_name: str, task: str) -> Dict[str, Any]:
        """
        Delegate a task to a specific agent
        
        Args:
            agent_name: Name of agent ("research", "data", or "intelligence")
            task: Task description
            
        Returns:
            Result from the agent
        """
        agent = self.agents.get(agent_name)
        
        if not agent:
            return {
                "status": "error",
                "message": f"Unknown agent: {agent_name}"
            }
        
        print(f"📤 Delegating to {agent.name}...")
        
        try:
            result = agent.run(task)
            print(f"✓ {agent.name} completed task\n")
            return result
        except Exception as e:
            print(f"❌ {agent.name} failed: {str(e)}\n")
            return {
                "status": "error",
                "message": str(e),
                "agent": agent_name
            }
    
    def aggregate_results(self, results: List[Dict[str, Any]]) -> str:
        """
        Aggregate results from multiple agents into a unified summary
        
        Args:
            results: List of results from different agents
            
        Returns:
            Unified summary string
        """
        summary_parts = []
        
        for result in results:
            if result.get("status") == "success":
                agent_name = result.get("agent", "Unknown")
                
                # Extract key information based on agent type
                if "papers_found" in result:
                    summary_parts.append(f"Research: Found {result['papers_found']} relevant papers")
                elif "successful_checks" in result:
                    summary_parts.append(f"Monitoring: {result['successful_checks']}/{result['total_checks']} checks successful, avg {result['avg_response_time_ms']}ms")
                elif "key_topics" in result:
                    topics = ', '.join(result['key_topics'][:3])
                    summary_parts.append(f"Intelligence: Analyzed {result['url']}, key topics: {topics}")
        
        if not summary_parts:
            return "No successful results from agents"
        
        return " | ".join(summary_parts)
    
    def run(self, task: str) -> Dict[str, Any]:
        """
        Main orchestration logic - coordinates multiple agents
        
        Args:
            task: High-level task description
            
        Returns:
            Aggregated results from all agents
        """
        print(f"\n{'='*70}")
        print(f"🤖 {self.name} starting orchestration")
        print(f"{'='*70}")
        
        # Step 1: Analyze the task
        analysis = self.analyze_task(task)
        
        # Step 2: Delegate to appropriate agents
        agent_results = []
        
        for agent_name in analysis["agents_needed"]:
            result = self.delegate_task(agent_name, task)
            result["agent"] = agent_name
            agent_results.append(result)
        
        # Step 3: Aggregate results
        print("="*70)
        print("📊 AGGREGATING RESULTS")
        print("="*70 + "\n")
        
        summary = self.aggregate_results(agent_results)
        
        # Step 4: Store in memory
        self.add_to_memory(f"Orchestrated task using {len(analysis['agents_needed'])} agents")
        
        # Step 5: Return unified response
        return {
            "status": "success",
            "task": task,
            "agents_used": analysis["agents_needed"],
            "agent_results": agent_results,
            "summary": summary
        }