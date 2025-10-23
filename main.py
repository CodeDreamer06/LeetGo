from os import getenv
import requests
from dotenv import load_dotenv
import discord
from discord import app_commands
from discord.ext import commands, tasks
from database import Database
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('leetgo.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('LeetGo')

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

# Initialize local database instance
db = Database()

# Roadmap options
ROADMAPS = {
    "Beginner": {
        "description": "Start your coding journey with fundamental algorithms and data structures",
        "topics": ["Arrays", "Strings", "Hash Tables", "Two Pointers", "Sliding Window"]
    },
    "Intermediate": {
        "description": "Build on fundamentals with more complex patterns",
        "topics": ["Binary Search", "Trees", "Graphs", "Dynamic Programming (Basic)", "Backtracking"]
    },
    "Advanced": {
        "description": "Master advanced algorithms and optimization techniques",
        "topics": ["Advanced DP", "Graph Algorithms", "Segment Trees", "Trie", "Advanced Math"]
    },
    "Interview Prep": {
        "description": "Focus on commonly asked interview questions",
        "topics": ["Top 150 Questions", "System Design Basics", "Behavioral Prep", "Mock Interviews"]
    }
}


def set_user(discord_username, lc_username):
    """Adds or edits a user's name in the database"""
    try:
        if db.does_the_user_exist(discord_username):
            db.change_user_name(discord_username, lc_username)
            logger.info(f"Updated username for {discord_username} to {lc_username}")
        else:
            db.add_user(discord_username, lc_username)
            logger.info(f"Added new user {discord_username} with LeetCode username {lc_username}")
    except Exception as e:
        logger.error(f"Error setting user {discord_username}: {e}")
        raise


bot = commands.Bot(command_prefix='$',
                   description='LeetGo is a bot that allows programmers to keep track of their LeetCode progress.', intents=intents)


@bot.event
async def on_ready():
    """Runs when the bot is up and ready"""
    logger.info(f'Logged in as {bot.user.name}')
    try:
        cohorts = db.get_all_cohorts()
        logger.info(f"Active cohorts: {len(cohorts)}")
        await bot.tree.sync()
        logger.info("Command tree synced successfully")
        
        # Start reminder task
        if not check_reminders.is_running():
            check_reminders.start()
            logger.info("Reminder task started")
    except Exception as e:
        logger.error(f"Error during bot startup: {e}")


@bot.event
async def on_error(event, *args, **kwargs):
    """Global error handler for events"""
    logger.error(f"Error in event {event}", exc_info=True)

@bot.tree.command(name='set-username', description='Set or change your LeetCode username')
@app_commands.describe(username='What\'s your LeetCode username?')
async def set_username(interaction: discord.Interaction, username: str):
    """Slash command that changes or adds the username to the database"""
    try:
        if not username or len(username.strip()) == 0:
            await interaction.response.send_message('Please provide a valid username.', ephemeral=True)
            return
        
        username = username.strip()
        set_user(str(interaction.user), username)
        await interaction.response.send_message(f'✅ Done! {interaction.user}\'s username is now set to **{username}**')
        logger.info(f"User {interaction.user} set LeetCode username to {username}")
    except Exception as e:
        logger.error(f"Error in set_username command: {e}")
        await interaction.response.send_message('❌ An error occurred while setting your username. Please try again.', ephemeral=True)

class RoadmapView(discord.ui.View):
    """View for selecting a roadmap"""
    def __init__(self, user_id: int):
        super().__init__(timeout=180)
        self.user_id = user_id
        self.value = None

    @discord.ui.select(
        placeholder="Choose your learning path...",
        options=[
            discord.SelectOption(label="Beginner", description="Fundamental algorithms and data structures", emoji="🌱"),
            discord.SelectOption(label="Intermediate", description="Build on fundamentals with complex patterns", emoji="📈"),
            discord.SelectOption(label="Advanced", description="Master advanced algorithms", emoji="🚀"),
            discord.SelectOption(label="Interview Prep", description="Focus on interview questions", emoji="💼")
        ]
    )
    async def select_roadmap(self, interaction: discord.Interaction, select: discord.ui.Select):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This menu is not for you!", ephemeral=True)
            return
        
        self.value = select.values[0]
        roadmap_data = ROADMAPS[self.value]
        
        try:
            # Save roadmap to database
            db.set_user_roadmap(str(interaction.user), self.value)
            
            embed = discord.Embed(
                title=f"📚 {self.value} Roadmap Selected",
                description=roadmap_data["description"],
                color=discord.Color.green()
            )
            embed.add_field(
                name="Topics to Cover",
                value="\n".join(f"• {topic}" for topic in roadmap_data["topics"]),
                inline=False
            )
            embed.set_footer(text="Good luck on your learning journey!")
            
            await interaction.response.edit_message(content=None, embed=embed, view=None)
            logger.info(f"User {interaction.user} selected {self.value} roadmap")
        except Exception as e:
            logger.error(f"Error saving roadmap: {e}")
            await interaction.response.send_message("❌ Error saving roadmap. Please try again.", ephemeral=True)

@bot.tree.command(name='roadmap', description='Select a learning roadmap to follow')
async def roadmap(interaction: discord.Interaction):
    """Slash command that allows the user to select a roadmap"""
    try:
        # Check if user has set their username
        username = db.find_user(str(interaction.user))
        if not username:
            await interaction.response.send_message('Please set your LeetCode username first using `/set-username`.', ephemeral=True)
            return
        
        # Check if user already has a roadmap
        current_roadmap = db.get_user_roadmap(str(interaction.user))
        
        embed = discord.Embed(
            title="🗺️ Choose Your Learning Path",
            description="Select a roadmap that matches your current skill level and goals.",
            color=discord.Color.blue()
        )
        
        if current_roadmap:
            embed.add_field(
                name="Current Roadmap",
                value=f"**{current_roadmap}**",
                inline=False
            )
        
        view = RoadmapView(interaction.user.id)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        logger.info(f"User {interaction.user} opened roadmap selection")
    except Exception as e:
        logger.error(f"Error in roadmap command: {e}")
        await interaction.response.send_message('❌ An error occurred. Please try again.', ephemeral=True)


@bot.tree.command(name='host-a-cohort', description='Create and host a study cohort')
@app_commands.describe(name='What\'s the name of the cohort?')
async def host_a_cohort(interaction: discord.Interaction, name: str):
    """Slash command that allows the user to host a cohort"""
    try:
        if not name or len(name.strip()) == 0:
            await interaction.response.send_message('❌ Please provide a valid cohort name.', ephemeral=True)
            return
        
        name = name.strip()
        channel_name = name.lower().replace(' ', '-')
        
        # Check if user has set their username
        username = db.find_user(str(interaction.user))
        if not username:
            await interaction.response.send_message('Please set your LeetCode username first using `/set-username`.', ephemeral=True)
            return
        
        existing_category = discord.utils.get(
            interaction.guild.categories, name='Cohorts')
        
        if not existing_category:
            await interaction.response.send_message('❌ The "Cohorts" category does not exist. Please ask a server admin to create it.', ephemeral=True)
            logger.warning(f"Cohorts category not found in guild {interaction.guild.name}")
            return
        
        existing_channel = discord.utils.get(
            existing_category.channels, name=channel_name)

        if existing_channel:
            await interaction.response.send_message(f'❌ Channel **{channel_name}** already exists!', ephemeral=True)
            return

        if db.get_user_cohort(str(interaction.user)):
            await interaction.response.send_message('❌ You cannot join more than one cohort at a time. Please use `/leave-cohort` first.', ephemeral=True)
            return

        db.create_cohort(channel_name, str(interaction.user))
        new_channel = await interaction.guild.create_text_channel(channel_name, category=existing_category)
        
        # Send welcome message to the new cohort channel
        welcome_embed = discord.Embed(
            title=f"🎉 Welcome to {name}!",
            description=f"This cohort was created by {interaction.user.mention}",
            color=discord.Color.green()
        )
        welcome_embed.add_field(
            name="How to Join",
            value="Others can join this cohort using `/join-a-cohort`",
            inline=False
        )
        await new_channel.send(embed=welcome_embed)
        
        await interaction.response.send_message(f'✅ Channel **{channel_name}** has been created! Others can join using `/join-a-cohort`.', ephemeral=True)
        logger.info(f"User {interaction.user} created cohort {channel_name}")
    except discord.Forbidden:
        await interaction.response.send_message('❌ I don\'t have permission to create channels. Please contact a server admin.', ephemeral=True)
        logger.error(f"Missing permissions to create channel in {interaction.guild.name}")
    except Exception as e:
        logger.error(f"Error in host_a_cohort command: {e}")
        await interaction.response.send_message('❌ An error occurred while creating the cohort. Please try again.', ephemeral=True)

class CohortSelectView(discord.ui.View):
    """View for selecting a cohort to join"""
    def __init__(self, user_id: int, cohorts: list):
        super().__init__(timeout=180)
        self.user_id = user_id
        self.value = None
        
        options = [
            discord.SelectOption(
                label=cohort[1],
                description=f"Cohort ID: {cohort[0]}",
                value=str(cohort[0])
            )
            for cohort in cohorts[:25]  # Discord limit
        ]
        
        select = discord.ui.Select(
            placeholder="Choose a cohort to join...",
            options=options
        )
        select.callback = self.select_cohort
        self.add_item(select)
    
    async def select_cohort(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This menu is not for you!", ephemeral=True)
            return
        
        cohort_id = int(self.children[0].values[0])
        cohort_name = next(opt.label for opt in self.children[0].options if opt.value == str(cohort_id))
        
        try:
            db.update_user_cohort(str(interaction.user), cohort_id)
            
            embed = discord.Embed(
                title="✅ Successfully Joined Cohort",
                description=f"You are now a member of **{cohort_name}**!",
                color=discord.Color.green()
            )
            embed.set_footer(text="Good luck with your studies!")
            
            await interaction.response.edit_message(content=None, embed=embed, view=None)
            logger.info(f"User {interaction.user} joined cohort {cohort_name}")
        except Exception as e:
            logger.error(f"Error joining cohort: {e}")
            await interaction.response.send_message("❌ Error joining cohort. Please try again.", ephemeral=True)

@bot.tree.command(name='join-a-cohort', description='Join an existing study cohort')
async def join_a_cohort(interaction: discord.Interaction):
    """Slash command that allows the user to join a cohort"""
    try:
        # Check if user has set their username
        username = db.find_user(str(interaction.user))
        if not username:
            await interaction.response.send_message('Please set your LeetCode username first using `/set-username`.', ephemeral=True)
            return
        
        # Check if user is already in a cohort
        if db.get_user_cohort(str(interaction.user)):
            await interaction.response.send_message('❌ You are already in a cohort. Use `/leave-cohort` first if you want to switch.', ephemeral=True)
            return
        
        # Get all available cohorts
        cohorts = db.get_all_cohorts()
        
        if not cohorts:
            await interaction.response.send_message('❌ No cohorts available. Create one using `/host-a-cohort`!', ephemeral=True)
            return
        
        embed = discord.Embed(
            title="📚 Available Cohorts",
            description="Select a cohort to join from the dropdown below.",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="Total Cohorts",
            value=str(len(cohorts)),
            inline=False
        )
        
        view = CohortSelectView(interaction.user.id, cohorts)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        logger.info(f"User {interaction.user} opened cohort selection")
    except Exception as e:
        logger.error(f"Error in join_a_cohort command: {e}")
        await interaction.response.send_message('❌ An error occurred. Please try again.', ephemeral=True)

@bot.tree.command(name='leave-cohort', description='Leave your current cohort')
async def leave_cohort(interaction: discord.Interaction):
    """Slash command that allows the user to leave their current cohort"""
    try:
        cohort_id = db.get_user_cohort(str(interaction.user))
        
        if not cohort_id:
            await interaction.response.send_message('❌ You are not in any cohort.', ephemeral=True)
            return
        
        cohort_name = db.get_cohort_name(cohort_id)
        db.remove_user_from_cohort(str(interaction.user))
        
        embed = discord.Embed(
            title="👋 Left Cohort",
            description=f"You have left **{cohort_name}**.",
            color=discord.Color.orange()
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        logger.info(f"User {interaction.user} left cohort {cohort_name}")
    except Exception as e:
        logger.error(f"Error in leave_cohort command: {e}")
        await interaction.response.send_message('❌ An error occurred. Please try again.', ephemeral=True)


@bot.tree.command(name='set-reminders', description='Configure daily study reminders')
@app_commands.describe(
    hour='Hour of the day (0-23) to receive reminders',
    minute='Minute of the hour (0-59) to receive reminders'
)
async def set_reminders(interaction: discord.Interaction, hour: int, minute: int):
    """Slash command that allows the user to set reminders"""
    try:
        # Validate inputs
        if not (0 <= hour <= 23):
            await interaction.response.send_message('❌ Hour must be between 0 and 23.', ephemeral=True)
            return
        
        if not (0 <= minute <= 59):
            await interaction.response.send_message('❌ Minute must be between 0 and 59.', ephemeral=True)
            return
        
        # Check if user has set their username
        username = db.find_user(str(interaction.user))
        if not username:
            await interaction.response.send_message('Please set your LeetCode username first using `/set-username`.', ephemeral=True)
            return
        
        # Save reminder time
        db.set_user_reminder(str(interaction.user), hour, minute)
        
        time_str = f"{hour:02d}:{minute:02d}"
        embed = discord.Embed(
            title="⏰ Reminder Set",
            description=f"You will receive daily study reminders at **{time_str}** (server time).",
            color=discord.Color.green()
        )
        embed.add_field(
            name="Tip",
            value="Make sure your DMs are open to receive reminders!",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        logger.info(f"User {interaction.user} set reminder for {time_str}")
    except Exception as e:
        logger.error(f"Error in set_reminders command: {e}")
        await interaction.response.send_message('❌ An error occurred while setting reminders. Please try again.', ephemeral=True)

@bot.tree.command(name='view-reminders', description='View your configured reminders')
async def view_reminders(interaction: discord.Interaction):
    """Slash command that allows the user to view their reminders"""
    try:
        reminder = db.get_user_reminder(str(interaction.user))
        
        if not reminder:
            await interaction.response.send_message('❌ You have no reminders set. Use `/set-reminders` to configure one!', ephemeral=True)
            return
        
        hour, minute = reminder
        time_str = f"{hour:02d}:{minute:02d}"
        
        embed = discord.Embed(
            title="⏰ Your Reminders",
            description=f"Daily reminder at **{time_str}** (server time)",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="Actions",
            value="• Use `/set-reminders` to change the time\n• Use `/remove-reminders` to stop reminders",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        logger.info(f"User {interaction.user} viewed reminders")
    except Exception as e:
        logger.error(f"Error in view_reminders command: {e}")
        await interaction.response.send_message('❌ An error occurred. Please try again.', ephemeral=True)

@bot.tree.command(name='remove-reminders', description='Stop receiving study reminders')
async def remove_reminders(interaction: discord.Interaction):
    """Slash command that allows the user to remove their reminders"""
    try:
        reminder = db.get_user_reminder(str(interaction.user))
        
        if not reminder:
            await interaction.response.send_message('❌ You have no reminders set.', ephemeral=True)
            return
        
        db.remove_user_reminder(str(interaction.user))
        
        embed = discord.Embed(
            title="🔕 Reminders Removed",
            description="You will no longer receive daily study reminders.",
            color=discord.Color.orange()
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        logger.info(f"User {interaction.user} removed reminders")
    except Exception as e:
        logger.error(f"Error in remove_reminders command: {e}")
        await interaction.response.send_message('❌ An error occurred. Please try again.', ephemeral=True)

@tasks.loop(minutes=1)
async def check_reminders():
    """Background task to check and send reminders"""
    try:
        now = datetime.now()
        current_hour = now.hour
        current_minute = now.minute
        
        # Get all users with reminders for this time
        users_to_remind = db.get_users_with_reminder_time(current_hour, current_minute)
        
        for discord_username in users_to_remind:
            try:
                # Find the user across all guilds
                user = None
                for guild in bot.guilds:
                    member = discord.utils.get(guild.members, name=discord_username.split('#')[0])
                    if member and str(member) == discord_username:
                        user = member
                        break
                
                if user:
                    embed = discord.Embed(
                        title="⏰ Daily Coding Reminder",
                        description="Time to solve some problems and level up your skills!",
                        color=discord.Color.gold()
                    )
                    embed.add_field(
                        name="Suggestions",
                        value="• Try solving 1-2 problems today\n• Review your progress with `/stats`\n• Check your goals and roadmap",
                        inline=False
                    )
                    embed.set_footer(text="Use /remove-reminders to stop these notifications")
                    
                    try:
                        await user.send(embed=embed)
                        logger.info(f"Sent reminder to {discord_username}")
                    except discord.Forbidden:
                        logger.warning(f"Could not send DM to {discord_username} - DMs may be disabled")
            except Exception as e:
                logger.error(f"Error sending reminder to {discord_username}: {e}")
    except Exception as e:
        logger.error(f"Error in check_reminders task: {e}")

@check_reminders.before_loop
async def before_check_reminders():
    """Wait until the bot is ready before starting the reminder loop"""
    await bot.wait_until_ready()


@bot.tree.command(name='set-goal', description='Set a personal coding goal')
@app_commands.describe(questions='Number of questions you\'d like to solve', months='Time period in months to achieve your goal')
async def set_goal(interaction: discord.Interaction, questions: int, months: int):
    """Slash command that allows the user to set a goal for themselves"""
    try:
        # Validate inputs
        if questions <= 0:
            await interaction.response.send_message('❌ Please enter a positive number of questions.', ephemeral=True)
            return
        
        if months <= 0:
            await interaction.response.send_message('❌ Please enter a positive number of months.', ephemeral=True)
            return
        
        # Check if user has set their username
        username = db.find_user(str(interaction.user))
        if not username:
            await interaction.response.send_message('Please set your LeetCode username first using `/set-username`.', ephemeral=True)
            return
        
        # Save goal to database
        start_date = datetime.now().strftime('%Y-%m-%d')
        db.set_user_goal(str(interaction.user), questions, months, start_date)
        
        questions_per_month = questions / months
        questions_per_week = questions_per_month / 4.33
        
        embed = discord.Embed(
            title="🎯 Goal Set Successfully",
            description=f"You've committed to solving **{questions}** questions in **{months}** month{'s' if months > 1 else ''}!",
            color=discord.Color.green()
        )
        embed.add_field(
            name="Target Breakdown",
            value=f"• Per Month: ~{questions_per_month:.1f} questions\n• Per Week: ~{questions_per_week:.1f} questions",
            inline=False
        )
        embed.add_field(
            name="Start Date",
            value=start_date,
            inline=True
        )
        embed.set_footer(text="Use /stats to track your progress!")
        
        await interaction.response.send_message(embed=embed)
        logger.info(f"User {interaction.user} set goal: {questions} questions in {months} months")
    except Exception as e:
        logger.error(f"Error in set_goal command: {e}")
        await interaction.response.send_message('❌ An error occurred while setting your goal. Please try again.', ephemeral=True)


@bot.tree.command(name='stats', description='View your LeetCode statistics and progress')
async def get_stats(interaction: discord.Interaction):
    """Slash command that allows the user to check their leetcode statistics"""
    try:
        username = db.find_user(str(interaction.user))
        if not username:
            await interaction.response.send_message('Please set your username by using the `/set-username` command.', ephemeral=True)
            return

        await interaction.response.defer()

        try:
            response = requests.get(f'https://leetcodestats.cyclic.app/{username}', timeout=10)
            response.raise_for_status()
            results = response.json()
        except requests.exceptions.Timeout:
            await interaction.followup.send('❌ Request timed out. Please try again later.', ephemeral=True)
            logger.error(f"Timeout fetching stats for {username}")
            return
        except requests.exceptions.RequestException as e:
            await interaction.followup.send('❌ Could not fetch LeetCode stats. Please try again later.', ephemeral=True)
            logger.error(f"Error fetching stats for {username}: {e}")
            return

        if results.get('status') == 'error':
            await interaction.followup.send(f'❌ Username **{username}** was not found on LeetCode.', ephemeral=True)
            return

        # Create embed for better formatting
        embed = discord.Embed(
            title=f"📊 LeetCode Stats for {username}",
            color=discord.Color.blue()
        )
        
        total_solved = results.get('totalSolved', 0)
        total_questions = results.get('totalQuestions', 0)
        
        # Progress section
        if total_questions > 0:
            progress_percent = (total_solved / total_questions) * 100
            embed.add_field(
                name="Overall Progress",
                value=f"**{total_solved}** / {total_questions} ({progress_percent:.1f}%)",
                inline=False
            )
        
        # Difficulty breakdown
        easy_solved = results.get('easySolved', 0)
        easy_total = results.get('totalEasy', 0)
        medium_solved = results.get('mediumSolved', 0)
        medium_total = results.get('totalMedium', 0)
        hard_solved = results.get('hardSolved', 0)
        hard_total = results.get('totalHard', 0)
        
        embed.add_field(
            name="🟢 Easy",
            value=f"{easy_solved} / {easy_total}",
            inline=True
        )
        embed.add_field(
            name="🟡 Medium",
            value=f"{medium_solved} / {medium_total}",
            inline=True
        )
        embed.add_field(
            name="🔴 Hard",
            value=f"{hard_solved} / {hard_total}",
            inline=True
        )
        
        # Additional stats
        ranking = results.get('ranking', 'N/A')
        contribution_points = results.get('contributionPoints', 0)
        reputation = results.get('reputation', 0)
        
        if ranking != 'N/A':
            embed.add_field(
                name="🏆 Ranking",
                value=f"#{ranking:,}",
                inline=True
            )
        
        embed.add_field(
            name="🌟 Contribution",
            value=str(contribution_points),
            inline=True
        )
        
        embed.add_field(
            name="💯 Reputation",
            value=str(reputation),
            inline=True
        )
        
        # Check if user has a goal
        goal = db.get_user_goal(str(interaction.user))
        if goal:
            goal_questions, goal_months, start_date = goal
            embed.add_field(
                name="🎯 Your Goal",
                value=f"Solve {goal_questions} questions in {goal_months} month{'s' if goal_months > 1 else ''}",
                inline=False
            )
        
        await interaction.followup.send(embed=embed)
        logger.info(f"Fetched stats for user {interaction.user} (LeetCode: {username})")
    except Exception as e:
        logger.error(f"Error in get_stats command: {e}")
        try:
            await interaction.followup.send('❌ An error occurred while fetching stats. Please try again.', ephemeral=True)
        except:
            await interaction.response.send_message('❌ An error occurred while fetching stats. Please try again.', ephemeral=True)


bot.run(getenv("BOT_TOKEN"))
db.kill()
