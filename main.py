"""
FastAPI backend for Agentic Vibe-to-Playlist

Endpoints:
- POST /analyze      : multipart form upload with field `file` (image)
- POST /analyze-text : JSON body with `mood_text`

Both endpoints call `VibeAnalyzer` and `SpotifyPlaylistGenerator` and return
vibe analysis + Spotify playlist info in JSON.

Run with: `uvicorn main:app --host 0.0.0.0 --port 8000`
"""

import os
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional
import logging

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from vibe_analyzer import VibeAnalyzer
from itunes_playlist_generator import ItunesPlaylistGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Vibe-to-Playlist API")

# Allow CORS for all origins (change in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event() -> None:
    app.state.analyzer = None
    app.state.generator = None

    try:
        app.state.analyzer = VibeAnalyzer()
        logger.info("VibeAnalyzer initialized successfully")
    except Exception as exc:
        logger.error("Error initializing VibeAnalyzer: %s", exc)

    try:
        app.state.generator = ItunesPlaylistGenerator()
        logger.info("ItunesPlaylistGenerator initialized successfully")
    except Exception as exc:
        logger.error("Error initializing ItunesPlaylistGenerator: %s", exc)


def get_analyzer() -> VibeAnalyzer:
    analyzer = getattr(app.state, "analyzer", None)
    if analyzer is None:
        raise HTTPException(status_code=500, detail="VibeAnalyzer not initialized on server")
    return analyzer


def get_generator() -> ItunesPlaylistGenerator:
    generator = getattr(app.state, "generator", None)
    if generator is None:
        raise HTTPException(status_code=500, detail="ItunesPlaylistGenerator not initialized on server")
    return generator


class MoodText(BaseModel):
    mood_text: str


@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)) -> Dict[str, Any]:
    """Accept an uploaded image, analyze vibe, and create a Spotify playlist."""
    suffix = Path(file.filename).suffix if file.filename else ".jpg"
    tmp_path: Optional[str] = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp_path = tmp.name
            tmp.write(await file.read())

        analyzer = get_analyzer()
        vibe_data = analyzer.analyze_image(tmp_path)
        vibe_data = analyzer.refine_vibe_analysis(vibe_data)

        generator = get_generator()
        playlist_result = generator.generate_playlist_from_vibe(vibe_data, num_tracks=20)

        return {
            "ok": True,
            "vibe_data": vibe_data,
            "playlist_result": playlist_result,
        }

    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to analyze image")
        raise HTTPException(status_code=500, detail=str(exc))
    finally:
        if tmp_path:
            try:
                os.unlink(tmp_path)
            except OSError:
                logger.warning("Failed to delete temporary file: %s", tmp_path)


@app.post("/analyze-text")
async def analyze_text(mood: MoodText) -> Dict[str, Any]:
    """Accept a JSON mood_text, analyze vibe, and create a Spotify playlist."""
    try:
        analyzer = get_analyzer()
        vibe_data = analyzer.analyze_text(mood.mood_text)
        vibe_data = analyzer.refine_vibe_analysis(vibe_data)

        generator = get_generator()
        playlist_result = generator.generate_playlist_from_vibe(vibe_data, num_tracks=20)

        return {
            "ok": True,
            "vibe_data": vibe_data,
            "playlist_result": playlist_result,
        }

    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to analyze text")
        raise HTTPException(status_code=500, detail=str(exc))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
