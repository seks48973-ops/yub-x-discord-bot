import discord
import os
from discord.ext import commands
from urllib.parse import urlparse, parse_qs

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)  # Change to "$" if you want $bypass

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
        await ctx.reply("Please provide a link. Example: `!bypass https://links.lootlabs.gg/...`")
        return

    if "zoaTgCxk" not in link:
        await ctx.reply("Not YuB-X keysystem, please try again.")
        return

    try:
        parsed = urlparse(link)
        query_params = parse_qs(parsed.query)
        sub_id = query_params.get("sub_id", [None])[0]

        if not sub_id:
            await ctx.reply("Invalid link: No `sub_id` found.")
            return

        key_url = f"https://yub-x.best/get-key?rn=true&c={sub_id}"

        embed = discord.Embed(
            title="YuB-X Key System",
            description="Click the button below to get your key.",
            color=0x00ff00
        )
        embed.add_field(name="Status", value="Valid YuB-X link detected ✅", inline=False)

        await ctx.reply(embed=embed, view=KeyButtonView(key_url))

    except Exception:
        await ctx.reply("Error processing the link.")

bot.run(os.getenv("DISCORD_TOKEN"))
