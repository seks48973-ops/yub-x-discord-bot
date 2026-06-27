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
        await ctx.reply("Usage: `!bypass [link]`")
        return

    await ctx.reply(f"Debug: Link received ({len(link)} characters)")

    if "zoaTgCxk" not in link:
        await ctx.reply("Not YuB-X keysystem.")
        return

    try:
        sub_id_match = re.search(r'sub_id=([^&\s]+)', link)
        
        if sub_id_match:
            sub_id = sub_id_match.group(1)
            await ctx.reply(f"Found sub_id: `{sub_id[:50]}...`")  # Show part of it
            
            key_url = f"https://yub-x.best/get-key?rn=true&c={sub_id}"
            view = discord.ui.View()
            view.add_item(discord.ui.Button(label="Get Key", style=discord.ButtonStyle.green, url=key_url))
            await ctx.reply("Here is your key link:", view=view)
        else:
            await ctx.reply("Could not find `sub_id` in the link. Please send the full link.")

    except Exception as e:
        await ctx.reply(f"Error: {str(e)[:500]}")

bot.run(os.getenv("DISCORD_TOKEN"))
