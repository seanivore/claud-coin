# $CLAUD Forum Flag System

## Flag System Overview
The $CLAUD forum implements a command-line inspired flag system that serves multiple purposes:
1. Content categorization for improved discoverability
2. Reward structure for encouraging valuable contributions
3. Filtering mechanism for personalized content browsing
4. Community culture reinforcement through terminal aesthetics

## Flag Categories

### Primary Flags (Required)
Each post must include exactly one primary flag that defines its core purpose.

| Flag                   | Reward    | Description                       | Use Case                                       |
| ---------------------- | --------- | --------------------------------- | ---------------------------------------------- |
| `--build`              | 16 tokens | Development projects and tools    | Sharing work-in-progress or completed projects |
| `--how-to`             | 24 tokens | Tutorials and educational content | Step-by-step guides, tutorials, best practices |
| `--technical-question` | 12 tokens | Help requests and problem-solving | Specific technical problems needing solutions  |
| `--discussion`         | 16 tokens | General topics and conversations  | Broader topics, opinions, industry trends      |
| `--announcement`       | 20 tokens | Official updates and news         | Community news, significant releases, events   |
| `--showcase`           | 16 tokens | Demonstrating completed work      | Displaying finished projects without tutorial  |
| `--resource`           | 20 tokens | Sharing valuable resources        | Links, tools, libraries, datasets              |

### Modifier Flags (Optional)
Users may select up to two modifier flags that provide context about the content's state or availability.

| Flag                  | Multiplier | Description                | Use Case                                    |
| --------------------- | ---------- | -------------------------- | ------------------------------------------- |
| `--progress`          | 1.2x       | Work in development        | Ongoing projects seeking early feedback     |
| `--shipped`           | 1.5x       | Completed project          | Fully functional released work              |
| `--open-source`       | 1.3x       | Freely available code      | Projects with public repositories           |
| `--seeking-feedback`  | 1.1x       | Requesting community input | Early ideas needing refinement              |
| `--experimental`      | 1.2x       | Cutting-edge concepts      | Novel approaches or techniques              |
| `--beginner-friendly` | 1.2x       | Accessible to newcomers    | Content specifically designed for beginners |
| `--advanced`          | 1.2x       | Complex technical content  | Topics requiring significant expertise      |

### Platform Flags (Optional)
Users may select up to three platform flags to indicate relevant environments.

| Category          | Flags                                                   | Bonus     | Examples                      |
| ----------------- | ------------------------------------------------------- | --------- | ----------------------------- |
| Operating Systems | `--windows`, `--macos`, `--linux`, `--ios`, `--android` | +2 tokens | OS-specific implementations   |
| Deployment        | `--web`, `--mobile`, `--desktop`, `--cloud`, `--edge`   | +2 tokens | Deployment target discussions |
| Services          | `--aws`, `--azure`, `--gcp`, `--firebase`               | +2 tokens | Cloud service implementations |
| Frameworks        | `--react`, `--angular`, `--vue`, `--django`, `--flask`  | +2 tokens | Framework-specific solutions  |

### Language Flags (Optional)
Users may select up to three language flags to indicate relevant programming languages.

| Category       | Examples                                           | Bonus     | Use Case                    |
| -------------- | -------------------------------------------------- | --------- | --------------------------- |
| Frontend       | `--javascript`, `--typescript`, `--html`, `--css`  | +2 tokens | Frontend development topics |
| Backend        | `--python`, `--java`, `--csharp`, `--go`, `--rust` | +2 tokens | Backend development topics  |
| Mobile         | `--swift`, `--kotlin`, `--dart`                    | +2 tokens | Mobile development topics   |
| Data           | `--sql`, `--r`, `--julia`                          | +2 tokens | Data processing topics      |
| Infrastructure | `--yaml`, `--terraform`, `--bash`                  | +2 tokens | Infrastructure topics       |

## Usage Rules

### Flag Limitations
- **Primary Flags**: Exactly 1 required
- **Modifier Flags**: Maximum of 2 allowed
- **Platform/Language Flags**: Maximum of 3 of each type allowed
- **Total Maximum**: 9 flags per post (1 primary + 2 modifier + 3 platform + 3 language)

### Reward Calculation
```
Final Reward = (Primary Flag Base Value × Modifier Multipliers) + Platform/Language Bonuses
```

#### Example Calculations:
1. Basic tutorial: `--how-to` = 24 tokens
2. Open-source project: `--build --open-source` = 16 × 1.3 = 20.8 tokens
3. Comprehensive guide: `--how-to --shipped --beginner-friendly --python --javascript` = (24 × 1.5 × 1.2) + 2 + 2 = 47.2 tokens

### Flag Usage Best Practices
- Use the most specific primary flag for your content
- Only use modifier flags that genuinely apply
- Include relevant platform/language flags for better discoverability
- Don't use flags solely for token maximization
- Consider your audience when selecting flags

## Flag Discovery and Management

### Finding Available Flags
- Use `man flags` in the forum to view all available flags
- Use auto-completion when typing a flag name
- Browse flag categories in the posting interface

### Suggesting New Flags
The flag system can evolve with community needs:
1. Community members can propose new flags
2. Proposals undergo review period
3. Approved flags are added to the system
4. Flag rewards may be adjusted periodically for balance

## Implementation Guidelines

### User Interface
- Flags should appear as terminal-style arguments in post headings
- Clicking a flag should filter content by that flag
- Flag selection should include auto-completion
- Visual indicators should distinguish flag categories

### Technical Requirements
- Flag storage as metadata with posts
- Indexing for efficient filtering
- Reward calculation at post submission time
- Flag suggestion system based on post content