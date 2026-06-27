import discord
import os
import re
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

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
            else:
                await message.reply("Could not extract `sub_id` from the link.")

        except Exception:
            await message.reply("Error processing the link.")

    elif "links.lootlabs.gg" in content:
        await message.reply("Not YuB-X keysystem, please try again.")

bot.run(os.getenv("DISCORD_TOKEN"))
