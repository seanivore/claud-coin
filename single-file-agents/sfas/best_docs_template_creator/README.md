# Best Docs Template Creator

**Status**: Planned

## Purpose
Creates documentation templates based on industry best practices that provide structure for creating professional, consistent documentation.

## Overview
This agent transforms the best practices guide into practical, reusable documentation templates. The templates include properly structured headings, placeholder content, and embedded instructions for AI assistance in completing the documentation.

## Requirements
- OpenAI API key (set in `.env` file)
- Python 3.9+
- `uv` package manager
- `BEST_DOCS_GUIDE_2025.md` file from Best Docs Guide Creator

## Usage Examples
```bash
# Basic usage
uv run best_docs_template_creator.py -g "/Users/seanivore/Development/clôd/docs/documentation-needs/BEST_DOCS_GUIDE_2025.md" -o "/Users/seanivore/Development/clôd/docs/documentation-needs/BEST_DOCS_TEMPLATE_2025.md"

# Create specific template types
uv run best_docs_template_creator.py -g "/Users/seanivore/Development/clôd/docs/documentation-needs/BEST_DOCS_GUIDE_2025.md" -o "/Users/seanivore/Development/clôd/docs/documentation-needs/BEST_DOCS_TEMPLATE_2025.md" -t "api,implementation"
```

## Command-Line Options
- `--guide, -g`: Path to the best practices guide file [required]
- `--output, -o`: Output template file path [required]
- `--template-types, -t`: Specific template types to create (comma-separated) [optional]
- `--aider-compatible, -a`: Flag to ensure compatibility with Aider agent [default: true]

## Implementation Details
- Extracts structure and organization principles from the best practices guide
- Creates empty template with complete section hierarchy
- Includes AI-compatible prompt comments for content completion
- Ensures compatibility with the Aider watch-files workflow
- Provides consistent documentation structure across networks

## Related Agents
- [Best Docs Guide Creator](../best_docs_guide_creator/README.md) - Creates the guide used by this agent
- [Doc Gap Filler](../doc_gap_filler/README.md) - Creates content that will fill the template

## Output Format
The agent will produce a `BEST_DOCS_TEMPLATE_2025.md` file that includes:
1. Complete documentation structure with all required sections and subsections
2. Placeholder text indicating what content should be added to each section
3. Special comment blocks for AI assistance that include:
   - Instructions on what content to place in each section
   - Format guidelines
   - Linking requirements
   - Any special considerations for the section

The template will be designed for use with Aider's watch-files mode, allowing for efficient completion of the documentation.