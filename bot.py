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

    content = message.content.strip()
    debug_info = []

    if "links.lootlabs.gg" in content and "zoaTgCxk" in content:
        debug_info.append("✅ Detected valid YuB-X lootlabs link")

        try:
            # Debug: Show first part of the link
            debug_info.append(f"Link length: {len(content)} characters")

            # Try to find sub_id
            sub_id_match = re.search(r'sub_id=([^&\s]+)', content)
            
            if sub_id_match:
                sub_id = sub_id_match.group(1)
                debug_info.append(f"✅ Extracted sub_id (length: {len(sub_id)})")
                
                key_url = f"https://yub-x.best/get-key?rn=true&c={sub_id}"
                debug_info.append("✅ Built key URL")

                embed = discord.Embed(
                    title="YuB-X Key System",
                    description="Click the button below to get your key.",
                    color=0x00ff00
                )

                await message.reply(embed=embed, view=KeyButtonView(key_url))
                return
            else:
                debug_info.append("❌ Could not find sub_id with regex")

            await message.reply("\n".join(debug_info))

        except Exception as e:
            debug_info.append(f"❌ Error: {str(e)[:300]}")
            await message.reply("\n".join(debug_info))

    elif "links.lootlabs.gg" in content:
        await message.reply("Not YuB-X keysystem, please try again.")

bot.run(os.getenv("DISCORD_TOKEN"))
