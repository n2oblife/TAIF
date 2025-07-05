"""
Agentic System CLI

This system uses a dual-LLM architecture for intelligent intent parsing:
1. Thinker model: Analyzes natural language and determines intent
2. Formatter model: Converts intent into structured JSON
3. Commands: Execute the parsed intent using appropriate command classes
"""
import os
import typer
import importlib
import pkgutil
from agentic_system.commands.basic.base import BaseCommand
from agentic_system.intent.dual_llm_parser import DualLLMIntentParser
from .core import Agent

app = typer.Typer()

# Create dual-LLM intent parser
intent_parser = DualLLMIntentParser()

# Dynamically load all commands
commands = {}
commands_dir = os.path.join(os.path.dirname(__file__), 'commands', 'basic')
for _, module_name, _ in pkgutil.iter_modules([commands_dir]):
    if module_name == 'base':
        continue
    try:
        module = importlib.import_module(f'agentic_system.commands.basic.{module_name}')
        for attr in dir(module):
            cls = getattr(module, attr)
            if isinstance(cls, type) and issubclass(cls, BaseCommand) and cls is not BaseCommand:
                action = module_name.replace('_command', '').replace('command', '')
                commands[action] = cls
    except Exception as e:
        print(f"[ERROR] Failed to import module '{module_name}': {e}")

@app.command()
def taif(
    instruction: str = typer.Argument(..., help="Natural language instruction for the agent"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
    dual_llm: bool = typer.Option(False, "--dual-llm", help="Use dual LLM architecture (thinker + formatter)"),
    thinker_model: str = typer.Option("llama3", "--thinker-model", help="Model for reasoning (default: llama3)"),
    formatter_model: str = typer.Option("mistral", "--formatter-model", help="Model for formatting (default: mistral)"),
    analyze_complexity: bool = typer.Option(False, "--analyze-complexity", help="Analyze request complexity without executing")
):
    """Interpret and execute a natural language instruction."""
    
    # Create agent for complexity analysis
    agent = Agent(
        verbose=verbose,
        thinker_model=thinker_model if dual_llm else None,
        formatter_model=formatter_model if dual_llm else None
    )
    
    # Analyze complexity if requested
    if analyze_complexity:
        analysis = agent.get_complexity_analysis(instruction)
        print(f"\n=== Complexity Analysis ===")
        print(f"Prompt: {analysis['prompt']}")
        print(f"Word count: {analysis['word_count']}")
        print(f"Complexity score: {analysis['complexity_score']}")
        print(f"Is complex: {analysis['is_complex']}")
        print(f"Indicators: {', '.join(analysis['indicators']) if analysis['indicators'] else 'None'}")
        print(f"Recommended approach: {'Dual-LLM' if analysis['is_complex'] else 'Single LLM'}")
        return
    
    # Use dual-LLM intent parser
    intent = intent_parser.parse(instruction)
    if intent and intent.get('action'):
        action = intent.get('action')
        cmd_class = commands.get(action)
        if not cmd_class:
            print(f"No command found for action '{action}'")
            return
        # Unpack parameters dict if present
        params = intent.get('parameters', {})
        cmd = cmd_class(**params)
        result = cmd.execute()
        print(result)
        return
    print("Sorry, I couldn't understand the instruction or no command is available.")


if __name__ == "__main__":
    app() 