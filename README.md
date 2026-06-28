# Link Rewrite — Discord Instagram Embed-Fix Bot

A small, self-hosted Discord bot that fixes Instagram links. When someone posts an
`instagram.com` link, Discord can't render a usable embed (Instagram blocks it), so
you get a dead preview or nothing at all. This bot detects those links and replies
with the same link rewritten to a community **embed-proxy host** that Discord *does*
render inline — so the video/photo actually shows up.

## How it works

The bot does **one thing**: it swaps the domain.

```
https://www.instagram.com/reel/ABC123/   →   https://kkinstagram.com/reel/ABC123
```

That's it. It does **not** download or re-upload media (no `yt-dlp`, no scraping).
The domain-rewrite approach is near-zero maintenance: when an embed-proxy host stops
working, you change one environment variable and you're back in business.

## Why not download the video?

Downloading server-side (e.g. with `yt-dlp`) breaks constantly: Instagram changes
its internals, rate-limits, and throws up login walls; it risks the scraping account
and bumps into Discord's upload size limits. Rewriting the domain sidesteps all of
that.

## Requirements

- Python 3.13+
- A Discord bot application (free — see setup below)

## Setup

### 1. Create the Discord application & bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. **New Application** → name it → **Create**.
3. Open the **Bot** tab → **Add Bot**.
4. Under **Token**, click **Reset Token** and copy it. You'll put this in `.env`.
   Keep it secret — anyone with this token controls your bot.

### 2. Enable the Message Content Intent (required)

Still on the **Bot** tab, scroll to **Privileged Gateway Intents** and turn on
**Message Content Intent**. Without it the bot connects but can't read message text,
so it can never see the links.

### 3. Invite the bot to your server

Build an invite URL (OAuth2 → URL Generator, or use the template below). The bot
needs these permissions:

- **View Channels** — to see messages
- **Send Messages** — to reply
- **Embed Links** — so its rewritten links unfurl into embeds
- **Read Message History** — to reply in context
- **Manage Messages** — to suppress the original dead embed (optional; the bot
  degrades gracefully without it)

Template (replace `<APPLICATION_ID>` with your app's ID from the **General
Information** tab):

```
https://discord.com/api/oauth2/authorize?client_id=<APPLICATION_ID>&permissions=93184&scope=bot
```

Open the URL, pick your server, authorize.

### 4. Install

```bash
git clone git@github.com:roberswd/link-rewrite.git
cd link-rewrite
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 5. Configure

```bash
cp .env.example .env
```

Edit `.env` and paste your bot token:

```
DISCORD_TOKEN=your-real-token-here
INSTAGRAM_HOST=kkinstagram.com
```

### 6. Run

```bash
python main.py
```

You should see `Logged in as <bot name>`. Post an Instagram link in your server and
the bot will reply with the fixed version.

## Configuration

| Variable         | Required | Default            | Description                                  |
| ---------------- | -------- | ------------------ | -------------------------------------------- |
| `DISCORD_TOKEN`  | Yes      | —                  | Your bot token from the Developer Portal.    |
| `INSTAGRAM_HOST` | No       | `kkinstagram.com`  | The embed-proxy host used to rewrite links.  |

## A note on embed-proxy hosts

The rewrite hosts (`kkinstagram.com`, and others like `ddinstagram` before it) are
**third-party community services**, not run by this project or by Instagram. They
come and go. If embeds stop working, swap `INSTAGRAM_HOST` for a different host —
that's the only change needed.

Also note: occasionally a *specific* post will only resolve to a still cover-frame
rather than a playable video. That's an upstream limitation of what Instagram
exposes for that post to anonymous fetchers — not something the bot can fix.

## Planned

- TikTok and X/Twitter support (via their own embed-proxy hosts)
- `Dockerfile` + `docker-compose.yml` for running on a server or Raspberry Pi

## License

[MIT](LICENSE)
