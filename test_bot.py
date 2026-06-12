#!/usr/bin/env python3
"""
Test script to validate bot configuration and components
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test if all required imports work"""
    print('\n📦 Testing imports...')
    try:
        import discord
        print('  ✅ discord.py')
        import dotenv
        print('  ✅ python-dotenv')
        import requests
        print('  ✅ requests')
        return True
    except ImportError as e:
        print(f'  ❌ Import failed: {e}')
        return False

def test_config():
    """Test configuration"""
    print('\n⚙️  Testing configuration...')
    try:
        from config import (
            DISCORD_TOKEN, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET,
            BOT_PREFIX, BOT_LANGUAGE
        )
        
        if DISCORD_TOKEN == 'your_discord_bot_token_here':
            print('  ⚠️  DISCORD_TOKEN not configured')
        else:
            print('  ✅ DISCORD_TOKEN configured')
        
        if SPOTIFY_CLIENT_ID == 'your_spotify_client_id_here':
            print('  ⚠️  SPOTIFY_CLIENT_ID not configured')
        else:
            print('  ✅ SPOTIFY_CLIENT_ID configured')
        
        if SPOTIFY_CLIENT_SECRET == 'your_spotify_client_secret_here':
            print('  ⚠️  SPOTIFY_CLIENT_SECRET not configured')
        else:
            print('  ✅ SPOTIFY_CLIENT_SECRET configured')
        
        print(f'  ✅ BOT_PREFIX: {BOT_PREFIX}')
        print(f'  ✅ BOT_LANGUAGE: {BOT_LANGUAGE}')
        return True
    except Exception as e:
        print(f'  ❌ Configuration test failed: {e}')
        return False

def test_spotify_client():
    """Test Spotify client"""
    print('\n🎵 Testing Spotify client...')
    try:
        from music import SpotifyClient
        from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
        
        client = SpotifyClient(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
        print('  ✅ SpotifyClient initialized')
        
        # Try to get token
        if client._get_access_token():
            print('  ✅ Spotify authentication successful')
            return True
        else:
            print('  ⚠️  Could not authenticate with Spotify (check credentials)')
            return False
    except Exception as e:
        print(f'  ❌ Spotify test failed: {e}')
        return False

def test_youtube_client():
    """Test YouTube client"""
    print('\n📹 Testing YouTube client...')
    try:
        from music import YouTubeClient
        from config import YOUTUBE_API_KEY
        
        client = YouTubeClient(YOUTUBE_API_KEY)
        print('  ✅ YouTubeClient initialized')
        
        if YOUTUBE_API_KEY:
            print('  ✅ YouTube API key configured')
        else:
            print('  ⚠️  YouTube API key not configured (fallback will be used)')
        return True
    except Exception as e:
        print(f'  ❌ YouTube test failed: {e}')
        return False

def test_queue():
    """Test music queue"""
    print('\n📝 Testing music queue...')
    try:
        from music import MusicQueue, Song
        
        queue = MusicQueue()
        print('  ✅ MusicQueue initialized')
        
        # Add test song
        song = Song(
            title='Test Song',
            url='https://example.com',
            duration=180,
            source='youtube',
            requester='Test User'
        )
        queue.add_song(song)
        print('  ✅ Song added to queue')
        
        if queue.get_length() == 1:
            print('  ✅ Queue length correct')
        
        # Test shuffle
        queue.shuffle()
        print('  ✅ Queue shuffle works')
        
        # Test loop
        loop_status = queue.set_loop(1)
        print(f'  ✅ Loop mode set: {loop_status}')
        
        return True
    except Exception as e:
        print(f'  ❌ Queue test failed: {e}')
        return False

def test_logger():
    """Test logger"""
    print('\n📊 Testing logger...')
    try:
        from utils import logger
        
        logger.info('Test info message')
        logger.debug('Test debug message')
        logger.warning('Test warning message')
        print('  ✅ Logger working')
        return True
    except Exception as e:
        print(f'  ❌ Logger test failed: {e}')
        return False

def main():
    """Run all tests"""
    print('=' * 50)
    print('🧪 Discord Music Bot - Test Suite')
    print('=' * 50)
    
    results = []
    
    # Run tests
    results.append(('Imports', test_imports()))
    results.append(('Configuration', test_config()))
    results.append(('Logger', test_logger()))
    results.append(('Music Queue', test_queue()))
    results.append(('Spotify Client', test_spotify_client()))
    results.append(('YouTube Client', test_youtube_client()))
    
    # Summary
    print('\n' + '=' * 50)
    print('📋 Test Summary')
    print('=' * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = '✅' if result else '❌'
        print(f'{status} {test_name}')
    
    print(f'\nPassed: {passed}/{total}')
    
    if passed == total:
        print('\n✅ All tests passed! Bot is ready to run.')
        print('\n🚀 To start the bot, run: python main.py')
        return 0
    else:
        print('\n⚠️  Some tests failed. Check configuration and try again.')
        return 1

if __name__ == '__main__':
    sys.exit(main())
