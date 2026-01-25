pip instal discord.py
import discord
from discord.ext import commands
import random

# ====== NASTAVENÍ ======
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

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

# ====== EVENTY ======

@bot.event
async def on_ready():
    print(f"✅ Shrek bot online: {bot.user}")

# ====== PŘÍKAZY ======

@bot.command()
async def shrek(ctx):
    await ctx.send(random.choice(shrek_quotes))

@bot.command()
async def swamp(ctx):
    await ctx.send("🏞️ Vítej v Shrekově bažině!")
    await ctx.send(random.choice(swamp_events))

@bot.command()
async def osel(ctx):
    await ctx.send("🐴 Já jsem Osel! A jsem otravnej a hrdý na to!")

@bot.command()
async def cibule(ctx):
    vrstvy = random.randint(2, 10)
    await ctx.send(f"🧅 Tahle cibule má **{vrstvy} vrstev**. Jako ty.")

@bot.command()
async def nadavka(ctx, member: discord.Member = None):
    if member:
        await ctx.send(f"😈 {member.mention}, Shrek říká: Jsi jak mokrá bažina!")
    else:
        await ctx.send("😈 Koho mám urazit, ty cibulo?")

@bot.command()
async def roast(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("🔥 Koho mám hodit do bahna?")
        return

    roasts = [
        "je jak rozlitá cibulová polévka.",
        "má osobnost mokrého kamene.",
        "by prohrál i s Oslem v šachu.",
        "má charisma plesnivé houby.",
        "je legenda… v bažině trapnosti."
    ]

    await ctx.send(f"🔥 {member.mention} {random.choice(roasts)}")

@bot.command()
async def ai(ctx, *, text: str):
    await ctx.send(f"🧠 Shrek přemýšlí o: *{text}*")
    await ctx.send(random.choice(ai_answers))

@bot.command()
async def pomoc(ctx):
    text = """
🧅 **SHREK BOT CZ – PŘÍKAZY**

!shrek  
!swamp  
!osel  
!cibule  
!nadavka @uživatel  
!roast @uživatel  
!ai text  
!pomoc  
"""
    await ctx.send(text)

# ====== AUTO AI ======

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