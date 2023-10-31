from os import getenv
import requests
from dotenv import load_dotenv
import discord
from discord import app_commands
from discord.ext import commands
import leetcode
from leetcode.auth import get_csrf_cookie
from database import Database

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

leetcode_session = getenv('LEETCODE_SESSION')
csrf_token = get_csrf_cookie(leetcode_session)
configuration = leetcode.Configuration()
configuration.api_key["x-csrftoken"] = csrf_token
configuration.api_key["csrftoken"] = csrf_token
configuration.api_key["LEETCODE_SESSION"] = leetcode_session
configuration.api_key["Referer"] = "https://leetcode.com"
configuration.debug = False

api_instance = leetcode.DefaultApi(leetcode.ApiClient(configuration))
graphql_request = leetcode.GraphqlQuery(
    query="""
        {
        user {
                username
            }
        }
        """,
    variables=leetcode.GraphqlQueryVariables(),
)

print(api_instance.graphql_post(body=graphql_request))

db = Database()

# api_response = api_instance.api_problems_topic_get(topic="algorithms")
# solved_questions = []
# for questions in api_response.stat_status_pairs:
#     if questions.status == "ac":
#         solved_questions.append(questions.stat.question__title)
# print(solved_questions)
# print("Total number of solved questions:", len(solved_questions))


def set_user(discord_username, lc_username):
    """Adds or edits a user's name in the database"""
    if db.does_the_user_exist(discord_username):
        db.change_user_name(discord_username, lc_username)

    else:
        db.add_user(discord_username, lc_username)


bot = commands.Bot(command_prefix='$',
                   description='LeetGo is a bot that allows programmers to keep track of their LeetCode progress.', intents=intents)


@bot.event
async def on_ready():
    """Runs when the bot is up and ready"""
    print(f'Logged in as {bot.user.name}')
    print(db.get_all_cohorts())
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
    """Slash command that changes or adds the username to the database"""
    set_user(str(interaction.user), username)
    await interaction.response.send_message(f'Done! {interaction.user}\'s username is now set to {username}')


@bot.tree.command(name='resources', description='Resources for learning and improving at competitive programming')
async def resources(interaction: discord.Interaction):
    """Slash command that displays resources to learn and improve at competitive programming"""
    # TODO: Populate resources
    await interaction.response.send_message('Resources')


@bot.tree.command(name='roadmap', description='Pick a roadmap to follow through')
async def roadmap(interaction: discord.Interaction):
    """Slash command that allows the user to select a roadmap"""
    # TODO: Add roadmaps here
    await interaction.response.send_message('Roadmap')


@bot.tree.command(name='host-a-cohort', description='Host a cohort')
@app_commands.describe(name='What\'s the name of the cohort?')
async def host_a_cohort(interaction: discord.Interaction, name: str):
    """Slash command that allows the user to host a cohort"""
    channel_name = name.lower().replace(' ', '-')
    existing_category = discord.utils.get(
        interaction.guild.categories, name='Cohorts')
    existing_channel = discord.utils.get(
        existing_category.channels, name=channel_name)

    if existing_channel:
        await interaction.response.send_message(f'Channel **{channel_name}** already exists!', ephemeral=True)
        return

    if db.get_user_cohort(interaction.user.name):
        await interaction.response.send_message('You cannot join more than one cohort at a time. Please exit your current cohort.', ephemeral=True)
        return

    db.create_cohort(channel_name, str(interaction.user))
    await interaction.guild.create_text_channel(channel_name, category=existing_category)
    await interaction.response.send_message(f'Channel **{channel_name}** has been created! \nFor others to join this cohort, use the /join-a-cohort command, or react to this message with a thumbs up!', ephemeral=True)


@bot.tree.command(name='join-a-cohort', description='Join a cohort')
async def join_a_cohort(interaction: discord.Interaction):
    """Slash command that allows the user to join a cohort"""
    await interaction.response.send_message('Join a cohort')


@bot.tree.command(name='view-remainders', description='View your remainders')
async def view_remainders(interaction: discord.Interaction):
    """Slash command that allows the user to view their remainders"""
    await interaction.response.send_message('Remainders:')


@bot.tree.command(name='set-remainders', description='Set your remainders')
async def set_remainders(interaction: discord.Interaction):
    """Slash command that allows the user to set remainders"""
    await interaction.response.send_message('set')


@bot.tree.command(name='set-goal', description='Set a goal for yourself')
@app_commands.describe(questions='What\'s the number of questions you\'d like to solve?', months='In how many months would you want to achieve your goal?')
async def set_goal(interaction: discord.Interaction, questions: int, months: int):
    """Slash command that allows the user to set a goal for themselves"""
    await interaction.response.send_message(f'You\'d like to solve {questions} questions in {months} months.')


@bot.tree.command(name='stats', description='Get basic LeetCode statistics')
async def get_stats(interaction: discord.Interaction):
    """Slash command that allows the user to check their leetcode statistics"""
    username = db.find_user(str(interaction.user))
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
db.kill()
