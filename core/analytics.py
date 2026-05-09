import requests

def fetch_youtube_stats(credentials, video_id: str) -> float:
    """
    Fetches real video performance from YouTube Analytics API.
    Returns a normalized score 0-10.
    """
    from googleapiclient.discovery import build

    try:
        analytics = build('youtubeAnalytics', 'v2', credentials=credentials)
        response = analytics.reports().query(
            ids='channel==MINE',
            startDate='2024-01-01',
            endDate='2099-01-01',
            metrics='views,likes,estimatedMinutesWatched,subscribersGained',
            filters=f'video=={video_id}'
        ).execute()

        rows = response.get('rows', [[0, 0, 0, 0]])
        if not rows:
             rows = [[0, 0, 0, 0]]

        views, likes, watch_time, subs = rows[0]

        # Weighted scoring formula
        score = min(10.0, (
            (views / 1000) * 3.0 +
            (likes / 100) * 3.0 +
            (watch_time / 500) * 2.0 +
            (subs / 10) * 2.0
        ))
        return round(score, 2)
    except Exception as e:
        print(f"[Analytics] Failed to fetch real stats for {video_id}: {e}")
        # Return fallback score or base score if fetch fails
        return 5.0
