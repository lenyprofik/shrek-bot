import os
import random
import logging
import sys
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from typing import Optional
import asyncio
import time
from database import init_db, get_user, add_xp, set_level_and_title

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
    "Mluv dál… aspoň se bažina zasměje.",
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

# Hezké odpovědi (20% šance)
nice_answers = [
    "Hele… nejsi tak špatnej, jak si myslíš.",
    "Bažina je lepší, když tu jsi.",
    "Možná jsem ogre… ale ty nejsi úplně k zahození.",
    "Někdy jsi fakt otravnej… ale mám tě docela rád.",
    "Víš… nejsi úplně marný. To je kompliment.",
    "Možná nejsi cibule… ale máš svoje vrstvy.",
    "Jsi lepší než většina, co sem vleze.",
    "Neříkej to nikomu, ale… jsi mi sympatickej.",
    "Jsi jako teplé bahno. Nepříjemné, ale vlastně uklidňující.",
    "Jsi světlo v bažině. Slabé, ale je tam."
]

# Nadávky
roasts = [
    "smrdíš jak mokrá bažina.",
    "vypadáš jak plesnivá cibule.",
    "jsi jak bahno po dešti-smrdíš.",
    "smrdíš víc než Osel po běhu.",
    "vypadáš jak cibule po týdnu v bahně.",
    "jsi jak žumpa na slunci.",
    "jsi jak šlem z bažiny.",
    "máš mozek jak mokrá houba.",
    "jsi jak plesnivý mech na kameni.",
    "smraďochu.",
    "cibulo.",
    "trole.",
    "bahňáku.",
    "žumpo.",
    "šlemáku.",
    "kundo.",
    "jsi se učit."
]

# Role reakce
role_replies = {
    "Rivals Master": [
        "Tak tohle je ten Rivals Master? Čekal jsem víc vrstev… i cibule má víc."
    ],
    "Pillars Master": [
        "Pillars Master… no jo, ten co si myslí, že je chytřejší než Shrek. Doufám že příště z toho pilíře spadneš"
    ],
    "Velkej Táta Shrek": [
        "Aha, velkej šéf bažiny přišel. Konečně někdo, kdo má větší IQ než Osel."
    ],
    "Lord Farquaad": [
        "Farquaad přišel… a bažina je hned o něco krásnější.🥵"
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
def xp_needed_for_level(level: int) -> int:
    if level < 3:
        return 50
    elif level < 10:
        return 70
    elif level < 15:
        return 80
    elif level < 20:
        return 100
    else:
        return 999999999  # level 20 je max


def title_for_level(level: int) -> str:
    if level < 3:
        return "Cibulový učedník"
    elif level < 10:
        return "Bahenní poutník"
    elif level < 15:
        return "Oslův rival"
    elif level < 20:
        return "Shrekův parťák"
    else:
        return "Legenda bažiny"
async def check_level_up(user, source):
    user_id = user["user_id"]
    xp = user["xp"]
    level = user["level"]

    needed = xp_needed_for_level(level)

    if xp < needed:
        return  # žádný level-up

    new_level = level + 1
    new_title = title_for_level(new_level)

    await set_level_and_title(user_id, new_level, new_title)

    # Rozlišení mezi zprávou a slash commandem
    if isinstance(source, discord.Message):
        guild = source.guild
        author = source.author
    else:
        guild = source.guild
        author = source.user

    # role při levelu 3
    if new_level == 3:
        role = discord.utils.get(guild.roles, name="Bahenní poutník")
        if role:
            await author.add_roles(role)

    # level-up hláška do leveling kanálu
    channel = discord.utils.get(guild.channels, name="shrek-levling⚡")
    if channel:
        await channel.send(
            f"🎉 **{author.mention} dosáhl levelu {new_level}!**\n"
            f"Titul: *{new_title}*\n"
            f"„Bažina tě začíná respektovat.“"
        )
# ====== READY + EVENT ENGINE ======
import asyncio  # musí být nahoře v importech

# ====== EVENT ENGINE ======
async def event_engine():
    await bot.wait_until_ready()

    channel = discord.utils.get(bot.get_all_channels(), name="shrekovy-eventy🧬")
    if not channel:
        print("⚠️ Event kanál 'shrekovy-eventy🧬' nebyl nalezen.")
        return

    while not bot.is_closed():
        # Náhodný interval 40–100 minut
        wait_minutes = random.randint(40, 100)
        await asyncio.sleep(wait_minutes * 60)

        guild = channel.guild
        online_members = [
            m for m in guild.members
            if m.status in (discord.Status.online, discord.Status.idle, discord.Status.dnd)
            and not m.bot
        ]

        if not online_members:
            await channel.send("🌫️ Bažina je tichá… nikdo není online.")
            continue

        roll = random.random()

        # 5 % šance na ultra-rare event: MINUS LEVEL
        if roll < 0.05:
            await channel.send(
                "💀 **Katastrofa v bažině!**\n"
                "Bažina se zlobí… všichni aktivní hráči ztrácejí **1 level**!"
            )

            for member in online_members:
                user = await get_user(member.id)
                old_level = user["level"]

                if old_level > 1:
                    new_level = old_level - 1
                    new_title = title_for_level(new_level)

                    await set_level_and_title(member.id, new_level, new_title)

                    # Odebrání role pokud spadnou pod level 3
                    if old_level >= 3 and new_level < 3:
                        role = discord.utils.get(guild.roles, name="Bahenní poutník")
                        if role and role in member.roles:
                            await member.remove_roles(role)

                    await channel.send(f"❌ {member.mention} spadl na level **{new_level}**!")
                else:
                    await channel.send(f"😬 {member.mention} je už na minimu… level 1 zůstává.")
            continue

        # 50 % šance na pozitivní event
        elif roll < 0.525:
            xp_gain = random.randint(10, 30)
            await channel.send(
                f"🌟 **Bažina žehná aktivním hráčům!**\n"
                f"Všichni online získávají **+{xp_gain} XP**!"
            )

            for member in online_members:
                await add_xp(member.id, xp_gain)
                user = await get_user(member.id)
                await check_level_up(user, channel)
            continue

        # 45 % šance na negativní event
        else:
            xp_loss = random.randint(5, 20)
            await channel.send(
                f"💨 **Bažina vypouští toxický plyn!**\n"
                f"Všichni online přicházejí o **-{xp_loss} XP**!"
            )

            for member in online_members:
                await add_xp(member.id, -xp_loss)
                user = await get_user(member.id)
                await check_level_up(user, channel)
            continue


# ====== READY ======
@bot.event
async def on_ready():
    await init_db()

    try:
        await tree.sync()
        logger.info(f"Slash commands synchronizovány jako: {bot.user}")
    except Exception as e:
        logger.exception("Chyba při syncu: %s", e)

    print(f"Bot je online jako {bot.user}")

    # Spuštění event enginu
    bot.loop.create_task(event_engine())
# ====== SLASH COMMANDS ======

@tree.command(name="shrek", description="Shrek řekne náhodnou hlášku")
async def shrek(interaction: discord.Interaction):
    user = await get_user(interaction.user.id)
    await add_xp(interaction.user.id, 1)
    user = await get_user(interaction.user.id)
    await check_level_up(user, interaction)
    await interaction.response.send_message(random.choice(shrek_quotes))


@tree.command(name="swamp", description="Vstup do Shrekovy bažiny")
async def swamp(interaction: discord.Interaction):
    user = await get_user(interaction.user.id)
    await add_xp(interaction.user.id, 1)
    user = await get_user(interaction.user.id)
    await check_level_up(user, interaction)
    await interaction.response.send_message("🏞️ Vítej v Shrekově bažině!")
    await interaction.followup.send(random.choice(swamp_events))


@tree.command(name="osel", description="Osel něco řekne")
async def osel(interaction: discord.Interaction):
    user = await get_user(interaction.user.id)
    await add_xp(interaction.user.id, 1)
    user = await get_user(interaction.user.id)
    await check_level_up(user, interaction)
    await interaction.response.send_message("🐴 Já jsem Osel! A jsem otravnej a hrdý na to!")


@tree.command(name="cibule", description="Zjisti, kolik vrstev má cibule")
async def cibule(interaction: discord.Interaction):
    user = await get_user(interaction.user.id)
    await add_xp(interaction.user.id, 1)
    user = await get_user(interaction.user.id)
    await check_level_up(user, interaction)
    vrstvy = random.randint(2, 10)
    await interaction.response.send_message(f"🧅 Tahle cibule má **{vrstvy} vrstev**. Jako ty.")


@tree.command(name="nadavka", description="Shrek někoho urazí")
async def nadavka(interaction: discord.Interaction, member: Optional[discord.Member] = None):
    user = await get_user(interaction.user.id)
    await add_xp(interaction.user.id, 1)
    user = await get_user(interaction.user.id)
    await check_level_up(user, interaction)
    if member:
        await interaction.response.send_message(f"😈 {member.mention}, Shrek říká: {random.choice(roasts)}")
    else:
        await interaction.response.send_message("😈 Koho mám urazit, ty cibulo?")


@tree.command(name="roast", description="Shrek někoho roastne")
async def roast(interaction: discord.Interaction, member: Optional[discord.Member] = None):
    user = await get_user(interaction.user.id)
    await add_xp(interaction.user.id, 1)
    user = await get_user(interaction.user.id)
    await check_level_up(user, interaction)
    if member:
        await interaction.response.send_message(f"🔥 {member.mention} {random.choice(roasts)}")
    else:
        await interaction.response.send_message("🔥 Koho mám hodit do bahna?")


@tree.command(name="ai", description="Shrek ti odpoví jako AI")
async def ai(interaction: discord.Interaction, text: str):
    user = await get_user(interaction.user.id)
    await add_xp(interaction.user.id, 1)
    user = await get_user(interaction.user.id)
    await check_level_up(user, interaction)
    await interaction.response.send_message(f"🧠 Shrek přemýšlí o: *{text}*")
    await interaction.followup.send(random.choice(ai_answers))


@tree.command(name="pomoc", description="Zobrazí seznam příkazů")
async def pomoc(interaction: discord.Interaction):
    user = await get_user(interaction.user.id)
    await add_xp(interaction.user.id, 1)
    user = await get_user(interaction.user.id)
    await check_level_up(user, interaction)

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
/profil
"""
    await interaction.response.send_message(text)


@tree.command(name="profil", description="Zobrazí tvůj Shrek level, XP a titul")
async def profil(interaction: discord.Interaction):
    user = await get_user(interaction.user.id)

    # bezpečné čtení hodnot (fallbacky pokud by chyběly)
    level = user.get("level", 1) if isinstance(user, dict) else 1
    xp = user.get("xp", 0) if isinstance(user, dict) else 0
    needed = xp_needed_for_level(level)
    title = title_for_level(level)

    await interaction.response.send_message(
        f"🧅 **Tvůj Shrek profil:**\n"
        f"**Level:** {level}\n"
        f"**XP:** {xp} / {needed}\n"
        f"**Titul:** *{title}*"
    )

# ====== START ======
if __name__ == "__main__":
    try:
        bot.run(DISCORD_TOKEN)
    except Exception as e:
        logger.exception("Bot se nepodařilo spustit: %s", e)
        sys.exit(1)