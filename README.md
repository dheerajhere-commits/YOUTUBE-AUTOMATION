# NEXUS-100: Multi-Agent Automation System

NEXUS-100 is a Windows-compatible CLI tool designed to manage an automated YouTube and Instagram empire (up to 100 channels). The system uses a Multi-Agent System (MAS) architecture to operate entirely programmatically, utilizing open-source libraries to perform everything from niche discovery to final video posting.

## Features

1. **Neural Cognitive Brain**: Dynamically scales operations based on your hardware (Windows 7 low-end PCs to modern high-end rigs) and utilizes a SQLite-backed memory engine to learn and adjust confidence based on the historical success of niches and strategies.
2. **Research Agent (`--niche-finder`)**: Scrapes trending data to identify high-CPM, low-competition niches.
3. **Strategy Agent**: Formulates channel themes and strategies to guide content generation.
4. **Creative Agent**: Generates viral scripts using Gemini 1.5 Flash.
5. **SEO Agent**: Optimizes titles, descriptions, and hashtags for maximum platform visibility and click-through rates.
6. **Production Agent**: Programmatically generates videos using `MoviePy` to overlay AI-generated voiceovers (`gTTS`) onto stock footage.
7. **Ops Agent**: Manages OAuth2 token rotation for accounts and implements a "Cooldown" logic to prevent IP flagging.
8. **Posting Agent (`--auto-pilot`)**: Handles scheduled uploads via YouTube Data API v3 and Instagram Graph API with anti-spam measures.

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
   Securely add new Gmail/Instagram accounts. You can also specify an optional `--channel-name`.
   ```bash
   # For YouTube
   python main.py account-link --platform youtube --account-id your_email@gmail.com --channel-name "My Channel"

   # For Instagram
   python main.py account-link --platform instagram --account-id your_ig_handle --token your_access_token
   ```

3. **Manage Accounts**:
   View or remove your connected accounts.
   ```bash
   # List all connected accounts
   python main.py list-accounts

   # Remove a specific account
   python main.py remove-account your_email@gmail.com
   ```

4. **Run Auto-Pilot**:
   Starts the continuous multi-agent loop that finds a niche, develops a strategy, generates a script, optimizes SEO, creates the video, and schedules posts for all linked accounts.
   ```bash
   python main.py auto-pilot
   ```

5. **Anti-Spam Features**:
   View information about the built-in anti-spam measures.
   ```bash
   python main.py anti-spam
   ```

## Building for Windows

If you want to package the entire project into a single standalone executable `.exe` file for Windows:

```bash
# Run the included build script
build.bat
```

The resulting `NEXUS-100.exe` will be located in the `dist/` directory.

## Demo

### Screenshot

![CLI Interface Placeholder](https://via.placeholder.com/800x400.png?text=CLI+Interface+Screenshot)

### Video Walkthrough

[![Video Walkthrough Placeholder](https://via.placeholder.com/800x400.png?text=Click+to+watch+Video+Walkthrough)](https://www.youtube.com/watch?v=dQw4w9WgXcQ)
