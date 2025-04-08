# /// script
# dependencies = [
#   "openai>=1.63.0",
#   "anthropic>=0.17.0",
#   "rich>=13.7.0",
#   "pydantic>=2.0.0",
#   "python-dotenv>=1.0.0",
# ]
# ///

import os
import json
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
import openai
from anthropic import Anthropic
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv

# Global variables
args = None
task_complete = False

# Load environment variables
load_dotenv()

# Initialize console for pretty output
console = Console()

# Initialize OpenAI client
openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize Anthropic client
anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Define tool schemas
class ReadDocumentArgs(BaseModel):
    reasoning: str = Field(..., description="Explanation for reading this document")
    file_path: str = Field(..., description="Path to the document file")

class AnalyzeDocumentArgs(BaseModel):
    reasoning: str = Field(..., description="Explanation for analyzing this document")
    content: str = Field(..., description="Document content to analyze")
    focus_areas: Optional[List[str]] = Field(None, description="Specific areas to focus analysis on")

class SaveFeedbackArgs(BaseModel):
    reasoning: str = Field(..., description="Explanation for saving this feedback")
    feedback: str = Field(..., description="Documentation feedback to save")
    output_path: str = Field(..., description="Path to save feedback")

class CompleteTaskArgs(BaseModel):
    reasoning: str = Field(..., description="Explanation of why the task is complete")

# Create tools list for Claude API
tools = [
    {
        "name": "read_document",
        "description": "Reads a document file",
        "input_schema": {
            "type": "object",
            "properties": {
                "reasoning": {
                    "type": "string", 
                    "description": "Explanation for reading this document"
                },
                "file_path": {
                    "type": "string", 
                    "description": "Path to the document file"
                }
            },
            "required": ["reasoning", "file_path"]
        }
    },
    {
        "name": "analyze_document",
        "description": "Analyzes document for quality, consistency, and completeness",
        "input_schema": {
            "type": "object",
            "properties": {
                "reasoning": {
                    "type": "string", 
                    "description": "Explanation for analyzing this document"
                },
                "content": {
                    "type": "string", 
                    "description": "Document content to analyze"
                },
                "focus_areas": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Specific areas to focus analysis on"
                }
            },
            "required": ["reasoning", "content"]
        }
    },
    {
        "name": "save_feedback",
        "description": "Saves feedback to a file",
        "input_schema": {
            "type": "object",
            "properties": {
                "reasoning": {
                    "type": "string", 
                    "description": "Explanation for saving this feedback"
                },
                "feedback": {
                    "type": "string", 
                    "description": "Documentation feedback to save"
                },
                "output_path": {
                    "type": "string", 
                    "description": "Path to save feedback"
                }
            },
            "required": ["reasoning", "feedback", "output_path"]
        }
    },
    {
        "name": "complete_task",
        "description": "Signals that the feedback task is complete",
        "input_schema": {
            "type": "object",
            "properties": {
                "reasoning": {
                    "type": "string", 
                    "description": "Explanation of why the task is complete"
                }
            },
            "required": ["reasoning"]
        }
    }
]

# Tool implementation functions
def read_document(reasoning: str, file_path: str) -> str:
    """Read a document file and return its content."""
    console.log(f"[blue]Reading document[/blue] - Path: {file_path} - Reasoning: {reasoning}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return content[:100000]  # Increased limit for larger files
    except Exception as e:
        console.log(f"[red]Error reading document: {str(e)}[/red]")
        return f"Error: {str(e)}"

def analyze_document(reasoning: str, content: str, focus_areas: Optional[List[str]] = None) -> str:
    """Analyze document content for quality, consistency, and completeness."""
    console.log(f"[blue]Analyzing document[/blue] - Focus Areas: {focus_areas} - Reasoning: {reasoning}")
    
    # Here we would typically process the document in some way
    # For our agent, we'll let the LLM handle this analysis via the conversation
    focus_areas_str = ", ".join(focus_areas) if focus_areas else "all aspects"
    return f"Document content received ({len(content)} characters). Ready for analysis focusing on {focus_areas_str}."

def save_feedback(reasoning: str, feedback: str, output_path: str) -> str:
    """Save feedback to a file."""
    # Override with the correct output path from command line args
    global args, task_complete
    
    # Use the output path from command line arguments
    actual_output_path = args.output
    console.log(f"[blue]Saving feedback[/blue] - Path: {actual_output_path} - Reasoning: {reasoning}")
    
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(actual_output_path)), exist_ok=True)
        
        with open(actual_output_path, "w", encoding="utf-8") as f:
            f.write(feedback)
            
        # Automatically mark task as complete after saving feedback
        task_complete = True
        console.print(Panel(f"[green]Task Complete[/green] - Feedback saved to {actual_output_path}", title="Complete"))
        
        return f"Successfully saved {len(feedback)} characters to {actual_output_path}"
    except Exception as e:
        console.log(f"[red]Error saving feedback: {str(e)}[/red]")
        return f"Error: {str(e)}"

def complete_task(reasoning: str) -> str:
    """Signal that the feedback task is complete."""
    global task_complete
    task_complete = True
    console.print(Panel(f"[green]Task Complete[/green] - Reasoning: {reasoning}", title="Complete"))
    return "Documentation feedback task completed successfully"

def process_streamed_response(stream) -> Dict[str, Any]:
    """Process a streamed response from Anthropic API and combine it into a single response object."""
    console.log("[blue]Processing streamed response[/blue]")
    
    # Initialize structure to collect streamed content
    content_blocks = []
    
    # Process each event in the stream
    for event in stream:
        if hasattr(event, 'delta') and hasattr(event.delta, 'content_block'):
            if event.delta.content_block is not None:
                # For the first part of a content block
                if event.delta.type == "content_block_start":
                    current_block = event.delta.content_block
                    content_blocks.append(current_block)
                # For content_block_delta events, update the last content block
                elif event.delta.type == "content_block_delta" and content_blocks:
                    last_block = content_blocks[-1]
                    # Update text for text blocks
                    if last_block.type == "text" and hasattr(event.delta.content_block, 'text'):
                        last_block.text += event.delta.content_block.text
                    # Update other fields similarly if needed
    
    # Return a response object with the collected content
    return type('obj', (object,), {
        "content": content_blocks,
        "id": "streamed_response",
        "model": "claude-3-7-sonnet-20250219",
        "role": "assistant",
        "stop_reason": "end_turn",
        "stop_sequence": None,
        "usage": None
    })

def main():
    global task_complete, args
    task_complete = False
    
    parser = argparse.ArgumentParser(description="Documentation feedback agent that analyzes document quality")
    parser.add_argument("--file", "-f", required=True, help="Input document to analyze")
    parser.add_argument("--output", "-o", default="feedback.md", help="Output file for feedback")
    parser.add_argument("--compute-limit", "-c", type=int, default=3, help="Maximum number of agent iterations")
    parser.add_argument("--focus", "-F", help="Focus areas for analysis (comma-separated)")
    parser.add_argument("--extended-thinking", "-e", action="store_true", help="Enable extended thinking mode with larger token limit")
    parser.add_argument("--token-limit", "-t", type=int, help="Override token limit")
    
    args = parser.parse_args()
    
    # Parse focus areas if provided
    focus_areas = args.focus.split(",") if args.focus else None
    
    # Create the system prompt
    system_prompt = f"""You are a documentation quality expert. Your goal is to analyze a document and provide actionable feedback.

Your task involves:
1. Reading the document
2. Analyzing it for quality, consistency, and completeness
3. Providing specific, actionable feedback
4. Organizing your feedback in a clear, structured format
5. After saving your feedback, explicitly call the complete_task function to signal completion
"""
    
    if focus_areas:
        system_prompt += f"\nSpecifically focus on these areas: {', '.join(focus_areas)}"
    
    # Initialize conversation
    messages = [{
        "role": "user",
        "content": f"Please analyze this document file: {args.file} and provide detailed feedback."
    }]
    
    # Agent loop
    iterations = 0
    max_iterations = args.compute_limit
    
    while iterations < max_iterations and not task_complete:
        iterations += 1
        console.rule(f"[yellow]Agent Loop {iterations}/{max_iterations}[/yellow]")
        
        try:
            # Determine token limit based on command line args and extended thinking mode
            if args.token_limit:
                token_limit = args.token_limit
            elif args.extended_thinking:
                token_limit = 100000
            else:
                token_limit = 10000  # Reduced to avoid streaming requirement for small requests
            
            # For high token limits, we need to use streaming
            use_streaming = token_limit > 15000
            
            if use_streaming:
                console.log(f"[blue]Using streaming mode with token limit {token_limit}[/blue]")
                # Get streaming completion from Anthropic
                stream = anthropic_client.messages.create(
                    model="claude-3-7-sonnet-20250219",  # Using Claude 3.7 Sonnet for better performance
                    max_tokens=token_limit,
                    system=system_prompt,
                    messages=messages,
                    tools=tools,
                    stream=True  # Enable streaming
                )
                
                # Process the streamed response
                response = process_streamed_response(stream)
            else:
                console.log(f"[blue]Using standard mode with token limit {token_limit}[/blue]")
                # Get standard completion from Anthropic
                response = anthropic_client.messages.create(
                    model="claude-3-7-sonnet-20250219",  # Using Claude 3.7 Sonnet for better performance
                    max_tokens=token_limit,
                    system=system_prompt,
                    messages=messages,
                    tools=tools
                )
            
            # Check if Claude wants to use tools
            has_tool_use = False
            for content_block in response.content:
                if hasattr(content_block, 'type') and content_block.type == "tool_use":
                    has_tool_use = True
                    break
            
            # If Claude just provided text (no tool use), add it to conversation and continue
            if not has_tool_use:
                # Just extract the text content
                text_content = ""
                for content_block in response.content:
                    if hasattr(content_block, 'type') and content_block.type == "text":
                        text_content += content_block.text
                
                # Add Claude's text response to conversation
                messages.append({
                    "role": "assistant",
                    "content": text_content
                })
            else:
                # For tool use, add the entire response content as is
                messages.append({
                    "role": "assistant",
                    "content": response.content
                })
                
                # Process each tool use and add results
                tool_results = []
                for content_block in response.content:
                    if hasattr(content_block, 'type') and content_block.type == "tool_use":
                        tool_use = content_block
                        function_name = tool_use.name
                        function_args = tool_use.input
                        tool_id = tool_use.id
                        
                        # Execute appropriate function
                        result = None
                        if function_name == "read_document":
                            result = read_document(**function_args)
                        elif function_name == "analyze_document":
                            result = analyze_document(**function_args)
                        elif function_name == "save_feedback":
                            result = save_feedback(**function_args)
                        elif function_name == "complete_task":
                            result = complete_task(**function_args)
                        else:
                            result = f"Unknown function: {function_name}"
                        
                        # Add to tool results
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": tool_id,
                            "content": str(result)
                        })
                
                # Add all tool results in a single message
                if tool_results:
                    messages.append({
                        "role": "user",
                        "content": tool_results
                    })
        
        except Exception as e:
            console.log(f"[red]Error in agent loop: {str(e)}[/red]")
            console.print_exception()
    
    if iterations >= max_iterations and not task_complete:
        console.print("[yellow]Reached maximum iterations without completion[/yellow]")
    
if __name__ == "__main__":
    main()