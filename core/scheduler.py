import asyncio
from datetime import datetime
from database.db import get_db_connection
from agents.posting_agent import post_video
import json

async def run_scheduler():
    """
    Checks every 60s for due scheduled posts and fires them.
    """
    print("[Scheduler] Starting background scheduler...")
    while True:
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT ps.id, ps.video_id, vl.video_path, vl.account_id, vl.video_title
                    FROM posting_schedules ps
                    JOIN video_logs vl ON ps.video_id = vl.id
                    WHERE ps.status = 'pending' AND ps.scheduled_time <= ?
                """, (datetime.now().isoformat(),))
                due_jobs = cursor.fetchall()

            for job in due_jobs:
                print(f"[Scheduler] Firing job for account {job['account_id']}: {job['video_title']}")
                metadata = {"title": job['video_title'], "tags": [], "description": ""}
                await post_video(job['video_path'], metadata, job['account_id'])

                with get_db_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE posting_schedules SET status='completed' WHERE id=?",
                        (job['id'],)
                    )
                    conn.commit()

        except Exception as e:
            print(f"[Scheduler] Error: {e}")

        await asyncio.sleep(60)
