# 🔊 Discord Voice Notifier Bot

A lightweight, self-hostable Discord bot that sends a notification to a designated text channel whenever a member joins a voice channel in your server. Built with Python and discord.py, it's easy to configure, secure by design, and built to run permanently in the background on a Linux machine.

---

## 📋 Table of Contents

- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Creating the Discord Bot](#-creating-the-discord-bot)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Bot](#-running-the-bot)
- [Self-Hosting on Linux with systemd](#-self-hosting-on-linux-with-systemd)
- [Updating the Bot](#-updating-the-bot)
- [Project Structure](#-project-structure)
- [Troubleshooting](#-troubleshooting)
- [Security](#-security)

---

## ✨ Features

- 📣 Sends a notification message to a text channel whenever a member joins a voice channel
- 🔒 Secure credential handling via environment variables — no tokens ever in source code
- 🐧 Designed to be self-hosted on a Linux machine using `systemd`
- ♻️ Automatically restarts if the bot crashes
- 🚀 Starts automatically on server reboot
- 🧩 Easy to extend with additional events or commands

---

## 🧰 Prerequisites

Before you begin, make sure you have the following:

- A [Discord account](https://discord.com)
- Access to the [Discord Developer Portal](https://discord.com/developers/applications)
- Admin permissions on the Discord server you want the bot in
- A Linux machine to host the bot (a VPS, home server, or Raspberry Pi all work)
- Python 3.8 or higher installed on that machine
- `git` installed on that machine

---

## 🤖 Creating the Discord Bot

You need to create a bot user in the Discord Developer Portal before running any code.

### Step 1 — Create an Application

1. Go to [discord.com/developers/applications](https://discord.com/developers/applications) and log in
2. Click **"New Application"** in the top right corner
3. Give it a name (e.g. `VoiceNotifier`) and click **Create**

### Step 2 — Create the Bot User

1. On the left sidebar, click **"Bot"**
2. Click **"Add Bot"** → confirm with **"Yes, do it!"**
3. Click **"Reset Token"** and copy the token that appears — **save this somewhere safe, you won't see it again**

> ⚠️ **Never share your bot token with anyone or commit it to GitHub.** If it is ever exposed, immediately click "Reset Token" to invalidate the old one.

### Step 3 — Enable Privileged Gateway Intents

Still on the Bot page, scroll down to **"Privileged Gateway Intents"** and enable:

- ✅ **Server Members Intent** — required to receive member information
- ✅ **Message Content Intent** — required for the bot to interact with messages
- ✅ **Presence Intent** — optional, needed only if you want to filter by online status

Click **Save Changes**.

### Step 4 — Get Your Notification Channel ID

1. Open Discord and go to **User Settings → Advanced**
2. Toggle on **Developer Mode**
3. Right-click the text channel where you want notifications to be posted
4. Click **"Copy Channel ID"** and save it alongside your token

### Step 5 — Invite the Bot to Your Server

1. In the Developer Portal, navigate to **OAuth2 → URL Generator** on the left sidebar
2. Under **Scopes**, tick: `bot`
3. Under **Bot Permissions**, tick:
   - `View Channels`
   - `Send Messages`
   - `Connect`
4. Copy the generated URL at the bottom of the page
5. Paste it into your browser, select your server, and click **Authorise**

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/discord-voice-notifier.git
cd discord-voice-notifier
```

### 2. Create a Virtual Environment

A virtual environment keeps the bot's dependencies isolated from the rest of your system:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

The bot uses a `.env` file to store sensitive credentials. This file is listed in `.gitignore` and will never be committed to GitHub.

### 1. Copy the example environment file

```bash
cp .env.example .env
```

### 2. Fill in your values

Open `.env` in a text editor:

```bash
nano .env
```

Replace the placeholder values with your own:

```env
DISCORD_TOKEN=your_bot_token_here
NOTIFICATION_CHANNEL_ID=your_channel_id_here
```

| Variable | Description | Where to get it |
|---|---|---|
| `DISCORD_TOKEN` | Your bot's secret token | Discord Developer Portal → Bot → Reset Token |
| `NOTIFICATION_CHANNEL_ID` | The ID of the text channel to post notifications in | Discord → Right-click channel → Copy Channel ID |

Save and close the file (`Ctrl+X` → `Y` → `Enter` if using nano).

---

## ▶️ Running the Bot

Once configured, you can run the bot directly to test it:

```bash
python3 bot.py
```

You should see output like:

```
✅ Bot is online — logged in as VoiceNotifier#1234
📢 Sending notifications to channel ID: 123456789
```

Now try joining a voice channel in your server — you should see a notification appear in your designated text channel.

Press `Ctrl+C` to stop the bot. To run it permanently in the background, follow the section below.

---

## 🐧 Self-Hosting on Linux with systemd

`systemd` is a Linux service manager that will keep your bot running in the background, restart it if it crashes, and start it automatically whenever your server reboots.

### Step 1 — Create the Service File

```bash
sudo nano /etc/systemd/system/discord-bot.service
```

Paste the following, replacing `your_linux_username` and the path with your actual values:

```ini
[Unit]
Description=Discord Voice Notification Bot
After=network.target

[Service]
Type=simple
User=your_linux_username
WorkingDirectory=/home/your_linux_username/discord-voice-notifier
ExecStart=/home/your_linux_username/discord-voice-notifier/venv/bin/python3 bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Save and close the file.

### Step 2 — Enable and Start the Service

```bash
# Reload systemd so it picks up the new service file
sudo systemctl daemon-reload

# Enable the service to start automatically on boot
sudo systemctl enable discord-bot

# Start the service now
sudo systemctl start discord-bot
```

### Step 3 — Verify It's Running

```bash
sudo systemctl status discord-bot
```

You should see `Active: active (running)` in green.

### Useful Service Commands

| Command | Description |
|---|---|
| `sudo systemctl status discord-bot` | Check if the bot is running |
| `sudo systemctl start discord-bot` | Start the bot |
| `sudo systemctl stop discord-bot` | Stop the bot |
| `sudo systemctl restart discord-bot` | Restart the bot (use after updates) |
| `sudo journalctl -u discord-bot -f` | View live logs |
| `sudo journalctl -u discord-bot --since today` | View today's logs |

---

## 🔄 Updating the Bot

When you push new code to GitHub and want to pull the changes onto your server:

```bash
cd discord-voice-notifier
git pull
sudo systemctl restart discord-bot
```

Check the logs to confirm everything started correctly:

```bash
sudo journalctl -u discord-bot -f
```

---

## 📁 Project Structure

```
discord-voice-notifier/
├── bot.py              # Main bot logic
├── .env                # Your secret credentials (never committed)
├── .env.example        # Safe template for others to copy
├── .gitignore          # Ensures .env is never tracked by git
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## 🔧 Troubleshooting

**Bot is online but no notifications are appearing**
- Double-check that `NOTIFICATION_CHANNEL_ID` in your `.env` file is correct
- Make sure the bot has `Send Messages` and `View Channels` permissions in that channel
- Confirm the bot was invited to the server using the correct OAuth2 URL

**`discord.errors.PrivilegedIntentsRequired` error**
- Go to the Discord Developer Portal → Your App → Bot
- Make sure **Server Members Intent** and **Message Content Intent** are both enabled
- Click Save Changes and restart the bot

**`ValueError: DISCORD_TOKEN is missing` error**
- Make sure your `.env` file exists and contains `DISCORD_TOKEN=your_token_here`
- Make sure you ran `cp .env.example .env` and filled in the values

**Bot goes offline after closing the SSH session**
- You need to set up the `systemd` service as described in the [Self-Hosting](#-self-hosting-on-linux-with-systemd) section
- Without it, the bot only runs while your terminal is open

**`ModuleNotFoundError: No module named 'discord'`**
- Make sure your virtual environment is active: `source venv/bin/activate`
- Then install dependencies: `pip install -r requirements.txt`

**Bot token was accidentally committed to GitHub**
- Immediately go to the Developer Portal → Bot → **Reset Token**
- Update your `.env` file with the new token
- Remove the token from your git history (see [GitHub's guide on removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository))

---

## 🔒 Security

This project is designed with security in mind:

- **No credentials in source code** — all tokens and IDs live in `.env`, which is excluded from version control via `.gitignore`
- **`.env.example` is provided** so others know what variables are needed without exposing any real values
- **Anyone cloning this repo** simply copies `.env.example` to `.env` and fills in their own credentials

**Best practices to follow:**

- Never share your bot token publicly
- Regenerate your token immediately if you suspect it has been exposed
- Restrict bot permissions to only what it needs (`Send Messages`, `View Channels`, `Connect`)
- Keep your Linux server and Python packages up to date

---