use borsh::{BorshDeserialize, BorshSerialize};
use solana_program::{
    account_info::{next_account_info, AccountInfo},
    clock::Clock,
    entrypoint::ProgramResult,
    program_error::ProgramError,
    msg,
    pubkey::Pubkey,
    sysvar::{rent::Rent, Sysvar},
};

use crate::{
    error::ClaudCoinError,
    instruction::ClaudCoinInstruction,
    state::{TokenState, UserStats, Achievement},
};

/// Processor implementation for the Claud Coin program
/// 
/// This implementation follows a phased approach:
/// Phase 1: Core state management and validation (current)
/// Phase 2: SPL Token integration for rewards (planned)
/// Phase 3: Advanced achievement system with NFTs (planned)
///
/// IMPLEMENTATION NOTES:
/// 1. Several parameters are marked [UNUSED] intentionally - they are placeholders for
///    Phase 2 when we implement SPL Token integration and cross-program invocation (CPI)
/// 2. The 60-second cooldown between tool usages is intentionally short during development
///    and will be adjusted based on mainnet usage patterns
/// 3. Complexity scores are capped at 1000 to prevent gaming of the reward system
/// 4. Base reward rates (100/50/200) are initial values and can be adjusted by governance
/// 5. Achievement claims currently only track times_claimed - user-specific tracking
///    will be added in Phase 3 with the NFT integration
pub struct Processor;

impl Processor {
    /// Main processing function that handles all program instructions
    /// Currently implements core validation and state management
    /// Token transfers will be implemented using SPL Token program in Phase 2
    pub fn process(
        program_id: &Pubkey,
        accounts: &[AccountInfo],
        instruction_data: &[u8],
    ) -> ProgramResult {
        let instruction = ClaudCoinInstruction::unpack(instruction_data)?;

        match instruction {
            ClaudCoinInstruction::Initialize => {
                msg!("Instruction: Initialize");
                Self::process_initialize(program_id, accounts)
            }
            ClaudCoinInstruction::MintReward { amount, reward_type } => {
                msg!("Instruction: MintReward");
                Self::process_mint_reward(accounts, amount, reward_type, program_id)
            }
            ClaudCoinInstruction::RecordToolUsage { tool_id, complexity_score } => {
                msg!("Instruction: RecordToolUsage");
                Self::process_record_tool_usage(accounts, tool_id, complexity_score, program_id)
            }
            ClaudCoinInstruction::CreateAchievement { id, required_score, reward_amount } => {
                msg!("Instruction: CreateAchievement");
                Self::process_create_achievement(program_id, accounts, id, required_score, reward_amount)
            }
            ClaudCoinInstruction::ClaimAchievement { achievement_id } => {
                msg!("Instruction: ClaimAchievement");
                Self::process_claim_achievement(program_id, accounts, achievement_id)
            }
        }
    }

    /// Initializes the token program with base reward rates
    /// Sets up the foundation for the three-tiered reward system:
    /// - Tool usage rewards (100 tokens base)
    /// - Resource access rewards (50 tokens base)
    /// - Community contributions (200 tokens base)
    ///
    /// Note: The base_community_reward is intentionally set higher (200) to
    /// incentivize early community building and knowledge sharing
    pub fn process_initialize(
        program_id: &Pubkey,
        accounts: &[AccountInfo],
    ) -> ProgramResult {
        let account_info_iter = &mut accounts.iter();
        let initializer = next_account_info(account_info_iter)?;
        let mint_account = next_account_info(account_info_iter)?;
        let rent = &Rent::from_account_info(next_account_info(account_info_iter)?)?;

        if !initializer.is_signer {
            return Err(ProgramError::MissingRequiredSignature);
        }

        if !rent.is_exempt(mint_account.lamports(), TokenState::SIZE) {
            return Err(ClaudCoinError::NotRentExempt.into());
        }

        let token_state = TokenState {
            mint_authority: *initializer.key,
            total_supply: 0,
            decimals: 9,
            is_initialized: true,
            base_tool_reward: 100, // Base reward of 100 tokens for tool usage
            base_resource_reward: 50, // Base reward of 50 tokens for resource access
            base_community_reward: 200, // Base reward of 200 tokens for community contributions
        };

        token_state.serialize(&mut &mut mint_account.data.borrow_mut()[..])?;
        Ok(())
    }

    /// Mints reward tokens based on user actions
    /// Phase 2 will implement actual token transfers via SPL Token program
    /// Currently tracks total supply and validates mint authority
    ///
    /// Design Note: reward_type is u8 (not enum) to allow for future reward types
    /// without requiring program upgrade. Current valid values are 0-2.
    pub fn process_mint_reward(
        accounts: &[AccountInfo],
        amount: u64,
        reward_type: u8,
        program_id: &Pubkey,    // [UNUSED] Will be used for CPI to SPL Token program
    ) -> ProgramResult {
        let account_info_iter = &mut accounts.iter();
        let mint_authority = next_account_info(account_info_iter)?;
        let mint_account = next_account_info(account_info_iter)?;
        let destination_account = next_account_info(account_info_iter)?;  // [UNUSED] Will store recipient's token account

        if !mint_authority.is_signer {
            return Err(ProgramError::MissingRequiredSignature);
        }

        let mut token_state = TokenState::try_from_slice(&mint_account.data.borrow())?;
        
        if token_state.mint_authority != *mint_authority.key {
            return Err(ClaudCoinError::InvalidAuthority.into());
        }

        // Validate reward type
        if reward_type > 2 {
            return Err(ClaudCoinError::InvalidRewardType.into());
        }

        // Calculate actual reward based on type
        let base_reward = match reward_type {
            0 => token_state.base_tool_reward,
            1 => token_state.base_resource_reward,
            2 => token_state.base_community_reward,
            _ => return Err(ClaudCoinError::InvalidRewardType.into()),
        };

        let actual_reward = amount.saturating_mul(base_reward);

        token_state.total_supply = token_state
            .total_supply
            .checked_add(actual_reward)
            .ok_or(ClaudCoinError::AmountOverflow)?;

        token_state.serialize(&mut &mut mint_account.data.borrow_mut()[..])?;
        
        // TODO: Implement actual token transfer using spl_token
        
        Ok(())
    }

    /// Records and validates tool usage, preparing for reward distribution
    /// Phase 2 will add automatic reward calculation and token transfers
    /// Phase 3 will integrate with achievement tracking system
    ///
    /// Design Notes:
    /// 1. tool_id is [u8; 32] to support future integration with arbitrary tool identifiers
    /// 2. complexity_score is u16 (not u8) to allow for future expansion of scoring system
    /// 3. 60-second cooldown is a temporary value for testing - will be governance-controlled
    pub fn process_record_tool_usage(
        accounts: &[AccountInfo],
        tool_id: [u8; 32],      // [UNUSED] Will track specific tool usage
        complexity_score: u16,
        program_id: &Pubkey,    // [UNUSED] Will be used for CPI to token program
    ) -> ProgramResult {
        let account_info_iter = &mut accounts.iter();
        let user_account = next_account_info(account_info_iter)?;
        let user_token_account = next_account_info(account_info_iter)?;  // [UNUSED] Will store user's reward tokens
        let stats_account = next_account_info(account_info_iter)?;
        let clock = Clock::get()?;

        if !user_account.is_signer {
            return Err(ProgramError::MissingRequiredSignature);
        }

        // Validate complexity score (0-1000 range)
        if complexity_score > 1000 {
            return Err(ClaudCoinError::InvalidComplexityScore.into());
        }

        let mut user_stats = if stats_account.data_is_empty() {
            UserStats {
                user: *user_account.key,
                total_tool_uses: 0,
                total_complexity: 0,
                total_rewards: 0,
                last_reward_time: 0,
            }
        } else {
            UserStats::try_from_slice(&stats_account.data.borrow())?
        };

        // Ensure minimum time between tool usages (e.g., 1 minute)
        if clock.unix_timestamp - user_stats.last_reward_time < 60 {
            return Err(ClaudCoinError::ToolUsageTooFrequent.into());
        }

        user_stats.total_tool_uses += 1;
        user_stats.total_complexity += complexity_score as u64;
        user_stats.last_reward_time = clock.unix_timestamp;

        user_stats.serialize(&mut &mut stats_account.data.borrow_mut()[..])?;

        // TODO: Calculate and distribute rewards based on complexity score
        
        Ok(())
    }

    /// Creates new achievements that users can earn
    /// Phase 3 will expand this to include NFT rewards and advanced tracking
    ///
    /// Design Notes:
    /// 1. Achievement IDs use [u8; 32] to maintain compatibility with future NFT integration
    /// 2. is_active flag allows for achievement deprecation without removal
    /// 3. times_claimed is u64 to support high-volume achievement claims
    pub fn process_create_achievement(
        program_id: &Pubkey,    // [UNUSED] Will be used for CPI to token program
        accounts: &[AccountInfo],
        id: [u8; 32],
        required_score: u64,
        reward_amount: u64,
    ) -> ProgramResult {
        let account_info_iter = &mut accounts.iter();
        let authority = next_account_info(account_info_iter)?;
        let achievement_account = next_account_info(account_info_iter)?;
        let rent = &Rent::from_account_info(next_account_info(account_info_iter)?)?;

        if !authority.is_signer {
            return Err(ProgramError::MissingRequiredSignature);
        }

        if !rent.is_exempt(achievement_account.lamports(), Achievement::SIZE) {
            return Err(ClaudCoinError::NotRentExempt.into());
        }

        let achievement = Achievement {
            id,
            required_score,
            reward_amount,
            is_active: true,
            times_claimed: 0,
        };

        achievement.serialize(&mut &mut achievement_account.data.borrow_mut()[..])?;
        Ok(())
    }

    /// Processes achievement claims and distributes rewards
    /// Phase 2 will implement token transfers for achievement rewards
    /// Phase 3 will add NFT minting for special achievements
    ///
    /// Design Notes:
    /// 1. Achievement validation is intentionally minimal in Phase 1
    /// 2. User-specific claim tracking will be added in Phase 3
    /// 3. NFT minting capability is prepared via program_id parameter
    pub fn process_claim_achievement(
        program_id: &Pubkey,    // [UNUSED] Will be used for CPI to token program
        accounts: &[AccountInfo],
        achievement_id: [u8; 32],
    ) -> ProgramResult {
        let account_info_iter = &mut accounts.iter();
        let user_account = next_account_info(account_info_iter)?;
        let user_token_account = next_account_info(account_info_iter)?;  // [UNUSED] Will store achievement rewards
        let achievement_account = next_account_info(account_info_iter)?;

        if !user_account.is_signer {
            return Err(ProgramError::MissingRequiredSignature);
        }

        let mut achievement = Achievement::try_from_slice(&achievement_account.data.borrow())?;
        
        if !achievement.is_active {
            return Err(ClaudCoinError::AchievementNotActive.into());
        }

        if achievement.id != achievement_id {
            return Err(ClaudCoinError::AchievementNotFound.into());
        }

        // TODO: Check if user meets achievement requirements
        // TODO: Check if achievement already claimed by user
        // TODO: Distribute reward tokens to user
        
        achievement.times_claimed += 1;
        achievement.serialize(&mut &mut achievement_account.data.borrow_mut()[..])?;

        Ok(())
    }
} 