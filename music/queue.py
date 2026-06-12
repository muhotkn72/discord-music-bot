from collections import deque
from typing import Optional, List

class Song:
    """Represents a song in the queue"""
    def __init__(self, title: str, url: str, duration: int, source: str, requester: str):
        self.title = title
        self.url = url
        self.duration = duration
        self.source = source  # 'youtube' or 'spotify'
        self.requester = requester
    
    def __str__(self):
        return f"**{self.title}** (Source: {self.source}) - Requested by {self.requester}"

class MusicQueue:
    """Manages the music queue for a guild"""
    def __init__(self):
        self.queue = deque()
        self.current_song: Optional[Song] = None
        self.is_playing = False
        self.is_paused = False
        self.loop_mode = 0  # 0: no loop, 1: loop song, 2: loop queue
    
    def add_song(self, song: Song) -> None:
        """Add a song to the queue"""
        self.queue.append(song)
    
    def add_songs(self, songs: List[Song]) -> None:
        """Add multiple songs to the queue"""
        for song in songs:
            self.queue.append(song)
    
    def next_song(self) -> Optional[Song]:
        """Get the next song from the queue"""
        if len(self.queue) == 0:
            return None
        
        song = self.queue.popleft()
        self.current_song = song
        return song
    
    def skip(self) -> Optional[Song]:
        """Skip the current song and play the next one"""
        if len(self.queue) == 0:
            self.current_song = None
            self.is_playing = False
            return None
        return self.next_song()
    
    def remove_song(self, index: int) -> Optional[Song]:
        """Remove a song from the queue by index"""
        try:
            songs = list(self.queue)
            song = songs.pop(index)
            self.queue = deque(songs)
            return song
        except IndexError:
            return None
    
    def clear(self) -> None:
        """Clear the entire queue"""
        self.queue.clear()
        self.current_song = None
        self.is_playing = False
    
    def get_queue(self) -> List[Song]:
        """Get all songs in the queue"""
        return list(self.queue)
    
    def get_length(self) -> int:
        """Get the number of songs in the queue"""
        return len(self.queue)
    
    def shuffle(self) -> None:
        """Shuffle the queue"""
        import random
        songs = list(self.queue)
        random.shuffle(songs)
        self.queue = deque(songs)
    
    def set_loop(self, mode: int) -> str:
        """Set loop mode (0: no loop, 1: loop song, 2: loop queue)"""
        self.loop_mode = mode % 3
        modes = ['Loop: OFF', 'Loop: CURRENT SONG', 'Loop: QUEUE']
        return modes[self.loop_mode]
