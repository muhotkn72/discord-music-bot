import discord
from discord.ext import commands
from music import MusicQueue, SpotifyClient, YouTubeClient, Song
from utils.logger import logger
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, YOUTUBE_API_KEY, BOT_PREFIX

class Music(commands.Cog):
    """Music commands cog"""
    def __init__(self, bot):
        self.bot = bot
        self.queues = {}  # guild_id -> MusicQueue
        self.spotify = SpotifyClient(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
        self.youtube = YouTubeClient(YOUTUBE_API_KEY)
    
    def get_queue(self, guild_id: int) -> MusicQueue:
        """Get or create a queue for a guild"""
        if guild_id not in self.queues:
            self.queues[guild_id] = MusicQueue()
        return self.queues[guild_id]
    
    @commands.command(name='join', help='Bot joins your voice channel')
    async def join(self, ctx):
        """Bot joins the voice channel"""
        try:
            if ctx.author.voice is None:
                await ctx.send('❌ You must be in a voice channel!')
                return
            
            channel = ctx.author.voice.channel
            
            # Check if already connected
            if ctx.voice_client is not None:
                if ctx.voice_client.channel.id == channel.id:
                    await ctx.send(f'✅ Already connected to {channel.name}')
                    return
                else:
                    await ctx.voice_client.disconnect()
            
            vc = await channel.connect()
            embed = discord.Embed(
                title='✅ Joined Voice Channel',
                description=f'Connected to {channel.name}',
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
            logger.info(f'Bot joined voice channel: {channel.name}')
        except Exception as e:
            logger.error(f'Error joining voice channel: {e}')
            await ctx.send(f'❌ Could not join voice channel: {str(e)}')
    
    @commands.command(name='leave', help='Bot leaves the voice channel')
    async def leave(self, ctx):
        """Bot leaves the voice channel"""
        try:
            if ctx.voice_client is None:
                await ctx.send('❌ Bot is not connected to a voice channel')
                return
            
            await ctx.voice_client.disconnect()
            embed = discord.Embed(
                title='👋 Left Voice Channel',
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
            logger.info('Bot left voice channel')
        except Exception as e:
            logger.error(f'Error leaving voice channel: {e}')
            await ctx.send(f'❌ Could not leave voice channel: {str(e)}')
    
    @commands.command(name='play', help='Play a song from Spotify or YouTube')
    async def play(self, ctx, *, query: str):
        """Play a song"""
        if not query:
            await ctx.send('❌ Please provide a song name or URL')
            return
        
        try:
            # Auto-join if not connected
            if ctx.voice_client is None:
                if ctx.author.voice is None:
                    await ctx.send('❌ You must be in a voice channel!')
                    return
                await ctx.invoke(self.join)
            
            # Determine source and search
            if 'spotify' in query.lower():
                songs = self.spotify.search_track(query.replace('spotify ', ''), limit=1)
                if not songs:
                    await ctx.send('❌ No songs found on Spotify')
                    return
                song_data = songs[0]
                song = Song(
                    title=f"{song_data['title']} - {song_data['artist']}",
                    url=song_data['url'],
                    duration=song_data['duration'],
                    source='spotify',
                    requester=ctx.author.mention
                )
            else:
                videos = self.youtube.search_video(query, limit=1)
                if not videos:
                    await ctx.send('❌ No videos found on YouTube')
                    return
                video_data = videos[0]
                song = Song(
                    title=video_data['title'],
                    url=video_data['url'],
                    duration=0,
                    source='youtube',
                    requester=ctx.author.mention
                )
            
            queue = self.get_queue(ctx.guild.id)
            queue.add_song(song)
            
            embed = discord.Embed(
                title='🎵 Song Added to Queue',
                description=song.title,
                color=discord.Color.green()
            )
            embed.add_field(name='Source', value=song.source.capitalize())
            embed.add_field(name='Requested by', value=ctx.author.mention)
            embed.add_field(name='Queue Position', value=queue.get_length())
            
            await ctx.send(embed=embed)
            logger.info(f'Added song to queue: {song.title}')
        except Exception as e:
            logger.error(f'Error in play command: {e}')
            await ctx.send(f'❌ An error occurred: {str(e)}')
    
    @commands.command(name='queue', help='Show the current queue')
    async def queue_command(self, ctx):
        """Show the queue"""
        try:
            queue = self.get_queue(ctx.guild.id)
            songs = queue.get_queue()
            
            if not songs and not queue.current_song:
                await ctx.send('📭 The queue is empty')
                return
            
            embed = discord.Embed(
                title='🎶 Current Queue',
                color=discord.Color.blue()
            )
            
            if queue.current_song:
                embed.add_field(
                    name='🎵 Now Playing',
                    value=queue.current_song,
                    inline=False
                )
            
            if songs:
                queue_text = '\n'.join([f'{i+1}. {song}' for i, song in enumerate(songs[:10])])
                if len(songs) > 10:
                    queue_text += f'\n... and {len(songs) - 10} more songs'
                embed.add_field(
                    name=f'Upcoming ({len(songs)} songs)',
                    value=queue_text,
                    inline=False
                )
            
            await ctx.send(embed=embed)
        except Exception as e:
            logger.error(f'Error in queue command: {e}')
            await ctx.send(f'❌ An error occurred: {str(e)}')
    
    @commands.command(name='skip', help='Skip the current song')
    async def skip(self, ctx):
        """Skip the current song"""
        try:
            queue = self.get_queue(ctx.guild.id)
            next_song = queue.skip()
            
            if next_song:
                embed = discord.Embed(
                    title='⏭️ Song Skipped',
                    description=f'Now playing: {next_song}',
                    color=discord.Color.orange()
                )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title='⏭️ Song Skipped',
                    description='Queue is empty',
                    color=discord.Color.orange()
                )
                await ctx.send(embed=embed)
        except Exception as e:
            logger.error(f'Error in skip command: {e}')
            await ctx.send(f'❌ An error occurred: {str(e)}')
    
    @commands.command(name='stop', help='Stop playing music and clear the queue')
    async def stop(self, ctx):
        """Stop music and clear queue"""
        try:
            queue = self.get_queue(ctx.guild.id)
            queue.clear()
            
            # Stop voice playback
            if ctx.voice_client and ctx.voice_client.is_playing():
                ctx.voice_client.stop()
            
            embed = discord.Embed(
                title='⏹️ Music Stopped',
                description='Queue has been cleared',
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        except Exception as e:
            logger.error(f'Error in stop command: {e}')
            await ctx.send(f'❌ An error occurred: {str(e)}')
    
    @commands.command(name='shuffle', help='Shuffle the queue')
    async def shuffle(self, ctx):
        """Shuffle the queue"""
        try:
            queue = self.get_queue(ctx.guild.id)
            if queue.get_length() < 2:
                await ctx.send('❌ Queue has less than 2 songs')
                return
            
            queue.shuffle()
            embed = discord.Embed(
                title='🔀 Queue Shuffled',
                description=f'{queue.get_length()} songs shuffled',
                color=discord.Color.purple()
            )
            await ctx.send(embed=embed)
        except Exception as e:
            logger.error(f'Error in shuffle command: {e}')
            await ctx.send(f'❌ An error occurred: {str(e)}')
    
    @commands.command(name='loop', help='Set loop mode (0: off, 1: song, 2: queue)')
    async def loop(self, ctx, mode: int = None):
        """Set loop mode"""
        try:
            queue = self.get_queue(ctx.guild.id)
            if mode is None:
                mode = (queue.loop_mode + 1) % 3
            
            loop_status = queue.set_loop(mode)
            embed = discord.Embed(
                title='🔁 Loop Mode Changed',
                description=loop_status,
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        except Exception as e:
            logger.error(f'Error in loop command: {e}')
            await ctx.send(f'❌ An error occurred: {str(e)}')
    
    @commands.command(name='search', help='Search for a song on Spotify or YouTube')
    async def search(self, ctx, source: str, *, query: str):
        """Search for songs"""
        if source.lower() not in ['spotify', 'youtube']:
            await ctx.send('❌ Source must be "spotify" or "youtube"')
            return
        
        try:
            if source.lower() == 'spotify':
                results = self.spotify.search_track(query, limit=5)
                if not results:
                    await ctx.send('❌ No songs found on Spotify')
                    return
                
                embed = discord.Embed(
                    title=f'🎵 Spotify Search Results for "{query}"',
                    color=discord.Color.green()
                )
                for i, song in enumerate(results, 1):
                    embed.add_field(
                        name=f'{i}. {song["title"]}',
                        value=f'Artist: {song["artist"]}\nDuration: {song["duration"]//1000}s',
                        inline=False
                    )
            else:
                results = self.youtube.search_video(query, limit=5)
                if not results:
                    await ctx.send('❌ No videos found on YouTube')
                    return
                
                embed = discord.Embed(
                    title=f'🎬 YouTube Search Results for "{query}"',
                    color=discord.Color.red()
                )
                for i, video in enumerate(results, 1):
                    embed.add_field(
                        name=f'{i}. {video["title"]}',
                        value=f'Channel: {video["channel"]}',
                        inline=False
                    )
            
            await ctx.send(embed=embed)
        except Exception as e:
            logger.error(f'Error in search command: {e}')
            await ctx.send(f'❌ An error occurred: {str(e)}')

async def setup(bot):
    """Setup the cog"""
    await bot.add_cog(Music(bot))
