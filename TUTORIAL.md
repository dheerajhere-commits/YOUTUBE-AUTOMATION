# NEXUS-100: Step-by-Step Usage Pipeline

Welcome to NEXUS-100. This document acts as your pipeline guide, walking you through the complete lifecycle of operating the multi-agent automation system, explaining the underlying features at every step.

---

## Step 1: Configuration & Setup (The Foundation)

Before the AI agents can work, they need access to the outside world.

1.  **Dependencies:** Ensure you have run `pip install -r requirements.txt` and have [FFmpeg](https://ffmpeg.org/download.html) installed on your system (required by the Production Agent to render video and audio).
2.  **API Keys:** Open `config.yaml` and input your keys.
    *   *Feature Explored:* **Config Loader (`core/config.py`)**. This module securely reads your `config.yaml` and distributes the credentials to the agents (e.g., passing the Gemini key to the Strategy Agent, and the Pexels key to the Production agent).
3.  **Initialization:** Run `python main.py init`
    *   *Feature Explored:* **Database schema creation**. This generates `nexus100.db` (creating tables for `accounts`, `posting_schedules`, `video_logs`, and the `neural_memory` brain). It also creates the `assets/` folder where videos will be stored.

---

## Step 2: Linking Channels (Ops Agent)

The system needs channels to manage.

1.  **Add a YouTube Channel:**
    ```bash
    python main.py account-link --platform youtube --account-id "my_tech_channel@gmail.com" --channel-name "Tech Daily"
    ```
    *   *Feature Explored:* **OAuth2 Flow (`core/auth.py`)**. This triggers a secure Google login window. Once authenticated, the system saves a refresh token.
2.  **Add an Instagram Channel:**
    ```bash
    python main.py account-link --platform instagram --account-id "tech_daily_ig" --token "YOUR_LONG_LIVED_ACCESS_TOKEN"
    ```
3.  **Verify Setup:** Run `python main.py list-accounts` to ensure they are active.

---

## Step 3: Simulation & Safety (The Dry Run)

Before spending rendering time and API quotas, simulate the pipeline.

1.  **Run a Dry Run:**
    ```bash
    python main.py auto-pilot --dry-run
    ```
    *   *Feature Explored:* **The Auto-Pilot Loop (`core/orchestrator.py`)**. You will see the CLI log the entire agent conversation without posting anything.
    *   *Feature Explored:* **Neural Cognitive Brain (`core/brain.py`)**. You'll notice the system prints `[Brain] Assessed Hardware: ...`. It evaluates your CPU and RAM to set the maximum number of concurrent video renderings your PC can handle.

---

## Step 4: Full Automation (The Content Pipeline)

Once you are confident, run the actual pipeline.

1.  **Start Auto-Pilot:**
    ```bash
    python main.py auto-pilot
    ```

**What happens under the hood during this single command?**

1.  **Research Agent:** Analyzes current trends (simulated via Google Trends/YouTube API) to find a high CPM niche.
2.  **Strategy Agent:** Takes the niche and decides the demographic and core message.
3.  **Creative Agent:** Uses Gemini 1.5 Flash to write a 60-second viral script.
4.  **SEO Agent:** Optimizes the generated title, adds clickbait hooks, and appends viral hashtags.
5.  **Video Deduplication:** If managing 100 channels, it hashes the script title and generates the `.mp4` **only once** to save CPU time.
6.  **Production Agent:** Uses `gTTS` to generate a voiceover, pulls relevant stock footage via the **Pexels API**, and stitches them together using `MoviePy`.
7.  **Async Cooldown:** The Ops agent intentionally pauses (`asyncio.sleep`) between interacting with accounts to prevent IP rate-limiting.
8.  **Posting Agent:** Securely connects to the YouTube/Instagram API and uploads the video (wrapped in exponential backoff retries via `tenacity` in case the network fails).

---

## Step 5: Background Scheduling (Hands-off Mode)

If videos were scheduled for later rather than posted immediately:

1.  **Start the Scheduler Engine:**
    ```bash
    python main.py start-scheduler
    ```
    *   *Feature Explored:* **Scheduler Engine (`core/scheduler.py`)**. This command runs indefinitely in the background. It wakes up every 60 seconds, queries the `posting_schedules` database, and triggers the `Posting Agent` when a video hits its due date.

---

## Step 6: System Observability & AI Learning (The Brain)

To see how your empire is performing:

1.  **Check Status:**
    ```bash
    python main.py status
    ```
    *   *Feature Explored:* **Analytics Feedback Loop & Neural Memory**. After a video is posted, the `core/analytics.py` module uses the YouTube API to fetch real Views, Likes, and Watch Time. It calculates a score out of 10.
    *   The `CognitiveBrain` logs this score in the `neural_memory` database.
    *   When you run `status`, you will see a visual representation of which niches (e.g., "AI Tutorials" vs "Finance Hacks") have the highest historical success scores, proving that the system is learning what works.

---

## Compiling for Distribution

If you want to move the tool to a server without installing Python dependencies manually:

1.  **Build Executable:** Run `build.bat` on Windows.
    *   *Feature Explored:* **PyInstaller**. This bundles all the multi-agent logic, MoviePy dependencies, and database schemas into a single `NEXUS-100.exe` file inside the `dist/` folder.
