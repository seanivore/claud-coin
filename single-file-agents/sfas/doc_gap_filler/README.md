# Doc Gap Filler

**Status**: Planned

## Purpose
Researches and compiles missing documentation elements identified by analysis of current documentation against best practices.

## Overview
This agent bridges documentation gaps by researching and compiling content for missing elements identified by previous analysis agents. It works with multiple input files to create comprehensive, network-specific documentation that adheres to industry best practices.

## Requirements
- OpenAI API key (set in `.env` file)
- Python 3.9+
- `uv` package manager
- Output files from previous documentation analysis agents

## Usage Examples
```bash
# Basic usage for Solana network
uv run doc_gap_filler.py -n "Solana" -e "/Users/seanivore/Development/clôd/docs/documentation-needs/OG_CLOD_DOCS_MCP_ELEMENTS.md,/Users/seanivore/Development/clôd/docs/documentation-needs/OG_CLOD_DOCS_BLOCKCHAIN_ELEMENTS.md,/Users/seanivore/Development/clôd/docs/documentation-needs/OG_CLOD_DOCS_OTHER_ELEMENTS.md" -g "/Users/seanivore/Development/clôd/docs/documentation-needs/BEST_DOCS_DOC_GAPS.md" -o "/Users/seanivore/Development/clôd/docs/Solana/"

# Run for specific element groups only
uv run doc_gap_filler.py -n "Solana" -e "/Users/seanivore/Development/clôd/docs/documentation-needs/OG_CLOD_DOCS_BLOCKCHAIN_ELEMENTS.md" -g "/Users/seanivore/Development/clôd/docs/documentation-needs/BEST_DOCS_DOC_GAPS.md" -o "/Users/seanivore/Development/clôd/docs/Solana/" --element-group "BLOCKCHAIN"
```

## Command-Line Options
- `--network, -n`: Blockchain network name [required]
- `--elements, -e`: Comma-separated paths to element list files [required]
- `--gaps, -g`: Path to documentation gaps file [required]
- `--output-dir, -o`: Directory to save output files [required]
- `--element-group`: Specific element group to process (MCP, BLOCKCHAIN, OTHER, BEST-DOCS) [optional]
- `--guide, -G`: Path to best practices guide [optional]
- `--compute-limit, -c`: Maximum number of research iterations [default: 15]

## Implementation Details
- Processes multiple input files to identify what needs to be researched
- Performs targeted research for each missing element
- Creates both individual element files and a consolidated document
- Organizes output according to industry best practices
- Adapts content to be network-specific

## Related Agents
- [OG Clod Docs Element Lister](../og_clod_docs_element_lister/README.md) - Provides input element lists
- [Best Docs Gap Finder](../best_docs_gap_finder/README.md) - Provides documentation gaps analysis
- [Best Docs Guide Creator](../best_docs_guide_creator/README.md) - Optional input for structuring output

## Output
The agent will produce:
1. Individual element files for each group (if run separately):
   - `MCP_CLOD_DOC_GAPS_FILLED.md`
   - `[Network-Name]_CLOD_DOC_GAPS_FILLED.md`
   - `OTHER_CLOD_DOC_GAPS_FILLED.md`
   - `BEST-DOCS_CLOD_DOC_GAPS_FILLED.md`

2. A consolidated document:
   - `[Network-Name]_CLOD_DOCS_COMPLETE.md`

The consolidated document will organize all researched content according to the structure defined in the best practices guide.