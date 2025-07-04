import discord
from discord.ext import commands
import json
import os

intents = discord.Intents.default()
intents.members = True  # 멤버 이벤트를 받기 위해 필요

bot = commands.Bot(command_prefix='/', intents=intents)

CONFIG_FILE = 'config.json'

# 설정 로딩
def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

# 설정 저장
def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

config = load_config()

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
@commands.has_permissions(administrator=True)
async def set(ctx, channel: discord.TextChannel, *, message):
    guild_id = str(ctx.guild.id)
    config[guild_id] = {
        "channel_id": channel.id,
        "message": message
    }
    save_config(config)
    await ctx.send(f"✅ 메시지가 설정되었습니다: {channel.mention} - `{message}`")

@bot.event
async def on_member_join(member):
    guild_id = str(member.guild.id)
    if guild_id in config:
        data = config[guild_id]
        channel = member.guild.get_channel(data["channel_id"])
        if channel:
            await channel.send(data["message"].replace("{user}", member.mention))

# 토큰으로 실행
bot.run("YOUR_BOT_TOKEN")
