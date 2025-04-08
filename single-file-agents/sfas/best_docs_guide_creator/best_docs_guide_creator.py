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
import sys
import json
import argparse
from typing import List, Dict, Any, Optional, Union, Literal
from enum import Enum

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.markdown import Markdown

from pydantic import BaseModel, Field
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize console for rich output
console = Console()

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define research depth enum
class ResearchDepth(str, Enum):
    BASIC = "basic"
    STANDARD = "standard"
    COMPREHENSIVE = "comprehensive"

# Define guide type enum
class GuideType(str, Enum):
    TECHNICAL = "technical"
    GENERAL = "general"
    BOTH = "both"

# Define tool schemas as Python dictionaries
RESEARCH_TECHNICAL_SCHEMA = {
    "type": "function",
    "name": "research_technical_best_practices",
    "description": "Research technical documentation best practices",
    "parameters": {
        "type": "object",
        "properties": {
            "findings": {
                "type": "string",
                "description": "Comprehensive research findings on technical documentation best practices"
            },
            "sources": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": "List of sources consulted for the research"
            }
        },
        "required": ["findings"]
    }
}

RESEARCH_GENERAL_SCHEMA = {
    "type": "function",
    "name": "research_general_best_practices",
    "description": "Research general documentation best practices",
    "parameters": {
        "type": "object",
        "properties": {
            "findings": {
                "type": "string",
                "description": "Comprehensive research findings on general documentation best practices"
            },
            "sources": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": "List of sources consulted for the research"
            }
        },
        "required": ["findings"]
    }
}

COMPILE_TECHNICAL_SCHEMA = {
    "type": "function",
    "name": "compile_technical_guide",
    "description": "Compile research findings into a technical documentation best practices guide",
    "parameters": {
        "type": "object",
        "properties": {
            "guide_content": {
                "type": "string",
                "description": "Compiled technical documentation best practices guide in markdown format"
            },
            "reasoning": {
                "type": "string",
                "description": "Reasoning behind the guide structure and content"
            }
        },
        "required": ["guide_content"]
    }
}

COMPILE_GENERAL_SCHEMA = {
    "type": "function",
    "name": "compile_general_guide",
    "description": "Compile research findings into a general documentation best practices guide",
    "parameters": {
        "type": "object",
        "properties": {
            "guide_content": {
                "type": "string",
                "description": "Compiled general documentation best practices guide in markdown format"
            },
            "reasoning": {
                "type": "string",
                "description": "Reasoning behind the guide structure and content"
            }
        },
        "required": ["guide_content"]
    }
}

SAVE_GUIDE_SCHEMA = {
    "type": "function",
    "name": "save_guide",
    "description": "Save the best practices guide to a file",
    "parameters": {
        "type": "object",
        "properties": {
            "guide_type": {
                "type": "string",
                "description": "Type of guide (TECHNICAL or GENERAL)"
            },
            "output_path": {
                "type": "string",
                "description": "File path where to save the guide"
            },
            "content": {
                "type": "string",
                "description": "Content of the guide to save"
            }
        },
        "required": ["guide_type", "output_path", "content"]
    }
}

COMPLETE_TASK_SCHEMA = {
    "type": "function",
    "name": "complete_task",
    "description": "Signal that the guide creation task is complete",
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

# Define system prompts for different guide types
TECHNICAL_SYSTEM_PROMPT = """You are Best Docs Guide Creator, an expert agent that researches and compiles technical documentation best practices.

Your task is to create a comprehensive guide on technical documentation best practices, focusing on:
- API documentation standards
- Code examples and snippets formatting
- Technical diagrams and visualization
- Schema documentation
- Architecture documentation
- Reference documentation structure
- Protocol specifications
- Testing documentation
- Technical implementation details

For blockchain projects, include specific guidance on:
- Smart contract documentation
- Consensus mechanism documentation
- Protocol architecture documentation
- Security considerations documentation

For MCP (Model Context Protocol) projects, include specific guidance on:
- Model capabilities documentation
- Integration patterns documentation 
- Error handling documentation
- Performance considerations documentation

IMPORTANT: Create a comprehensive, well-structured guide that follows best practices from leading technical organizations. 
The guide should be in Markdown format and organized with clear headings, subheadings, and examples.
Always include a ## Sources section at the end with the references you consulted.
"""

GENERAL_SYSTEM_PROMPT = """You are Best Docs Guide Creator, an expert agent that researches and compiles general documentation best practices.

Your task is to create a comprehensive guide on general documentation best practices, focusing on:
- Documentation structure and organization
- Writing style and tone
- Content requirements by document type
- Audience considerations
- Platform selection and configuration
- Publishing workflow
- Documentation versioning
- Maintenance considerations
- User guides, tutorials, and onboarding

For blockchain projects, include specific guidance on:
- User onboarding documentation
- Wallet interaction guides
- Transaction explanation guides
- Community documentation

For MCP (Model Context Protocol) projects, include specific guidance on:
- User interaction patterns
- Documentation for non-technical users
- Example-based guides
- Troubleshooting guides

IMPORTANT: Create a comprehensive, well-structured guide that follows best practices from leading technical organizations.
The guide should be in Markdown format and organized with clear headings, subheadings, and examples.
Always include a ## Sources section at the end with the references you consulted.
"""

# Function implementations
def research_technical_best_practices(focus_areas: Optional[List[str]] = None, depth: ResearchDepth = ResearchDepth.STANDARD) -> Dict[str, Any]:
    """
    Research technical documentation best practices.
    """
    console.print(f"[bold blue]Researching technical documentation best practices...[/bold blue]")
    
    # Prepare focus area info
    focus_info = ""
    if focus_areas:
        focus_info = f"Focus particularly on these areas: {', '.join(focus_areas)}.\n\n"
    
    # Prepare depth info
    depth_info = {
        ResearchDepth.BASIC: "Provide a basic overview of essential practices.",
        ResearchDepth.STANDARD: "Provide a standard, comprehensive coverage of best practices.",
        ResearchDepth.COMPREHENSIVE: "Provide an extremely detailed, exhaustive analysis of best practices, including examples and implementation details."
    }
    
    # Prepare the prompt
    user_prompt = f"""Research and compile current industry best practices for technical documentation.

{focus_info}Research depth: {depth.value} - {depth_info[depth]}

Focus on leading technology companies, open-source projects, and documentation platforms that exemplify excellent technical documentation.

Include specific guidance for:
1. API documentation (REST, GraphQL, etc.)
2. Code examples and snippets
3. Technical diagrams and visualization
4. Schema documentation
5. Architecture documentation
6. Reference documentation
7. Protocol specifications
8. Testing documentation
9. Technical implementation details

For blockchain projects, research specific best practices for:
- Smart contract documentation
- Consensus mechanism documentation
- Protocol architecture documentation
- Security considerations documentation

For MCP (Model Context Protocol) projects, research specific best practices for:
- Model capabilities documentation
- Integration patterns documentation
- Error handling documentation
- Performance considerations documentation

For each area, identify:
- Industry standards and conventions
- Tools and platforms commonly used
- Format and structure recommendations
- Notable examples of excellence

Cite reputable sources for your findings. Include specific names of documentation platforms, company style guides, and industry standards documents.
"""
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]Researching technical documentation best practices...[/bold blue]"),
        transient=True,
    ) as progress:
        task = progress.add_task("Researching...", total=None)
        try:
            # Using the new Responses API format
            response = openai_client.responses.create(
                model="gpt-4o-2024-08-06",  # Using GPT-4o for robust reasoning
                input=user_prompt,
                tools=[RESEARCH_TECHNICAL_SCHEMA],
                tool_choice={"type": "function", "name": "research_technical_best_practices"}
            )
            
            # Extract function call response
            for item in response.output:
                if item.type == "function_call" and item.name == "research_technical_best_practices":
                    return json.loads(item.arguments)
            
            # If no function call was found
            console.print("[bold red]Error:[/bold red] Expected function call not received")
            return {"findings": "", "sources": []}
        except Exception as e:
            console.print(f"[bold red]Error during research:[/bold red] {str(e)}")
            return {"findings": "", "sources": []}

def research_general_best_practices(focus_areas: Optional[List[str]] = None, depth: ResearchDepth = ResearchDepth.STANDARD) -> Dict[str, Any]:
    """
    Research general documentation best practices.
    """
    console.print(f"[bold blue]Researching general documentation best practices...[/bold blue]")
    
    # Prepare focus area info
    focus_info = ""
    if focus_areas:
        focus_info = f"Focus particularly on these areas: {', '.join(focus_areas)}.\n\n"
    
    # Prepare depth info
    depth_info = {
        ResearchDepth.BASIC: "Provide a basic overview of essential practices.",
        ResearchDepth.STANDARD: "Provide a standard, comprehensive coverage of best practices.",
        ResearchDepth.COMPREHENSIVE: "Provide an extremely detailed, exhaustive analysis of best practices, including examples and implementation details."
    }
    
    # Prepare the prompt
    user_prompt = f"""Research and compile current industry best practices for general documentation.

{focus_info}Research depth: {depth.value} - {depth_info[depth]}

Focus on leading technology companies, open-source projects, and documentation platforms that exemplify excellent documentation.

Include guidance for:
1. Documentation structure and organization
2. Writing style and tone
3. Content requirements by document type
4. Audience considerations
5. Platform selection and configuration
6. Publishing workflow
7. Documentation versioning
8. Maintenance considerations
9. User guides, tutorials, and onboarding

For blockchain projects, research specific best practices for:
- User onboarding documentation
- Wallet interaction guides
- Transaction explanation guides
- Community documentation

For MCP (Model Context Protocol) projects, research specific best practices for:
- User interaction patterns
- Documentation for non-technical users
- Example-based guides
- Troubleshooting guides

For each area, identify:
- Industry standards and conventions
- Tools and platforms commonly used
- Format and structure recommendations
- Notable examples of excellence

Cite reputable sources for your findings. Include specific names of documentation platforms, company style guides, and industry standards documents.
"""
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]Researching general documentation best practices...[/bold blue]"),
        transient=True,
    ) as progress:
        task = progress.add_task("Researching...", total=None)
        try:
            # Using the new Responses API format
            response = openai_client.responses.create(
                model="gpt-4o-2024-08-06",  # Using GPT-4o for robust reasoning
                input=user_prompt,
                tools=[RESEARCH_GENERAL_SCHEMA],
                tool_choice={"type": "function", "name": "research_general_best_practices"}
            )
            
            # Extract function call response
            for item in response.output:
                if item.type == "function_call" and item.name == "research_general_best_practices":
                    return json.loads(item.arguments)
            
            # If no function call was found
            console.print("[bold red]Error:[/bold red] Expected function call not received")
            return {"findings": "", "sources": []}
        except Exception as e:
            console.print(f"[bold red]Error during research:[/bold red] {str(e)}")
            return {"findings": "", "sources": []}

def ensure_sources_section(content: str, sources: List[str]) -> str:
    """
    Ensures the content has a sources section at the end.
    If no sources section exists, adds one with the provided sources.
    If no sources are provided, adds an empty sources section.
    """
    # Check if content already has a Sources section
    if "## Sources" in content:
        return content
    
    # Prepare sources content
    sources_content = "\n\n## Sources\n"
    if sources and len(sources) > 0:
        for source in sources:
            sources_content += f"- {source}\n"
    else:
        sources_content += "No specific sources cited.\n"
    
    return content + sources_content

def compile_technical_guide(research_findings: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compile research findings into a technical documentation best practices guide.
    """
    console.print(f"[bold blue]Compiling technical documentation best practices guide...[/bold blue]")
    
    # Get findings and sources safely
    findings = research_findings.get('findings', "")
    sources = research_findings.get('sources', [])
    sources_text = ', '.join(sources) if sources else "No specific sources cited"
    
    # If no findings were returned, create a default research summary
    if not findings:
        findings = """
Based on industry best practices, technical documentation should follow these guidelines:

1. API documentation should include clear endpoints, parameters, request/response examples, and error handling.
2. Code samples should be concise, well-commented, and cover common use cases.
3. Technical diagrams should follow standard notation and clearly illustrate system architecture.
4. Documentation should be version-controlled alongside code.
5. Blockchain documentation requires special attention to consensus mechanisms and security models.
6. MCP documentation should detail model capabilities, integration patterns, and performance considerations.
"""
    
    # Prepare the prompt with explicit instruction to include sources
    user_prompt = f"""
Based on the following research findings, compile a comprehensive technical documentation best practices guide.

The guide should be well-structured, with clear headings, subheadings, and examples.

Include specific guidance for blockchain and MCP (Model Context Protocol) projects.

Format the guide in Markdown, with a title, table of contents, and proper section headings.

IMPORTANT: Include a "## Sources" section at the end listing all references used.

Research Findings:
{findings}

Sources:
{sources_text}
"""
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]Compiling technical documentation guide...[/bold blue]"),
        transient=True,
    ) as progress:
        task = progress.add_task("Compiling...", total=None)
        try:
            # Using the new Responses API format
            response = openai_client.responses.create(
                model="gpt-4o-2024-08-06",  # Using GPT-4o for robust reasoning
                input=user_prompt,
                tools=[COMPILE_TECHNICAL_SCHEMA],
                tool_choice={"type": "function", "name": "compile_technical_guide"}
            )
            
            # Extract function call response
            for item in response.output:
                if item.type == "function_call" and item.name == "compile_technical_guide":
                    guide_results = json.loads(item.arguments)
                    
                    # Ensure sources section exists
                    guide_content = guide_results.get('guide_content', "# Technical Documentation Best Practices Guide\n\nNo content available.")
                    guide_content = ensure_sources_section(guide_content, sources)
                    guide_results['guide_content'] = guide_content
                    
                    return guide_results
            
            # If no function call was found
            console.print("[bold red]Error:[/bold red] Expected function call not received")
            # Create a basic fallback guide
            fallback_content = "# Technical Documentation Best Practices Guide\n\nThis guide couldn't be generated properly. Please try again."
            fallback_content = ensure_sources_section(fallback_content, sources)
            return {
                "guide_content": fallback_content,
                "reasoning": "Function call failed."
            }
        except Exception as e:
            console.print(f"[bold red]Error during guide compilation:[/bold red] {str(e)}")
            # Create a basic fallback guide
            fallback_content = "# Technical Documentation Best Practices Guide\n\nThis guide couldn't be generated due to an error. Please try again."
            fallback_content = ensure_sources_section(fallback_content, sources)
            return {
                "guide_content": fallback_content,
                "reasoning": f"Error: {str(e)}"
            }

def compile_general_guide(research_findings: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compile research findings into a general documentation best practices guide.
    """
    console.print(f"[bold blue]Compiling general documentation best practices guide...[/bold blue]")
    
    # Get findings and sources safely
    findings = research_findings.get('findings', "")
    sources = research_findings.get('sources', [])
    sources_text = ', '.join(sources) if sources else "No specific sources cited"
    
    # If no findings were returned, create a default research summary
    if not findings:
        findings = """
Based on industry best practices, general documentation should follow these guidelines:

1. Documentation should be structured with clear navigation and logical organization.
2. Writing should be clear, concise, and appropriate for the target audience.
3. Documentation should include getting started guides, tutorials, and reference material.
4. Content should be versioned alongside the product it documents.
5. Blockchain documentation for users should focus on wallet interactions and transaction flows.
6. MCP documentation should include example-based guides and troubleshooting sections.
"""
    
    # Prepare the prompt with explicit instruction to include sources
    user_prompt = f"""
Based on the following research findings, compile a comprehensive general documentation best practices guide.

The guide should be well-structured, with clear headings, subheadings, and examples.

Include specific guidance for blockchain and MCP (Model Context Protocol) projects.

Format the guide in Markdown, with a title, table of contents, and proper section headings.

IMPORTANT: Include a "## Sources" section at the end listing all references used.

Research Findings:
{findings}

Sources:
{sources_text}
"""
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]Compiling general documentation guide...[/bold blue]"),
        transient=True,
    ) as progress:
        task = progress.add_task("Compiling...", total=None)
        try:
            # Using the new Responses API format
            response = openai_client.responses.create(
                model="gpt-4o-2024-08-06",  # Using GPT-4o for robust reasoning
                input=user_prompt,
                tools=[COMPILE_GENERAL_SCHEMA],
                tool_choice={"type": "function", "name": "compile_general_guide"}
            )
            
            # Extract function call response
            for item in response.output:
                if item.type == "function_call" and item.name == "compile_general_guide":
                    guide_results = json.loads(item.arguments)
                    
                    # Ensure sources section exists
                    guide_content = guide_results.get('guide_content', "# General Documentation Best Practices Guide\n\nNo content available.")
                    guide_content = ensure_sources_section(guide_content, sources)
                    guide_results['guide_content'] = guide_content
                    
                    return guide_results
            
            # If no function call was found
            console.print("[bold red]Error:[/bold red] Expected function call not received")
            # Create a basic fallback guide
            fallback_content = "# General Documentation Best Practices Guide\n\nThis guide couldn't be generated properly. Please try again."
            fallback_content = ensure_sources_section(fallback_content, sources)
            return {
                "guide_content": fallback_content,
                "reasoning": "Function call failed."
            }
        except Exception as e:
            console.print(f"[bold red]Error during guide compilation:[/bold red] {str(e)}")
            # Create a basic fallback guide
            fallback_content = "# General Documentation Best Practices Guide\n\nThis guide couldn't be generated due to an error. Please try again."
            fallback_content = ensure_sources_section(fallback_content, sources)
            return {
                "guide_content": fallback_content,
                "reasoning": f"Error: {str(e)}"
            }

def save_guide(guide_type: str, output_path: str, content: str) -> str:
    """
    Save the best practices guide to a file.
    """
    console.print(f"[bold blue]Saving {guide_type} documentation best practices guide...[/bold blue]")
    
    # Create the output file path
    output_file = os.path.join(output_path, f"BEST_DOCS_{guide_type}_GUIDE_2025.md")
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Write the file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        console.print(f"[bold green]Guide saved to:[/bold green] {output_file}")
        return output_file
    except Exception as e:
        console.print(f"[bold red]Error saving guide:[/bold red] {str(e)}")
        sys.exit(1)

def complete_task(reasoning: str) -> str:
    """
    Signal completion of the task.
    """
    message = f"Guide creation task completed: {reasoning}"
    console.print(Panel(message, title="[bold green]Task Complete[/bold green]", border_style="green"))
    return message

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Best Docs Guide Creator - Researches and compiles documentation best practices")
    
    parser.add_argument("--output-dir", "-o", required=True, 
                        help="Directory to save the guides")
    parser.add_argument("--focus", "-f", default="",
                        help="Additional focus areas for research (comma-separated)")
    parser.add_argument("--depth", "-d", default=ResearchDepth.STANDARD.value,
                        choices=[e.value for e in ResearchDepth],
                        help="Research depth (basic, standard, comprehensive)")
    parser.add_argument("--type", "-t", default=GuideType.BOTH.value,
                        choices=[e.value for e in GuideType],
                        help="Type of guide to create (technical, general, both)")
    parser.add_argument("--compute-limit", "-c", type=int, default=10,
                        help="Maximum number of research iterations")
    
    args = parser.parse_args()
    
    # Convert depth to enum
    depth = ResearchDepth(args.depth)
    
    # Convert type to enum
    guide_type = GuideType(args.type)
    
    # Parse focus areas
    focus_areas = [area.strip() for area in args.focus.split(",")] if args.focus else None
    
    console.print(Panel(f"Best Docs Guide Creator", title="[bold]Starting Research[/bold]", border_style="blue"))
    console.print(f"Output directory: [bold]{args.output_dir}[/bold]")
    console.print(f"Research depth: [bold]{depth.value}[/bold]")
    console.print(f"Guide type: [bold]{guide_type.value}[/bold]")
    if focus_areas:
        console.print(f"Focus areas: [bold]{', '.join(focus_areas)}[/bold]\n")
    
    # Track original sources for each guide
    technical_sources = []
    general_sources = []
    
    # Create technical guide if requested
    if guide_type in [GuideType.TECHNICAL, GuideType.BOTH]:
        console.print(Panel(f"Creating [bold]Technical[/bold] Documentation Guide", border_style="blue"))
        
        # Step 1: Research technical best practices
        technical_research = research_technical_best_practices(focus_areas, depth)
        
        # Keep track of original sources
        technical_sources = technical_research.get('sources', [])
        
        # Display research summary
        console.print(f"\n[bold]Technical Research Summary:[/bold]")
        console.print(f"Consulted [bold]{len(technical_sources)}[/bold] sources")
        if technical_sources:
            sample_sources = technical_sources[:min(3, len(technical_sources))]
            console.print(f"Sample sources: {', '.join(sample_sources)}")
        
        # Check if findings exist
        if not technical_research.get('findings'):
            console.print("[bold yellow]Warning:[/bold yellow] No findings returned from research. Using default content.")
        
        # Step 2: Compile technical guide
        technical_guide = compile_technical_guide(technical_research)
        
        # Display guide preview
        console.print(f"\n[bold]Technical Guide Preview:[/bold]")
        guide_content = technical_guide.get('guide_content', "# Technical Documentation Best Practices Guide\n\nNo content available.")
        preview_lines = guide_content.split('\n')[:10]
        console.print(Markdown('\n'.join(preview_lines) + '\n...'))
        
        # Step 3: Save technical guide
        technical_output = save_guide(
            guide_type="TECHNICAL",
            output_path=args.output_dir,
            content=guide_content
        )
    
    # Create general guide if requested
    if guide_type in [GuideType.GENERAL, GuideType.BOTH]:
        console.print(Panel(f"Creating [bold]General[/bold] Documentation Guide", border_style="blue"))
        
        # Step 1: Research general best practices
        general_research = research_general_best_practices(focus_areas, depth)
        
        # Keep track of original sources
        general_sources = general_research.get('sources', [])
        
        # Display research summary
        console.print(f"\n[bold]General Research Summary:[/bold]")
        console.print(f"Consulted [bold]{len(general_sources)}[/bold] sources")
        if general_sources:
            sample_sources = general_sources[:min(3, len(general_sources))]
            console.print(f"Sample sources: {', '.join(sample_sources)}")
        
        # Check if findings exist
        if not general_research.get('findings'):
            console.print("[bold yellow]Warning:[/bold yellow] No findings returned from research. Using default content.")
        
        # Step 2: Compile general guide
        general_guide = compile_general_guide(general_research)
        
        # Display guide preview
        console.print(f"\n[bold]General Guide Preview:[/bold]")
        guide_content = general_guide.get('guide_content', "# General Documentation Best Practices Guide\n\nNo content available.")
        preview_lines = guide_content.split('\n')[:10]
        console.print(Markdown('\n'.join(preview_lines) + '\n...'))
        
        # Step 3: Save general guide
        general_output = save_guide(
            guide_type="GENERAL",
            output_path=args.output_dir,
            content=guide_content
        )
    
    # Signal completion
    guides_created = []
    if guide_type in [GuideType.TECHNICAL, GuideType.BOTH]:
        guides_created.append("Technical")
    if guide_type in [GuideType.GENERAL, GuideType.BOTH]:
        guides_created.append("General")
    
    complete_task(f"Successfully created {' and '.join(guides_created)} Documentation Best Practices Guide(s) in {args.output_dir}")

if __name__ == "__main__":
    main()