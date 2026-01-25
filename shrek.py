import os
import random
import logging
import sys
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from typing import Optional

# ====== ENV TOKEN ======
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# ====== BASIC CHECKS ======
if not DISCORD_TOKEN:
    # Pokud token není nastaven, skončíme s chybou (prevence NoneType tokenu)
    print("ERROR: DISCORD_TOKEN není nastaven. Nastav proměnnou prostředí v Railway nebo .env souboru.")
    sys.exit(1)

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("shrek-bot")

# ====== INTENTS ======
intents = discord.Intents.default()
intents.message_content = True  # potřeba pro on_message

# ====== BOT & TREE ======
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

# ====== DATA ======
shrek_quotes = [
    "🧅 Ogres jsou jako cibule!",
    "🏞️ Tohle je moje bažina!",
    "😡 Co děláš v mojí bažině?!",
    "🐴 Osle, drž zobák!",
    "👑 Nejsem princ. Jsem Shrek.",
    "💚 Radši ven než dovnitř.",
    "🗿 Krása je uvnitř… ale já jsem krásný i venku.",
]

swamp_events = [
    "Bažina bublá… něco smrdí. 💨",
    "Shrek hází bahno po okolí. 😂",
    "Osel zpívá… a Shrek ho chce umlčet. 🎤",
    "Ve vodě je podezřelá cibule. 🧅",
    "Shrek si označuje teritorium. 😈"
]

ai_answers = [
    "Ty mluvíš… a bažina pláče.",
    "Tohle řekl někdo, kdo spadl do bahna po hlavě.",
    "Osle by to řekl líp. A to je co říct.",
    "Máš charisma mokré ponožky.",
    "Mluv dál… aspoň se bažina směje.",
    "Ty nejsi cibule. Ty jsi brambora.",
    "Když přemýšlíš, slyším šplouchání.",
    "Tohle není chyba. To je tvoje osobnost."
]

smart_triggers = {
    "ahoj": ["Nazdar, cibulo.", "Čau. Nešlapej mi po bahně.", "Zdravím, návštěvníku bažiny."],
    "jak": ["Jak? Blbě.", "Na styl Shreka.", "S bahnem a elegancí."],
    "proč": ["Protože bažina rozhodla.", "Protože Osel mlčí.", "Protože Shrek řekl."],
    "lol": ["Směj se, než uklouzneš.", "Haha… bažina má humor.", "Tvůj smích zní jak žába."],
    "ne": ["Bažina nesouhlasí.", "Tvoje ne je slabé.", "Řekl jsi ne, ale myslíš ano."],
}

# ====== READY EVENT ======
@bot.event
async def on_ready():
    try:
        # Pokud chceš rychlejší vývoj, můžeš synchronizovat jen do jedné testovací guildy:
        # GUILD_ID = 123456789012345678
        # await tree.sync(guild=discord.Object(id=GUILD_ID))
        await tree.sync()
        logger.info(f"✅ Slash commands synchronizovány jako: {bot.user}")
    except Exception as e:
        logger.exception("Chyba při synchronizaci slash commands: %s", e)

# ====== SLASH COMMANDS ======
@tree.command(name="shrek", description="Shrek řekne náhodnou hlášku")
async def shrek(interaction: discord.Interaction):
    await interaction.response.send_message(random.choice(shrek_quotes))

@tree.command(name="swamp", description="Vstup do Shrekovy bažiny")
async def swamp(interaction: discord.Interaction):
    await interaction.response.send_message("🏞️ Vítej v Shrekově bažině!")
    await interaction.followup.send(random.choice(swamp_events))

@tree.command(name="osel", description="Osel něco řekne")
async def osel(interaction: discord.Interaction):
    await interaction.response.send_message("🐴 Já jsem Osel! A jsem otravnej a hrdý na to!")

@tree.command(name="cibule", description="Zjisti, kolik vrstev má cibule")
async def cibule(interaction: discord.Interaction):
    vrstvy = random.randint(2, 10)
    await interaction.response.send_message(f"🧅 Tahle cibule má **{vrstvy} vrstev**. Jako ty.")

# member je volitelný; pokud není zvolen, bot odpoví obecně
@tree.command(name="nadavka", description="Shrek někoho urazí (volitelně vyber uživatele)")
async def nadavka(interaction: discord.Interaction, member: Optional[discord.Member] = None):
    if member:
        await interaction.response.send_message(f"😈 {member.mention}, Shrek říká: Jsi jak mokrá bažina!")
    else:
        await interaction.response.send_message("😈 Koho mám urazit, ty cibulo?")

@tree.command(name="roast", description="Shrek někoho roastne (volitelně vyber uživatele)")
async def roast(interaction: discord.Interaction, member: Optional[discord.Member] = None):
    roasts = [
        "je jak rozlitá cibulová polévka.",
        "má osobnost mokrého kamene.",
        "by prohrál i s Oslem v šachu.",
        "má charisma plesnivé houby.",
        "je legenda… v bažině trapnosti."
    ]
    if member:
        await interaction.response.send_message(f"🔥 {member.mention} {random.choice(roasts)}")
    else:
        await interaction.response.send_message("🔥 Koho mám hodit do bahna?")

@tree.command(name="ai", description="Shrek ti odpoví jako AI")
async def ai(interaction: discord.Interaction, text: str):
    await interaction.response.send_message(f"🧠 Shrek přemýšlí o: *{text}*")
    await interaction.followup.send(random.choice(ai_answers))

@tree.command(name="pomoc", description="Zobrazí seznam příkazů")
async def pomoc(interaction: discord.Interaction):
    text = """
🧅 **SHREK BOT CZ – SLASH PŘÍKAZY**

/shrek  
/swamp  
/osel  
/cibule  
/nadavka @uživatel  
/roast @uživatel  
/ai text  
/pomoc  
"""
    await interaction.response.send_message(text)

# ====== AUTO AI (on_message) ======
# jednoduchý cooldown pro automatické odpovědi (prevence spamu)
_auto_ai_last = 0
_AUTO_AI_COOLDOWN = 5  # v sekundách

@bot.event
async def on_message(message):
    global _auto_ai_last
    if message.author == bot.user:
        return

    # zpracuj příkazy nejdřív
    await bot.process_commands(message)

    # automatické odpovědi (jen pokud je cooldown uplynul)
    import time
    now = time.time()
    if now - _auto_ai_last < _AUTO_AI_COOLDOWN:
        return

    msg = message.content.lower()

    for key, replies in smart_triggers.items():
        if key in msg and random.random() < 0.35:
            await message.channel.send(random.choice(replies))
            _auto_ai_last = now
            return

    if random.random() < 0.05:
        await message.channel.send("😈 " + random.choice(ai_answers))
        _auto_ai_last = now
        return

    if "shrek" in msg:
        await message.channel.send("🧅 Někdo mě volal z bažiny?")
        _auto_ai_last = now

# ====== GLOBAL ERROR HANDLING FOR COMMANDS ======
@bot.event
async def on_command_error(ctx, error):
    # Loguj chybu a informuj uživatele stručně
    logger.exception("Chyba v příkazu: %s", error)
    try:
        await ctx.send("Došlo k chybě při vykonávání příkazu. Mrkni do logu.")
    except Exception:
        pass

# ====== START ======
if __name__ == "__main__":
    try:
        bot.run(DISCORD_TOKEN)
    except Exception as e:
        logger.exception("Bot se nepodařilo spustit: %s", e)
        sys.exit(1)