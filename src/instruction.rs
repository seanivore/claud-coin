use solana_program::program_error::ProgramError;
use std::convert::TryInto;

#[derive(Debug)]
pub enum ClaudCoinInstruction {
    /// Initialize a new token
    /// 
    /// Accounts expected:
    /// 1. `[signer]` The account of the person initializing the token
    /// 2. `[writable]` The token mint account
    /// 3. `[]` The rent sysvar
    /// 4. `[]` The token program
    Initialize,

    /// Mint new tokens as rewards for MCP usage
    /// 
    /// Accounts expected:
    /// 1. `[signer]` The mint authority
    /// 2. `[writable]` The token mint account
    /// 3. `[writable]` The destination account
    /// 4. `[]` The token program
    MintReward {
        /// The amount of tokens to mint as reward
        amount: u64,
        /// The type of reward (0 = tool usage, 1 = resource access, 2 = community contribution)
        reward_type: u8,
    },

    /// Record MCP tool usage and distribute rewards
    /// 
    /// Accounts expected:
    /// 1. `[signer]` The user account
    /// 2. `[writable]` The user's token account
    /// 3. `[writable]` The usage stats account
    /// 4. `[]` The token program
    RecordToolUsage {
        /// Tool identifier
        tool_id: [u8; 32],
        /// Usage complexity score (affects reward calculation)
        complexity_score: u16,
    },

    /// Create achievement milestone
    /// 
    /// Accounts expected:
    /// 1. `[signer]` The authority account
    /// 2. `[writable]` The achievement account
    /// 3. `[]` The rent sysvar
    CreateAchievement {
        /// Achievement identifier
        id: [u8; 32],
        /// Required score to unlock
        required_score: u64,
        /// Reward amount
        reward_amount: u64,
    },

    /// Claim achievement reward
    /// 
    /// Accounts expected:
    /// 1. `[signer]` The user account
    /// 2. `[writable]` The user's token account
    /// 3. `[writable]` The achievement account
    /// 4. `[]` The token program
    ClaimAchievement {
        /// Achievement identifier
        achievement_id: [u8; 32],
    },
}

impl ClaudCoinInstruction {
    /// Unpacks a byte buffer into a ClaudCoinInstruction
    pub fn unpack(input: &[u8]) -> Result<Self, ProgramError> {
        let (tag, rest) = input.split_first().ok_or(ProgramError::InvalidInstructionData)?;

        Ok(match tag {
            0 => Self::Initialize,
            1 => {
                let amount = Self::unpack_amount(rest)?;
                let reward_type = rest.get(8).ok_or(ProgramError::InvalidInstructionData)?;
                Self::MintReward {
                    amount,
                    reward_type: *reward_type,
                }
            },
            2 => {
                let tool_id = Self::unpack_bytes32(&rest[..32])?;
                let complexity_score = rest
                    .get(32..34)
                    .and_then(|slice| slice.try_into().ok())
                    .map(u16::from_le_bytes)
                    .ok_or(ProgramError::InvalidInstructionData)?;
                Self::RecordToolUsage {
                    tool_id,
                    complexity_score,
                }
            },
            3 => {
                let id = Self::unpack_bytes32(&rest[..32])?;
                let required_score = Self::unpack_u64(&rest[32..40])?;
                let reward_amount = Self::unpack_u64(&rest[40..48])?;
                Self::CreateAchievement {
                    id,
                    required_score,
                    reward_amount,
                }
            },
            4 => {
                let achievement_id = Self::unpack_bytes32(rest)?;
                Self::ClaimAchievement { achievement_id }
            },
            _ => return Err(ProgramError::InvalidInstructionData),
        })
    }

    fn unpack_amount(input: &[u8]) -> Result<u64, ProgramError> {
        Self::unpack_u64(input)
    }

    fn unpack_u64(input: &[u8]) -> Result<u64, ProgramError> {
        input
            .get(..8)
            .and_then(|slice| slice.try_into().ok())
            .map(u64::from_le_bytes)
            .ok_or(ProgramError::InvalidInstructionData)
    }

    fn unpack_bytes32(input: &[u8]) -> Result<[u8; 32], ProgramError> {
        input
            .get(..32)
            .and_then(|slice| slice.try_into().ok())
            .ok_or(ProgramError::InvalidInstructionData)
    }
}