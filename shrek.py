import os
import random
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

# ====== ENV TOKEN ======
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# ====== INTENTS ======
intents = discord.Intents.default()
intents.message_content = True

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
    await tree.sync()
    print(f"✅ Slash commands synchronizovány jako: {bot.user}")

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

@tree.command(name="nadavka", description="Shrek někoho urazí")
async def nadavka(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message(f"😈 {member.mention}, Shrek říká: Jsi jak mokrá bažina!")

@tree.command(name="roast", description="Shrek někoho roastne")
async def roast(interaction: discord.Interaction, member: discord.Member):
    roasts = [
        "je jak rozlitá cibulová polévka.",
        "má osobnost mokrého kamene.",
        "by prohrál i s Oslem v šachu.",
        "má charisma plesnivé houby.",
        "je legenda… v bažině trapnosti."
    ]
    await