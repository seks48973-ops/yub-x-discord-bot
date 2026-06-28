import discord
import os
from discord.ext import commands
import re

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# The Userscript Code (as string)
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
        button.style.cssText = `
            position: fixed;
            top: 30px;
            right: 30px;
            padding: 12px 24px;
            background: #00ff00;
            color: black;
            font-size: 16px;
            font-weight: bold;
            border: 3px solid white;
            border-radius: 8px;
            cursor: pointer;
            z-index: 2147483647;
            box-shadow: 0 4px 15px rgba(0, 255, 0, 0.6);
        `;

        button.onclick = () => window.open(bypassUrl, '_blank');
        document.body.appendChild(button);
    }

    setTimeout(addButton, 800);
    setTimeout(addButton, 2000);
    setTimeout(addButton, 4000);
})();
"""

class UserscriptView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)

        # Button 1: Download
        self.add_item(discord.ui.Button(
            label="📥 Download Userscript (.js)",
            style=discord.ButtonStyle.green,
            custom_id="download"
        ))

        # Button 2: Tampermonkey
        self.add_item(discord.ui.Button(
            label="🔧 Install Tampermonkey",
            style=discord.ButtonStyle.blurple,
            url="https://tampermonkey.net/"
        ))

    @discord.ui.button(label="📋 Copy Userscript", style=discord.ButtonStyle.gray)
    async def copy_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            f"```js\n{USERSCRIPT_CODE}\n```",
            ephemeral=True
        )

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

@bot.command(name="userscript")
async def userscript(ctx):
    embed = discord.Embed(
        title="YuB-X LootLabs Userscript",
        description="Install this userscript to automatically get the bypass button on lootlabs.gg pages.",
        color=0x00ff00
    )
    embed.add_field(
        name="How to use:",
        value="1. Install Tampermonkey\n2. Click 'Download Userscript'\n3. Paste into Tampermonkey",
        inline=False
    )

    await ctx.reply(embed=embed, view=UserscriptView())

# Auto-detect links (optional, keep your previous logic)
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

bot.run(os.getenv("DISCORD_TOKEN"))
