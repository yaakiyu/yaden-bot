import discord
from discord.ext import commands
import os

bot = commands.Bot(
    command_prefix="ya!",
    help_command=None
)

bot.load_extension("cogs._first")

bot.run(os.getenv("TOKEN"))