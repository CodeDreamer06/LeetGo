from os import getenv
import requests
from dotenv import load_dotenv
import discord
from discord import app_commands
from discord.ext import commands
import sqlite3

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

connection = sqlite3.connect('storage.db')
c = connection.cursor()
c.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, discord_username TEXT NOT NULL, lc_username TEXT, roadmap INTEGER, cohort INTEGER, goal_questions INTEGER, goal_duration INTEGER, goal_start_date TEXT)')


def set_user(discord_username, lc_username):
    user_exists = c.execute(
        'SELECT * FROM users WHERE discord_username=?', (discord_username,)).fetchone()

    if user_exists:
        c.execute(
            'UPDATE users SET lc_username=? WHERE discord_username=?', (lc_username, discord_username))

    else:
        c.execute('INSERT INTO users (discord_username, lc_username) VALUES (?, ?)',
                  (discord_username, lc_username))

    connection.commit()


def get_lc_username(discord_username):
    user = c.execute('SELECT lc_username FROM users WHERE discord_username=?',
                     (discord_username,)).fetchone()
    if user:
        return user[0]
    else:
        return None


# TODO: Add TOC in readme.md
bot = commands.Bot(command_prefix='$',
                   description='LeetGo is a bot that allows programmers to keep track of their LeetCode progress.', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.tree.sync()


# TODO: Ask user for username upon joining
# @bot.event
# async def on_member_join(member):
#     await member.create_dm()
#     await member.dm_channel.send(
#         f'Hi {member.name}, welcome to my Discord server!'
#     )

@bot.tree.command(name='set-username', description='Set or change your username')
@app_commands.describe(username='What\'s your LeetCode username?')
async def set_username(interaction: discord.Interaction, username: str):
    set_user(str(interaction.user), username)
    await interaction.response.send_message(f'Done! {interaction.user}\'s username is now set to {username}')


@bot.tree.command(name='resources', description='Resources for learning and improving at competitive programming')
async def resources(interaction: discord.Interaction):
    await interaction.response.send_message('Resources')


@bot.tree.command(name='stats', description='Get basic LeetCode statistics')
async def get_stats(interaction: discord.Interaction):
    username = get_lc_username(str(interaction.user))
    if not username:
        await interaction.response.send_message('Please set your username by using the /set-username command.', ephemeral=True)
        return

    results = requests.get(
        f'https://leetcodestats.cyclic.app/{username}').json()

    if results['status'] == 'error':
        await interaction.response.send_message(f'Your username {username} was not found.', ephemeral=True)
        return

    fetch_map = {
        '☎️  Total Solved': 'totalSolved',
        '📊  Total Questions': 'totalQuestions',
        '✅  Easy Solved': 'easySolved',
        '🔢  Total Easy': 'totalEasy',
        '✅  Medium Solved': 'mediumSolved',
        '🔢  Total Medium': 'totalMedium',
        '✅  Hard Solved': 'hardSolved',
        '🔢  Total Hard': 'totalHard',
        '🏆  Ranking': 'ranking',
        '🌟  Contribution Points': 'contributionPoints',
        '💯  Reputation': 'reputation'
    }
    new_line_delimiter = '\n'
    difficulty_categories = ("easySolved", "mediumSolved", "hardSolved")
    details = '\n\n'.join(
        f'{(new_line_delimiter if value in difficulty_categories or value == "ranking" else "") + (key.replace("✅", "❌") if results[value] == 0 and value in difficulty_categories else key)}: {results[value]}' for key, value in fetch_map.items())

    await interaction.response.send_message('🏁 Your LeetCode stats: \n\n' + details)


bot.run(getenv("BOT_TOKEN"))
connection.close()
