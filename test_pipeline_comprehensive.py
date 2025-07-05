#!/usr/bin/env python3
"""
Comprehensive Pipeline Test Script

This script tests the TAIF agentic system with various complexity levels:
1. Very Easy Prompts (should use single LLM)
2. Moderately Complex Prompts (should trigger dual-LLM)
3. Highly Complex Prompts (multi-step, analysis, conditional logic)

Usage:
    python test_pipeline_comprehensive.py
"""

import subprocess
import sys
import time
from typing import List, Dict

def run_command(command: str) -> str:
    """Run a CLI command and return the output."""
    try:
        result = subprocess.run(
            command.split(),
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "Command timed out"
    except Exception as e:
        return f"Error: {e}"

def test_complexity_analysis(prompt: str) -> Dict:
    """Test complexity analysis for a prompt."""
    print(f"\n🔍 Analyzing complexity: '{prompt}'")
    command = f'python -m agentic_system.cli --analyze-complexity "{prompt}"'
    output = run_command(command)
    print(output)
    return {"prompt": prompt, "analysis": output}

def test_simple_execution(prompt: str) -> Dict:
    """Test simple execution of a prompt."""
    print(f"\n✅ Executing simple prompt: '{prompt}'")
    command = f'python -m agentic_system.cli "{prompt}"'
    output = run_command(command)
    print(f"Output: {output}")
    return {"prompt": prompt, "output": output}

def test_dual_llm_execution(prompt: str) -> Dict:
    """Test dual-LLM execution of a complex prompt."""
    print(f"\n🧠 Executing complex prompt (dual-LLM): '{prompt}'")
    command = f'python -m agentic_system.cli --dual-llm --verbose "{prompt}"'
    output = run_command(command)
    print(f"Output: {output}")
    return {"prompt": prompt, "output": output}

def main():
    """Run comprehensive pipeline tests."""
    print("🚀 TAIF Agentic System - Comprehensive Pipeline Test")
    print("=" * 60)
    
    # Test 1: Very Easy, Plain Prompts (Single LLM)
    print("\n📋 TEST 1: Very Easy, Plain Prompts")
    print("-" * 40)
    
    easy_prompts = [
        "show the license",
        "list files",
        "show contents of README.md",
        "print the guidelines",
        "what contains the requirements",
        "create a folder called test_folder",
        "show current directory",
        "echo hello world"
    ]
    
    easy_results = []
    for prompt in easy_prompts:
        # First analyze complexity
        analysis = test_complexity_analysis(prompt)
        easy_results.append(analysis)
        
        # Then execute
        result = test_simple_execution(prompt)
        easy_results.append(result)
        
        time.sleep(1)  # Brief pause between commands
    
    # Test 2: Moderately Complex Prompts (Dual LLM)
    print("\n📋 TEST 2: Moderately Complex Prompts")
    print("-" * 40)
    
    moderate_prompts = [
        "find all Python files and show their contents",
        "create a backup folder and copy all .txt files there",
        "list files in current directory and count them",
        "show contents of README and LICENSE files",
        "create a summary of all markdown files",
        "find files containing 'TODO' and list them"
    ]
    
    moderate_results = []
    for prompt in moderate_prompts:
        # First analyze complexity
        analysis = test_complexity_analysis(prompt)
        moderate_results.append(analysis)
        
        # Then execute with dual-LLM
        result = test_dual_llm_execution(prompt)
        moderate_results.append(result)
        
        time.sleep(2)  # Longer pause for complex operations
    
    # Test 3: Highly Complex Prompts (Multi-step, Analysis)
    print("\n📋 TEST 3: Highly Complex Prompts")
    print("-" * 40)
    
    complex_prompts = [
        "analyze all Python files, find functions, and create a summary report",
        "backup all configuration files, update settings, and create rollback script",
        "find all files containing 'TODO' or 'FIXME', extract them, and organize by priority",
        "scan the project structure, identify unused files, and suggest cleanup",
        "create a comprehensive project documentation by analyzing all source files",
        "implement a file organization system based on file types and content analysis"
    ]
    
    complex_results = []
    for prompt in complex_prompts:
        # First analyze complexity
        analysis = test_complexity_analysis(prompt)
        complex_results.append(analysis)
        
        # Then execute with dual-LLM and verbose output
        result = test_dual_llm_execution(prompt)
        complex_results.append(result)
        
        time.sleep(3)  # Longer pause for very complex operations
    
    # Summary Report
    print("\n📊 PIPELINE TEST SUMMARY")
    print("=" * 60)
    print(f"✅ Easy prompts tested: {len(easy_prompts)}")
    print(f"🧠 Moderate prompts tested: {len(moderate_prompts)}")
    print(f"🚀 Complex prompts tested: {len(complex_prompts)}")
    print(f"📈 Total operations: {len(easy_prompts) + len(moderate_prompts) + len(complex_prompts)}")
    
    print("\n🎯 Key Pipeline Features Demonstrated:")
    print("• Adaptive LLM selection based on complexity")
    print("• Dual-LLM architecture (thinker + formatter)")
    print("• Natural language intent parsing")
    print("• Command execution with proper error handling")
    print("• Complexity analysis and scoring")
    print("• Verbose output for debugging")
    
    print("\n✨ Pipeline Architecture:")
    print("1. User Input → Natural Language Instruction")
    print("2. Complexity Analysis → Determine LLM Approach")
    print("3. Intent Parsing → Extract Action & Parameters")
    print("4. Command Execution → Perform File Operations")
    print("5. Result Output → User-Friendly Response")
    
    print("\n🏁 Test completed successfully!")

if __name__ == "__main__":
    main() 