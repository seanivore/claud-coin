# /// script
# dependencies = [
#   "openai>=1.63.0",
#   "anthropic>=0.17.0", 
#   "rich>=13.7.0",
#   "pydantic>=2.0.0",
#   "python-dotenv>=1.0.0",
#   "markdown>=3.6.0",
# ]
# ///

import os
import sys
import json
import argparse
import glob
from pathlib import Path
from typing import List, Dict, Any, Optional
from enum import Enum

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn

from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize console for rich output
console = Console()

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define element status enum
class ElementStatus(str, Enum):
    MISSING = "MISSING"
    INCOMPLETE = "INCOMPLETE"
    PRESENT = "PRESENT"  # Changed from OUTDATED since this agent can't determine if content is outdated

# Define element importance enum
class ElementImportance(str, Enum):
    HIGH = "10/10"
    MEDIUM_HIGH = "9/10"
    MEDIUM = "8/10"
    MEDIUM_LOW = "7/10"
    LOW = "6/10"

# Define tool schemas as Python dictionaries for the OpenAI Responses API
ANALYZE_TECHNICAL_DOCS_SCHEMA = {
    "type": "function",
    "name": "analyze_technical_docs",
    "description": "Analyze documentation to identify present, missing, and incomplete technical elements",
    "parameters": {
        "type": "object",
        "properties": {
            "analysis_reasoning": {
                "type": "string",
                "description": "Reasoning behind the technical documentation analysis"
            },
            "technical_elements": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "element": {
                            "type": "string",
                            "description": "Technical documentation element name"
                        },
                        "status": {
                            "type": "string",
                            "enum": ["PRESENT", "MISSING", "INCOMPLETE"],
                            "description": "Status of the technical documentation element"
                        },
                        "description": {
                            "type": "string",
                            "description": "Description of what this technical documentation element should contain"
                        },
                        "importance": {
                            "type": "string",
                            "enum": ["10/10", "9/10", "8/10", "7/10", "6/10"],
                            "description": "Importance rating of this element on a scale of 6-10 out of 10"
                        },
                        "technical_feedback": {
                            "type": "string",
                            "description": "Technical feedback on this element's current state or implementation needs"
                        }
                    },
                    "required": ["element", "status", "description", "importance", "technical_feedback"],
                    "description": "A technical documentation element with status and feedback"
                },
                "description": "List of technical documentation elements with their status and feedback"
            }
        },
        "required": ["analysis_reasoning", "technical_elements"]
    }
}

ANALYZE_GENERAL_DOCS_SCHEMA = {
    "type": "function",
    "name": "analyze_general_docs",
    "description": "Analyze documentation to identify present, missing, and incomplete general documentation elements",
    "parameters": {
        "type": "object",
        "properties": {
            "analysis_reasoning": {
                "type": "string",
                "description": "Reasoning behind the general documentation analysis"
            },
            "general_elements": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "element": {
                            "type": "string",
                            "description": "General documentation element name"
                        },
                        "status": {
                            "type": "string",
                            "enum": ["PRESENT", "MISSING", "INCOMPLETE"],
                            "description": "Status of the general documentation element"
                        },
                        "description": {
                            "type": "string",
                            "description": "Description of what this general documentation element should contain"
                        },
                        "importance": {
                            "type": "string",
                            "enum": ["10/10", "9/10", "8/10", "7/10", "6/10"],
                            "description": "Importance rating of this element on a scale of 6-10 out of 10"
                        },
                        "general_feedback": {
                            "type": "string",
                            "description": "General writing/structure feedback on this element's current state or implementation needs"
                        }
                    },
                    "required": ["element", "status", "description", "importance", "general_feedback"],
                    "description": "A general documentation element with status and feedback"
                },
                "description": "List of general documentation elements with their status and feedback"
            }
        },
        "required": ["analysis_reasoning", "general_elements"]
    }
}

SAVE_TECHNICAL_RESULTS_SCHEMA = {
    "type": "function",
    "name": "save_technical_results",
    "description": "Save the technical documentation gap analysis results to a markdown file",
    "parameters": {
        "type": "object",
        "properties": {
            "output_path": {
                "type": "string",
                "description": "File path where to save the technical gap analysis report"
            },
            "content": {
                "type": "string",
                "description": "Content of the technical gap analysis report in markdown format"
            }
        },
        "required": ["output_path", "content"]
    }
}

SAVE_GENERAL_RESULTS_SCHEMA = {
    "type": "function",
    "name": "save_general_results",
    "description": "Save the general documentation gap analysis results to a markdown file",
    "parameters": {
        "type": "object",
        "properties": {
            "output_path": {
                "type": "string",
                "description": "File path where to save the general gap analysis report"
            },
            "content": {
                "type": "string",
                "description": "Content of the general gap analysis report in markdown format"
            }
        },
        "required": ["output_path", "content"]
    }
}

COMPLETE_TASK_SCHEMA = {
    "type": "function",
    "name": "complete_task",
    "description": "Signal that the documentation gap finding task is complete",
    "parameters": {
        "type": "object",
        "properties": {
            "reasoning": {
                "type": "string",
                "description": "Explanation of why the task is now complete"
            }
        },
        "required": ["reasoning"]
    }
}

# Function implementations
def analyze_technical_docs(technical_guide_path: str, docs_dir: str) -> Dict[str, Any]:
    """
    Analyze the technical documentation guide and existing docs to identify present, missing, and incomplete elements.
    """
    console.print(f"[bold blue]Analyzing technical documentation...[/bold blue]")
    
    # Read the technical guide content
    try:
        with open(technical_guide_path, 'r', encoding='utf-8') as f:
            technical_guide_content = f.read()
    except Exception as e:
        console.print(f"[bold red]Error reading technical guide:[/bold red] {str(e)}")
        sys.exit(1)
    
    # Find all markdown files in the docs directory
    md_files = glob.glob(os.path.join(docs_dir, "**/*.md"), recursive=True)
    
    if not md_files:
        console.print(f"[bold red]Error:[/bold red] No markdown files found in {docs_dir}")
        sys.exit(1)
    
    console.print(f"Found [bold]{len(md_files)}[/bold] markdown files to analyze")
    
    # Read the markdown files
    file_contents = {}
    for file_path in md_files:
        file_name = os.path.basename(file_path)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                file_contents[file_name] = f.read()
        except Exception as e:
            console.print(f"[bold red]Error reading {file_name}:[/bold red] {str(e)}")
    
    # Prepare the prompt for OpenAI
    docs_content = "\n\n".join([f"FILE: {name}\n{content}" for name, content in file_contents.items()])
    
    prompt = f"""
Using the technical documentation best practices guide below, analyze the existing project documentation 
to identify which technical documentation elements are PRESENT, MISSING, or INCOMPLETE.

For each technical element from the best practices guide:
1. Determine if it's PRESENT (exists adequately), MISSING (doesn't exist), or INCOMPLETE (exists but needs more detail)
2. Provide a description of what this element should contain
3. Rate its importance on a scale of 6-10 out of 10, with 10 being most critical
4. Provide specific technical feedback on its current state or implementation needs

Format each element entry with:
- Element name
- Status (PRESENT/MISSING/INCOMPLETE)
- Description of what it should contain
- Importance rating (10/10, 9/10, 8/10, 7/10, or 6/10)
- Technical feedback

Include a thorough analysis reasoning section at the beginning explaining your approach and key findings.

TECHNICAL DOCUMENTATION BEST PRACTICES GUIDE:
{technical_guide_content}

EXISTING PROJECT DOCUMENTATION:
{docs_content}
"""
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]Analyzing technical documentation...[/bold blue]"),
        transient=True,
    ) as progress:
        task = progress.add_task("Analyzing...", total=None)
        try:
            # Use the Responses API format
            response = openai_client.responses.create(
                model="gpt-4o-2024-08-06",  # Using GPT-4o for robust reasoning
                input=prompt,
                tools=[ANALYZE_TECHNICAL_DOCS_SCHEMA],
                tool_choice={"type": "function", "name": "analyze_technical_docs"}
            )
            
            # Extract function call response
            technical_results = None
            for item in response.output:
                if item.type == "function_call" and item.name == "analyze_technical_docs":
                    technical_results = json.loads(item.arguments)
                    # Sort elements by importance and then status (MISSING first)
                    def element_sort_key(element):
                        importance_map = {"10/10": 0, "9/10": 1, "8/10": 2, "7/10": 3, "6/10": 4}
                        status_map = {"MISSING": 0, "INCOMPLETE": 1, "PRESENT": 2}
                        return (importance_map.get(element["importance"], 5), status_map.get(element["status"], 3))
                    
                    technical_results["technical_elements"] = sorted(
                        technical_results["technical_elements"], 
                        key=element_sort_key
                    )
            
            if not technical_results:
                console.print("[bold red]Error:[/bold red] Expected function call not received")
                sys.exit(1)
                
            return technical_results
            
        except Exception as e:
            console.print(f"[bold red]Error during technical analysis:[/bold red] {str(e)}")
            sys.exit(1)

def analyze_general_docs(general_guide_path: str, docs_dir: str) -> Dict[str, Any]:
    """
    Analyze the general documentation guide and existing docs to identify present, missing, and incomplete elements.
    """
    console.print(f"[bold blue]Analyzing general documentation...[/bold blue]")
    
    # Read the general guide content
    try:
        with open(general_guide_path, 'r', encoding='utf-8') as f:
            general_guide_content = f.read()
    except Exception as e:
        console.print(f"[bold red]Error reading general guide:[/bold red] {str(e)}")
        sys.exit(1)
    
    # Find all markdown files in the docs directory
    md_files = glob.glob(os.path.join(docs_dir, "**/*.md"), recursive=True)
    
    if not md_files:
        console.print(f"[bold red]Error:[/bold red] No markdown files found in {docs_dir}")
        sys.exit(1)
    
    console.print(f"Found [bold]{len(md_files)}[/bold] markdown files to analyze")
    
    # Read the markdown files
    file_contents = {}
    for file_path in md_files:
        file_name = os.path.basename(file_path)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                file_contents[file_name] = f.read()
        except Exception as e:
            console.print(f"[bold red]Error reading {file_name}:[/bold red] {str(e)}")
    
    # Prepare the prompt for OpenAI
    docs_content = "\n\n".join([f"FILE: {name}\n{content}" for name, content in file_contents.items()])
    
    prompt = f"""
Using the general documentation best practices guide below, analyze the existing project documentation 
to identify which general documentation elements are PRESENT, MISSING, or INCOMPLETE.

For each general element from the best practices guide:
1. Determine if it's PRESENT (exists adequately), MISSING (doesn't exist), or INCOMPLETE (exists but needs more detail)
2. Provide a description of what this element should contain
3. Rate its importance on a scale of 6-10 out of 10, with 10 being most critical
4. Provide specific general writing/structure feedback on its current state or implementation needs

Format each element entry with:
- Element name
- Status (PRESENT/MISSING/INCOMPLETE)
- Description of what it should contain
- Importance rating (10/10, 9/10, 8/10, 7/10, or 6/10)
- General feedback

Include a thorough analysis reasoning section at the beginning explaining your approach and key findings.

GENERAL DOCUMENTATION BEST PRACTICES GUIDE:
{general_guide_content}

EXISTING PROJECT DOCUMENTATION:
{docs_content}
"""
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]Analyzing general documentation...[/bold blue]"),
        transient=True,
    ) as progress:
        task = progress.add_task("Analyzing...", total=None)
        try:
            # Use the Responses API format
            response = openai_client.responses.create(
                model="gpt-4o-2024-08-06",  # Using GPT-4o for robust reasoning
                input=prompt,
                tools=[ANALYZE_GENERAL_DOCS_SCHEMA],
                tool_choice={"type": "function", "name": "analyze_general_docs"}
            )
            
            # Extract function call response
            general_results = None
            for item in response.output:
                if item.type == "function_call" and item.name == "analyze_general_docs":
                    general_results = json.loads(item.arguments)
                    # Sort elements by importance and then status (MISSING first)
                    def element_sort_key(element):
                        importance_map = {"10/10": 0, "9/10": 1, "8/10": 2, "7/10": 3, "6/10": 4}
                        status_map = {"MISSING": 0, "INCOMPLETE": 1, "PRESENT": 2}
                        return (importance_map.get(element["importance"], 5), status_map.get(element["status"], 3))
                    
                    general_results["general_elements"] = sorted(
                        general_results["general_elements"], 
                        key=element_sort_key
                    )
            
            if not general_results:
                console.print("[bold red]Error:[/bold red] Expected function call not received")
                sys.exit(1)
                
            return general_results
            
        except Exception as e:
            console.print(f"[bold red]Error during general analysis:[/bold red] {str(e)}")
            sys.exit(1)

def save_technical_results(output_path: str, technical_results: Dict[str, Any]) -> str:
    """
    Save the technical documentation elements analysis to a markdown file.
    """
    console.print(f"[bold blue]Saving technical documentation analysis...[/bold blue]")
    
    # Create the output file path
    output_file = output_path
    
    # Create the markdown content
    content = f"# BEST_DOCS_TECHNICAL_GAPS\n\n"
    content += "## Analysis Reasoning\n\n"
    content += f"{technical_results['analysis_reasoning']}\n\n"
    content += "## Element List\n\n"
    
    # Add each element to the list with numbering
    for i, element in enumerate(technical_results['technical_elements'], 1):
        status = element["status"]
        content += f"{i}. **{element['element']}** [{status}]\n"
        content += f"   - **Description**: {element['description']}\n"
        content += f"   - **Importance**: {element['importance']}\n"
        content += f"   - **Technical Feedback**: {element['technical_feedback']}\n\n"
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Write the file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        console.print(f"[bold green]Technical documentation analysis saved to:[/bold green] {output_file}")
        return output_file
    except Exception as e:
        console.print(f"[bold red]Error saving technical results:[/bold red] {str(e)}")
        sys.exit(1)

def save_general_results(output_path: str, general_results: Dict[str, Any]) -> str:
    """
    Save the general documentation elements analysis to a markdown file.
    """
    console.print(f"[bold blue]Saving general documentation analysis...[/bold blue]")
    
    # Create the output file path
    output_file = output_path
    
    # Create the markdown content
    content = f"# BEST_DOCS_GENERAL_GAPS\n\n"
    content += "## Analysis Reasoning\n\n"
    content += f"{general_results['analysis_reasoning']}\n\n"
    content += "## Element List\n\n"
    
    # Add each element to the list with numbering
    for i, element in enumerate(general_results['general_elements'], 1):
        status = element["status"]
        content += f"{i}. **{element['element']}** [{status}]\n"
        content += f"   - **Description**: {element['description']}\n"
        content += f"   - **Importance**: {element['importance']}\n"
        content += f"   - **General Feedback**: {element['general_feedback']}\n\n"
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Write the file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        console.print(f"[bold green]General documentation analysis saved to:[/bold green] {output_file}")
        return output_file
    except Exception as e:
        console.print(f"[bold red]Error saving general results:[/bold red] {str(e)}")
        sys.exit(1)

def complete_task(reasoning: str) -> str:
    """
    Signal completion of the task.
    """
    message = f"Documentation gap finding task completed: {reasoning}"
    console.print(Panel(message, title="[bold green]Task Complete[/bold green]", border_style="green"))
    return message

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Best Docs Gap Finder - Identifies documentation gaps by comparing against best practices")
    
    parser.add_argument("--technical-guide", "-t", required=True, 
                        help="Path to the technical best practices guide file")
    parser.add_argument("--general-guide", "-g", required=True, 
                        help="Path to the general best practices guide file")
    parser.add_argument("--docs-dir", "-d", required=True, 
                        help="Directory containing documents to analyze")
    parser.add_argument("--technical-output", "-to", required=True, 
                        help="Output file path for the technical gap analysis report")
    parser.add_argument("--general-output", "-go", required=True, 
                        help="Output file path for the general gap analysis report")
    parser.add_argument("--focus", "-f", default="",
                        help="Specific aspects to focus on (comma-separated)")
    parser.add_argument("--compute-limit", "-c", type=int, default=5,
                        help="Maximum number of analysis iterations")
    
    args = parser.parse_args()
    
    # Parse focus areas if provided
    focus_areas = [area.strip() for area in args.focus.split(",")] if args.focus else None
    
    console.print(Panel(f"Best Docs Gap Finder", title="[bold]Starting Analysis[/bold]", border_style="blue"))
    console.print(f"Technical guide: [bold]{args.technical_guide}[/bold]")
    console.print(f"General guide: [bold]{args.general_guide}[/bold]")
    console.print(f"Analyzing documentation in: [bold]{args.docs_dir}[/bold]")
    console.print(f"Technical output file: [bold]{args.technical_output}[/bold]")
    console.print(f"General output file: [bold]{args.general_output}[/bold]")
    if focus_areas:
        console.print(f"Focus areas: [bold]{', '.join(focus_areas)}[/bold]\n")
    
    # Step 1: Analyze technical documentation
    console.print(Panel(f"Step 1: Analyzing Technical Documentation", border_style="blue"))
    technical_results = analyze_technical_docs(args.technical_guide, args.docs_dir)
    
    # Display analysis summary
    console.print(f"\n[bold]Technical Documentation Analysis Summary:[/bold]")
    elements = technical_results['technical_elements']
    console.print(f"Analyzed [bold]{len(elements)}[/bold] technical documentation elements")
    
    # Count elements by status
    status_counts = {"MISSING": 0, "INCOMPLETE": 0, "PRESENT": 0}
    for element in elements:
        status_counts[element['status']] += 1
    
    for status, count in status_counts.items():
        status_color = {
            "MISSING": "red",
            "INCOMPLETE": "yellow",
            "PRESENT": "green"
        }.get(status, "white")
        console.print(f"[bold {status_color}]{status}:[/bold {status_color}] {count} elements")
    
    # Step 2: Analyze general documentation
    console.print(Panel(f"Step 2: Analyzing General Documentation", border_style="blue"))
    general_results = analyze_general_docs(args.general_guide, args.docs_dir)
    
    # Display analysis summary
    console.print(f"\n[bold]General Documentation Analysis Summary:[/bold]")
    elements = general_results['general_elements']
    console.print(f"Analyzed [bold]{len(elements)}[/bold] general documentation elements")
    
    # Count elements by status
    status_counts = {"MISSING": 0, "INCOMPLETE": 0, "PRESENT": 0}
    for element in elements:
        status_counts[element['status']] += 1
    
    for status, count in status_counts.items():
        status_color = {
            "MISSING": "red",
            "INCOMPLETE": "yellow",
            "PRESENT": "green"
        }.get(status, "white")
        console.print(f"[bold {status_color}]{status}:[/bold {status_color}] {count} elements")
    
    # Step 3: Save results
    console.print(Panel(f"Step 3: Saving Results", border_style="blue"))
    technical_file = save_technical_results(args.technical_output, technical_results)
    general_file = save_general_results(args.general_output, general_results)
    
    # Display file previews
    try:
        with open(technical_file, 'r', encoding='utf-8') as f:
            content = f.read()
        preview_lines = content.split('\n')[:20]
        console.print(f"\n[bold]Technical Report Preview:[/bold]")
        console.print(Markdown('\n'.join(preview_lines) + '\n...\n'))
    except Exception as e:
        console.print(f"[bold yellow]Warning:[/bold yellow] Could not display technical report preview: {str(e)}")
    
    try:
        with open(general_file, 'r', encoding='utf-8') as f:
            content = f.read()
        preview_lines = content.split('\n')[:20]
        console.print(f"\n[bold]General Report Preview:[/bold]")
        console.print(Markdown('\n'.join(preview_lines) + '\n...\n'))
    except Exception as e:
        console.print(f"[bold yellow]Warning:[/bold yellow] Could not display general report preview: {str(e)}")
    
    # Signal completion
    complete_task(f"Successfully analyzed documentation and saved reports to {args.technical_output} and {args.general_output}")

if __name__ == "__main__":
    main()