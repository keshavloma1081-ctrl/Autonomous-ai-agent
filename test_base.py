"""
Test the Base Agent to verify it works
"""
from agents.base_agent import BaseAgent
from typing import Dict, Any

# Create a simple test agent (inherits from BaseAgent)
class TestAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Test Agent",
            role="Testing the base agent functionality"
        )
    
    def run(self, task: str) -> Dict[str, Any]:
        # Simple implementation for testing
        result = self.think(task)
        return {"status": "success", "result": result}

# Run the test
if __name__ == "__main__":
    print("Creating test agent...")
    agent = TestAgent()
    
    print("\nAdding items to memory...")
    agent.add_to_memory("First memory item")
    agent.add_to_memory("Second memory item")
    
    print("\nGetting memory context:")
    print(agent._get_memory_context())
    
    print("\n✓ Base Agent works correctly!")