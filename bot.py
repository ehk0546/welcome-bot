import discord
from discord.ext import commands
import os

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)

welcome_config = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def set(ctx, channel: discord.TextChannel, *, message):
    welcome_config[ctx.guild.id] = {
        "channel_id": channel.id,
        "message": message
    }
    await ctx.send(f"✅ 환영 메시지가 설정되었습니다: {channel.mention} - {message}")

@bot.event
async def on_member_join(member):
    config = welcome_config.get(member.guild.id)
    if config:
        channel = member.guild.get_channel(config["channel_id"])
        if channel:
            await channel.send(f"{member.mention} {config['message']}")

bot.run(TOKEN)
