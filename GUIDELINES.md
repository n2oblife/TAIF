# Agentic System Development Guidelines

## 1. Cross-Platform Compatibility
- Always use Python's `os`, `pathlib`, and `shutil` for file and directory operations to ensure compatibility with both Windows and Linux.
- Avoid hardcoding file paths; use `os.path.join` or `pathlib.Path`.

## 2. CLI Design Principles
- Each core capability (e.g., list, read, rewrite, write, move, copy, delete) should be a separate CLI subcommand.
- Use clear, descriptive command names and arguments.
- Provide helpful `--help` messages for every command.

## 3. File Safety
- Before overwriting or deleting files, prompt for confirmation or provide a `--force` flag.
- Handle file-not-found and permission errors gracefully.

## 4. ML Model Integration
- Use Ollama's local API for all ML-powered text rewriting or generation tasks.
- Always allow the user to specify the model and prompt.
- Never send sensitive data to remote servers; keep all processing local.

## 5. Modularity and Extensibility
- Implement each CLI command as a separate function or class for maintainability.
- Make it easy to add new commands or extend existing ones.
- Keep agent logic (ML, task orchestration, reasoning) separate from CLI parsing.

## 6. Agentic Reasoning (Chain-of-Thought & Tree-of-Thought)
- The Agent class must support both chain-of-thought (linear) and tree-of-thought (branching) reasoning.
- The agent should:
  - Parse the intent of the prompt.
  - Set a goal to achieve.
  - Assess the current situation.
  - Plan and execute a sequence (chain) or branching set (tree) of steps.
  - Assess progress between steps and adapt as needed.
  - Check if the goal is achieved and keep a full reasoning trace.
- Provide methods to add, traverse, and reset reasoning steps and trees.

## 7. User Experience
- Output should be clear and actionable.
- Errors should be informative and never cryptic.
- Support both interactive and scriptable (non-interactive) usage.

## 8. Documentation
- Update the README and this guideline with every new feature or change.
- Provide usage examples for each command and agentic reasoning feature.

## 9. Security
- Never execute arbitrary code unless explicitly requested by the user.
- Validate all user inputs, especially file paths and shell commands.

---

**Always follow these guidelines when developing or extending the agentic system.** 