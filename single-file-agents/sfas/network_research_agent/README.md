# Network Research Agent

**Status**: Planned

## Purpose
Researches blockchain networks, grant opportunities, and technical requirements for cross-network scaling of the Clôd Protocol.

## Overview
This agent performs comprehensive research on blockchain networks to identify grant opportunities, technical integration requirements, and decentralization metrics. It focuses on truly decentralized networks that align with the Clôd Protocol objectives and provides actionable insights for expanding beyond the initial Solana implementation.

## Requirements
- OpenAI API key (set in `.env` file)
- Python 3.9+
- `uv` package manager

## Usage Examples
```bash
# Research a specific network
uv run network_research_agent.py --network ethereum --output "/Users/seanivore/Development/clôd/ethereum/research.md"

# Find grant opportunities
uv run network_research_agent.py --focus grants --networks "ethereum,solana,near" --output "grant_opportunities.md"

# Research technical implementation requirements
uv run network_research_agent.py --focus technical --network polygon --output "/Users/seanivore/Development/clôd/polygon/technical.md"

# Assess decentralization metrics
uv run network_research_agent.py --focus decentralization --networks "ethereum,solana,near,polygon,avalanche" --output "decentralization_analysis.md"
```

## Command-Line Options
- `--network`: Specific network to research [conditional]
- `--networks`: Multiple networks (comma-separated) [conditional]
- `--focus`: Research focus area (grants, technical, community, decentralization) [optional]
- `--output`: Output file for results [required]
- `--compute-limit, -c`: Maximum iterations [default: 10]
- `--existing-grants, -e`: Path to existing grant research directory [optional]

## Implementation Details
- Uses function-calling to research network details from authoritative sources
- Implements decentralization assessment using multiple metrics
- Provides technical requirements for cross-network scaling
- Organizes findings in a structured format suitable for documentation
- Compares findings with existing grant research when available

## Related Agents
- [Doc Gap Filler](../doc_gap_filler/README.md) - Uses output to fill documentation gaps
- [Research Agent](../research_agent/README.md) - More general research capabilities

## Issues and Limitations
- Research depth depends on available public information
- Decentralization metrics may be subjective or difficult to quantify
- Grant opportunities change frequently and require verification

## Output Format
The agent produces detailed research reports covering:
1. Network overview and key features
2. Integration requirements for Clôd Protocol
3. Grant opportunities with application details
4. Decentralization assessment
5. Community resources and documentation
6. Recommended next steps for implementation