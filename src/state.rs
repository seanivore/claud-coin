use borsh::{BorshDeserialize, BorshSerialize};
use solana_program::pubkey::Pubkey;

/// Main token state holding mint information and global settings
#[derive(BorshSerialize, BorshDeserialize, Debug)]
pub struct TokenState {
    /// The mint authority that can mint new tokens
    pub mint_authority: Pubkey,
    /// Total supply of tokens
    pub total_supply: u64,
    /// Number of decimal places
    pub decimals: u8,
    /// Whether the mint authority can be updated
    pub is_initialized: bool,
    /// Base reward rate for tool usage (can be adjusted by complexity)
    pub base_tool_reward: u64,
    /// Base reward rate for resource access
    pub base_resource_reward: u64,
    /// Base reward rate for community contributions
    pub base_community_reward: u64,
}

/// Tracks a user's MCP tool usage statistics
#[derive(BorshSerialize, BorshDeserialize, Debug)]
pub struct UserStats {
    /// The user's public key
    pub user: Pubkey,
    /// Total number of tool usages
    pub total_tool_uses: u64,
    /// Cumulative complexity score
    pub total_complexity: u64,
    /// Total rewards earned
    pub total_rewards: u64,
    /// Last reward claim timestamp
    pub last_reward_time: i64,
}

/// Represents an achievement that users can earn
#[derive(BorshSerialize, BorshDeserialize, Debug)]
pub struct Achievement {
    /// Achievement identifier
    pub id: [u8; 32],
    /// Required score to unlock
    pub required_score: u64,
    /// Reward amount when claimed
    pub reward_amount: u64,
    /// Whether this achievement is still active
    pub is_active: bool,
    /// Total times this achievement has been claimed
    pub times_claimed: u64,
}

/// Tracks a user's progress towards achievements
#[derive(BorshSerialize, BorshDeserialize, Debug)]
pub struct UserAchievements {
    /// The user's public key
    pub user: Pubkey,
    /// Vector of claimed achievement IDs
    pub claimed_achievements: Vec<[u8; 32]>,
    /// Current progress scores for various metrics
    pub scores: Vec<(String, u64)>,
}

impl TokenState {
    /// Get the size of the state struct for rent calculation
    pub const SIZE: usize = 32 + 8 + 1 + 1 + 8 + 8 + 8;
}

impl UserStats {
    /// Get the size of the state struct for rent calculation
    pub const SIZE: usize = 32 + 8 + 8 + 8 + 8;
}

impl Achievement {
    /// Get the size of the state struct for rent calculation
    pub const SIZE: usize = 32 + 8 + 8 + 1 + 8;
}

// UserAchievements size is dynamic due to Vec, will need to be calculated at runtime 