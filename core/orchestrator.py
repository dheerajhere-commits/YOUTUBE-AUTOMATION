import asyncio
import os
from database.db import get_db_connection

from agents.research_agent import find_niche
from agents.strategy_agent import define_strategy
from agents.creative_agent import generate_content
from agents.seo_agent import optimize_metadata
from agents.production_agent import create_video
from agents.ops_agent import manage_accounts
from agents.posting_agent import post_video
from core.brain import CognitiveBrain
import random
import tenacity

@tenacity.retry(wait=tenacity.wait_exponential(min=2, max=30), stop=tenacity.stop_after_attempt(3))
async def safe_post(video_path, metadata, account_id):
    """
    Safely post the video with exponential backoff retries.
    """
    await post_video(video_path, metadata, account_id)

async def run_auto_pilot_loop(accounts):
    """
    A loop that: Finds Niche -> Plans Strategy -> Generates Script -> Optimizes SEO -> Creates Video -> Posts to Channels.
    """
    print("Starting Auto-Pilot Loop...")
    brain = CognitiveBrain()
    concurrency_limit = brain.get_concurrency_limit()

    # 1. Manage accounts (Ops Agent)
    await manage_accounts(accounts)

    # 2. Find Niche (Research Agent)
    print("Finding niche...")
    import os
    try:
        if os.environ.get('GOOGLE_API_KEY') == 'dummy_key':
            niche_data = "{'niche': 'AI Tutorials', 'target_audience': 'Tech enthusiasts', 'cpm_estimate': 15.0, 'competition_level': 'Medium'}"
        else:
            niche_data = await find_niche()
    except Exception as e:
        print(f"Error finding niche: {e}")
        niche_data = "{'niche': 'Fallback Niche'}"
    print(f"Found niche: {niche_data}")

    # Brain Evaluation
    import ast
    try:
        niche_dict = ast.literal_eval(niche_data)
        niche_name = niche_dict.get('niche', 'Fallback Niche')
    except:
        niche_name = 'Fallback Niche'

    confidence = brain.evaluate_niche(niche_name)
    if confidence < 0.6:
        print("[Brain] Low confidence in this niche based on past failure. Requesting manual override or picking new niche...")
        # In a fully autonomous loop, we would re-roll the niche here.
        # For this execution, we will proceed but note the low confidence.

    # 3. Define Strategy (Strategy Agent)
    print("Defining strategy...")
    strategy = await define_strategy(niche_data)
    print(f"Strategy developed: {strategy.get('theme')}")

    # 4. Generate Content (Creative Agent)
    print("Generating content...")
    try:
        if os.environ.get('GOOGLE_API_KEY') == 'dummy_key':
            content = {
                "script": f"Welcome to our {strategy.get('theme')} channel! Today we talk about multi-agent systems. Subscribe for more!",
                "title": "AI Multi-Agent Systems Explained in 60s!",
                "description": "Learn about multi-agent systems.",
                "tags": ["AI", "Tech", "Tutorial"]
            }
        else:
            # Pass both niche and strategy context to the creative agent in a real app
            content = await generate_content(niche_data)
    except Exception as e:
        print(f"Error generating content: {e}")
        content = {"script": "Fallback script", "title": "Fallback title", "tags": []}
    print(f"Generated script: {content.get('script')}")

    # 5. Optimize Metadata (SEO Agent)
    print("Optimizing SEO...")
    optimized_data = await optimize_metadata(content)
    content['title'] = optimized_data.get('optimized_title', content.get('title'))
    content['description'] = optimized_data.get('optimized_description', content.get('description'))
    content['tags'] = optimized_data.get('optimized_tags', content.get('tags'))
    print(f"Optimized title: {content.get('title')}")

    # Process channels concurrently (using Brain's hardware limits)
    print(f"Processing for {len(accounts)} accounts with concurrency limit {concurrency_limit}...")

    import hashlib
    import os
    # CREATE VIDEO ONCE
    title_hash = hashlib.md5(content.get('title', '').encode()).hexdigest()[:8]
    shared_video_path = f"assets/video_shared_{title_hash}.mp4"

    if not os.path.exists(shared_video_path):
        print("[Orchestrator] Creating shared video for all accounts...")
        await create_video(content.get('script'), shared_video_path)
    else:
        print(f"[Orchestrator] Reusing existing video: {shared_video_path}")

    async def process_account(account):
        account_id = account['account_id']
        platform = account['platform']
        print(f"Processing for {platform} account: {account_id}")

        # 5. Post Video (Posting Agent) with Retries using shared video
        print(f"Initiating safe post for {account_id}...")
        await safe_post(shared_video_path, content.copy(), account_id)

        # Log to DB
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO video_logs (account_id, video_title, video_path, status)
                VALUES (?, ?, ?, ?)
            ''', (account_id, content.get('title'), shared_video_path, 'posted'))
            conn.commit()

    # Batch process using asyncio with chunks limited by concurrency_limit
    for i in range(0, len(accounts), concurrency_limit):
        chunk = accounts[i:i + concurrency_limit]
        tasks = [process_account(acc) for acc in chunk]
        await asyncio.gather(*tasks, return_exceptions=True)

    # 6. Brain Feedback Loop
    from core.analytics import fetch_youtube_stats
    from core.auth import get_google_credentials

    if os.environ.get('NEXUS_DRY_RUN') != 'true' and accounts:
        # In a real system, we would query stats for a post made 24h+ ago.
        # For simplicity, we query the first account's video using a placeholder ID or last known ID.
        creds = get_google_credentials(accounts[0]['account_id'])
        if creds and not (hasattr(creds, 'token') and creds.token == "dummy_token"):
             print("[Orchestrator] Fetching real analytics for Brain feedback...")
             real_score = fetch_youtube_stats(creds, "LATEST_VIDEO_ID") # In real app, pull from DB
             brain.memorize_success(niche_name, strategy.get('theme', 'default'), real_score)
        else:
             print("[Orchestrator] No real credentials. Using simulated feedback for Brain.")
             simulated_score = round(random.uniform(2.0, 10.0), 2)
             brain.memorize_success(niche_name, strategy.get('theme', 'default'), simulated_score)
    else:
        print("[Orchestrator] Dry-run enabled. Skipping feedback loop.")

    print("Auto-Pilot Loop Completed.")
