# Contributing to LeetGo

Thank you for considering contributing to LeetGo! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help create a welcoming environment for all contributors

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Your environment (Python version, OS, etc.)
- Relevant log output from `leetgo.log`

### Suggesting Features

Feature suggestions are welcome! Please create an issue with:
- Clear description of the feature
- Use case and benefits
- Any implementation ideas you have

### Pull Requests

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/LeetGo.git
   cd LeetGo
   ```

2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Your Changes**
   - Follow the code quality guidelines below
   - Test your changes thoroughly
   - Update documentation if needed

4. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Add: brief description of changes"
   ```
   
   Use commit prefixes:
   - `Add:` for new features
   - `Fix:` for bug fixes
   - `Update:` for improvements to existing features
   - `Docs:` for documentation changes
   - `Refactor:` for code refactoring

5. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a Pull Request on GitHub

## Code Quality Guidelines

### Error Handling

Always wrap operations that can fail in try-catch blocks:

```python
def some_function(self, param):
    """Function description"""
    try:
        # Your code here
        self.c.execute('SELECT * FROM table WHERE id=?', (param,))
        self.connection.commit()
    except Exception as e:
        logger.error(f"Error in some_function: {e}")
        raise  # or return appropriate default value
```

### Logging

Use the logging system for important events:

```python
logger.info("User completed action successfully")
logger.warning("Non-critical issue occurred")
logger.error(f"Error occurred: {e}")
```

### Input Validation

Always validate user inputs:

```python
if not username or len(username.strip()) == 0:
    await interaction.response.send_message('❌ Please provide a valid username.', ephemeral=True)
    return
```

### User Feedback

Provide clear, emoji-enhanced feedback:

```python
# Success
await interaction.response.send_message('✅ Operation completed successfully!')

# Error
await interaction.response.send_message('❌ An error occurred. Please try again.', ephemeral=True)

# Info
await interaction.response.send_message('ℹ️ Here is some information...')
```

### Documentation

Add docstrings to all functions:

```python
def function_name(self, param1: str, param2: int) -> bool:
    """Brief description of what the function does
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
    """
    pass
```

### Type Hints

Include type hints where appropriate:

```python
def find_user(self, discord_username: str) -> str:
    """Fetches leetcode username from the database"""
    # implementation
```

## Testing

Before submitting your PR:

1. Test basic functionality manually
2. Check for syntax errors: `python3 -m py_compile main.py database.py`
3. Verify database operations work correctly
4. Test error cases (invalid inputs, missing data, etc.)
5. Check that logging works as expected

## Project Structure

```
LeetGo/
├── main.py              # Bot commands and event handlers
├── database.py          # Database operations
├── requirements.txt     # Python dependencies
├── .env.example         # Environment template
├── LICENSE              # MIT License
├── README.md            # Main documentation
├── CHANGELOG.md         # Version history
└── CONTRIBUTING.md      # This file
```

## Questions?

If you have questions about contributing, feel free to:
- Open an issue for discussion
- Reach out to the maintainers
- Check existing issues and PRs for similar questions

Thank you for contributing to LeetGo! 🚀
