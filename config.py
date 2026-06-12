import os
from dotenv import load_dotenv

load_dotenv()

# Discord Configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_GUILD_ID = os.getenv('DISCORD_GUILD_ID')

# Spotify Configuration
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

# YouTube Configuration
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY', '')

# Bot Configuration
BOT_PREFIX = os.getenv('BOT_PREFIX', '!')
BOT_LANGUAGE = os.getenv('BOT_LANGUAGE', 'en')

# Validation
def validate_config():
    """Validate required configuration"""
    if not DISCORD_TOKEN:
        raise ValueError('DISCORD_TOKEN is required in .env file')
    if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
        raise ValueError('Spotify credentials are required in .env file')
    print('✅ Configuration validated successfully')

if __name__ == '__main__':
    validate_config()
