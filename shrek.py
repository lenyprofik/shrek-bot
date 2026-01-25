import os
import random
import logging
import sys
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from typing import Optional
import time

# ====== ENV TOKEN ======
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

if not DISCORD_TOKEN:
    print("ERROR: DISCORD_TOKEN není nastaven.")
    sys.exit(1)

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("shrek-bot")

# ====== INTENTS ======
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

# ====== DATA ======

# Normální Shrek hlášky
shrek_quotes = [
    "🧅 Ogres jsou jako cibule!",
    "🏞️ Tohle je moje bažina!",
    "😡 Co děláš v mojí bažině?!",
    "🐴 Osle, drž zobák!",
    "👑 Nejsem princ. Jsem Shrek.",
    "💚 Radši ven než dovnitř.",
    "🗿 Krása je uvnitř… ale já jsem krásný i venku.",
    "Bažina volá… a já odpovídám.",
    "Jestli sem vlezeš ještě jednou, udělám z tebe hnojivo.",
    "Mám hlad. A ty nevypadáš jedle.",
    "Někdo tu smrdí… a tentokrát to nejsem já.",
    "Jestli chceš moudro, běž za Fionou. Já ti dám jen pravdu.",
    "Máš problém? V bažině jich mám plno, přidej se.",
    "Nesnáším lidi. Ale tebe… tebe nesnáším o trochu víc."
]

# Události v bažině
swamp_events = [
    "Bažina bublá… něco smrdí. 💨",
    "Shrek hází bahno po okolí. 😂",
    "Osel zpívá… a Shrek ho chce umlčet. 🎤",
    "Ve vodě je podezřelá cibule. 🧅",
    "Shrek si označuje teritorium. 😈"
]

# AI odpovědi
ai_answers = [
    "Ty mluvíš… a bažina pláče.",
    "Tohle řekl někdo, kdo spadl do bahna po hlavě.",
    "Osle by to řekl líp. A to je co říct.",
    "Máš charisma mokré ponožky.",
    "Mluv dál… aspoň se bažina směje.",
    "Ty nejsi cibule. Ty jsi brambora.",
    "Když přemýšlíš, slyším šplouchání.",
    "Tohle není chyba. To je tvoje osobnost.",
    "Tohle je tak hluboké, že se bažina rozesmála.",
    "Kdybys přemýšlel víc, uvaříš si mozek.",
    "Tohle by ani Osel nechtěl slyšet.",
    "Jsi dno bažiny. Gratuluju.",
    "Máš pravdu… někde v paralelním vesmíru.",
    "Tohle je tak špatné, že radši sním syrovou cibuli.",
    "Bažina ti odpovídá: ‘Prosím, už nemluv.’",
    "Tohle je úroveň Farquaada… a to je co říct.",
    "Jestli tohle byla otázka, odpověď je NE.",
    "Tvůj mozek právě udělal *plop*.",
    "Tohle je tak mimo, že i drak by se urazil.",
    "Chceš být chytrý? Začni tím, že přestaneš psát.",
    "Tohle je tak špatné, že tě pošlu zpátky do bažiny na restart."
]

# Drsné roasty
roasts = [
    "je jak rozlitá cibulová polévka.",
    "má osobnost mokrého kamene.",
    "by prohrál i s Oslem v šachu.",
    "má charisma plesnivé houby.",
    "je legenda… v bažině trapnosti.",
    "má mozek jak mokrá houba po týdnu v bažině.",
    "vypadá, jako kdyby ho Osel učil žít.",
    "má styl jak rozšlapaná cibule.",
    "je tak slabý, že by ho porazila i Fiona po ránu.",
    "má ego větší než Farquaadův hrad, ale skill menší než Oslova trpělivost.",
    "je tak zbytečný, že by ho ani drak nesežral.",
    "má charisma jako mokrý mech na kameni.",
    "je tak pomalý, že by ho předběhla i bažina."
]

# Role reakce
role_replies = {
    "Rivals Master": [
        "Tak tohle je ten vítěz? Čekal jsem víc vrstev… i cibule má víc."
    ],
    "Pillars Master": [
        "Pillars Master… no jo, ten co si myslí, že je chytřejší než Shrek. Hodně štěstí."
    ],
    "Velkej Táta Shrek": [
        "Aha, velkej šéf bažiny přišel. Konečně někdo, kdo má větší ego než Osel."
    ],
    "Lord Farquaad": [
        "Farquaad přišel… a bažina je hned o něco krásnější."
    ]
}

# Cooldowny
last_role_reply = {
    "Rivals Master": 0,
    "Pillars Master": 0,
    "Velkej Táta Shrek": 0,
    "Lord Farquaad": 0
}

ROLE_COOLDOWN = 7200 


last_auto_ai = 0
AUTO_AI_COOLDOWN = 5

# ====== READY ======
@bot.event
async def on_ready():
    try:
        await tree.sync()
        logger.info(f"Slash commands synchronizovány jako: {bot.user}")
    except Exception as e:
        logger.exception("Chyba při syncu: %s", e)

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
async def nadavka(interaction: discord.Interaction, member: Optional[discord.Member] = None):
    if member:
        await interaction.response.send_message(f"😈 {member.mention}, Shrek říká: Jsi jak mokrá bažina!")
    else:
        await interaction.response.send_message("😈 Koho mám urazit, ty cibulo?")

@tree.command(name="roast", description="Shrek někoho roastne")
async def roast(interaction: discord.Interaction, member: Optional[discord.Member] = None):
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

# ====== ON MESSAGE ======

@bot.event
async def on_message(message):
    global last_role_reply, last_auto_ai

    if message.author == bot.user:
        return

    now = time.time()

    # 1) ROLE REAKCE (pokud proběhne → konec)
    if now - last_role_reply > ROLE_COOLDOWN:
        for role in message.author.roles:
            if role.name in role_replies:
                await message.channel.send(random.choice(role_replies[role.name]))
                last_role_reply = now
                return

    # 2) AUTO AI ODPOVĚĎ (pokud proběhne → konec)
    if now - last_auto_ai > AUTO_AI_COOLDOWN:
        msg = message.content.lower()

        triggers = ["ahoj", "jak", "proč", "lol", "ne"]
        if any(t in msg for t in triggers):
            await message.channel.send(random.choice(ai_answers))
            last_auto_ai = now
            return

        if "shrek" in msg:
            await message.channel.send("🧅 Někdo mě volal z bažiny?")
            last_auto_ai = now
            return

    # 3) Zpracování příkazů
    await bot.process_commands(message)

# ====== START ======
if __name__ == "__main__":
    try:
        bot.run(DISCORD_TOKEN)
    except Exception as e:
        logger.exception("Bot se nepodařilo spustit: %s", e)
        sys.exit(1)