import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# -------------------------------------------------------
# Load environment variables from .env file
# -------------------------------------------------------
load_dotenv()

BOT_TOKEN = os.getenv("DISCORD_TOKEN")
NOTIFICATION_CHANNEL_ID = int(os.getenv("NOTIFICATION_CHANNEL_ID"))

# Validate that the required env vars are actually set
if not BOT_TOKEN:
    raise ValueError("DISCORD_TOKEN is missing from your .env file")
if not NOTIFICATION_CHANNEL_ID:
    raise ValueError("NOTIFICATION_CHANNEL_ID is missing from your .env file")

# -------------------------------------------------------
# Set up intents (what events the bot is allowed to see)
# -------------------------------------------------------
intents = discord.Intents.default()
intents.voice_states = True  # Required to detect voice channel joins
intents.members = True       # Required to access member details

# -------------------------------------------------------
# Create the bot instance
# -------------------------------------------------------
bot = commands.Bot(command_prefix="!", intents=intents)


# -------------------------------------------------------
# Event: Bot is ready and connected
# -------------------------------------------------------
@bot.event
async def on_ready():
    print(f"✅ Bot is online — logged in as {bot.user}")
    print(f"📢 Sending notifications to channel ID: {NOTIFICATION_CHANNEL_ID}")


# -------------------------------------------------------
# Event: A member's voice state changes
# Fires when someone joins, leaves, mutes, or moves channels
# -------------------------------------------------------
@bot.event
async def on_voice_state_update(member, before, after):
    """
    before: voice state before the change
    after:  voice state after the change

    If before.channel is None and after.channel is not None,
    the member has freshly joined a voice channel.
    """

    joined_channel = before.channel is None and after.channel is not None

    if joined_channel:
        notif_channel = bot.get_channel(NOTIFICATION_CHANNEL_ID)

        if notif_channel:
            await notif_channel.send(
                f"🔊 **{member.display_name}** just joined **{after.channel.name}**!"
            )
        else:
            print(f"⚠️  Could not find notification channel with ID {NOTIFICATION_CHANNEL_ID}")


# -------------------------------------------------------
# Start the bot
# -------------------------------------------------------
bot.run(BOT_TOKEN)