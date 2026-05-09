from pydantic_ai import Agent

import os
from core.config import config

gemini_key = config.get('api_keys', {}).get('gemini_api', 'dummy_key')
os.environ.setdefault('GOOGLE_API_KEY', gemini_key if gemini_key != "YOUR_GEMINI_API_KEY" else 'dummy_key')

creative_agent = Agent(
    'gemini-1.5-flash',
    system_prompt="""You are a Creative Agent.
    Generate a viral, 60-second script for a short-form video based on the provided niche.
    Also generate SEO-optimized metadata.
    Output must be JSON with 'script', 'title', 'description', and 'tags' (list of strings).""",
)

async def generate_content(niche_data: str) -> dict:
    """
    Generates script and metadata based on niche.
    """
    prompt = f"Generate a script and metadata for this niche: {niche_data}"
    result = await creative_agent.run(prompt)

    from core.utils import parse_llm_json
    try:
        data = parse_llm_json(result.data)
        return data
    except Exception as e:
        print(f"[Creative Agent] Error parsing JSON: {e}")
        # Fallback if json parsing fails
        return {
            "script": "Did you know that AI is taking over the world? Subscribe for more!",
            "title": "AI is taking over!",
            "description": "A quick fact about AI.",
            "tags": ["AI", "Tech", "Future"]
        }
