# iPhone Shortcut: Take Photo → Vibe-to-Playlist

This guide shows how to create an iPhone Shortcut that takes a photo, sends it to your Vibe-to-Playlist FastAPI backend (`/analyze`), and returns a Spotify playlist notification with an "Open in Spotify" button.

Prerequisites
- Your FastAPI server must be reachable from your iPhone (same LAN or public URL). Example: `http://192.168.1.50:8000` or a public HTTPS endpoint.
- The API endpoint: `POST /analyze` accepts a multipart form upload with field name `file` and returns JSON containing `playlist_result.playlist.url` and `playlist_result.playlist.name`.

Steps to create the Shortcut

1. Open the Shortcuts app and tap **+** to create a new shortcut.
2. Add action **Take Photo** (set to `Back` or `Front` as desired). Choose `Show When Run` if you want to confirm.
3. Add action **Get Latest Photos** (optional) if you prefer to pick instead of taking a new photo.
4. Add action **Get Contents of URL**:
   - URL: `http://<YOUR_SERVER_IP_OR_DOMAIN>:8000/analyze` (replace with your server)
   - Method: `POST`
   - Request Body: `Form` (tap `Add new field`)
     - Name: `file`
     - Type: `File` (choose **Provided Input** or the `Photo` from the previous step)
   - Headers: Add `Accept: application/json`
   - Leave `Show While Running` on (useful for debugging)
5. Add action **Get Dictionary from Input** (this parses the JSON response).
6. Add action **Get Dictionary Value**:
   - Get `playlist_result` from the dictionary.
7. Add action **Get Dictionary Value** (again):
   - From `playlist_result`, get `playlist`.
8. Add action **Get Dictionary Value**:
   - From `playlist`, get `url` (this is the Spotify web URL) and save to a variable named `PlaylistURL`.
9. Add another **Get Dictionary Value**:
   - From `playlist`, get `name` and save to `PlaylistName`.
10. (Optional) Convert web URL to a Spotify deep link:
    - Add **Text** action with the following transformation logic using `Get Component of URL` or simple text manipulation:
      - If `PlaylistURL` looks like `https://open.spotify.com/playlist/<PLAYLIST_ID>`, extract `<PLAYLIST_ID>` and build `spotify:playlist:<PLAYLIST_ID>`.
    - You can use **Match Text** with a regular expression like `playlist/([A-Za-z0-9]+)` to extract the ID, then build the `spotify:playlist:` URI.
11. Add action **Show Notification**:
    - Title: `Playlist Ready`
    - Subtitle: `PlaylistName` (insert the variable)
    - Body: `Tap to open in Spotify` (or include `PlaylistURL`)
    - Enable `Play Sound` if desired.
12. Add action **Open URLs** (or **Open App** if you have the `spotify:playlist:` URI):
    - If you built a `spotify:playlist:` URI, use that as the URL to open. Otherwise, use `PlaylistURL` (this will open in the Spotify app if the OS resolves the URL to the app).

Tips & Troubleshooting
- If your server is on your local machine, make sure your iPhone is on the same Wi-Fi network and you use the machine's LAN IP, not `localhost`.
- For HTTPS and public access, consider using a tunnel service (ngrok, Cloudflare Tunnel) and use that URL in the Shortcut.
- If the Shortcut fails to parse JSON, temporarily enable `Show While Running` on the `Get Contents of URL` action and inspect the raw response.
- If the Spotify deep link does not open the app, verify the `spotify:playlist:` scheme is correct and that Spotify is installed.

Result
Take a photo, wait up to ~15 seconds (analysis + playlist creation), receive a notification with the playlist name, and tap to open the playlist in Spotify.
