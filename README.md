# 🎵 Vibe-to-Playlist Multimodal AI

Transform your mood into music! This project demonstrates cutting-edge AI concepts by generating iTunes playlists based on image or text input.

##  What You Can Do

- **Upload a Photo** (breakfast scene, café corner, sunset) → AI analyzes the vibe
- **Write a Description** of your mood → AI understands your feelings
- **Get a Custom Playlist** that matches your vibe perfectly

## Technical Concepts

### Multimodal AI
The application processes both **image and text** inputs using OpenAI's Vision API:
- Images are encoded as base64 and sent to the vision model
- Text is processed with natural language understanding
- Both inputs analyzed for emotional and atmospheric context

### Prompt Engineering
Strategic prompt design extracts structured vibe data:
- Return JSON format for reliable parsing
- Specific instructions for emotion, energy, and genre detection
- Guided classification without explicit training

### Zero-Shot Classification
Classify vibes into music genres without training data:
- Vibe description → Genres (e.g., "cozy" → indie, acoustic, lo-fi)
- Energy levels → Audio feature targets (high energy → 0.7+)
- Tempo mapping → BPM targets for playlist matching


##  Getting Started

### Prerequisites
- Python 3.8+
- OpenAI API key ([get here](https://platform.openai.com/api-keys))

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd vibe-playlist-AI
   ```

2. **Create a Python virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```

5. **Edit `.env` with your credentials:**
   ```
   OPENAI_API_KEY=your_openai_api_key
 
   ```

### Running the App

```bash
streamlit run app.py
```

The app opens at `http://localhost:8000/docs`

##  Project Structure

```
vibe-playlist-AI/
├── app.py                         # Streamlit UI & main application
├── vibe_analyzer.py               # Multimodal vibe analysis (image & text)
├── iTunes_playlist_generator.py   # iTunes API integration & playlist creation
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
├── .gitignore                     # Git ignore rules
└── README.md                      # This file
```

##  Module Overview

### `vibe_analyzer.py`
**Multimodal AI for mood detection**

- `VibeAnalyzer.analyze_image(image_path)` - Vision API analysis
- `VibeAnalyzer.analyze_text(text)` - Text sentiment analysis
- `VibeAnalyzer.refine_vibe_analysis(vibe_data)` - Enhance with itunes features

Returns: Genre recommendations, energy levels, tempo, emotional tags

### `iTunes_playlist_generator.py`
**iTunes playlist creation**

- `iTunesPlaylistGenerator.search_tracks()` - Find matching tracks
- `iTunesPlaylistGenerator.get_track_features()` - Retrieve audio features
- `iTunesPlaylistGenerator.rank_tracks_by_vibe()` - ML-based track ranking
- `iTunesPlaylistGenerator.create_playlist()` - Create iTunes playlist

**Algorithm**: Matches target energy and tempo to track features, ranks by score

### `app.py`
**Streamlit web interface**

- Tab 1: Image upload with vibe analysis
- Tab 2: Text input for mood description
- Real-time playlist generation
- Track listing with feature visualization

## Application Flow

```
User Input (Image/Text)
    ↓
Vibe Analyzer (AI)
    ├─ Detect emotions
    ├─ Classify genres
    ├─ Determine energy level
    └─ Extract keywords
    ↓
iTunes Playlist Generator
    ├─ Search tracks by genre & keywords
    ├─ Fetch audio features
    ├─ Rank by energy/tempo match
    └─ Create iTunes playlist
    ↓
Display Results
```

## Key Features

**Multimodal Input** - Process images and text  
**Zero-Shot Learning** - No training required  
**Smart Ranking** - Match playlists to vibe using audio features  
**Itunes Integration** - Direct playlist creation and sharing  
**Real-time UI** - Streamlit for instant feedback  
**Feature Visualization** - Show energy, tempo, and matching scores  

##  Learning Outcomes

By studying this project, you'll understand:

1. **Multimodal AI** - Processing diverse input types
2. **Vision APIs** - Image understanding and analysis
3. **Prompt Engineering** - Designing effective AI prompts
4. **Zero-Shot Classification** - Classifying without training data
5. **API Integration** - Authentication and data retrieval
6. **Audio Features** - Music metadata and analysis
7. **Ranking Algorithms** - Scoring and sorting strategies
8. **UI/UX** - Building user-friendly AI applications

##  Troubleshooting

**"OPENAI_API_KEY not found"**
- Make sure `.env` file exists in the project root
- Verify the API key is correct

**"Preview URL not available"**
- Some tracks don't have preview URLs; this is normal
- Playlists still create successfully


##  API Documentation

- [OpenAI Vision API](https://platform.openai.com/docs/guides/vision)
- [Streamlit Documentation](https://docs.streamlit.io/)

##  Customization

### Adjust Playlist Length
In `app.py`, change `num_tracks`:
```python
playlist_result = generator.generate_playlist_from_vibe(
    st.session_state.vibe_data, num_tracks=50  # Default: 20
)
```

### Modify Energy/Tempo Mapping
In `vibe_analyzer.py`, adjust the feature maps:
```python
energy_map = {"high": 0.8, "medium": 0.5, "low": 0.2}
tempo_map = {"fast": 150, "moderate": 90, "slow": 50}
```

### Add More Genres
Update the prompt in `analyze_image()` and `analyze_text()` to include more genres:
```python
"genres": ["pop", "indie", "electronic", "jazz", "metal", ...]
```

## License

This project is open source and available for educational purposes.


---

**Happy vibing! 
