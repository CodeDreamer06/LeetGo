from os import getenv
import requests
import json
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

# TODO: Add TOC in readme.md
# TODO: Add description later
bot = commands.Bot(command_prefix='$', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.tree.sync()


@bot.event
async def on_message(message):
    if message.author == bot.user.name:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


# TODO: Ask user for username upon joining
# @client.event
# async def on_member_join(member):
#     await member.create_dm()
#     await member.dm_channel.send(
#         f'Hi {member.name}, welcome to my Discord server!'
#     )

# TODO: Let user change their username & let existing users input their username
# TODO: Implement a help command

@bot.tree.command(name='stats', description='Get basic LeetCode statistics')
# @app_commands.describe()
async def get_stats(interaction: discord.Interaction):
    # Ephemeral=True to show the message only to the executor of the slash command
    results = requests.get(
        'https://leetcodestats.cyclic.app/CodeDreamer06').json()
    fetch_map = {
        '☎️ Total Solved': 'totalSolved',
        '📊 Total Questions': 'totalQuestions',
        '✅ Easy Solved': 'easySolved',
        '🔢 Total Easy': 'totalEasy',
        '✅ Medium Solved': 'mediumSolved',
        '🔢 Total Medium': 'totalMedium',
        '✅ Hard Solved': 'hardSolved',
        # TODO: Show a ❌ if a user has solved 0 questions in a category
        # TODO: Separate each of the categories with an extra new line
        '🔢 Total Hard': 'totalHard',
        '🏆 Ranking': 'ranking',
        '🌟 Contribution Points': 'contributionPoints',
        '💯 Reputation': 'reputation'
    }
    details = '\n\n'.join(
        f'{key} : {results[value]}' for key, value in fetch_map.items())

    # TODO: Make sure that the username exists
    await interaction.response.send_message('🏁 Your LeetCode stats: \n\n' + details)


bot.run(getenv("BOT_TOKEN"))
