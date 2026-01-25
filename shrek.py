# shrek.py
import os
import logging
import asyncio
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands

from database import init_db, get_user, set_title, touch_user

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("shrek-bot")

# Intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = False

# Bot setup
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

@bot.event
async def on_ready():
    # Inicializace DB před synchronizací příkazů
    await init_db()
    await tree.sync()
    logger.info(f"Bot je online jako {bot.user} (id: {bot.user.id})")

# Simple slash command that touches user record
@tree.command(name="shrek", description="Pozdraví a aktualizuje poslední přítomnost uživatele")
async def shrek(interaction: discord.Interaction):
    user_id = interaction.user.id
    await touch_user(user_id)
    await interaction.response.send_message(f"Ahoj {interaction.user.display_name} — zaznamenal jsem tě.", ephemeral=True)

# Profile command shows stored info
@tree.command(name="profil", description="Zobrazí informace o tobě z databáze")
async def profil(interaction: discord.Interaction):
    user_id = interaction.user.id
    row = await get_user(user_id)
    if not row:
        await interaction.response.send_message("Nemám o tobě žádné informace.", ephemeral=True)
        return

    title = row.get("title") or "Žádný titul"
    created = row.get("created_at")
    last_seen = row.get("last_seen")

    created_str = created.strftime("%Y-%m-%d %H:%M:%S UTC") if isinstance(created, datetime) else str(created)
    last_seen_str = last_seen.strftime("%Y-%m-%d %H:%M:%S UTC") if isinstance(last_seen, datetime) else str(last_seen)

    embed = discord.Embed(title=f"Profil {interaction.user.display_name}", color=discord.Color.green())
    embed.add_field(name="Titul", value=title, inline=False)
    embed.add_field(name="Vytvořeno", value=created_str, inline=True)
    embed.add_field(name="Naposledy viděn", value=last_seen_str, inline=True)
    await interaction.response.send_message(embed=embed, ephemeral=True)

# Command to set a title
@tree.command(name="nastav_titul", description="Nastaví tvůj titul v DB")
@app_commands.describe(titul="Text titulu, který chceš uložit")
async def nastav_titul(interaction: discord.Interaction, titul: str):
    user_id = interaction.user.id
    await set_title(user_id, titul)
    await interaction.response.send_message(f"Titul nastaven na: {titul}", ephemeral=True)

# Run
if __name__ == "__main__":
    if not DISCORD_TOKEN:
        logger.error("DISCORD_TOKEN není nastaven v proměnných prostředí.")
    else:
        bot.run(DISCORD_TOKEN)