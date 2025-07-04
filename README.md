# TAIF
tAIsk force

## Agentic System CLI

### Setup

1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   pip install -e .
   ```
2. Make sure Ollama is running locally and your desired models are available:
   ```sh
   ollama serve
   ollama pull deepseek-r1  # For reasoning (thinker)
   ollama pull mistral      # For formatting (formatter)
   ```

### Adaptive Dual-LLM Architecture

TAIF features an intelligent dual-LLM architecture that automatically adapts based on request complexity:

- **Single LLM Mode**: Used for simple, one-step operations (fast response)
- **Dual LLM Mode**: Used for complex, multi-step operations (high quality)

#### Complexity Detection

The system analyzes requests using multiple indicators:
- **Multi-step operations**: "and", "then", "also", "furthermore"
- **Conditional logic**: "if", "when", "unless", "based on"
- **Complex file patterns**: wildcards, "all", "multiple", "recursive"
- **Analysis tasks**: "analyze", "summarize", "review", "examine"
- **Multi-location operations**: "from", "to", "between", "across"

#### Usage Examples

**Simple requests (Single LLM):**
```sh
python -m agentic_system.cli "list files in current directory"
python -m agentic_system.cli "show contents of file.txt"
python -m agentic_system.cli "create a new folder called backup"
```

**Complex requests (Dual LLM):**
```sh
python -m agentic_system.cli --dual-llm "analyze all Python files and summarize functionality"
python -m agentic_system.cli --dual-llm "find all files containing 'TODO', extract them, and organize by priority"
python -m agentic_system.cli --dual-llm "backup config files, update settings, and create rollback script"
```

**Analyze complexity without executing:**
```sh
python -m agentic_system.cli --analyze-complexity "find all files and create a report"
```

**Custom models with verbose output:**
```sh
python -m agentic_system.cli --dual-llm --thinker-model llama3 --formatter-model mistral --verbose "complex task here"
```

#### Performance Benefits

- **Simple requests**: Fast single LLM response (0.5-2s)
- **Complex requests**: High-quality dual LLM processing with fallback mechanisms
- **Adaptive switching**: Automatic selection based on request complexity
- **Error handling**: Graceful fallback if models are unavailable

### Usage

#### Natural Language Prompt (Recommended)
The primary way to use TAIF is to give a natural language prompt describing your goal. The agent will automatically choose the best LLM approach based on complexity, parse your intent, set a goal, plan, and execute the necessary CLI commands under the hood to achieve it.

Example:
```sh
python -m agentic_system.cli "Move all .txt files from /A to /B except those containing 'draft'"
```

The agent will:
- Parse your intent and set a goal.
- Assess the current situation (e.g., list files in /A).
- Plan the steps needed (e.g., filter files, move them).
- Execute the steps using the appropriate CLI commands.
- Assess progress and adapt as needed.
- Check if the goal is achieved and provide a reasoning trace.

#### Direct CLI Subcommands (Advanced/Integration)
You can still use individual CLI subcommands for scripting, automation, or integration with other software:

- `ls` — List files/folders in a directory
  ```sh
  python -m agentic_system.cli ls --path "/path/to/dir"
  ```
- `cat` — Show contents of a file
  ```sh
  python -m agentic_system.cli cat --file mycv.txt
  ```
- `rewrite` — Rewrite a text file using an ML model (Ollama)
  ```sh
  python -m agentic_system.cli rewrite --file mycv.txt --prompt "Tailor this CV for a software engineering job" --output mycv-tailored.txt
  ```
- `write` — Write text to a file
  ```sh
  python -m agentic_system.cli write --file notes.txt --text "Some content"
  ```
- `cp`, `mv`, `rm` — Copy, move, delete files
  ```sh
  python -m agentic_system.cli cp --src file1.txt --dst file2.txt
  python -m agentic_system.cli mv --src file1.txt --dst /new/location/
  python -m agentic_system.cli rm --file file1.txt
  ```

---

## Agentic Reasoning: Chain-of-Thought & Tree-of-Thought

The Agent class supports advanced reasoning workflows:
- **Chain-of-Thought:** The agent can keep a linear sequence of reasoning steps, recording each thought or action as it works toward a goal.
- **Tree-of-Thought:** The agent can branch its reasoning, exploring multiple options or parallel plans, and keep a tree structure of all reasoning paths.

### Agentic Reasoning Workflow
1. **Parse Intent:** The agent interprets the user's prompt and extracts the intended action and parameters.
2. **Set Goal:** The agent defines a goal to achieve based on the intent.
3. **Assess Situation:** The agent evaluates the current state (e.g., files, directories, content).
4. **Plan Steps:** The agent plans a sequence (chain) or branching set (tree) of steps to achieve the goal.
5. **Execute & Assess:** The agent executes each step, assessing progress and adapting as needed.
6. **Goal Check:** The agent checks if the goal is achieved and provides a reasoning trace.

### Example: Using Agentic Reasoning in Python
```python
from agentic_system.core import Agent

# Create agent with adaptive dual-LLM capability
agent = Agent(
    verbose=True,
    thinker_model="llama3",      # For complex reasoning
    formatter_model="mistral"    # For JSON formatting
)

# Analyze request complexity
analysis = agent.get_complexity_analysis("Move all .txt files from /A to /B")
print(f"Complexity score: {analysis['complexity_score']}")
print(f"Is complex: {analysis['is_complex']}")

# Set goal and track reasoning
agent.goal_description = "Move all .txt files from /A to /B"
agent.add_chain_thought("Parsed intent: move .txt files")
agent.add_chain_thought("Checked /A for .txt files")
agent.add_chain_thought("Planned move operations")
print(agent.chain_of_thought)

# For tree-of-thought:
root = agent.tree_of_thought
option1 = agent.add_tree_thought("Move only files modified today", parent=root)
option2 = agent.add_tree_thought("Move all .txt files", parent=root)
print(agent.tree_of_thought)
```

---

## Development Guidelines (Summary)

- Use cross-platform file operations (`os`, `pathlib`, `shutil`).
- Each core capability is a separate CLI subcommand.
- Prioritize file safety (confirm before overwrite/delete, handle errors gracefully).
- Use Ollama's local API for all ML-powered rewriting; never send data remotely.
- Keep code modular and extensible; separate CLI parsing from agent logic.
- Ensure clear, actionable output and informative errors.
- Update documentation with every change.
- Never execute arbitrary code unless explicitly requested; validate all user input.
