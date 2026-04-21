"""
Configuration settings for the AI Agent System
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

import os
from dotenv import load_dotenv

load_dotenv()


# API Keys
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# LLM Configuration
MODEL_NAME = "claude-sonnet-4-20250514"
MAX_TOKENS = 4096
TEMPERATURE = 0.7

# Agent Names
ORCHESTRATOR_NAME = "Orchestrator"
RESEARCH_AGENT_NAME = "Research Agent"
DATA_AGENT_NAME = "Data Agent"
INTELLIGENCE_AGENT_NAME = "Intelligence Agent"
