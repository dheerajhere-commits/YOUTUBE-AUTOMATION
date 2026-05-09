import re
import json

def parse_llm_json(text):
    """
    Safely parses JSON out of a raw LLM text response using regex.
    Useful when the model wraps JSON in markdown blocks or includes conversational filler.
    """
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        return json.loads(match.group())
    raise ValueError("No JSON found in response")
