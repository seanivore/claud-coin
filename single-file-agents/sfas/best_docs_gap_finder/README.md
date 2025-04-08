# Best Docs Gap Finder 
`best_docs_gap_finder.py`

**Status**: Validated

## Purpose
Analyzes existing documentation against best practices to identify gaps, inconsistencies, and improvement opportunities.

## Overview
This agent uses the industry best practices guide created by the Best Docs Guide Creator to evaluate current Clôd project documentation. It identifies missing elements, structural issues, and content gaps, producing a detailed report of areas that need improvement.

## Requirements
- OpenAI API key (set in `.env` file)
- Python 3.9+
- `uv` package manager
- `BEST_DOCS_GUIDE_2025.md` file from Best Docs Guide Creator

## Usage Examples
```bash
uv run sfas/best_docs_gap_finder/best_docs_gap_finder.py \
  -t "/Users/seanivore/Development/claude-agents/sfa-project-output/best-doc-updating-finals/BEST_DOCS_TECHNICAL_GUIDE_2025.md" \
  -g "/Users/seanivore/Development/claude-agents/sfa-project-output/best-doc-updating-finals/BEST_DOCS_GENERAL_GUIDE_2025.md" \
  -d "/Users/seanivore/Development/claud-coin/docs/feature-build/" \
  -o "/Users/seanivore/Development/claude-agents/sfa-project-output/BEST_DOCS_DOC_GAPS.md" \
  -f "structure,content"
```

## Command-Line Options
- `--guide, -g`: Path to the best practices guide file [required]
- `--docs-dir, -d`: Directory containing documents to analyze [required]
- `--output, -o`: Output file path [required]
- `--focus, -f`: Specific aspects to focus on (comma-separated) [optional]
- `--compute-limit, -c`: Maximum number of analysis iterations [default: 5]

## Implementation Details
- Uses the guide as reference knowledge
- Performs detailed analysis of all markdown files in the specified directory
- Creates a structured report of documentation gaps organized by priority
- Ensures the output is clear and actionable for subsequent agents

## Related Agents
- [Best Docs Guide Creator](../best_docs_guide_creator/README.md) - Creates the guide used by this agent
- [Doc Gap Filler](../doc_gap_filler/README.md) - Uses the output to fill identified gaps

## Output Format
The agent will produce a `BEST_DOCS_DOC_GAPS.md` file that includes:
1. Summary of documentation evaluation
2. List of missing sections and elements
3. Structural improvement recommendations
4. Content enhancement opportunities
5. Prioritized action items

Each gap will be clearly described with a priority level and rationale to enable effective follow-up by the Doc Gap Filler agent.