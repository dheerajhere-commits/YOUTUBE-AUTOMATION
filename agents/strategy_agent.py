from pydantic_ai import Agent
import os
from core.config import config

gemini_key = config.get('api_keys', {}).get('gemini_api', 'dummy_key')
os.environ.setdefault('GOOGLE_API_KEY', gemini_key if gemini_key != "YOUR_GEMINI_API_KEY" else 'dummy_key')

strategy_agent = Agent(
    'gemini-1.5-flash',
    system_prompt="""You are the Strategy Director for a digital media company.
    Your task is to review a given niche and define a content strategy.
    Output must be JSON with 'theme', 'target_demographic', 'posting_frequency', and 'core_message'.""",
)

async def define_strategy(niche_data: str) -> dict:
    """
    Defines the overall channel strategy based on the selected niche.
    """
    prompt = f"Develop a channel strategy for this niche: {niche_data}"

    try:
        if os.environ.get('GOOGLE_API_KEY') == 'dummy_key':
            return {
                "theme": "Daily Tech Insights",
                "target_demographic": "18-35 tech enthusiasts",
                "posting_frequency": "1 per day",
                "core_message": "Simplifying complex AI concepts."
            }

        result = await strategy_agent.run(prompt)
        from core.utils import parse_llm_json
        data = parse_llm_json(result.data)
        return data
    except Exception as e:
        print(f"[Strategy Agent] Error defining strategy: {e}")
        return {
            "theme": "General Trending Content",
            "target_demographic": "Broad audience",
            "posting_frequency": "1 per day",
            "core_message": "Stay updated with trends."
        }
