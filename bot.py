import discord
import os
from discord.ext import commands
from urllib.parse import urlparse, parse_qs

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

    if "links.lootlabs.gg/s?zoaTgCxk" in content:
        try:
            # Extract URL
            url = None
            for word in content.split():
                if word.startswith("https://links.lootlabs.gg/s?zoaTgCxk"):
                    url = word
                    break

            if not url:
                return

            parsed = urlparse(url)
            query_params = parse_qs(parsed.query)
            sub_id_list = query_params.get("sub_id")

            if not sub_id_list:
                await message.reply("Invalid link: No `sub_id` found.")
                return

            sub_id = sub_id_list[0]
            key_url = f"https://yub-x.best/get-key?rn=true&c={sub_id}"

            embed = discord.Embed(
                title="YuB-X Key System",
                description="Click the button below to get your key.",
                color=0x00ff00
            )
            embed.add_field(name="Status", value="Valid YuB-X link detected ✅", inline=False)

            await message.reply(embed=embed, view=KeyButtonView(key_url))

        except Exception:
            await message.reply("Error processing the link.")

    elif "links.lootlabs.gg" in content and "zoaTgCxk" not in content:
        await message.reply("Not YuB-X keysystem, please try again.")

# Run the bot
bot.run(os.getenv("DISCORD_TOKEN"))
