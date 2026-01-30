# AnimAID Project Instructions

## Design Philosophy
- Focus on Python APIs rather than requiring front-end/CSS knowledge
- Provide simple Python methods for common operations instead of exposing raw CSS
- The target user is a Python programmer, not a web developer
- Hide complexity behind intuitive method names (e.g., `.full_width()` instead of `.styled(width="100%")`)

## Project Naming
- In documentation, README, and other non-code locations, use "AnimAID" (with capital A, I, D)
- In code (package names, imports, variables), use lowercase "animaid"

## HTML Render Objects
- Whenever we update an HTML render object (HTMLString, HTMLList, HTMLDict, etc.), make sure to update both the docs and the tutorial.

## Allowed commands with full permissions
- uv run pytest (all commands and flags)
- uv run invoke (all tasks)
- uv run shot-scraper (all commands and flags)
