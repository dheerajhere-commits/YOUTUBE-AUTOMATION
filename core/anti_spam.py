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

def apply_cooldown(minutes=30):
    """
    Applies a cooldown to prevent IP flagging.
    """
    print(f"Applying cooldown for {minutes} minutes to prevent IP flagging...")
    # In a real async environment, we'd use asyncio.sleep
    # time.sleep(minutes * 60)
    print(f"Cooldown completed.")
