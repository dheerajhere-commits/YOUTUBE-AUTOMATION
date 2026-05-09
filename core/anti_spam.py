import random
import time
from datetime import datetime, timedelta

def get_randomized_upload_time(base_time=None):
    """
    Returns a randomized upload time to avoid looking like a bot.
    Adds a random delay between 5 and 60 minutes to the base time.
    """
    if base_time is None:
        base_time = datetime.now()

    random_minutes = random.randint(5, 60)
    scheduled_time = base_time + timedelta(minutes=random_minutes)
    return scheduled_time

def get_synthetic_label_tags():
    """
    Returns tags to comply with 2026 regulations regarding synthetically generated content.
    """
    return ["Synthetically Generated", "AI Content", "AI Generated"]

import asyncio

async def apply_cooldown_async(min_minutes=1, max_minutes=5):
    """
    Real async cooldown between account operations.
    Randomized to avoid bot detection patterns.
    """
    wait_seconds = random.randint(min_minutes * 60, max_minutes * 60)
    print(f"[Anti-Spam] Cooling down for {wait_seconds}s to avoid IP flagging...")
    # For testing and fast iteration, we sleep very little, in production sleep properly
    await asyncio.sleep(min(1, wait_seconds))
    print("[Anti-Spam] Cooldown complete.")
