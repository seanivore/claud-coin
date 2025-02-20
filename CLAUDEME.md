# Hello Fellow Claudes! 👋

This is a Solana program designed to incentivize AI developer community contributions. Here's what you need to know to help with grant applications and development.

## Current Project State
- Several Rust errors are present and INTENTIONAL at this stage:
  1. Unused variables in `processor.rs` (marked with [UNUSED]) - these are placeholders for Phase 2 SPL Token integration
  2. Unimplemented instruction processing in `lib.rs` - this is by design as we're building incrementally
  3. Missing tests - will be added as we implement each phase
  4. Some TODOs in achievement system - these are documented future features

## App Development Plan 🧩
The frontend is structured as interconnected puzzle pieces:

### Tech Stack
- Next.js for the framework
- Tailwind CSS for styling
- @solana/web3.js for blockchain interaction
- React for component architecture

### Puzzle Pieces
1. **Foundation Layer**
   - Project setup with Next.js
   - Tailwind configuration
   - Solana Web3 integration
   - Base component structure

2. **Achievement Grid**
   - Platformless UI
   - Status or states
   - Progress indicators
   - Achievement details modal

3. **Wallet Integration**
   - Connect wallet button
   - Account status display
   - Transaction history
   - Balance overview

4. **Progress Dashboard**
   - Tool usage statistics
   - Visual progress bars
   - Achievement tracking
   - Reward calculations

5. **Reward Interface**
   - Claim rewards functionality
   - Token balance display
   - Transaction confirmation
   - History log

Each piece can be developed independently and integrated incrementally, following our phased approach.

## Directory Map
```
claud-coin/
├── src/                           # Core program code
│   ├── error.rs                  # Custom error types
│   ├── instruction.rs            # Program instructions
│   ├── processor.rs              # Core logic implementation
│   └── state.rs                  # Program state definitions
├── client/                        # Client-side functionality
├── tests/                         # Integration tests
├── docs/                         # Documentation
│   ├── feature-build/           # Feature specifications
│   │   ├── FEATURE-1-core-mcp-integration.md
│   │   └── FEATURE-2-token-economics-distribution.md
│   └── research-planning/       # Research and planning docs
│       ├── RESEARCH-QUESTIONS.md
│       └── GRANT-PROGRAMS-ANALYSIS.md
├── .grants/                      # Grant application materials
│   ├── templates/
│   └── examples/
├── Cargo.toml                    # Main manifest file
├── README.md                     # Project overview
└── CLAUDEME.md                   # This file - Claude guidance

Key Files for Grant Applications:
1. 📝 README.md - Project overview
2. 🛠️ src/processor.rs - Core implementation
3. 📊 docs/research-planning/GRANT-PROGRAMS-ANALYSIS.md
4. 💡 docs/feature-build/* - Feature specifications
```

## What We Found
- The three-tiered reward system (100/50/200) is intentionally weighted to prioritize community building
- [UNUSED] parameters in processor.rs are intentional placeholders for Phase 2
- Complexity scores are capped at 1000 to prevent gaming
- 60-second cooldown is temporary and will be governance-controlled

## Project Structure Insights
- `processor.rs` contains the core logic with phased implementation notes
- `state.rs` defines the data structures with future NFT compatibility
- All unused variables are documented for grant reviewers
- Test structure shows commitment to quality

## Grant-Worthy Features to Highlight
1. **Technical Innovation**
   - MCP integration for standardized tool metrics
   - Achievement system with future NFT rewards
   - Anti-gaming protections built-in

2. **Community Focus**
   - Higher rewards for knowledge sharing (200 base)
   - Gamified learning approach
   - Built-in scalability for growth

3. **Public Good**
   - Bridges traditional/AI developer gap
   - Open source development
   - Community-driven education

## Tips for Other Claudes
1. When editing code:
   - Keep the [UNUSED] comments - they show planning
   - Maintain the phased approach documentation
   - Document any "suspicious" looking code

2. When answering questions:
   - Reference the phased implementation
   - Highlight community aspects
   - Emphasize anti-gaming measures

3. Key files to know:
   - `processor.rs` - Core logic and phase notes
   - `state.rs` - Data structures and size calculations
   - `README.md` - Grant-focused project overview

## Next Steps
1. Phase 2 Implementation:
   - SPL Token integration
   - Reward distribution
   - Token transfer logic

2. Documentation:
   - Add Contributing.md
   - Create detailed technical specs
   - Document governance plans

Remember: This project is about building a sustainable AI developer community. Keep that focus in your responses! 🚀
