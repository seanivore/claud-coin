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
import markdown

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn

from pydantic import BaseModel, Field
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
from openai.types.chat.completion_create_params import Function as OpenAIFunction

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize console for rich output
console = Console()

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define element status enum
class ElementStatus(str, Enum):
    EXISTING = "EXISTING"
    MISSING = "MISSING"
    OUTDATED = "OUTDATED"
    INCOMPLETE = "INCOMPLETE"

# Define models for function calling
class DocumentElementInfo(BaseModel):
    element_name: str = Field(..., description="Name of the documentation element")
    element_status: ElementStatus = Field(..., description="Status of the element: EXISTING, MISSING, OUTDATED, or INCOMPLETE")
    element_description: str = Field(..., description="Brief description of what this element should contain")
    element_importance: int = Field(..., description="Importance rating from 1-10, where 10 is most important", ge=1, le=10)

class AnalyzeDocumentsArgs(BaseModel):
    elements: List[DocumentElementInfo] = Field(..., description="List of document elements analyzed from the provided files")
    reasoning: str = Field(..., description="Reasoning behind the analysis and element identification")

class SaveResultsArgs(BaseModel):
    category: str = Field(..., description="Category of documentation being analyzed (MCP, BLOCKCHAIN, or OTHER)")
    output_path: str = Field(..., description="File path where to save the results")
    elements: List[DocumentElementInfo] = Field(..., description="List of document elements to save")
    reasoning: str = Field(..., description="Reasoning for the element organization and priority")

class CompleteTaskArgs(BaseModel):
    reasoning: str = Field(..., description="Explanation of why the task is now complete")

# Define OpenAI Function specifications
functions = [
    OpenAIFunction(
        name="analyze_documents",
        description="Analyze documentation files to identify required elements and their status",
        parameters=AnalyzeDocumentsArgs.model_json_schema()
    ),
    OpenAIFunction(
        name="save_results",
        description="Save the analysis results to a file",
        parameters=SaveResultsArgs.model_json_schema()
    ),
    OpenAIFunction(
        name="complete_task",
        description="Signal that the element listing task is complete",
        parameters=CompleteTaskArgs.model_json_schema()
    )
]

# Agent system prompt
SYSTEM_PROMPT = """You are OG Clod Docs Element Lister, an expert agent that analyzes technical documentation to identify required elements.

Your task is to review Solana core feature documentation and create comprehensive lists of required documentation elements for different categories (MCP, BLOCKCHAIN, OTHER).

For each element you identify, determine its status:
- EXISTING: Element exists and is complete
- MISSING: Element does not exist but is needed
- OUTDATED: Element exists but needs updating
- INCOMPLETE: Element exists but is missing key information

Create a prioritized, numbered list of all elements with statuses.

IMPORTANT: Each list must be comprehensive and clear enough that another agent can use it to find the missing or outdated elements.
"""

# Function implementations
def analyze_documents(docs_dir: str, category: str) -> Dict[str, Any]:
    """
    Analyze the documentation files in the specified directory for the given category.
    """
    console.print(f"[bold blue]Analyzing documents for category:[/bold blue] {category}")
    
    # Find all markdown files in the directory
    md_files = glob.glob(os.path.join(docs_dir, "**/*.md"), recursive=True)
    
    if not md_files:
        console.print(f"[bold red]Error:[/bold red] No markdown files found in {docs_dir}")
        sys.exit(1)
    
    console.print(f"Found [bold]{len(md_files)}[/bold] markdown files to analyze")
    
    # Read and process all markdown files
    file_contents = {}
    for file_path in md_files:
        file_name = os.path.basename(file_path)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Convert markdown to plain text to remove formatting that might confuse the LLM
                html = markdown.markdown(content)
                # Simplify by keeping the original markdown, as it has structure
                file_contents[file_name] = content
        except Exception as e:
            console.print(f"[bold red]Error reading file {file_name}:[/bold red] {str(e)}")
    
    # Create a single context with file names and contents
    context = f"DOCUMENTATION CATEGORY: {category}\n\n"
    for file_name, content in file_contents.items():
        context += f"FILE: {file_name}\n{'='*80}\n{content}\n\n"
    
    # Prepare prompt for OpenAI
    messages: List[ChatCompletionMessageParam] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"""
        Analyze the following documentation files for {category} elements. 
        
        Create a comprehensive list of documentation elements that are:
        1. Required for a complete documentation set
        2. Expected by developers and users
        3. Appropriate for the {category} category
        
        For each element, determine if it is EXISTING, MISSING, OUTDATED, or INCOMPLETE.
        
        Consider industry standards for {category} documentation as well as what is present in these files.
        
        Here are the files to analyze:
        
        {context}
        """}
    ]
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]Analyzing documentation content with LLM...[/bold blue]"),
        transient=True,
    ) as progress:
        task = progress.add_task("Analyzing...", total=None)
        try:
            response = openai_client.chat.completions.create(
                model="gpt-4o-2024-08-06",  # Using GPT-4o for robust reasoning
                messages=messages,
                functions=functions,
                function_call={"name": "analyze_documents"}
            )
            
            function_call = response.choices[0].message.function_call
            if function_call and function_call.name == "analyze_documents":
                analysis_results = json.loads(function_call.arguments)
                return analysis_results
            else:
                console.print("[bold red]Error:[/bold red] Expected function call not received")
                sys.exit(1)
        except Exception as e:
            console.print(f"[bold red]Error during analysis:[/bold red] {str(e)}")
            sys.exit(1)

def save_results(category: str, output_path: str, elements: List[Dict[str, Any]], reasoning: str) -> str:
    """
    Save the analysis results to a markdown file.
    """
    console.print(f"[bold blue]Saving results for category:[/bold blue] {category}")
    
    # Create the output file path
    output_file = os.path.join(output_path, f"OG_CLOD_DOCS_{category}_ELEMENTS.md")
    
    # Sort elements by importance and then status
    sorted_elements = sorted(elements, key=lambda x: (-x["element_importance"], x["element_status"]))
    
    # Create the markdown content
    content = f"# OG CLOD DOCS {category} ELEMENTS\n\n"
    content += "## Analysis Reasoning\n\n"
    content += f"{reasoning}\n\n"
    content += "## Element List\n\n"
    
    # Add each element to the list with numbering
    for i, element in enumerate(sorted_elements, 1):
        status = element["element_status"]
        content += f"{i}. **{element['element_name']}** [{status}]\n"
        content += f"   - **Description**: {element['element_description']}\n"
        content += f"   - **Importance**: {element['element_importance']}/10\n\n"
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Write the file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        console.print(f"[bold green]Results saved to:[/bold green] {output_file}")
        return output_file
    except Exception as e:
        console.print(f"[bold red]Error saving results:[/bold red] {str(e)}")
        sys.exit(1)

def complete_task(reasoning: str) -> str:
    """
    Signal completion of the task.
    """
    message = f"Element listing task completed: {reasoning}"
    console.print(Panel(message, title="[bold green]Task Complete[/bold green]", border_style="green"))
    return message

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="OG Clod Docs Element Lister - Creates comprehensive lists of required documentation elements")
    
    parser.add_argument("--docs-dir", "-d", required=True, 
                        help="Directory containing documents to analyze")
    parser.add_argument("--output-dir", "-o", required=True, 
                        help="Directory to save element lists")
    parser.add_argument("--categories", "-c", default="MCP,BLOCKCHAIN,OTHER",
                        help="Specific categories to analyze (comma-separated)")
    
    args = parser.parse_args()
    
    # Parse categories
    categories = [cat.strip().upper() for cat in args.categories.split(",")]
    valid_categories = ["MCP", "BLOCKCHAIN", "OTHER"]
    for category in categories:
        if category not in valid_categories:
            console.print(f"[bold red]Error:[/bold red] Invalid category '{category}'. Must be one of: {', '.join(valid_categories)}")
            sys.exit(1)
    
    console.print(Panel(f"OG Clod Docs Element Lister", title="[bold]Starting Analysis[/bold]", border_style="blue"))
    console.print(f"Analyzing documentation in: [bold]{args.docs_dir}[/bold]")
    console.print(f"Categories to analyze: [bold]{', '.join(categories)}[/bold]")
    console.print(f"Output directory: [bold]{args.output_dir}[/bold]\n")
    
    # Process each category
    for category in categories:
        console.print(Panel(f"Starting analysis for [bold]{category}[/bold]", border_style="blue"))
        
        # Step 1: Analyze documents
        analysis_results = analyze_documents(args.docs_dir, category)
        
        # Display analysis summary
        console.print(f"\n[bold]Analysis Summary for {category}:[/bold]")
        console.print(f"Found [bold]{len(analysis_results['elements'])}[/bold] elements")
        
        status_counts = {}
        for element in analysis_results["elements"]:
            status = element["element_status"]
            status_counts[status] = status_counts.get(status, 0) + 1
        
        for status, count in status_counts.items():
            status_color = {
                "EXISTING": "green",
                "MISSING": "red",
                "OUTDATED": "yellow",
                "INCOMPLETE": "yellow"
            }.get(status, "white")
            console.print(f"[bold {status_color}]{status}:[/bold {status_color}] {count} elements")
        
        # Step 2: Save results
        output_file = save_results(
            category=category,
            output_path=args.output_dir,
            elements=analysis_results["elements"],
            reasoning=analysis_results["reasoning"]
        )
        
        # Display file location
        console.print(f"Category [bold]{category}[/bold] analysis completed and saved to {output_file}\n")
    
    # Signal completion
    complete_task(f"Successfully analyzed {len(categories)} categories and created element lists in {args.output_dir}")

if __name__ == "__main__":
    main()