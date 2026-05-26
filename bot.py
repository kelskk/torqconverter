import discord
from discord.ext import commands
from dotenv import load_dotenv

import os
import asyncio

# =========================
# ENV
# =========================

load_dotenv()

TOKEN = os.getenv(
    "TOKEN"
)

if not TOKEN:

    raise Exception(
        "TOKEN não encontrado"
    )

# =========================
# BOT
# =========================

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(

    command_prefix="!",

    intents=intents

)

os.makedirs(

    "temp",

    exist_ok=True

)

# =========================
# READY
# =========================

@bot.event
async def on_ready():

    await bot.tree.sync()

    print(

        f"ONLINE: {bot.user}"

    )

# =========================
# LOAD COGS
# =========================

async def load_cogs():

    for file in os.listdir(
        "cogs"
    ):

        if file.endswith(
            ".py"
        ):

            await bot.load_extension(

                f"cogs.{file[:-3]}"

            )

# =========================
# MAIN
# =========================

async def main():

    async with bot:

        await load_cogs()

        await bot.start(
            TOKEN
        )

asyncio.run(
    main()
)