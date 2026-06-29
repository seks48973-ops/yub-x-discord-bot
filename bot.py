import discord
import os
import re
import io
import asyncio
import aiohttp
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ================== CHANNEL IDS ==================
YUBX_STATUS_CHANNEL_ID = 1517123238331940924
ROBLOX_VERSION_CHANNEL_ID = 1517137352034881556

# ================== USERSCRIPT CODE ==================
USERSCRIPT_CODE = """// ==UserScript==
// @name         YuB-X LootLabs Bypass Button
// @namespace    http://tampermonkey.net/
// @version      1.6
// @description  Adds Get YuB-X Key button on lootlabs.gg links
// @author       Grok
// @match        *://links.lootlabs.gg/*
// @grant        none
// @run-at       document-idle
// ==/UserScript==

(function() {
    'use strict';
    function getSubId() {
        const url = window.location.href;
        const match = url.match(/sub_id=([^&\\s]+)/);
        return match ? match[1] : null;
    }
    function addButton() {
        if (document.getElementById('yubx-bypass-button')) return;
        const subId = getSubId();
        if (!subId) return;
        const bypassUrl = `https://yub-x.best/get-key?rn=true&c=${encodeURIComponent(subId)}`;
        const button = document.createElement('button');
        button.id = 'yubx-bypass-button';
        button.textContent = "🔑 GET YUB-X KEY";
        button.style.cssText = `position:fixed;top:30px;right:30px;padding:12px 24px;background:#00ff00;color:black;font-weight:bold;border:3px solid white;border-radius:8px;cursor:pointer;z-index:2147483647;`;
        button.onclick = () => window.open(bypassUrl, '_blank');
        document.body.appendChild(button);
    }
    setTimeout(addButton, 1000);
    setTimeout(addButton, 3000);
})();"""

# ================== VIEWS ==================
class UserscriptView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=600)
        self.add_item(discord.ui.Button(
            label="🔧 Tampermonkey",
            style=discord.ButtonStyle.blurple,
            url="https://tampermonkey.net/"
        ))

    @discord.ui.button(label="📥 Download .js", style=discord.ButtonStyle.green)
    async def download(self, interaction: discord.Interaction, button: discord.ui.Button):
        file_bytes = io.BytesIO(USERSCRIPT_CODE.encode('utf-8'))
        file = discord.File(file_bytes, filename="yub-x-lootlabs-bypass.user.js")
        await interaction.response.send_message("✅ Here is your userscript:", file=file, ephemeral=True)

    @discord.ui.button(label="📋 Copy Code", style=discord.ButtonStyle.gray)
    async def copy(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"```js\n{USERSCRIPT_CODE}\n```", ephemeral=True)

# ================== STATUS CHECKING ==================
async def check_yubx_status():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://yub-x.best", timeout=10) as resp:
                return "🟢 **Yub-X is UP**" if resp.status == 200 else "🔴 **Yub-X is DOWN**"
    except:
        return "⚠️ **Yub-X Status Check Failed**"

async def check_roblox_version():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://clientsettingscdn.roblox.com/v1/clientVersion/WindowsPlayer", timeout=10) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    version = data.get("version", "Unknown")
                    return f"📌 **Roblox Version:** {version}"
                else:
                    return "📌 **Roblox Version:** Checking..."
    except:
        return "📌 **Roblox Version:** Unable to fetch"

async def update_status_channels():
    await bot.wait_until_ready()
    while True:
        try:
            yubx_status = await check_yubx_status()
            roblox_status = await check_roblox_version()

            channel1 = bot.get_channel(YUBX_STATUS_CHANNEL_ID)
            if channel1:
                await channel1.purge(limit=5)
                await channel1.send(yubx_status)

            channel2 = bot.get_channel(ROBLOX_VERSION_CHANNEL_ID)
            if channel2:
                await channel2.purge(limit=5)
                await channel2.send(roblox_status)
        except Exception as e:
            print(f"Status update error: {e}")

        await asyncio.sleep(300)  # Every 5 minutes

# ================== EVENTS ==================
@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"✅ Bot is online as {bot.user} | Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"Sync error: {e}")
    
    bot.loop.create_task(update_status_channels())

# Auto-detect links
@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    content = message.content.strip()

    if "links.lootlabs.gg" in content and "zoaTgCxk" in content:
        try:
            sub_id_match = re.search(r'sub_id=([^&\s]+)', content)
            if sub_id_match:
                sub_id = sub_id_match.group(1)
                key_url = f"https://yub-x.best/get-key?rn=true&c={sub_id}"

                embed = discord.Embed(
                    title="YuB-X Key System",
                    description="Here is your bypass link:",
                    color=0x00ff00
                )
                embed.add_field(name="Key Link", value=key_url, inline=False)
                await message.reply(embed=embed)
        except:
            pass

# /bypass command
@bot.tree.command(name="bypass", description="Bypass a lootlabs.gg link")
@app_commands.describe(link="The full lootlabs.gg link")
async def bypass(interaction: discord.Interaction, link: str):
    if "zoaTgCxk" not in link:
        await interaction.response.send_message("Not YuB-X keysystem, please try again.", ephemeral=True)
        return

    try:
        sub_id_match = re.search(r'sub_id=([^&\s]+)', link)
        if sub_id_match:
            sub_id = sub_id_match.group(1)
            key_url = f"https://yub-x.best/get-key?rn=true&c={sub_id}"

            embed = discord.Embed(
                title="YuB-X Key System",
                description="Here is your bypass link:",
                color=0x00ff00
            )
            embed.add_field(name="Key Link", value=key_url, inline=False)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Could not find `sub_id` in the link.", ephemeral=True)
    except:
        await interaction.response.send_message("Error processing the link.", ephemeral=True)

# /userscript command
@bot.tree.command(name="userscript", description="Get the YuB-X LootLabs Userscript")
async def userscript(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🛠️ YuB-X LootLabs Userscript",
        description="Automatically adds a **Get YuB-X Key** button on lootlabs.gg pages.",
        color=0x00ff00
    )
    embed.add_field(
        name="How to install:",
        value="1. Click **Tampermonkey**\n2. Click **Download .js**\n3. Paste in Tampermonkey",
        inline=False
    )
    await interaction.response.send_message(embed=embed, view=UserscriptView())

bot.run(os.getenv("DISCORD_TOKEN"))
