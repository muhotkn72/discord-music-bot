import os
import discord
from discord.ext import commands
from config import DISCORD_TOKEN, BOT_PREFIX, validate_config
from utils.logger import logger

# Validate configuration before starting
try:
    validate_config()
except ValueError as e:
    logger.critical(f'Configuration error: {e}')
    exit(1)

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.guild_messages = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(
    command_prefix=BOT_PREFIX,
    intents=intents,
    help_command=commands.DefaultHelpCommand()
)

@bot.event
async def on_ready():
    """Called when bot is ready"""
    logger.info(f'✅ Bot is online as {bot.user}')
    logger.info(f'Bot ID: {bot.user.id}')
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name=f'{BOT_PREFIX}help for commands'
        )
    )

@bot.event
async def on_error(event, *args, **kwargs):
    """Handle errors"""
    logger.error(f'Error in {event}: {args}, {kwargs}')

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'❌ Command not found. Use `{BOT_PREFIX}help` for available commands.')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'❌ Missing required argument. Use `{BOT_PREFIX}help {ctx.command}` for help.')
    else:
        logger.error(f'Command error: {error}')
        await ctx.send(f'❌ An error occurred: {str(error)}')

async def load_cogs():
    """Load all cogs"""
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != '__init__.py':
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                logger.info(f'✅ Loaded cog: {filename[:-3]}')
            except Exception as e:
                logger.error(f'❌ Failed to load cog {filename[:-3]}: {e}')

async def main():
    """Main function"""
    async with bot:
        await load_cogs()
        await bot.start(DISCORD_TOKEN)

if __name__ == '__main__':
    logger.info('🚀 Starting Discord Music Bot...')
    try:
        import asyncio
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('⛔ Bot stopped by user')
    except Exception as e:
        logger.critical(f'Fatal error: {e}')
