use std::sync::Arc;
use tokio::sync::RwLock;
use solana_client::rpc_client::RpcClient;
use solana_sdk::{
    commitment_config::CommitmentConfig,
    pubkey::Pubkey,
    signature::{Keypair, Signer},
    transaction::Transaction,
};
use anyhow::Result;
use serde::{Deserialize, Serialize};

/// Client configuration
#[derive(Clone, Debug)]
pub struct Config {
    /// RPC endpoint URL
    pub url: String,
    /// Commitment level
    pub commitment: CommitmentConfig,
    /// Payer account for transactions
    pub payer: Arc<Keypair>,
}

/// Main client for interacting with Claud Coin program
pub struct ClaudCoinClient {
    /// Client configuration
    config: Config,
    /// RPC client
    rpc_client: Arc<RpcClient>,
    /// Program ID
    program_id: Pubkey,
    /// SSE client for real-time updates
    sse_client: Arc<RwLock<Option<EventSource>>>,
}

/// Real-time event types
#[derive(Debug, Serialize, Deserialize)]
#[serde(tag = "type", content = "data")]
pub enum ClaudCoinEvent {
    /// Tool usage recorded
    ToolUsage {
        user: Pubkey,
        tool_id: [u8; 32],
        complexity: u16,
    },
    /// Achievement unlocked
    AchievementUnlocked {
        user: Pubkey,
        achievement_id: [u8; 32],
    },
    /// Rewards distributed
    RewardsDistributed {
        user: Pubkey,
        amount: u64,
        reward_type: u8,
    },
}

impl ClaudCoinClient {
    /// Create a new client instance
    pub fn new(config: Config, program_id: Pubkey) -> Self {
        let rpc_client = Arc::new(RpcClient::new_with_commitment(
            config.url.clone(),
            config.commitment,
        ));

        Self {
            config,
            rpc_client,
            program_id,
            sse_client: Arc::new(RwLock::new(None)),
        }
    }

    /// Initialize real-time event streaming
    pub async fn init_streaming(&self, callback: impl Fn(ClaudCoinEvent) + Send + Sync + 'static) -> Result<()> {
        // TODO: Implement SSE client initialization
        Ok(())
    }

    /// Record tool usage and get rewards
    pub async fn record_tool_usage(&self, tool_id: [u8; 32], complexity_score: u16) -> Result<()> {
        // TODO: Implement tool usage recording
        Ok(())
    }

    /// Create a new achievement
    pub async fn create_achievement(
        &self,
        id: [u8; 32],
        required_score: u64,
        reward_amount: u64,
    ) -> Result<()> {
        // TODO: Implement achievement creation
        Ok(())
    }

    /// Claim an achievement reward
    pub async fn claim_achievement(&self, achievement_id: [u8; 32]) -> Result<()> {
        // TODO: Implement achievement claiming
        Ok(())
    }

    /// Get user statistics
    pub async fn get_user_stats(&self, user: &Pubkey) -> Result<UserStats> {
        // TODO: Implement user stats retrieval
        unimplemented!()
    }
}

/// Re-export common types
pub use claud_coin::state::{TokenState, UserStats, Achievement, UserAchievements}; 