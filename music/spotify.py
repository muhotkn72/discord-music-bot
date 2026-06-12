import requests
from typing import List, Dict, Optional
from utils.logger import logger

class SpotifyClient:
    """Handles Spotify API interactions"""
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token: Optional[str] = None
        self.token_expires_at = 0
        self.auth_url = 'https://accounts.spotify.com/api/token'
        self.api_url = 'https://api.spotify.com/v1'
    
    def _get_access_token(self) -> bool:
        """Get a new access token from Spotify"""
        try:
            auth = (self.client_id, self.client_secret)
            data = {'grant_type': 'client_credentials'}
            response = requests.post(self.auth_url, auth=auth, data=data, timeout=10)
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data['access_token']
            logger.info('✅ Spotify authentication successful')
            return True
        except Exception as e:
            logger.error(f'❌ Spotify authentication failed: {e}')
            return False
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """Make a request to Spotify API"""
        if not self.access_token:
            if not self._get_access_token():
                return None
        
        try:
            headers = {'Authorization': f'Bearer {self.access_token}'}
            url = f'{self.api_url}{endpoint}'
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f'❌ Spotify API request failed: {e}')
            return None
    
    def search_track(self, query: str, limit: int = 5) -> List[Dict]:
        """Search for tracks on Spotify"""
        try:
            params = {'q': query, 'type': 'track', 'limit': limit}
            result = self._make_request('/search', params)
            
            if result and 'tracks' in result:
                tracks = []
                for item in result['tracks']['items']:
                    tracks.append({
                        'title': item['name'],
                        'artist': ', '.join([artist['name'] for artist in item['artists']]),
                        'url': item['external_urls']['spotify'],
                        'duration': item['duration_ms'],
                        'cover': item['album']['images'][0]['url'] if item['album']['images'] else None
                    })
                return tracks
        except Exception as e:
            logger.error(f'❌ Spotify search failed: {e}')
        return []
    
    def get_playlist(self, playlist_id: str) -> Optional[Dict]:
        """Get playlist information from Spotify"""
        try:
            result = self._make_request(f'/playlists/{playlist_id}')
            if result:
                return {
                    'name': result['name'],
                    'description': result['description'],
                    'total_tracks': result['tracks']['total'],
                    'cover': result['images'][0]['url'] if result['images'] else None,
                    'url': result['external_urls']['spotify']
                }
        except Exception as e:
            logger.error(f'❌ Failed to get playlist: {e}')
        return None
    
    def get_playlist_tracks(self, playlist_id: str, limit: int = 50) -> List[Dict]:
        """Get tracks from a Spotify playlist"""
        try:
            params = {'limit': limit}
            result = self._make_request(f'/playlists/{playlist_id}/tracks', params)
            
            if result and 'items' in result:
                tracks = []
                for item in result['items']:
                    if item['track']:
                        track = item['track']
                        tracks.append({
                            'title': track['name'],
                            'artist': ', '.join([artist['name'] for artist in track['artists']]),
                            'url': track['external_urls']['spotify'],
                            'duration': track['duration_ms']
                        })
                return tracks
        except Exception as e:
            logger.error(f'❌ Failed to get playlist tracks: {e}')
        return []
