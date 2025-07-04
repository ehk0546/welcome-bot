import discord
from discord.ext import commands
import os

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.members = True  # on_member_join을 위해 멤버 intent 필요

bot = commands.Bot(command_prefix='!', intents=intents)  # prefix는 의미 없지만 유지
welcome_config = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} commands")
    except Exception as e:
        print(f"⚠️ Sync failed: {e}")

@bot.tree.command(name="set_welcome", description="환영 메시지를 설정합니다")
@discord.app_commands.describe(channel="환영 메시지를 보낼 채널", message="환영 메시지 내용")
async def set_welcome(interaction: discord.Interaction, channel: discord.TextChannel, message: str):
    welcome_config[interaction.guild_id] = {
        "channel_id": channel.id,
        "message": message
    }
    await interaction.response.send_message(f"✅ 환영 메시지가 설정되었습니다: {channel.mention} - {message}")

@bot.event
async def on_member_join(member):
    config = welcome_config.get(member.guild.id)
    if config:
        channel = member.guild.get_channel(config["channel_id"])
        if channel:
            await channel.send(f"{member.mention} {config['message']}")

bot.run(TOKEN)

