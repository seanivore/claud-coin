# Feedback Agent
`feedback_agent.py`

**Status**: Testing

## Purpose
Analyzes documentation for quality, consistency, and completeness, providing actionable feedback for improvement.

## Overview
The Feedback Agent examines documentation files and evaluates them across various dimensions including technical accuracy, completeness, clarity, organization, and user-friendliness. It then generates detailed feedback with specific recommendations for improvement, organized by priority.

## Requirements
- Anthropic API key (set in `.env` file)
- OpenAI API key (set in `.env` file) as fallback
- Python 3.9+
- `uv` package manager

## Usage Examples
```bash
# Basic documentation feedback
uv run feedback_agent.py -f "~/Development/claud-coin/README.md" -o "documentation_feedback.md"

# Focus on specific aspects
uv run feedback_agent.py -f "~/Development/claud-coin/SPECIFICATIONS.md" -o "spec_feedback.md" -F "technical-accuracy"

# Multiple focus areas with extended compute time
uv run feedback_agent.py -f "~/Development/claud-grants/GRANTME.md" -o "grant_feedback.md" -F "completeness,clarity" -c 5

# Use extended thinking mode for large documents
uv run feedback_agent.py -f "~/Development/claud-coin/TECHNICAL_SPEC.md" -o "tech_spec_feedback.md" -e
```

## Command-Line Options
- `--file, -f`: Input document to analyze [required]
- `--output, -o`: Output file for feedback [default: "feedback.md"]
- `--compute-limit, -c`: Maximum iterations [default: 3]
- `--focus, -F`: Focus areas for analysis (comma-separated) [optional]
- `--extended-thinking, -e`: Enable extended thinking mode with larger token limit [flag]
- `--token-limit, -t`: Override token limit [optional]

## Implementation Details
- Can use either Anthropic's Claude 3.7 Sonnet or OpenAI's models
- Adapts to streaming or standard completion based on token limit
- Implements custom tool definitions:
  - `read_document`: Fetches document content
  - `analyze_document`: Performs detailed analysis
  - `save_feedback`: Writes structured feedback
  - `complete_task`: Signals completion
- Handles large document analysis with streaming and chunking

## Testing Status
- [x] Basic functionality testing
- [x] Command-line interface testing
- [x] Streaming large document support
- [ ] Comprehensive error handling testing
- [ ] Anthropic-specific integration testing

## Related Agents
- [OG Clod Docs Element Lister](../og_clod_docs_element_lister/README.md) - Works with documentation elements
- [Best Docs Gap Finder](../best_docs_gap_finder/README.md) - Identifies documentation gaps

## Issues and Limitations
- Currently refining Anthropic Claude integration
- Very large documents may require extended thinking mode for complete analysis
- Performance varies based on document complexity and structure

## Changelog
- 2025-03-05: Initial implementation
- 2025-03-12: Added extended thinking mode
- 2025-03-15: Added streaming support for large documents