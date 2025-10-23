# LeetGo

A Discord bot designed to help developers track their LeetCode progress, participate in study cohorts, and maintain consistent coding practice through goals and reminders.

## Features

- **Profile Linking**: Connect your Discord account to your LeetCode username
- **Statistics Tracking**: View your LeetCode stats including problems solved by difficulty, ranking, and contribution points
- **Study Cohorts**: Create and manage dedicated study groups with their own Discord channels
- **Goal Setting**: Define personal targets for solving problems within specific timeframes
- **Progress Monitoring**: Track your journey towards becoming a better problem solver

## Commands

The bot provides the following slash commands:

| Command | Description | Status |
|---------|-------------|--------|
| `/set-username <username>` | Link or update your LeetCode username | ✅ Implemented |
| `/stats` | Display your LeetCode statistics | ✅ Implemented |
| `/host-a-cohort <name>` | Create a study cohort with a dedicated channel | ✅ Implemented |
| `/set-goal <questions> <months>` | Set a goal for problem-solving progress | ✅ Implemented |
| `/join-a-cohort` | Join an existing cohort | 🚧 Coming Soon |
| `/resources` | Access curated learning resources | 🚧 Coming Soon |
| `/roadmap` | Select a learning roadmap to follow | 🚧 Coming Soon |
| `/view-reminders` | View your configured reminders | 🚧 Coming Soon |
| `/set-reminders` | Configure study reminders | 🚧 Coming Soon |

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

## Technical Details

### Architecture

- **main.py**: Contains the Discord bot implementation, command handlers, and event listeners
- **database.py**: SQLite database wrapper managing users, cohorts, and relationships
- **storage.db**: SQLite database file (auto-created, ignored by git)

### Data Storage

The bot uses SQLite for local data persistence, storing:
- User profiles (Discord username, LeetCode username, goals)
- Cohort information
- User-cohort relationships

### LeetCode API

The bot uses a public LeetCode statistics API ([leetcodestats.cyclic.app](https://leetcodestats.cyclic.app)) to fetch user data without requiring authentication. This eliminates the need for LEETCODE_SESSION cookies.

## Development

### Project Structure

```
LeetGo/
├── main.py           # Bot implementation and commands
├── database.py       # Database layer
├── requirements.txt  # Python dependencies
├── .env.example      # Environment template
├── .gitignore        # Git ignore rules
└── README.md         # This file
```

### Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure your code follows Python best practices and includes appropriate documentation.

## Roadmap

- [ ] Implement cohort membership management (`/join-a-cohort`)
- [ ] Add curated learning resources (`/resources`)
- [ ] Create interactive roadmap selection (`/roadmap`)
- [ ] Build reminder system with scheduling
- [ ] Add automated testing and CI/CD pipeline
- [ ] Implement progress visualization and analytics
- [ ] Add support for competitive programming platforms beyond LeetCode

## Known Issues

- Cohort leave functionality not yet implemented
- Reminder system is currently a stub
- Goal tracking doesn't persist progress updates

## License

This project is open source and available under the MIT License.

## Acknowledgments

- LeetCode for providing the platform that inspired this bot
- discord.py for the excellent Discord API wrapper
- The competitive programming community for continuous inspiration
