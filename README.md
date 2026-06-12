# 🎵 Discord Music Bot

Modern Discord music bot with support for Spotify and YouTube.

## ✨ Features

- 🎶 Play music from Spotify and YouTube
- 📝 Queue system with shuffle support
- 🔁 Loop modes (off, current song, entire queue)
- 🔍 Search functionality for both platforms
- 📊 Queue management (skip, stop, remove)
- 🎨 Rich embeds for better UI
- ⚠️ Error handling and logging
- 🔐 Secure configuration management

## 📋 Prerequisites

- Python 3.8+
- Discord Bot Token
- Spotify Client ID & Client Secret
- YouTube API Key (optional for basic search)

## 🚀 Installation

### 1. Clone the repository
```bash
git clone https://github.com/muhotkn72/discord-music-bot.git
cd discord-music-bot
```

### 2. Create virtual environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure bot

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Edit `.env` and add your credentials:
```env
DISCORD_TOKEN=your_discord_bot_token_here
DISCORD_GUILD_ID=your_guild_id_here
SPOTIFY_CLIENT_ID=your_spotify_client_id_here
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here
YOUTUBE_API_KEY=your_youtube_api_key_here (optional)
```

### 5. Run the bot
```bash
python main.py
```

## 🎮 Commands

### Music Commands

| Command | Description | Example |
|---------|-------------|----------|
| `!play <query>` | Play a song | `!play spotify bad guy` or `!play bad guy` |
| `!queue` | Show current queue | `!queue` |
| `!skip` | Skip current song | `!skip` |
| `!stop` | Stop music and clear queue | `!stop` |
| `!shuffle` | Shuffle the queue | `!shuffle` |
| `!loop [mode]` | Set loop mode (0-2) | `!loop` or `!loop 1` |
| `!search <source> <query>` | Search for songs | `!search spotify adele` or `!search youtube music` |
| `!help` | Show help message | `!help` or `!help play` |

## 🔑 Getting Credentials

### Discord Bot Token
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to "Bot" section and click "Add Bot"
4. Copy the token
5. Enable "Message Content Intent" in Privileged Gateway Intents

### Spotify Credentials
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in or create an account
3. Create a new app
4. Copy Client ID and Client Secret

### YouTube API Key (Optional)
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable YouTube Data API v3
4. Create API key in credentials

## 📁 Project Structure

```
discord-music-bot/
├── main.py                 # Entry point
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment variables
├── .gitignore           # Git ignore file
├── utils/
│   ├── __init__.py
│   └── logger.py        # Logging system
├── music/
│   ├── __init__.py
│   ├── queue.py         # Queue management
│   ├── spotify.py       # Spotify integration
│   └── youtube.py       # YouTube integration
├── cogs/
│   ├── __init__.py
│   └── music.py         # Music commands
└── logs/                # Log files (created on first run)
```

## 🔧 Configuration

Edit `config.py` to customize:
- Bot prefix (default: `!`)
- Language (default: `en`)
- Logging level

## 🐛 Troubleshooting

### Bot doesn't respond
- Check if bot token is correct in `.env`
- Verify bot has message permissions in your server
- Check `logs/` directory for error messages

### Spotify search fails
- Verify Spotify Client ID and Secret are correct
- Check internet connection
- Spotify API might be rate-limiting

### YouTube search fails
- YouTube API key is optional but recommended
- Without it, bot uses fallback search method
- Add API key to `.env` for better results

## 📝 Logging

Logs are saved to `logs/` directory with timestamp. Check these files for debugging issues.

## 🤝 Contributing

Feel free to submit issues and pull requests!

## 📄 License

MIT License - See LICENSE file for details

## ⚠️ Disclaimer

This bot is for educational purposes. Please ensure you comply with Discord's Terms of Service and the APIs' usage policies.

## 🆘 Support

If you encounter issues:
1. Check the `logs/` directory
2. Review the troubleshooting section
3. Create an issue on GitHub

---

**Made with ❤️ by muhotkn72**
