"""
Chạy script này MỘT LẦN để login Spotify và lưu token vào .cache
Sau đó server sẽ tự dùng token đã lưu, không cần login lại.

Chạy: python auth_spotify.py
"""
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI", "http://localhost:8888/callback"),
    scope="playlist-modify-public playlist-modify-private",
    cache_path=".cache",
    open_browser=True,
))

user = sp.current_user()
print(f"Login thành công! Xin chào {user['display_name']} ({user['id']})")
print("Token đã lưu vào .cache — giờ có thể chạy server bình thường.")
