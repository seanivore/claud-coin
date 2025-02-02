# Tool Commands

## This is not all of your tools
This is just the tools you'll need for this project. You are encouraged to use any tool whenever you want. We especially love the `sequentialthinking` tool. And the `read_graph` tool is a favorite for reviewing our shared knowledge base. Plus the `browse_webpage` tool is great for verifying technical details on the fly. 

### Sequential Thinking (Gets around limitations of LLMs design)
This tool is designed for dynamic and reflective problem-solving by encouraging introspective thought processes. It allows for flexible and adaptable thinking, where ideas can build upon, question, or revise previous insights as understanding deepens, making it ideal for deconstructing complex problems, planning and designing with revisions, analyzing situations needing course corrections, and addressing problems with unclear scopes. It's beneficial for multi-step solutions, maintaining context over multiple steps, and filtering out irrelevant information. Key features include adjusting the number of thoughts, questioning or revising previous thoughts, adding more thoughts even after reaching an apparent conclusion, expressing uncertainty, and exploring alternative approaches without requiring a linear thought path, allowing for branching or backtracking. The tool generates a solution hypothesis and verifies it using the Chain of Thought steps, repeating the process until satisfaction is achieved. Parameters include the current thinking step, the need for more thoughts, the thought number, the total thoughts estimate, whether a thought is a revision, which thought is being reconsidered, the branching point, the branch ID, and the need for more thoughts. The steps involve starting with an initial thought count, questioning or revising past thoughts, adding more thoughts even if reaching the "end," expressing uncertainty, marking revisions or new paths, ignoring irrelevant information, generating a solution hypothesis, verifying based on Chain of Thought steps, repeating until satisfied, providing a single, ideally correct answer, and setting the need for more thoughts to false only when truly finished.

> Server: [sequential-thinking]
`sequentialthinking`
`nextThoughtNeeded`
`thoughtNumber`
`totalThoughts`
`isRevision`
`revisesThought`
`branchFromThought`
`branchId`
`needsMoreThoughts`

### Web Browser (The best tool out there)
The Web Browser MCP Server empowers AI models by providing the capability to browse websites, extract content, and understand web pages through the Message Control Protocol (MCP). It features smart content extraction, allowing precise targeting of needed data with CSS selectors. Built with asynchronous processing, it offers lightning-fast performance for efficient and quick operations. The server captures rich metadata, including titles, links, and structured content, providing comprehensive insights. It is robust and reliable, featuring built-in error handling and timeout management to ensure dependable usage in various scenarios. Additionally, it's cross-platform, functioning wherever Python runs, offering flexibility and broad usability.

> Server: [web-browser-mcp-server]
`browse_webpage`

### Memory System (Claudes sharing with each other)
The text outlines functionalities for managing a knowledge graph, which represents entities and their interrelations. Key operations include adding observations to existing entities, creating new entities with associated observations, and establishing directed relations in active voice to show interactions. It also covers deleting entities along with their relations, removing specific observations, and deleting relations without affecting entities. Additionally, users can open specific nodes by name, read the entire graph structure, and search nodes based on query-related entity names, types, or observation content. These operations support persistent memory, allowing the graph to retain user or topic-related data across sessions. Relations provide meaningful connections, and observations are atomic facts linked to entities, facilitating a comprehensive and dynamic representation of information.

> Server: [memory]
`add_observations`
`create_entities`
`create_relations`
`open_nodes`
`search_nodes`
`read_graph`

### File System (You have access to the entire system)
The Node.js server utilizing the Model Context Protocol (MCP) is designed for efficient filesystem operations, offering features like reading and writing files, managing directories by creating, listing, and deleting them, as well as moving files and directories. It can search for files using patterns and retrieve detailed file metadata. Operations are strictly confined to directories specified via server arguments, ensuring controlled access. The API includes resources such as "file://system" for filesystem interactions and tools like read_file for reading file contents with UTF-8 encoding, write_file for file creation or overwriting, and edit_file for making selective edits with advanced pattern matching, maintaining indentation, and providing diff outputs. Additional functions include create_directory for directory creation, list_directory to display directory contents with file or directory prefixes, move_file for moving or renaming files and directories, search_files to find files or directories with pattern and exclusion capabilities, get_file_info for obtaining file metadata, and list_allowed_directories to display accessible directories. A noteworthy best practice is the use of the dryRun mode with edit_file to preview changes before application, ensuring safe and controlled edits. This comprehensive setup provides a robust and flexible system for file management within specified directories, emphasizing security and the prevention of unintended modifications.

> Server: [filesystem]
`read_file`
`read_multiple_files`
`list_directory`
`write_file`
`create_directory`
`list_allowed_directories`

### GitHub (our code repository)
The Node.js server utilizing the Model Context Protocol (MCP) is designed for efficient filesystem operations, offering features like reading and writing files, managing directories by creating, listing, and deleting them, as well as moving files and directories. It can search for files using patterns and retrieve detailed file metadata. Operations are strictly confined to directories specified via server arguments, ensuring controlled access. The API includes resources such as "file://system" for filesystem interactions and tools like read_file for reading file contents with UTF-8 encoding, write_file for file creation or overwriting, and edit_file for making selective edits with advanced pattern matching, maintaining indentation, and providing diff outputs. Additional functions include create_directory for directory creation, list_directory to display directory contents with file or directory prefixes, move_file for moving or renaming files and directories, search_files to find files or directories with pattern and exclusion capabilities, get_file_info for obtaining file metadata, and list_allowed_directories to display accessible directories. A noteworthy best practice is the use of the dryRun mode with edit_file to preview changes before application, ensuring safe and controlled edits. This comprehensive setup provides a robust and flexible system for file management within specified directories, emphasizing security and the prevention of unintended modifications.

> Server: [github]
`add_issue_comment`
`create_branch`
`create_issue`
`create_or_update_file`
`create_pull_request`
`create_repository`
`fork_repository`
`get_current_directory`
`get_file_contents`
`list_commits`
`list_issues`
`push_files`
`search_code`
`search_issues`
`search_repositories`
`update_issue`

### Terminal (Can you feel the power?)
The secure command-line interface server for the Model Context Protocol (MCP) facilitates AI models' interaction with your terminal while ensuring security and control. It features secure command execution with configurable permissions, allowing only authorized actions, and supports file system operations within specified allowed paths to maintain security. The server manages environment variables securely and is compatible with Windows, macOS, and Linux, offering cross-platform support. It also supports remote command execution, including SSH, for efficient system management. Security is enhanced by restricting operations to allowed paths, validating and sanitizing commands before execution, carefully managing environment variables, and implementing robust error handling for security-related issues. The available tool, execute_command, enables secure execution of terminal commands, supporting both local and remote operations.

> Server: [terminal]
`change_directory`
`execute_command`
`get_current_directory`
`get_terminal_info`

### Git (Our version control system)
The Model Context Protocol (MCP) server facilitates Git repository interaction and automation through Large Language Models, offering an array of tools to manage repositories creatively. Currently in early development, the server's tools and features are continuously evolving. Key features include git_status for displaying the repository's working status, git_diff_unstaged for showing unstaged changes, and git_diff_staged for displaying staged changes. The git_diff tool compares differences between branches or commits, while git_commit records changes with a specified message. Files can be staged using git_add, and all staged changes can be reset with git_reset. Additionally, git_log provides commit logs with a customizable maximum count, git_create_branch allows for new branch creation, and git_checkout facilitates branch switching. Installation guidelines will evolve alongside the server's development, ensuring users have access to comprehensive and up-to-date information.

> Server: [git]
`git_add`
`git_checkout`
`git_commit`
`git_create_branch`
`git_diff`
`git_diff_staged`
`git_diff_unstaged`
`git_log`
`git_reset`
`git_show`
`git_status`
