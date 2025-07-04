# TAIF Prompts

This folder contains prompt templates for the TAIF (tAIsk force) agentic system.

## Overview

Prompts define how the AI agent behaves and responds to user requests. The system uses these prompts to instruct the LLM on how to interpret natural language commands and return structured responses.

## Files

- `default.py` - Contains the default system prompt used by the TAIF agent
- `__init__.py` - Package initialization file

## Default System Prompt

The default system prompt (`DEFAULT_SYSTEM_PROMPT`) instructs the agent to:

1. Act as TAIF (tAIsk force), an intelligent agent that can control a computer
2. Understand user intent and map it to appropriate CLI commands
3. Return responses in a specific JSON format
4. Use the correct parameter names for each command

## Customizing Prompts

### Method 1: Pass custom prompt during initialization

```python
from agentic_system.core import Agent

custom_prompt = """You are a specialized file management assistant..."""
agent = Agent(system_prompt=custom_prompt)
```

### Method 2: Update prompt after initialization

```python
from agentic_system.core import Agent

agent = Agent()
agent.set_system_prompt("Your custom prompt here...")
```

### Method 3: Create a new prompt file

1. Create a new file in this folder (e.g., `custom_prompt.py`)
2. Define your prompt as a string constant
3. Import and use it in your code

```python
# custom_prompt.py
CUSTOM_SYSTEM_PROMPT = """Your custom prompt here..."""

# In your code
from agentic_system.prompts.custom_prompt import CUSTOM_SYSTEM_PROMPT
agent = Agent(system_prompt=CUSTOM_SYSTEM_PROMPT)
```

## Prompt Structure

A good system prompt should include:

1. **Role definition** - What the agent is and what it can do
2. **Capabilities** - List of available actions and operations
3. **Response format** - How the agent should structure its responses
4. **Examples** - Sample inputs and expected outputs
5. **Constraints** - What the agent should and shouldn't do

## JSON Response Format

The agent must return responses in this format:

```json
{
  "action": "command_name",
  "parameters": {
    "param1": "value1",
    "param2": "value2"
  }
}
```

## Available Actions

- `cat` - Read file contents (parameter: `path`)
- `ls` - List directory contents (parameter: `path`)
- `write` - Write content to file (parameters: `file`, `content`)
- `copy` - Copy files (parameters: `src`, `dst`)
- `move` - Move files (parameters: `src`, `dst`)
- `delete` - Delete files (parameters: `src`, `files`)
- `grep` - Search for text (parameters: `directory`, `pattern`)
- `tree` - Show directory tree (parameter: `path`)

## Best Practices

1. **Be specific** - Clearly define what each action does
2. **Provide examples** - Show the expected input/output format
3. **Include constraints** - Specify what the agent shouldn't do
4. **Test thoroughly** - Verify your custom prompt works with all commands
5. **Keep it focused** - Don't add unnecessary complexity

## Testing Custom Prompts

After creating a custom prompt, test it with the pipeline tests:

```bash
pytest tests/test_pipeline_basic.py -v
```

This ensures your custom prompt maintains compatibility with the existing command structure. 