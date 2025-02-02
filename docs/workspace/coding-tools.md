# Coding Tools

## Aider
We'll be using **Aider** via the terminal to write code. Aider is a tool that allows you to write code in natural language in a few ways that you read about in the warm up. If you need to review the document again, use the `read_file` tool: /Users/seanivore/Development/aider-docs.txt 

## Cursor.ai IDE
The code files will be open in our **Cursor.ai IDE**. This will help us if Aider can't find a troubleshooting solution and allow us to review the code for errors that the app will flag. Additionally, their Composer tool gives us additional access to premium models that come with the subscription.

### Aider Agents 
1. Large Changes use `aider --architect` command; recommended `--yes-always` [defaulted]
Chat with Architect. Have them confirm your approach, give advice, and then hand off the task to the Aider editor to make the changes. The yes-always flag will automatically start the changes. Leave it off if you want to review the changes first. 
2. Self-Directed Changes use `aider --sonnet` command; try free `--gemini/gemini-2.0-flash-exp` for very simple tasks
This is the default mode. You can mention the model you want to use when starting Aider, but Sonnet is already default. Here, you'll act as the architect and hand off changes to the Aider editor. For simple cleaning up files, note that Gemini is a fast and free option. 
3. Fully Agentic outside the terminal changes, add `--watch-files` flag [defaulted]
This will make sure that the Edior is going to watch all files in your repo looking for any AI coding instructions you add directly to the files. Specifically, aider looks for one-liner comments (# … or // …) that either start or end with AI, AI! or AI? Comments with an exclamation point or question mark are special as they triggers aider to take action to collect all the AI comments and use them as your instructions. You can write code files using `filesystem` straight to the local discography with the `AI` mention right from the start, or add `AI` later if we need updates. Here are two examples: 
   > // AI: Make a snake game. //
   > // What is the purpose of this method AI? //
   > // Write a protein folding prediction engine. AI! //

   - Settings can be updated here [/Users/seanivore/Development/job-app-automation/aider.conf.yml]
   - Look here for a full list of all possible settings: [/Users/seanivore/Development/_sample.aider.conf.yml]

### Context Files 
Aider doesn't need every file in your project. When you start Aider, in the first command, add only add files that need changes at the end, simply with spaces between each and using the relative path to the file. Note that Aider can see all files in the project directory and will find necessary additional context when needed. For any only absolutely pertinent context files, use `read:` and add the relative path to the file. Example command to run with the terminal prompt in the project's root directory:

   > aider --architect --sonnet --yes-always src/mcp.js src/sse.js read: docs/feature-build/FEATURE-1-core-mcp-integration.md 
