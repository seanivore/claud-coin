use solana_program::program_error::ProgramError;
use thiserror::Error;

#[derive(Error, Debug, Copy, Clone)]
pub enum ClaudCoinError {
    #[error("Invalid instruction")]
    InvalidInstruction,
    
    #[error("Not rent exempt")]
    NotRentExempt,

    #[error("Expected amount mismatch")]
    ExpectedAmountMismatch,

    #[error("Amount overflow")]
    AmountOverflow,

    #[error("Achievement already claimed")]
    AchievementAlreadyClaimed,

    #[error("Achievement not found")]
    AchievementNotFound,

    #[error("Achievement requirements not met")]
    AchievementRequirementsNotMet,

    #[error("Invalid reward type")]
    InvalidRewardType,

    #[error("Tool usage too frequent")]
    ToolUsageTooFrequent,

    #[error("Invalid complexity score")]
    InvalidComplexityScore,

    #[error("User stats not initialized")]
    UserStatsNotInitialized,

    #[error("Achievement not active")]
    AchievementNotActive,

    #[error("Invalid authority")]
    InvalidAuthority,
}

impl From<ClaudCoinError> for ProgramError {
    fn from(e: ClaudCoinError) -> Self {
        ProgramError::Custom(e as u32)
    }
} 