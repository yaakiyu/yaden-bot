import discord
from discord.ext import commands
import os

bot = commands.Bot(command_prefix="ya!")

bot.run(os.getenv("TOKEN"))