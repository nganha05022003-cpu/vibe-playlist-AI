"""
Vibe-to-Playlist Multimodal AI Application
A Streamlit app that generates Spotify playlists based on image or text input
"""

import os
import tempfile
from pathlib import Path
import streamlit as st
from PIL import Image
from vibe_analyzer import VibeAnalyzer
from spotify_playlist_generator import SpotifyPlaylistGenerator

# Page configuration
st.set_page_config(
    page_title="Vibe to Playlist",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 1.2em;
    }
    .vibe-card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #1A1625;
        border: 2px solid #FF006E;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if "vibe_data" not in st.session_state:
        st.session_state.vibe_data = None
    if "playlist_result" not in st.session_state:
        st.session_state.playlist_result = None
    if "image_uploaded" not in st.session_state:
        st.session_state.image_uploaded = False


@st.cache_resource
def get_vibe_analyzer():
    """Get cached VibeAnalyzer instance - reused across button clicks"""
    return VibeAnalyzer()


@st.cache_resource
def get_spotify_generator():
    """Get cached SpotifyPlaylistGenerator instance - reused across button clicks"""
    return SpotifyPlaylistGenerator()


def display_vibe_analysis(vibe_data):
    """Display the vibe analysis results"""
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🎭 Vibe Analysis")
        st.markdown(f"**Vibe:** {vibe_data.get('vibe', 'N/A')}")
        st.markdown(f"**Atmosphere:** {vibe_data.get('atmosphere', 'N/A')}")
        st.markdown(f"**Energy Level:** {vibe_data.get('energy_level', 'N/A').upper()}")
        st.markdown(f"**Tempo:** {vibe_data.get('tempo', 'N/A').upper()}")

    with col2:
        st.markdown("### 🎵 Music Profile")
        
        emotions = vibe_data.get("emotions", [])
        if emotions:
            st.markdown(f"**Emotions:** {', '.join(emotions)}")

        genres = vibe_data.get("genres", [])
        if genres:
            st.markdown(f"**Genres:** {', '.join(genres)}")

        keywords = vibe_data.get("keywords", [])
        if keywords:
            st.markdown(f"**Keywords:** {', '.join(keywords)}")


def display_playlist_result(playlist_result):
    """Display the generated playlist"""
    playlist = playlist_result.get("playlist", {})

    st.success("✅ Playlist Created Successfully!")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(f"### 🎼 {playlist.get('name', 'Untitled Playlist')}")
        st.markdown(f"**Tracks Added:** {playlist.get('tracks_added', 0)}")

        if playlist.get("url"):
            st.markdown(
                f"[🎧 Open in Spotify]({playlist['url']})",
                unsafe_allow_html=True,
            )

    with col2:
        st.info(f"Total Tracks: {playlist_result.get('total_tracks', 0)}")

    # Display track list
    st.markdown("### 📝 Playlist Tracks")
    tracks = playlist_result.get("tracks", [])

    for idx, track in enumerate(tracks, 1):
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 1])

            with col1:
                artists = ", ".join(track.get("artists", ["Unknown"]))
                st.markdown(f"**{idx}. {track.get('name', 'Unknown')}**")
                st.markdown(f"*{artists}*", unsafe_allow_html=True)

            with col2:
                if "features" in track:
                    features = track["features"]
                    energy = features.get("energy", 0)
                    tempo = features.get("tempo", 0)
                    st.caption(f"🔋 {energy:.0%} | ♪ {tempo:.0f} BPM")

            with col3:
                score = track.get("score", 0)
                st.caption(f"Match: {score:.0%}")

            st.divider()


def main():
    """Main application function"""
    initialize_session_state()

    # Header
    st.markdown("# 🎵 Vibe to Playlist")
    st.markdown(
        "Transform your mood into music. Upload a photo or describe your vibe, and let AI generate a custom Spotify playlist."
    )

    st.divider()

    # Input method selection
    tab1, tab2 = st.tabs(["📸 Image Input", "📝 Text Input"])

    with tab1:
        st.markdown("### Upload a Photo")
        st.markdown("Upload an image (breakfast scene, café corner, sunset, etc.) and the AI will analyze its vibe.")

        uploaded_file = st.file_uploader(
            "Choose an image...",
            type=["jpg", "jpeg", "png", "gif", "webp"],
            key="image_uploader",
        )

        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file)
            col1, col2 = st.columns([1, 1])

            with col1:
                st.image(image, caption="Your Image", use_container_width=True)

            with col2:
                if st.button("🔍 Analyze Image Vibe", key="analyze_image_btn"):
                    with st.spinner("Analyzing image vibe..."):
                        try:
                            # Save uploaded file temporarily
                            with tempfile.NamedTemporaryFile(
                                delete=False,
                                suffix=f".{uploaded_file.name.split('.')[-1]}",
                            ) as tmp_file:
                                tmp_file.write(uploaded_file.getbuffer())
                                tmp_path = tmp_file.name

                            # Analyze image
                            analyzer = get_vibe_analyzer()
                            vibe_data = analyzer.analyze_image(tmp_path)
                            vibe_data = analyzer.refine_vibe_analysis(vibe_data)
                            st.session_state.vibe_data = vibe_data

                            # Cleanup
                            os.unlink(tmp_path)

                            st.success("Image analysis complete!")
                            st.rerun()

                        except Exception as e:
                            st.error(f"Error analyzing image: {str(e)}")

    with tab2:
        st.markdown("### Describe Your Vibe")
        st.markdown("Tell the AI how you're feeling or what mood you want to create.")

        mood_text = st.text_area(
            "Your mood or vibe description:",
            placeholder="e.g., 'Cozy coffee shop morning', 'High energy workout', 'Chill sunset evening'",
            height=150,
        )

        if st.button("🎯 Analyze Text Vibe", key="analyze_text_btn"):
            if mood_text.strip():
                with st.spinner("Analyzing your vibe..."):
                    try:
                        analyzer = get_vibe_analyzer()
                        vibe_data = analyzer.analyze_text(mood_text)
                        vibe_data = analyzer.refine_vibe_analysis(vibe_data)
                        st.session_state.vibe_data = vibe_data

                        st.success("Vibe analysis complete!")
                        st.rerun()

                    except Exception as e:
                        st.error(f"Error analyzing text: {str(e)}")
            else:
                st.warning("Please describe your vibe first!")

    st.divider()

    # Display vibe analysis results
    if st.session_state.vibe_data:
        display_vibe_analysis(st.session_state.vibe_data)

        st.divider()

        # Generate playlist button
        if st.button("🎼 Generate Spotify Playlist", key="generate_playlist_btn"):
            with st.spinner("Creating your playlist..."):
                try:
                    generator = get_spotify_generator()
                    playlist_result = generator.generate_playlist_from_vibe(
                        st.session_state.vibe_data, num_tracks=20
                    )
                    st.session_state.playlist_result = playlist_result
                    st.rerun()

                except Exception as e:
                    st.error(
                        f"Error generating playlist: {str(e)}\n\nMake sure your Spotify credentials are set in .env"
                    )

    # Display generated playlist
    if st.session_state.playlist_result:
        display_playlist_result(st.session_state.playlist_result)

        st.divider()

        # Reset button
        if st.button("🔄 Start Over", key="reset_btn"):
            st.session_state.vibe_data = None
            st.session_state.playlist_result = None
            st.rerun()

    # Sidebar information
    with st.sidebar:
        st.markdown("### 📚 How It Works")
        st.markdown(
            """
        1. **Upload Image or Text** - Share your vibe
        2. **AI Analysis** - Multimodal AI analyzes the mood
        3. **Music Matching** - Identifies genres and audio features
        4. **Spotify Playlist** - Generates a custom playlist
        
        **Technologies:**
        - 🤖 OpenAI Vision for image analysis
        - 📊 Zero-shot classification for mood detection
        - 🎵 Spotify Web API for playlist creation
        - 🔊 Audio feature matching algorithm
        """
        )

        st.divider()

        st.markdown("### ⚙️ Configuration")
        if not os.getenv("OPENAI_API_KEY"):
            st.error("⚠️ OPENAI_API_KEY not set")
        else:
            st.success("✓ OpenAI API connected")

        if not os.getenv("SPOTIFY_CLIENT_ID"):
            st.error("⚠️ Spotify credentials not set")
        else:
            st.success("✓ Spotify connected")

        st.divider()

        st.markdown(
            """
        **Setup Instructions:**
        1. Get API keys from [OpenAI](https://platform.openai.com/api-keys)
        2. Create a Spotify app at [developer.spotify.com](https://developer.spotify.com)
        3. Create a `.env` file with your credentials
        4. Run: `streamlit run app.py`
        """
        )


if __name__ == "__main__":
    main()
