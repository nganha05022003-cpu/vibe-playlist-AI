"""
Playlist Generator - Uses iTunes Search API (no API key required)
"""

import os
from typing import Dict, List, Any, Optional
import requests
from dotenv import load_dotenv

load_dotenv()


class ItunesPlaylistGenerator:

    def search_tracks(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        tracks = []
        try:
            response = requests.get(
                "https://itunes.apple.com/search",
                params={"term": query, "media": "music", "entity": "song", "limit": limit},
                timeout=10,
            )
            response.raise_for_status()
            for item in response.json().get("results", []):
                tracks.append({
                    "name": item.get("trackName"),
                    "artist": item.get("artistName"),
                    "album": item.get("collectionName"),
                    "artwork_url": item.get("artworkUrl100"),
                    "preview_url": item.get("previewUrl"),
                    "track_url": item.get("trackViewUrl"),
                })
        except Exception as e:
            print(f"Error searching iTunes: {e}")
        return tracks

    def generate_playlist_from_vibe(
        self,
        vibe_data: Dict[str, Any],
        playlist_name: Optional[str] = None,
        num_tracks: int = 10,
    ) -> Dict[str, Any]:
        vibe = vibe_data.get("vibe", "Untitled Vibe")
        genres = vibe_data.get("genres", [])
        keywords = vibe_data.get("keywords", [])

        primary_query = " ".join(([vibe] + genres)[:3])
        tracks = self.search_tracks(query=primary_query, limit=num_tracks)

        # fallback: search by genres only if not enough results
        if len(tracks) < num_tracks and genres:
            fallback_query = " ".join(genres[:2])
            extra = self.search_tracks(query=fallback_query, limit=num_tracks - len(tracks))
            seen = {t["track_url"] for t in tracks}
            tracks += [t for t in extra if t["track_url"] not in seen]

        return {
            "vibe": vibe,
            "playlist_name": playlist_name or f"Vibe: {vibe}",
            "tracks": tracks,
            "total_tracks": len(tracks),
        }
