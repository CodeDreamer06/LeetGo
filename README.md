# LeetGo

A Discord bot to help you track LeetCode progress, host study cohorts, and stay consistent with goals and reminders.

Looking for extended documentation? See the GitBook: https://abhinavs-personal-organization.gitbook.io/leetgo-docs/

## Features

- User profile linking: map your Discord account to your LeetCode username
- LeetCode stats: fetch totals by difficulty, ranking, and contribution points via the public stats API
- Cohorts: create a named cohort channel under a "Cohorts" category to host or study together
- Goals: set target questions over a time period
- Resources and roadmaps: placeholders for curated learning paths (commands stubbed for now)
- Reminders: command stubs for viewing/setting study reminders
- Local storage: lightweight SQLite database for users and cohorts

## Commands

Slash commands registered by the bot:
- /set-username <username> — Link or update your LeetCode username
- /resources — Show learning resources (placeholder)
- /roadmap — Pick a learning roadmap (placeholder)
- /host-a-cohort <name> — Create a cohort with a dedicated text channel under the "Cohorts" category
- /join-a-cohort — Join an existing cohort (placeholder)
- /view-reminders — View your reminders (placeholder)
- /set-reminders — Configure reminders (placeholder)
- /set-goal <questions> <months> — Set a goal like "100 questions in 3 months"
- /stats — Display your LeetCode stats based on your linked username

## Quick start

Prerequisites:
- Python 3.10+
- A Discord bot application and token (see https://discord.com/developers)

1) Clone and install

```bash
git clone <this-repo-url>
cd LeetGo
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

2) Configure environment

```bash
cp .env.example .env
# Edit .env and set BOT_TOKEN=<your discord bot token>
```

3) Run the bot

```bash
python main.py
```

Invite the bot to your server and ensure you have a category named "Cohorts" if you plan to use the cohort command.

## Configuration notes

- LeetCode GraphQL: this project previously initialized a LeetCode GraphQL client on startup. That code has been removed to avoid requiring a LEETCODE_SESSION cookie. The /stats command uses a public stats API instead.
- Database: an SQLite file (storage.db) will be created in the repo root. It is ignored by git.

## Repository hygiene

- VS Code project files: .vscode/ is now ignored via .gitignore. If you already committed it, you can remove it from history with:

```bash
git rm -r --cached .vscode
git commit -m "chore: stop tracking .vscode"
git push
```

- macOS metadata files are ignored (.DS_Store).

## Project layout

- main.py — Discord bot, commands, and runtime
- database.py — SQLite wrapper for users and cohorts

## Roadmap / TODOs

- Implement /resources with curated links and categories
- Implement /roadmap selection and persistence
- Implement /join-a-cohort and cohort membership management
- Implement reminders (scheduling and delivery)
- Add tests and CI

## Contributing

Contributions are welcome! Please open an issue or pull request. Be kind and follow the included Code of Conduct.

## License

Add your preferred license (MIT/Apache-2.0/etc.) or remove this section.
