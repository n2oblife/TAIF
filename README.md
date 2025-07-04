# TAIF
tAIsk force

## Agentic System CLI

### Setup

1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   pip install -e .
   ```
2. Make sure Ollama is running locally and your desired model (e.g., llama2) is available.

### Usage

#### Natural Language Prompt (Recommended)
The primary way to use TAIF is to give a natural language prompt describing your goal. The agent will parse your intent, set a goal, plan, and execute the necessary CLI commands under the hood to achieve it.

Example:
```sh
python -m agentic_system.cli taif "Move all .txt files from /A to /B except those containing 'draft'"
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
agent = Agent()
agent.goal_description = "Move all .txt files from /A to /B"
agent.add_chain_thought("Parsed intent: move .txt files")
agent.add_chain_thought("Checked /A for .txt files")
agent.add_chain_thought("Planned move operations")
# ...
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
