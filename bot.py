import discord
import os
import re
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

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

# ================== VIEW ==================
class UserscriptView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=600)
        # Tampermonkey URL Button
        self.add_item(discord.ui.Button(
            label="🔧 Tampermonkey",
            style=discord.ButtonStyle.blurple,
            url="https://tampermonkey.net/"
        ))

    @discord.ui.button(label="📥 Download .js", style=discord.ButtonStyle.green)
    async def download(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"```js\n{USERSCRIPT_CODE}\n```", ephemeral=True)

    @discord.ui.button(label="📋 Copy Code", style=discord.ButtonStyle.gray)
    async def copy(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"```js\n{USERSCRIPT_CODE}\n```", ephemeral=True)

@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")

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

# !userscript command
@bot.command(name="userscript")
async def userscript(ctx):
    embed = discord.Embed(
        title="🛠️ YuB-X LootLabs Userscript",
        description="Automatically adds a **Get YuB-X Key** button on lootlabs.gg pages.",
        color=0x00ff00
    )
    embed.add_field(
        name="How to install:",
        value="1. Click **Tampermonkey**\n2. Click **Download .js** or **Copy Code**\n3. Paste in Tampermonkey",
        inline=False
    )

    await ctx.reply(embed=embed, view=UserscriptView())

bot.run(os.getenv("DISCORD_TOKEN"))
