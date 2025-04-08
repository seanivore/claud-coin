# Master Map Agent

**Status**: Planned

## Purpose
Manages the MASTER_MAP.md project organization document, processing items between sections and maintaining task organization.

## Overview
The Master Map Agent automates the maintenance of the MASTER_MAP project organization document. It processes items from the New Business section into properly structured tasks in the In Focus section, cleans up completed tasks, and can generate summaries of current project status.

## Requirements
- OpenAI API key (set in `.env` file)
- Python 3.9+
- `uv` package manager
- Git (optional, for auto-commit functionality)

## Usage Examples
```bash
# Basic processing of MASTER_MAP
uv run master_map_agent.py -f "/Users/seanivore/Development/_ai.resources/_ai.MASTER_MAP.md"

# Scheduled update (for cron)
uv run master_map_agent.py -f "/Users/seanivore/Development/_ai.resources/_ai.MASTER_MAP.md" --auto-commit

# Generate task summary
uv run master_map_agent.py -f "/Users/seanivore/Development/_ai.resources/_ai.MASTER_MAP.md" --summary

# Post updates to Discord
uv run master_map_agent.py -f "/Users/seanivore/Development/_ai.resources/_ai.MASTER_MAP.md" --discord
```

## Command-Line Options
- `--file, -f`: Path to MASTER_MAP.md file [required]
- `--auto-commit`: Automatically commit changes to git [flag]
- `--summary`: Generate a summary of current tasks [flag]
- `--discord`: Post updates to Discord [flag]
- `--process-new`: Process items from New Business to In Focus [flag]
- `--cleanup`: Process cleanup triggers in In Focus section [flag]

## Implementation Details
- Uses regex and markdown parsing to analyze document structure
- Implements the task status flags and indicators defined in the document
- Can identify and process cleanup trigger flags
- Generates properly formatted tasks with appropriate status indicators
- Maintains cross-references between related tasks

## Related Agents
- [Task Agent](../task_agent/README.md) - Extracts tasks from the MASTER_MAP

## Issues and Limitations
- Requires specific formatting in the MASTER_MAP document
- Task organization is based on current status flags and may require adjustment
- Auto-commit functionality assumes git is properly configured

## Output
The agent can produce:
1. An updated MASTER_MAP.md with processed items
2. A summary report of current project status
3. Discord notifications of changes (when enabled)
4. Git commits documenting changes (when auto-commit is enabled)

The agent maintains all existing task organization while applying the rules defined in the Document Maintenance section of the MASTER_MAP.