# 🎵 Vibe-to-Playlist — Agentic Multimodal AI

**Snap a photo. Get a soundtrack. No typing. No searching. Just vibes.**

Vibe-to-Playlist is an agentic AI system that turns any photo into a personalized music playlist — instantly. Point your iPhone camera at a rainy café window, a sunset rooftop, or your messy desk at 2am, and the AI reads the mood, finds matching tracks, and delivers your playlist in seconds.

No app to download. No login. No subscription. Just one tap on an iPhone Shortcut.

---

## The Problem

You know that feeling — you're in a certain mood, and you want music that *matches*. But when you open a music app, you're staring at a search bar with no idea what to type. "Chill"? "Sad but not too sad"? "Coffee shop on a rainy Tuesday"?

**Mood is visual, not verbal.** You can *see* a vibe but you can't always describe it in words. That's the gap this project fills.

---

## How It Works

```
Snap a photo on iPhone
        ↓
GPT-4o Vision reads the mood, atmosphere, and energy
        ↓
iTunes Search finds tracks that match the vibe
        ↓
Notification appears with your playlist — tap to listen
```

The entire flow is **agentic** — once the user takes a photo, the system executes every step autonomously without additional input. No buttons to press, no options to choose. One action triggers a chain of AI decisions.

---

## Architecture

```
┌─────────────────┐     ┌──────────────────────┐     ┌─────────────────┐
│  iPhone Shortcut │────▶│   FastAPI Backend     │────▶│  iTunes Search  │
│  (Camera + Send) │     │   (Render Cloud)      │     │  API (Free)     │
└─────────────────┘     │                        │     └─────────────────┘
                        │  ┌──────────────────┐  │
                        │  │ GPT-4o Vision    │  │
                        │  │ (Vibe Analysis)  │  │
                        │  └──────────────────┘  │
                        └──────────────────────┘
```

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Input** | iPhone Shortcuts | Camera capture + API call in one tap |
| **Backend** | FastAPI on Render | Orchestrates the entire pipeline |
| **Vision AI** | OpenAI GPT-4o | Analyzes image mood, energy, atmosphere |
| **Music** | iTunes Search API | Finds tracks matching the detected vibe |
| **Web Demo** | Streamlit | Alternative interface for desktop demo |

---

## Live Demo

**API Docs**: [https://vibe-playlist-ai.onrender.com/docs](https://vibe-playlist-ai.onrender.com/docs)

> Free tier — first request may take ~30s to wake up the server.

---

## Quick Start

### Option 1: iPhone Shortcut (Recommended)

The native experience. One tap from photo to playlist.

**Setup (2 minutes):**

1. Open the **Shortcuts** app on your iPhone
2. Create a new Shortcut named **"Vibe to Music"**
3. Add these actions in order:

| Step | Action | Configuration |
|------|--------|--------------|
| 1 | **Take Photo** | Back camera |
| 2 | **Base64 Encode** | Input: Photo |
| 3 | **Get Contents of URL** | URL: `https://vibe-playlist-ai.onrender.com/analyze-base64` · Method: POST · Body: JSON · Key: `image_base64` · Value: Base64 Encoded |
| 4 | **Get Dictionary from** | Input: Contents of URL |
| 5 | **Show Notification** | Body: Dictionary |

4. Tap ▶️ to run — snap a photo and wait for your playlist!

> **Tip**: Open the API URL in Safari first to wake up the server before running the Shortcut.

### Option 2: Web Interface (Streamlit)

For desktop demo or screen sharing in interviews.

```bash
# Clone the repo
git clone https://github.com/nganha05022003-cpu/vibe-playlist-AI.git
cd vibe-playlist-AI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Run
streamlit run app.py
```

### Option 3: API Direct

For developers who want to integrate.

```bash
# Image analysis (base64)
curl -X POST https://vibe-playlist-ai.onrender.com/analyze-base64 \
  -H "Content-Type: application/json" \
  -d '{"image_base64": "<your-base64-string>"}'

# Text analysis
curl -X POST https://vibe-playlist-ai.onrender.com/analyze-text \
  -H "Content-Type: application/json" \
  -d '{"mood_text": "rainy afternoon in a cozy coffee shop"}'
```

---

## Example Response

```json
{
  "ok": true,
  "vibe_data": {
    "vibe": "cozy workspace",
    "emotions": ["content", "relaxed", "calm"],
    "genres": ["acoustic", "lo-fi", "indie"],
    "energy_level": "medium",
    "tempo": "moderate",
    "atmosphere": "A calm and cozy workspace with warm lighting",
    "keywords": ["workspace", "relaxed", "comfort", "calm"]
  },
  "playlist_result": {
    "tracks": [
      {
        "trackName": "Intro",
        "artistName": "The xx",
        "previewUrl": "https://audio-ssl.itunes.apple.com/...",
        "trackViewUrl": "https://music.apple.com/...",
        "artworkUrl100": "https://is1-ssl.mzstatic.com/..."
      }
    ],
    "total_tracks": 10
  }
}
```

---

## Project Structure

```
vibe-playlist-AI/
├── main.py                        # FastAPI backend — the brain of the system
│                                  # Endpoints: /analyze, /analyze-base64, /analyze-text
│
├── vibe_analyzer.py               # GPT-4o Vision integration
│                                  # Extracts mood, emotions, genres, energy from images
│
├── iTunes_playlist_generator.py   # iTunes Search API integration
│                                  # Converts vibe keywords → matching tracks
│
├── app.py                         # Streamlit web interface (desktop demo)
│
├── SHORTCUT_SETUP.md              # iPhone Shortcut setup instructions
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
├── .gitignore                     # Keeps API keys out of GitHub
├── Procfile                       # Render deployment config
└── README.md                      # You are here
```

---

## AI/ML Concepts Demonstrated

This project is a practical demonstration of several AI concepts relevant to product development:

**Multimodal AI** — The system processes visual input (photos) using GPT-4o Vision, extracting structured data (mood, energy, genres) from unstructured visual information. This is the same technology behind Google Lens, Snapchat filters, and autonomous vehicle perception.

**Prompt Engineering** — The system prompt is carefully designed to return structured JSON with specific fields (emotions, genres, energy_level, tempo). Small changes in prompt wording significantly affect output quality — a practical lesson in LLM behavior.

**Agentic Architecture** — Unlike traditional request-response apps, this system chains multiple AI decisions autonomously: image analysis → mood classification → genre mapping → track search → result ranking. The user triggers one action; the agent handles everything else.

**Zero-Shot Classification** — The AI classifies images into music genres without any training data or fine-tuning. It leverages GPT-4o's pre-trained understanding of both visual aesthetics and music culture to make these connections.

**API Design & Integration** — The backend integrates three external services (OpenAI, iTunes, iPhone Shortcuts) through a unified FastAPI interface, demonstrating practical API orchestration.

---

## Product Decisions & Trade-offs

Decisions made during development, documented for transparency:

| Decision | Options Considered | Chosen | Why |
|----------|-------------------|--------|-----|
| Music platform | Spotify API vs iTunes Search API | iTunes | Spotify requires Premium for all Developer Mode apps since Feb 2026. iTunes is free, no auth needed, includes 30-second previews |
| Input method | Web upload vs iPhone Shortcut | Both (Shortcut primary) | Shortcut eliminates browser friction — photo to playlist in one tap |
| Image transfer | Multipart file upload vs Base64 JSON | Base64 | iPhone Shortcuts doesn't support multipart/form-data natively |
| Hosting | Railway vs Render | Render | Free tier without credit card requirement |
| Backend framework | Streamlit vs FastAPI | FastAPI (+ Streamlit for demo) | FastAPI can serve both iPhone Shortcut and web interface; Streamlit only serves web |

---

## The Story Behind This Project

I built this as a PM exploring AI product development hands-on. The journey included:

- **Starting with Spotify** → discovering their API now requires Premium for all developer apps (Feb 2026 policy change)
- **Pivoting to iTunes** → a product decision driven by user accessibility, not technical limitation
- **Building web-first** → realizing browser-based upload creates too much friction
- **Redesigning as agentic** → iPhone Shortcut eliminates every unnecessary step between "I see a vibe" and "I hear matching music"

Each pivot taught me something about building AI products that I couldn't have learned from reading alone.

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key with GPT-4o access |

---

## Troubleshooting

**"The request timed out" on iPhone Shortcut**
Render free tier sleeps after 15 min of inactivity. Open `https://vibe-playlist-ai.onrender.com/docs` in Safari first to wake the server, then run the Shortcut.

**"OPENAI_API_KEY not found"**
Create a `.env` file in the project root with your key. See `.env.example` for the template.

**"Preview URL not available" for some tracks**
Normal behavior — not all iTunes tracks have 30-second previews. The playlist still generates successfully.

---

## Built With

- **Python 3.11** — Core language
- **FastAPI** — Backend API framework
- **OpenAI GPT-4o** — Multimodal vision AI
- **iTunes Search API** — Music catalog (free, no auth)
- **Streamlit** — Web demo interface
- **Render** — Cloud hosting (free tier)
- **iPhone Shortcuts** — Native mobile experience

---

## Author

**Nguyen Tran Ngan Ha** — Aspiring AI Product Manager

Built as a portfolio project demonstrating AI product thinking, technical literacy, and the ability to ship end-to-end.

[LinkedIn](https://www.linkedin.com/in/hanguyen0502/) · [GitHub](https://github.com/nganha05022003-cpu)

---

*Happy vibing! 🎵*
