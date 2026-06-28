import os
import re
import logging

import discord
from dotenv import load_dotenv

# Load variables from the .env file into the environment.
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("igfix")

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN or TOKEN == "PASTE_YOUR_TOKEN_HERE":
    raise SystemExit("DISCORD_TOKEN is not set. Edit .env and add your bot token.")

INSTAGRAM_HOST = os.getenv("INSTAGRAM_HOST", "kkinstagram.com")

# Matches instagram.com/<kind>/<id>, where kind is reel|reels|p|tv.
# Captures the kind and the id so we can rebuild the link on the proxy host.
IG_RE = re.compile(
    r"https?://(?:www\.)?instagram\.com/(reel|reels|p|tv)/([\w-]+)\S*",
    re.IGNORECASE,
)

# Intents declare what events Discord will send us. Message Content is a
# *privileged* intent and must also be enabled in the Developer Portal.
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    log.info("Logged in as %s (id=%s)", client.user, client.user.id)


@client.event
async def on_message(msg):
    # Ignore messages from any bot, including ourselves, to avoid loops.
    if msg.author.bot:
        return

    matches = IG_RE.findall(msg.content)
    if not matches:
        return

    fixed = [f"https://{INSTAGRAM_HOST}/{kind}/{ident}" for kind, ident in matches]
    log.info("Rewrote %d link(s) from %s", len(fixed), msg.author)

    # Suppress the original dead embed if we have Manage Messages permission;
    # degrade gracefully if we don't.
    try:
        await msg.edit(suppress=True)
    except discord.Forbidden:
        pass

    await msg.reply("\n".join(fixed), mention_author=False)


# log_handler=None tells discord.py not to install its own logging config,
# so our basicConfig above is the single source of truth.
client.run(TOKEN, log_handler=None)
