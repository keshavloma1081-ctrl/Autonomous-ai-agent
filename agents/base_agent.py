"""
Base Agent - Blueprint for all specialized agents
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime
from core.llm_client import LLMClient


class BaseAgent(ABC):
    """
    Abstract base class that all agents inherit from.
    Provides common functionality: thinking, memory, execution tracking.
    """
    
    def __init__(self, name: str, role: str):
        """
        Initialize the base agent
        
        Args:
            name: Agent's name (e.g., "Research Agent")
            role: Agent's purpose (e.g., "Find and summarize ML papers")
        """
        self.name = name
        self.role = role
        self.llm_client = LLMClient()
        self.memory = []
        self.execution_log = []
        
        print(f"✓ Initialized {self.name}")
    
    def think(self, prompt: str) -> str:
        """
        Agent uses LLM to reason about a problem
        
        Args:
            prompt: The question or task to think about
            
        Returns:
            The agent's reasoning/response as a string
        """
        # Check if API key is available
        from config.settings import ANTHROPIC_API_KEY
        import os
        
        groq_key = os.getenv("GROQ_API_KEY")
        
        if not ANTHROPIC_API_KEY and not groq_key:
            # Return a simple response without API call
            print("ℹ️  Skipping AI reasoning (no API credits)")
            return f"Processing task: {prompt[:100]}"
        
        # Build context from recent memory
        memory_context = self._get_memory_context()
        
        # Create system prompt with agent's identity
        system_prompt = f"""You are {self.name}, an autonomous AI agent.
Your role: {self.role}

{memory_context}

Think step-by-step and be thorough in your analysis."""
        
        # Prepare messages for Claude
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        try:
            # Call LLM API
            response = self.llm_client.call(
                messages=messages,
                system_prompt=system_prompt
            )
            
            # Extract text from response
            response_text = ""
            for block in response.content:
                if hasattr(block, "text"):
                    response_text += block.text
            
            # Store this interaction in memory
            self.add_to_memory(f"Thought about: {prompt[:50]}... Response: {response_text[:100]}...")
            
            return response_text
        
        except Exception as e:
            print(f"⚠️  AI reasoning failed: {str(e)}")
            return f"Processing task: {prompt[:100]}"
    
    def add_to_memory(self, content: str):
        """
        Add an item to the agent's memory
        
        Args:
            content: What to remember (string)
        """
        memory_item = {
            "timestamp": datetime.now().isoformat(),
            "content": content
        }
        self.memory.append(memory_item)
        
        # Keep memory bounded (last 50 items only)
        if len(self.memory) > 50:
            self.memory = self.memory[-50:]
    
    def _get_memory_context(self, last_n: int = 10) -> str:
        """
        Get recent memory items as a formatted string
        
        Args:
            last_n: Number of recent items to include (default 10)
            
        Returns:
            Formatted string of recent memories
        """
        if not self.memory:
            return "No previous memory."
        
        recent_memories = self.memory[-last_n:]
        
        context = "Recent Memory:\n"
        for item in recent_memories:
            context += f"[{item['timestamp']}] {item['content']}\n"
        
        return context
    
    @abstractmethod
    def run(self, task: str) -> Dict[str, Any]:
        """
        Main execution method - MUST be implemented by child classes
        
        Args:
            task: The task for this agent to execute
            
        Returns:
            Dictionary with results
        """
        pass