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

@bot.command(name="bypass")
async def bypass(ctx, *, link: str = None):
    if not link:
        await ctx.reply("Usage: `!bypass [full link]`")
        return

    if "zoaTgCxk" not in link:
        await ctx.reply("Not YuB-X keysystem, please try again.")
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

            await ctx.reply(embed=embed)

        else:
            await ctx.reply("Could not find `sub_id`.")

    except Exception as e:
        await ctx.reply(f"Error: {str(e)[:300]}")

bot.run(os.getenv("DISCORD_TOKEN"))
