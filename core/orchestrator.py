import asyncio
import os
from database.db import get_db_connection

from agents.research_agent import find_niche
from agents.creative_agent import generate_content
from agents.production_agent import create_video
from agents.ops_agent import manage_accounts
from agents.posting_agent import post_video

async def run_auto_pilot_loop(accounts):
    """
    A loop that: Finds Niche -> Generates Script -> Creates Video -> Posts to 100 Channels.
    """
    print("Starting Auto-Pilot Loop...")

    # 1. Manage accounts (Ops Agent)
    await manage_accounts(accounts)

    # 2. Find Niche (Research Agent)
    print("Finding niche...")
    try:
        if os.environ.get('GOOGLE_API_KEY') == 'dummy_key':
            niche_data = "{'niche': 'AI Tutorials', 'target_audience': 'Tech enthusiasts', 'cpm_estimate': 15.0, 'competition_level': 'Medium'}"
        else:
            niche_data = await find_niche()
    except Exception as e:
        print(f"Error finding niche: {e}")
        niche_data = "{'niche': 'Fallback Niche'}"
    print(f"Found niche: {niche_data}")

    # 3. Generate Content (Creative Agent)
    print("Generating content...")
    try:
        if os.environ.get('GOOGLE_API_KEY') == 'dummy_key':
            content = {
                "script": "Welcome to the latest AI tutorial. Today we talk about multi-agent systems. Subscribe for more!",
                "title": "AI Multi-Agent Systems Explained in 60s!",
                "description": "Learn about multi-agent systems.",
                "tags": ["AI", "Tech", "Tutorial"]
            }
        else:
            content = await generate_content(niche_data)
    except Exception as e:
        print(f"Error generating content: {e}")
        content = {"script": "Fallback script", "title": "Fallback title"}
    print(f"Generated script: {content.get('script')}")

    # Process 100 channels concurrently (simulated with a smaller number or batches)
    print(f"Processing for {len(accounts)} accounts...")

    async def process_account(account):
        account_id = account['account_id']
        platform = account['platform']
        print(f"Processing for {platform} account: {account_id}")

        # 4. Create Video (Production Agent)
        video_path = f"assets/video_{account_id}_{hash(content.get('title'))}.mp4"
        await create_video(content.get('script'), video_path)

        # 5. Post Video (Posting Agent)
        await post_video(video_path, content, account_id)

        # Log to DB
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO video_logs (account_id, video_title, video_path, status)
                VALUES (?, ?, ?, ?)
            ''', (account_id, content.get('title'), video_path, 'posted'))
            conn.commit()

    # Use asyncio.gather to process accounts concurrently
    tasks = [process_account(acc) for acc in accounts]
    await asyncio.gather(*tasks)

    print("Auto-Pilot Loop Completed.")
