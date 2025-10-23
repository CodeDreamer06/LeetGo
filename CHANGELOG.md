# Changelog

All notable changes to the LeetGo Discord bot are documented in this file.

## [2.0.0] - 2024

### Added

#### Features
- **Interactive Roadmap System**: Users can now select from 4 learning paths (Beginner, Intermediate, Advanced, Interview Prep) with topic breakdowns
- **Join Cohort Functionality**: Complete implementation with interactive dropdown menu to join existing study cohorts
- **Leave Cohort Command**: New `/leave-cohort` command allowing users to exit their current cohort
- **Daily Reminder System**: Fully functional reminder system with:
  - `/set-reminders` to configure daily study reminders at specific times
  - `/view-reminders` to check current reminder settings
  - `/remove-reminders` to disable reminders
  - Background task that sends DM reminders to users at their scheduled times
- **Enhanced Goal Tracking**: Goals now persist with start dates and display in `/stats` command
- **Improved Statistics Display**: Enhanced `/stats` command with:
  - Rich embed formatting
  - Progress percentages
  - Difficulty breakdown with color-coded emojis
  - Goal display integration

#### Technical Improvements
- **Comprehensive Error Handling**: All database operations and commands now have try-catch blocks with proper error messages
- **Logging System**: Implemented logging to both console and file (`leetgo.log`) for debugging and monitoring
- **Input Validation**: Added validation for all user inputs (usernames, goals, reminders, cohort names)
- **Database Enhancements**:
  - Added `roadmap` column (TEXT) to store user's selected learning path
  - Added `reminder_hour` and `reminder_minute` columns for reminder scheduling
  - Added `UNIQUE` constraint on `discord_username` to prevent duplicates
  - All database methods now include error handling and logging
- **Code Quality**:
  - Added comprehensive docstrings
  - Improved code organization and readability
  - Better type hints and return types
  - Consistent error messaging with emoji indicators

#### Documentation
- **MIT License**: Added LICENSE file
- **Enhanced README**: Updated with:
  - Complete command list with all implemented features
  - Bot permissions requirements
  - Step-by-step usage guide
  - Updated project structure
  - Future enhancements section
- **Environment Configuration**: Updated `.env.example` with clear instructions

### Changed
- **Stats Command**: Now uses embeds instead of plain text for better readability
- **Goal Setting**: Enhanced with breakdown showing per-month and per-week targets
- **Cohort Creation**: Now sends welcome message to newly created cohort channels
- **User Experience**: All commands now provide rich, emoji-enhanced feedback

### Removed
- **Resources Command**: Removed `/resources` command as requested
- **Known Issues Section**: Removed from README as all issues have been resolved
- **Roadmap Section**: Replaced with "Future Enhancements" after completing all roadmap items

### Fixed
- **Cohort Leave Functionality**: Implemented complete leave functionality that was previously missing
- **Reminder System**: Converted from stub to fully functional system with background tasks
- **Goal Persistence**: Goals now properly persist in database and display in stats
- **Database Connection**: Improved connection handling and proper cleanup
- **Error Messages**: All error messages are now user-friendly and informative

### Security
- **Timeout Handling**: Added 10-second timeout for LeetCode API requests
- **Permission Checks**: Added checks for bot permissions before creating channels
- **User Validation**: All commands validate that users exist before operations

## [1.0.0] - Previous Version

### Initial Features
- Basic user profile linking
- LeetCode statistics fetching
- Cohort hosting
- Basic goal setting
- SQLite database integration
