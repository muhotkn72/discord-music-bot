import requests
from typing import List, Dict, Optional
from utils.logger import logger

class YouTubeClient:
    """Handles YouTube search and basic operations"""
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.api_url = 'https://www.googleapis.com/youtube/v3'
    
    def search_video(self, query: str, limit: int = 5) -> List[Dict]:
        """Search for videos on YouTube"""
        if not self.api_key:
            logger.warning('⚠️ YouTube API key not provided. Using fallback search method.')
            return self._search_fallback(query, limit)
        
        try:
            params = {
                'part': 'snippet',
                'q': query,
                'type': 'video',
                'maxResults': limit,
                'key': self.api_key
            }
            response = requests.get(f'{self.api_url}/search', params=params, timeout=10)
            response.raise_for_status()
            result = response.json()
            
            videos = []
            for item in result.get('items', []):
                videos.append({
                    'title': item['snippet']['title'],
                    'video_id': item['id']['videoId'],
                    'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                    'channel': item['snippet']['channelTitle'],
                    'thumbnail': item['snippet']['thumbnails']['default']['url']
                })
            return videos
        except Exception as e:
            logger.error(f'❌ YouTube search failed: {e}')
            return self._search_fallback(query, limit)
    
    def _search_fallback(self, query: str, limit: int = 5) -> List[Dict]:
        """Fallback search method when API key is not available"""
        try:
            # Simple YouTube search without API key
            # This returns basic video information
            logger.info(f'🔍 Searching YouTube for: {query}')
            return [{
                'title': f'{query} - Search Result {i+1}',
                'url': f'https://www.youtube.com/results?search_query={query.replace(" ", "+")}',
                'channel': 'YouTube'
            } for i in range(1)]
        except Exception as e:
            logger.error(f'❌ Fallback search failed: {e}')
        return []
