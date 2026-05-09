from pydantic_ai import Agent

import os
from core.config import config

# Ensure key is set if not provided to allow imports to succeed
gemini_key = config.get('api_keys', {}).get('gemini_api', 'dummy_key')
os.environ.setdefault('GOOGLE_API_KEY', gemini_key if gemini_key != "YOUR_GEMINI_API_KEY" else 'dummy_key')

research_agent = Agent(
    'gemini-1.5-flash',
    system_prompt="""You are a Research Agent.
    Your task is to identify high-CPM, low-competition niches for YouTube Shorts and Instagram Reels.
    Analyze trending topics in the last 24 hours and output a detailed JSON with a 'niche', 'target_audience', 'cpm_estimate', and 'competition_level'.""",
)

async def find_niche() -> str:
    """
    Simulates finding a niche using Google Trends/YouTube trending data.
    """
    # In a real app, this would make API calls to Google Trends and YouTube Data API.
    prompt = "Give me a high CPM, low competition niche trending right now for short form video content."
    result = await research_agent.run(prompt)
    return result.data
