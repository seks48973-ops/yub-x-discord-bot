import discord
import os
import re
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

class KeyButtonView(discord.ui.View):
    def __init__(self, key_url: str):
        super().__init__(timeout=300)
        self.add_item(discord.ui.Button(
            label="Get YuB-X Key",
            style=discord.ButtonStyle.green,
            url=key_url
        ))

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    content = message.content

    # Auto-detect lootlabs links
    if "links.lootlabs.gg" in content and "zoaTgCxk" in content:
        try:
            # Extract sub_id
            sub_id_match = re.search(r'sub_id=([^&\s]+)', content)
            
            if sub_id_match:
                sub_id = sub_id_match.group(1)
                key_url = f"https://yub-x.best/get-key?rn=true&c={sub_id}"

                embed = discord.Embed(
                    title="YuB-X Key System",
                    description="Click the button below to get your key.",
                    color=0x00ff00
                )

                await message.reply(embed=embed, view=KeyButtonView(key_url))
            else:
                await message.reply("Could not find `sub_id` in the link.")

        except Exception:
            await message.reply("Error processing the link.")

    # Optional: Warn about non-YuB-X links
    elif "links.lootlabs.gg" in content:
        await message.reply("Not YuB-X keysystem, please try again.")

bot.run(os.getenv("DISCORD_TOKEN"))
