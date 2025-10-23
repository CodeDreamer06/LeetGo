# LeetGo

A Discord bot designed to help developers track their LeetCode progress, participate in study cohorts, and maintain consistent coding practice through goals and reminders.

## Features

- **Profile Linking**: Connect your Discord account to your LeetCode username
- **Statistics Tracking**: View your LeetCode stats including problems solved by difficulty, ranking, and contribution points
- **Study Cohorts**: Create, join, and leave dedicated study groups with their own Discord channels
- **Learning Roadmaps**: Choose from Beginner, Intermediate, Advanced, or Interview Prep learning paths
- **Goal Setting**: Define personal targets for solving problems within specific timeframes with progress tracking
- **Smart Reminders**: Set daily study reminders to stay consistent with your practice
- **Progress Monitoring**: Track your journey towards becoming a better problem solver

## Commands

The bot provides the following slash commands:

| Command | Description |
|---------|-------------|
| `/set-username <username>` | Link or update your LeetCode username |
| `/stats` | Display your LeetCode statistics and goal progress |
| `/host-a-cohort <name>` | Create a study cohort with a dedicated channel |
| `/join-a-cohort` | Join an existing cohort |
| `/leave-cohort` | Leave your current cohort |
| `/roadmap` | Select a learning roadmap to follow |
| `/set-goal <questions> <months>` | Set a goal for problem-solving progress |
| `/set-reminders <hour> <minute>` | Configure daily study reminders |
| `/view-reminders` | View your configured reminders |
| `/remove-reminders` | Stop receiving study reminders |

## Getting Started

### Prerequisites

- Python 3.10 or higher
- A Discord bot token (create one at the [Discord Developer Portal](https://discord.com/developers/applications))
- A Discord server where you have permission to add bots

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/CodeDreamer06/LeetGo.git
cd LeetGo
```

2. **Set up a virtual environment**

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

```bash
cp .env.example .env
```

Edit the `.env` file and add your Discord bot token:

```
BOT_TOKEN=your_discord_bot_token_here
```

5. **Run the bot**

```bash
python main.py
```

### Discord Server Setup

For the cohort feature to work properly, ensure your Discord server has a category named **"Cohorts"**. The bot will create cohort channels under this category.

### Bot Permissions

Make sure the bot has the following permissions in your Discord server:
- **Send Messages**: To respond to commands
- **Manage Channels**: To create cohort channels
- **Send Messages in Threads**: For future thread support
- **Embed Links**: To display rich embeds
- **Read Message History**: For context awareness

### Using the Bot

1. **Set up your profile**: Start by linking your LeetCode username with `/set-username`
2. **Choose a roadmap**: Select your learning path with `/roadmap` (Beginner, Intermediate, Advanced, or Interview Prep)
3. **Set goals**: Define your targets with `/set-goal` (e.g., solve 100 questions in 3 months)
4. **Enable reminders**: Stay consistent with `/set-reminders` to get daily study notifications
5. **Join or create a cohort**: Study with others using `/host-a-cohort` or `/join-a-cohort`
6. **Track progress**: Check your stats anytime with `/stats`

## Technical Details

### Architecture

- **main.py**: Contains the Discord bot implementation, command handlers, event listeners, and background tasks
- **database.py**: SQLite database wrapper managing users, cohorts, roadmaps, goals, and reminders with comprehensive error handling
- **storage.db**: SQLite database file (auto-created, ignored by git)
- **leetgo.log**: Application log file for debugging and monitoring (auto-created, ignored by git)

### Data Storage

The bot uses SQLite for local data persistence, storing:
- User profiles (Discord username, LeetCode username, goals, reminders, roadmaps)
- Cohort information and memberships
- Goal tracking with start dates
- Daily reminder schedules

### LeetCode API

The bot uses a public LeetCode statistics API ([leetcodestats.cyclic.app](https://leetcodestats.cyclic.app)) to fetch user data without requiring authentication. This eliminates the need for LEETCODE_SESSION cookies. The API calls include:
- 10-second timeout for reliability
- Proper error handling for network issues
- Graceful fallback for missing data

### Error Handling & Logging

The bot implements comprehensive error handling:
- **All database operations** are wrapped in try-catch blocks
- **API calls** have timeout protection and connection error handling
- **User input validation** ensures data integrity
- **Logging**: All significant events and errors are logged to `leetgo.log` and console
- **User-friendly messages**: All errors display helpful emoji-enhanced messages to users

## Development

### Project Structure

```
LeetGo/
├── main.py              # Bot implementation and commands
├── database.py          # Database layer with comprehensive error handling
├── requirements.txt     # Python dependencies
├── .env.example         # Environment template
├── .gitignore           # Git ignore rules
├── LICENSE              # MIT License
├── README.md            # This file
├── CHANGELOG.md         # Version history and changes
└── CONTRIBUTING.md      # Contribution guidelines
```

### Contributing

Contributions are welcome! For detailed guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md).

Quick start:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

#### Code Quality Guidelines

- **Error Handling**: Wrap operations in try-catch blocks with appropriate logging
- **Documentation**: Add docstrings to all functions and classes
- **Logging**: Use the logger for important events and errors
- **Validation**: Validate all user inputs before processing
- **Type Hints**: Include type hints for function parameters and returns
- **Testing**: Test your changes thoroughly before submitting
- **Formatting**: Follow PEP 8 style guidelines

## Future Enhancements

- [ ] Add automated testing and CI/CD pipeline
- [ ] Implement progress visualization and analytics with charts
- [ ] Add support for competitive programming platforms beyond LeetCode (Codeforces, HackerRank)
- [ ] Implement leaderboards for cohorts
- [ ] Add streak tracking and achievements system
- [ ] Create weekly/monthly progress reports

## License

This project is open source and available under the MIT License.

## Acknowledgments

- LeetCode for providing the platform that inspired this bot
- discord.py for the excellent Discord API wrapper
- The competitive programming community for continuous inspiration
