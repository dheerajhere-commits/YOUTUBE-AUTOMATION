# NEXUS-100: Multi-Agent Automation System

NEXUS-100 is a Windows-compatible CLI tool designed to manage an automated YouTube and Instagram empire (up to 100 channels). The system uses a Multi-Agent System (MAS) architecture to operate entirely programmatically, utilizing open-source libraries to perform everything from niche discovery to final video posting.

## Features

1. **Research Agent (`--niche-finder`)**: Scrapes trending data to identify high-CPM, low-competition niches.
2. **Creative Agent**: Generates viral scripts and SEO-optimized metadata using Gemini 1.5 Flash.
3. **Production Agent**: Programmatically generates videos using `MoviePy` to overlay AI-generated voiceovers (`gTTS`) onto stock footage.
4. **Ops Agent**: Manages OAuth2 token rotation for accounts and implements a "Cooldown" logic to prevent IP flagging.
5. **Posting Agent (`--auto-pilot`)**: Handles scheduled uploads via YouTube Data API v3 and Instagram Graph API with anti-spam measures.

## Setup Instructions

### Prerequisites

- Python 3.11+
- [FFmpeg](https://ffmpeg.org/download.html) (Required by `MoviePy` for video processing)
- ImageMagick (Optional, useful for advanced text overlays in `MoviePy`)

### 1. Clone and Install Dependencies

```bash
git clone <repository_url>
cd <repository_directory>
pip install -r requirements.txt
```

### 2. Configure API Keys

Edit the `config.yaml` file to add your API keys:

```yaml
api_keys:
  youtube_data_api: "YOUR_YOUTUBE_API_KEY"
  instagram_graph_api: "YOUR_INSTAGRAM_API_KEY"
  gemini_api: "YOUR_GEMINI_API_KEY"
  pexels_api: "YOUR_PEXELS_API_KEY"
```

You must also set your `GOOGLE_API_KEY` environment variable to use the Gemini agents:
```bash
# On Windows
set GOOGLE_API_KEY=your_key_here

# On Linux/macOS
export GOOGLE_API_KEY=your_key_here
```

### 3. Initialize the Database

Run the init command to set up the SQLite database and necessary directories:

```bash
python main.py init
```

## Usage Instructions

Use the built-in `--help` command to see all available options:

```bash
python main.py --help
```

### Available Commands

1. **Find a Niche**:
   Analyze trending data to find the best niches.
   ```bash
   python main.py niche-finder
   ```

2. **Link Accounts**:
   Securely add new Gmail/Instagram accounts.
   ```bash
   # For YouTube
   python main.py account-link --platform youtube --account-id your_email@gmail.com

   # For Instagram
   python main.py account-link --platform instagram --account-id your_ig_handle --token your_access_token
   ```

3. **Run Auto-Pilot**:
   Starts the continuous loop that finds a niche, generates a script, creates the video, and schedules posts for all linked accounts.
   ```bash
   python main.py auto-pilot
   ```

4. **Anti-Spam Features**:
   View information about the built-in anti-spam measures.
   ```bash
   python main.py anti-spam
   ```

## Demo

### Screenshot

![CLI Interface Placeholder](https://via.placeholder.com/800x400.png?text=CLI+Interface+Screenshot)

### Video Walkthrough

[![Video Walkthrough Placeholder](https://via.placeholder.com/800x400.png?text=Click+to+watch+Video+Walkthrough)](https://www.youtube.com/watch?v=dQw4w9WgXcQ)
