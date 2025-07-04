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

## 4. Adaptive Dual-LLM Architecture
- Implement intelligent complexity-based LLM selection:
  - **Single LLM Mode**: For simple, one-step operations (fast response)
  - **Dual LLM Mode**: For complex, multi-step operations (high quality)
- Use a **thinker model** (e.g., llama3, deepseek-r1) for complex reasoning and analysis
- Use a **formatter model** (e.g., mistral) for JSON formatting and structured output
- Implement automatic complexity detection based on:
  - Multi-step indicators ("and", "then", "also", "furthermore")
  - Conditional logic ("if", "when", "unless", "based on")
  - Complex file patterns (wildcards, "all", "multiple", "recursive")
  - Analysis tasks ("analyze", "summarize", "review", "examine")
  - Multi-location operations ("from", "to", "between", "across")
- Provide graceful fallback mechanisms when models are unavailable
- Always allow users to override LLM selection with CLI flags

## 5. ML Model Integration
- Use Ollama's local API for all ML-powered text rewriting or generation tasks
- Never send sensitive data to remote servers; keep all processing local
- Support custom model selection for both thinker and formatter roles
- Implement proper error handling for model availability and API failures
- Use JSON format for structured responses when required
- Provide verbose output options for debugging and monitoring

## 6. Modularity and Extensibility
- Implement each CLI command as a separate function or class for maintainability
- Make it easy to add new commands or extend existing ones
- Keep agent logic (ML, task orchestration, reasoning) separate from CLI parsing
- Design complexity analysis as a modular, extensible system
- Allow easy addition of new complexity indicators and scoring rules

## 7. Agentic Reasoning (Chain-of-Thought & Tree-of-Thought)
- The Agent class must support both chain-of-thought (linear) and tree-of-thought (branching) reasoning
- The agent should:
  - Analyze request complexity and select appropriate LLM approach
  - Parse the intent of the prompt
  - Set a goal to achieve
  - Assess the current situation
  - Plan and execute a sequence (chain) or branching set (tree) of steps
  - Assess progress between steps and adapt as needed
  - Check if the goal is achieved and keep a full reasoning trace
- Provide methods to add, traverse, and reset reasoning steps and trees
- Include complexity analysis in the reasoning trace for transparency

## 8. User Experience
- Output should be clear and actionable
- Errors should be informative and never cryptic
- Support both interactive and scriptable (non-interactive) usage
- Provide complexity analysis feedback to help users understand system decisions
- Include performance metrics and timing information when appropriate
- Offer verbose mode for debugging and transparency

## 9. Documentation
- Update the README and this guideline with every new feature or change
- Provide usage examples for each command and agentic reasoning feature
- Document complexity analysis rules and scoring mechanisms
- Include performance benchmarks and optimization guidelines
- Provide troubleshooting guides for common LLM and API issues

## 10. Security
- Never execute arbitrary code unless explicitly requested by the user
- Validate all user inputs, especially file paths and shell commands
- Ensure LLM responses are properly sanitized before execution
- Implement rate limiting and timeout mechanisms for API calls
- Log and monitor LLM interactions for security auditing

## 11. Performance and Optimization
- Optimize for response time while maintaining quality:
  - Use single LLM for simple operations (target: <2s response)
  - Use dual LLM for complex operations (target: <10s response)
- Implement intelligent caching for frequently used models
- Monitor and log performance metrics (response time, token usage, model availability)
- Provide fallback mechanisms for unavailable models
- Use appropriate model sizes for different tasks (smaller for formatting, larger for reasoning)
- Implement request queuing and load balancing when multiple models are available

## 12. Testing and Validation
- Test complexity analysis with diverse request types:
  - Simple single-step operations
  - Multi-step operations with various connectors
  - Conditional logic and branching scenarios
  - Complex file operations with wildcards and patterns
  - Analysis and summarization tasks
- Validate dual-LLM fallback mechanisms with unavailable models
- Test performance across different model combinations
- Verify JSON response formatting and parsing
- Test error handling for API failures and timeouts
- Include integration tests for end-to-end workflows

---

**Always follow these guidelines when developing or extending the agentic system.** 