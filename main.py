import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from telethon import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest

# --- НАСТРОЙКИ ---

# Telegram
API_ID =             # твой api_id
API_HASH = ""
SESSION_NAME = "spotify_status"

# Spotify
SPOTIFY_CLIENT_ID = ""
SPOTIFY_CLIENT_SECRET = ""
SPOTIFY_REDIRECT_URI = "http://127.0.0.1:8888/callback"

# --- ИНИЦИАЛИЗАЦИЯ ---
tg = TelegramClient(SESSION_NAME, API_ID, API_HASH)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-read-currently-playing"
))

# --- ЛОГИКА ---
async def update_status():
    last_status = ""
    while True:
        try:
            track = sp.current_user_playing_track()
            if track and track['is_playing']:
                artist = track['item']['artists'][0]['name']
                title = track['item']['name']
                status = f"🎧 {artist} – {title}"
            else:
                status = "🙊 Музыка не играет"

            # Обновляем статус только если он изменился
            if status != last_status:
                await tg(UpdateProfileRequest(about=status))
                print(f"Статус обновлён: {status}")
                last_status = status

        except Exception as e:
            print("Ошибка:", e)

        time.sleep(30)  # каждые 30 сек проверяем

with tg:
    tg.loop.run_until_complete(update_status())
