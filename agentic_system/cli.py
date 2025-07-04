"""
Agentic System CLI

How to add a new action:
1. Create a command class in agentic_system/commands/ inheriting from BaseCommand.
2. Create an intent parser in agentic_system/intent/ inheriting from BaseIntentParser.
3. Add a prompt file in agentic_system/intent_parsers/.
4. Ensure the class name matches the pattern: <Action>Command and <Action>IntentParser (e.g., MoveCommand, MoveIntentParser).
5. The system will dynamically discover and use new actions.
"""
import typer
import importlib
import pkgutil
from agentic_system.commands.base import BaseCommand
from agentic_system.intent.base import BaseIntentParser
from .core import Agent

app = typer.Typer()

# Dynamically load all intent parsers
intent_parsers = {}
for _, module_name, _ in pkgutil.iter_modules(['agentic_system/intent']):
    if module_name == 'base':
        continue
    module = importlib.import_module(f'agentic_system.intent.{module_name}')
    for attr in dir(module):
        cls = getattr(module, attr)
        if isinstance(cls, type) and issubclass(cls, BaseIntentParser) and cls is not BaseIntentParser:
            action = module_name.replace('_intentparser', '').replace('intentparser', '').replace('intent', '')
            intent_parsers[action] = cls()

# Dynamically load all commands
commands = {}
for _, module_name, _ in pkgutil.iter_modules(['agentic_system/commands']):
    if module_name == 'base':
        continue
    module = importlib.import_module(f'agentic_system.commands.{module_name}')
    for attr in dir(module):
        cls = getattr(module, attr)
        if isinstance(cls, type) and issubclass(cls, BaseCommand) and cls is not BaseCommand:
            action = module_name.replace('_command', '').replace('command', '')
            commands[action] = cls

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
    
    # Try each intent parser
    for action, parser in intent_parsers.items():
        intent = parser.parse(instruction)
        if intent and intent.get('action') == action:
            cmd_class = commands.get(action)
            if not cmd_class:
                print(f"No command found for action '{action}'")
                return
            # Pass all intent fields except 'action' as kwargs
            kwargs = {k: v for k, v in intent.items() if k != 'action'}
            cmd = cmd_class(**kwargs)
            result = cmd.execute()
            print(result)
            return
    print("Sorry, I couldn't understand the instruction or no command is available.")


if __name__ == "__main__":
    app() 