import os
import random
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

# ====== ENV TOKEN ======
load_dotenv()
DISCORD_TOKEN = os.getenv("MTQ2NDk0NDE4MjIwNzU3ODMzNw.Gkh-ud.Nj7OgARvhELSi2OGW4-r_8yzXap9V--qY6FjrQ")

# ====== INTENTS ======
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

# ====== DATA ======

shrek_quotes = [
    "🧅 Zlobři jsou jako cibule!",
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
    "ne": ["Bažina nesouhlasí.", "Ne*ře", "Tvoje ne je slabé.", "Řekl jsi ne, ale myslíš ano."],
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
    await interaction.response.send_message(f"🔥 {member.mention} {random.choice(roasts)}")

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

# ====== AUTO AI (funguje i se slash commands) ======

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    msg = message.content.lower()

    for key, replies in smart_triggers.items():
        if key in msg and random.random() < 0.35:
            await message.channel.send(random.choice(replies))
            break

    if random.random() < 0.05:
        await message.channel.send("😈 " + random.choice(ai_answers))

    if "shrek" in msg:
        await message.channel.send("🧅 Někdo mě volal z bažiny?")

    await bot.process_commands(message)

# ====== START ======
bot.run("MTQ2NDk0NDE4MjIwNzU3ODMzNw.Gkh-ud.Nj7OgARvhELSi2OGW4-r_8yzXap9V--qY6FjrQ")