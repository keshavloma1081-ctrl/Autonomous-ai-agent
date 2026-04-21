"""
LLM Client - Handles all communication with LLM APIs
Supports: Groq (FREE), Anthropic Claude
"""
import os
from config.settings import ANTHROPIC_API_KEY


class LLMClient:
    """
    Wrapper for LLM API calls - tries Groq first (free), then Claude
    """
    
    def __init__(self):
        """Initialize LLM client with available provider"""
        self.provider = None
        self.client = None
        
        # Try Groq first (FREE!)
        try:
            groq_key = os.getenv("GROQ_API_KEY")
            if groq_key:
                from groq import Groq
                self.client = Groq(api_key=groq_key)
                self.provider = "groq"
                self.model = "llama-3.3-70b-versatile"
                self.max_tokens = 4096
                self.temperature = 0.7
                print("✓ Using Groq (FREE)")
                return
        except Exception as e:
            print(f"⚠️  Groq failed: {e}")
        
        # Fallback to Anthropic
        if ANTHROPIC_API_KEY:
            try:
                from anthropic import Anthropic
                self.client = Anthropic(api_key=ANTHROPIC_API_KEY)
                self.provider = "anthropic"
                self.model = "claude-sonnet-4-20250514"
                self.max_tokens = 4096
                self.temperature = 0.7
                print("✓ Using Anthropic Claude")
                return
            except Exception as e:
                print(f"⚠️  Anthropic failed: {e}")
        
        print("⚠️  No API keys found - agents will work in limited mode")
    
    def call(self, messages, system_prompt=None, tools=None):
        """
        Make LLM API call
        
        Args:
            messages: List of message dicts
            system_prompt: Optional system prompt
            tools: Optional tools (for function calling)
            
        Returns:
            Response object
        """
        if not self.client:
            # Return simple response if no API available
            class SimpleResponse:
                def __init__(self):
                    class ContentBlock:
                        text = "Processing without AI..."
                    self.content = [ContentBlock()]
            return SimpleResponse()
        
        if self.provider == "groq":
            return self._call_groq(messages, system_prompt)
        else:
            return self._call_anthropic(messages, system_prompt, tools)
    
    def _call_groq(self, messages, system_prompt):
        """Call Groq API (FREE)"""
        # Add system prompt as first message
        if system_prompt:
            messages = [{"role": "system", "content": system_prompt}] + messages
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            # Convert to Anthropic-like format
            class ContentBlock:
                def __init__(self, text):
                    self.text = text
            
            class Response:
                def __init__(self, text):
                    self.content = [ContentBlock(text)]
            
            return Response(response.choices[0].message.content)
        
        except Exception as e:
            print(f"Error calling Groq API: {str(e)}")
            raise
    
    def _call_anthropic(self, messages, system_prompt, tools):
        """Call Anthropic API"""
        try:
            api_params = {
                "model": self.model,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "messages": messages,
            }
            
            if system_prompt:
                api_params["system"] = system_prompt
            if tools:
                api_params["tools"] = tools
            
            return self.client.messages.create(**api_params)
        
        except Exception as e:
            print(f"Error calling Claude API: {str(e)}")
            raise