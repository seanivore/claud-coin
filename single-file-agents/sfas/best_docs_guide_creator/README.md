# Best Docs Guide Creator 
`best_docs_guide_creator.py`

**Status**: Validated 

## Purpose
Researches and compiles current industry best practices for organizing, writing, and presenting technical documentation for development projects.

## Overview
This agent performs comprehensive research on technical documentation standards and best practices across the industry. It creates a detailed guide that covers all aspects of documentation creation, from structure and organization to writing style and platform selection.

## Requirements
- OpenAI API key (set in `.env` file)
- Python 3.9+
- `uv` package manager

## Usage Examples
```bash
# Basic usage
uv run best_docs_guide_creator.py -o "/Users/seanivore/Development/claude-agents/sfa-project-output/"

# Specify additional research focus areas
uv run best_docs_guide_creator.py -o "/Users/seanivore/Development/claude-agents/sfa-project-output/" -f "blockchain,mcp"

# Set research depth
uv run best_docs_guide_creator.py -o "/Users/seanivore/Development/claude-agents/sfa-project-output/" -d "comprehensive"

# Create only technical guide (skipping general guide)
uv run best_docs_guide_creator.py -o "/Users/seanivore/Development/claude-agents/sfa-project-output/" -t "technical"

# Create only general guide (skipping technical guide)
uv run best_docs_guide_creator.py -o "/Users/seanivore/Development/claude-agents/sfa-project-output/" -t "general"
```

## Command-Line Options
- `--output-dir, -o`: Directory to save the guides [required]
- `--focus, -f`: Additional focus areas for research (comma-separated) [optional]
- `--depth, -d`: Research depth (basic, standard, comprehensive) [default: "standard"]
- `--type, -t`: Type of guide to create (technical, general, both) [default: "both"]
- `--compute-limit, -c`: Maximum number of research iterations [default: 10]

## Implementation Details
- Uses OpenAI's Responses API with function calling to research and compile documentation best practices
- Note: This agent uses the newer OpenAI Responses API format rather than the Chat Completions API
- Focuses particularly on open-source documentation platforms
- Includes specific guidance for blockchain and MCP documentation
- Produces comprehensive guides with citations from industry sources
- May produce varying results between runs due to the non-deterministic nature of LLM outputs
- Recommended command: Basic usage without additional parameters for most consistent results

## Related Agents
- [Best Docs Gap Finder](../best_docs_gap_finder/README.md) - Uses the guide to analyze existing documentation
- [Best Docs Template Creator](../best_docs_template_creator/README.md) - Uses the guide to create documentation templates

## Output
The agent will produce two distinct guides:

1. `BEST_DOCS_TECHNICAL_GUIDE_2025.md` - A comprehensive guide covering technical documentation best practices, including:
   - API documentation standards
   - Code examples and snippets formatting
   - Technical diagrams and visualization
   - Schema documentation
   - Architecture documentation
   - Reference documentation structure
   - Protocol specifications
   - Testing documentation
   - Technical implementation details for blockchain and MCP

2. `BEST_DOCS_GENERAL_GUIDE_2025.md` - A comprehensive guide covering general documentation best practices, including:
   - Documentation structure and organization
   - Writing style and tone
   - Content requirements by document type
   - Audience considerations
   - Platform selection and configuration
   - Publishing workflow
   - Documentation versioning
   - Maintenance considerations
   - User guides, tutorials, and onboarding
   - Non-technical aspects for blockchain and MCP documentation