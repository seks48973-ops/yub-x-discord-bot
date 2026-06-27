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

@bot.command(name="bypass")
async def bypass(ctx, *, link: str = None):
    if not link:
        await ctx.reply("Usage: `!bypass [full link]`")
        return

    if "zoaTgCxk" not in link:
        await ctx.reply("Not YuB-X keysystem, please try again.")
        return

    try:
        # Clean the link
        if link.startswith('<') and link.endswith('>'):
            link = link[1:-1]

        parsed = urlparse(link)
        query = parsed.query

        # Handle both &sub_id= and sub_id= formats
        if "sub_id=" in query:
            sub_id_part = query.split("sub_id=")[1].split("&")[0]
            sub_id = sub_id_part.strip()
        else:
            await ctx.reply("Could not find sub_id in the link.")
            return

        if not sub_id:
            await ctx.reply("Could not find sub_id in the link.")
            return

        key_url = f"https://yub-x.best/get-key?rn=true&c={sub_id}"

        embed = discord.Embed(
            title="YuB-X Key System",
            description="Click the button below to get your key.",
            color=0x00ff00
        )

        await ctx.reply(embed=embed, view=KeyButtonView(key_url))

    except Exception as e:
        await ctx.reply("Error processing the link.")
        print(f"Error: {e}")

bot.run(os.getenv("DISCORD_TOKEN"))
