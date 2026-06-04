"""
Vibe Analyzer - Multimodal AI for mood and vibe detection
Supports both image and text input for analyzing vibes and emotions
"""

import base64
from io import BytesIO
import os
from typing import Optional, Dict, Any
import openai
from dotenv import load_dotenv
from PIL import Image

load_dotenv()


class VibeAnalyzer:
    """
    Analyzes images and text to extract vibe/mood information
    Uses OpenAI's multimodal vision API for image analysis
    """

    def __init__(self):
        """Initialize the OpenAI client"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.client = openai.OpenAI(api_key=api_key, timeout=30.0)

    def encode_image(self, image_path: str) -> str:
        """
        Encode image to base64 for API transmission
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Base64 encoded image string
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def analyze_image(self, image_path: str) -> Dict[str, Any]:
        """
        Analyze an image to detect vibe and mood using vision AI
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Dictionary containing vibe analysis with genres, mood, energy level, etc.
        """
        # Encode the image
        base64_image = self.encode_image(image_path)

        # Determine image type
        image_ext = image_path.lower().split(".")[-1]
        media_type_map = {
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "png": "image/png",
            "gif": "image/gif",
            "webp": "image/webp",
        }
        media_type = media_type_map.get(image_ext, "image/jpeg")

        # Call OpenAI Vision API
        response = self.client.chat.completions.create(
            model="gpt-4o",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{media_type};base64,{base64_image}",
                            },
                        },
                        {
                            "type": "text",
                            "text": """Analyze this image and extract the vibe/mood/atmosphere it conveys.
                            
Return a JSON response (and ONLY JSON, no other text) with:
{
    "vibe": "main vibe/mood in 2-3 words (e.g., 'cozy morning', 'energetic night')",
    "emotions": ["list", "of", "emotions"],
    "genres": ["music", "genres", "that", "match"],
    "energy_level": "high/medium/low",
    "tempo": "fast/moderate/slow",
    "atmosphere": "brief description",
    "keywords": ["tag1", "tag2", "tag3"]
}""",
                        },
                    ],
                }
            ],
        )

        # Parse response robustly (strip code fences, handle parse errors)
        response_text = response.choices[0].message.content
        import json
        import re

        raw = response_text if isinstance(response_text, str) else str(response_text)

        # Try to extract JSON inside ``` or ```json fences first
        m = re.search(r"```(?:json)?\s*(.*?)\s*```", raw, re.DOTALL)
        if m:
            json_text = m.group(1)
        else:
            # Fallback: remove any backtick fences and use the whole response
            json_text = raw.replace("```json", "").replace("```", "").strip()

        raw = response.choices[0].message.content
        print(f"RAW OPENAI RESPONSE: {repr(raw)}")

        raw = response.choices[0].message.content
        print(f"RAW OPENAI RESPONSE: {repr(raw)}")

        try:
            vibe_data = json.loads(json_text)
            return vibe_data
        except Exception:
            print("Failed to parse JSON from model response. Raw response:")
            print(raw)
            # Return a safe default structure instead of crashing
            default_vibe = {
                "vibe": "unknown",
                "emotions": [],
                "genres": [],
                "energy_level": "medium",
                "tempo": "moderate",
                "atmosphere": "",
                "keywords": [],
            }
            return default_vibe

    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Analyze text description to detect vibe and mood
        Uses zero-shot classification approach
        
        Args:
            text: Text description of mood/vibe
            
        Returns:
            Dictionary containing vibe analysis
        """
        response = self.client.chat.completions.create(
            model="gpt-4o",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": f"""Analyze this mood/vibe description and extract music preferences.
                    
Description: "{text}"

Return a JSON response (and ONLY JSON, no other text) with:
{{
    "vibe": "main vibe in 2-3 words",
    "emotions": ["list", "of", "emotions"],
    "genres": ["music", "genres", "that", "match"],
    "energy_level": "high/medium/low",
    "tempo": "fast/moderate/slow",
    "atmosphere": "brief description",
    "keywords": ["tag1", "tag2", "tag3"]
}}""",
                }
            ],
        )

        response_text = response.choices[0].message.content
        import json
        import re

        raw = response_text if isinstance(response_text, str) else str(response_text)

        # Try to extract JSON inside ``` or ```json fences first
        m = re.search(r"```(?:json)?\s*(.*?)\s*```", raw, re.DOTALL)
        if m:
            json_text = m.group(1)
        else:
            # Fallback: remove any backtick fences and use the whole response
            json_text = raw.replace("```json", "").replace("```", "").strip()

        raw = response.choices[0].message.content
        print(f"RAW OPENAI RESPONSE: {repr(raw)}")

        try:
            vibe_data = json.loads(json_text)
            return vibe_data
        except Exception:
            print("Failed to parse JSON from model response. Raw response:")
            print(raw)
            # Return a safe default structure instead of crashing
            default_vibe = {
                "vibe": "unknown",
                "emotions": [],
                "genres": [],
                "energy_level": "medium",
                "tempo": "moderate",
                "atmosphere": "",
                "keywords": [],
            }
            return default_vibe

    def refine_vibe_analysis(self, vibe_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Refine and enhance vibe analysis with additional context
        
        Args:
            vibe_data: Initial vibe analysis
            
        Returns:
            Enhanced vibe data with additional playlist guidance
        """
        # Extract key information
        genres = vibe_data.get("genres", [])
        energy = vibe_data.get("energy_level", "medium").lower()
        tempo = vibe_data.get("tempo", "moderate").lower()
        keywords = vibe_data.get("keywords", [])

        # Map energy levels to Spotify audio features
        energy_map = {"high": 0.7, "medium": 0.5, "low": 0.3}
        tempo_map = {"fast": 130, "moderate": 90, "slow": 60}

        vibe_data["music_features"] = {
            "target_energy": energy_map.get(energy, 0.5),
            "target_tempo": tempo_map.get(tempo, 90),
            "genres": genres,
            "search_keywords": " ".join(keywords),
        }

        return vibe_data
