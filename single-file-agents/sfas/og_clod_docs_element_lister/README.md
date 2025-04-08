# OG Clod Docs Element Lister 
`og_clod_docs_element_lister.py`

**STATUS**: Validated 

## Purpose
Reviews existing Clôd project documentation and creates comprehensive lists of required documentation elements for different documentation categories.

## Functionality
- Analyzes markdown files from the specified directory
- Categories documentation elements as EXISTING, MISSING, OUTDATED, or INCOMPLETE
- Sorts elements by importance and status
- Provides clean output with proper formatting
- Uses rich for attractive console output

### Our Use Case 
This agent analyzes current Solana core feature documentation to identify what documentation elements exist and what might be missing. It produces structured lists of elements separated by documentation category (MCP, Blockchain, Other) with status indicators for each element. 

## Requirements
- OpenAI API key (set in `.env` file)
- Python 3.9+
- `uv` package manager

## Usage Examples
```bash
# Basic usage to analyze all documentation categories
uv run SFAs/og_clod_docs_element_lister/og_clod_docs_element_lister.py -d "/Users/seanivore/Development/claud-coin/docs/feature-build/" -o "/Users/seanivore/Development/claude-agents/sfa-project-output/"

# Analyze only specific documentation categories
uv run SFAs/og_clod_docs_element_lister/og_clod_docs_element_lister.py -d "/Users/seanivore/Development/claud-coin/docs/feature-build/" -o "/Users/seanivore/Development/claude-agents/sfa-project-output/" -c "MCP"
```

## Command-Line Options
- `--docs-dir, -d`: Directory containing documents to analyze [required]
- `--output-dir, -o`: Directory to save element lists [required]
- `--categories, -c`: Specific categories to analyze (comma-separated) [default: "MCP,BLOCKCHAIN,OTHER"]

## Implementation Details
- Will scan all markdown files in the specified directory
- Will use OpenAI's function-calling API for analysis
- Will generate structured lists with numbering and status flags
- Output files will follow the naming pattern: `OG_CLOD_DOCS_[Category]_ELEMENTS.md`

## Related Agents
- [Best Docs Gap Finder](../best_docs_gap_finder/README.md) - Uses output to identify documentation gaps
- [Doc Gap Filler](../doc_gap_filler/README.md) - Uses output to fill documentation gaps

## Output Format
The agent will produce three output files:
1. `OG_CLOD_DOCS_MCP_ELEMENTS.md` - Elements related to Model Context Protocol
2. `OG_CLOD_DOCS_BLOCKCHAIN_ELEMENTS.md` - Elements related to blockchain functionality
3. `OG_CLOD_DOCS_OTHER_ELEMENTS.md` - Elements related to other aspects

Each file will contain a numbered list with status flags:
```
1. Element name [EXISTING]
2. Another element [MISSING]
3. Third element [OUTDATED]
```

### Documentation Workflow 
- Outputs to the specified directory (can be sfa-project-output)
- Files can then be reviewed and moved to best-doc-updating-finals
- Follows the naming convention: OG_CLOD_DOCS_[CATEGORY]_ELEMENTS.md

