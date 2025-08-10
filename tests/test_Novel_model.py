#!/usr/bin/env python3
"""
Test script for the Sacred Texts LLM
Demonstrates how to use the fine-tuned model for various tasks
"""

import subprocess
import sys

def run_ollama_command(model_name, prompt):
    """
    Run an Ollama command with the given model and prompt
    
    Args:
        model_name: Name of the Ollama model
        prompt: Text prompt to send to the model
        
    Returns:
        The model's response as a string
    """
    try:
        result = subprocess.run(
            ["ollama", "run", model_name, prompt],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Error: {result.stderr}"
            
    except subprocess.TimeoutExpired:
        return "Request timed out"
    except Exception as e:
        return f"Error running command: {e}"

def test_model_capabilities():
    """
    Test the model with various types of prompts
    """
    model_name = "sacred-texts-llm"
    
    test_prompts = [
        {
            "category": "Article Writing",
            "prompt": "Write an article about the role of meditation in spiritual development"
        },
        {
            "category": "Concept Explanation",
            "prompt": "Explain the concept of karma and how it appears in different religious traditions"
        },
        {
            "category": "Philosophical Discussion",
            "prompt": "Discuss the relationship between faith and reason in religious thought"
        },
        {
            "category": "Comparative Religion",
            "prompt": "Compare the creation stories found in different world religions"
        },
        {
            "category": "Practical Wisdom",
            "prompt": "What practical wisdom can we learn from ancient sacred texts for modern life?"
        }
    ]
    
    print("Testing Sacred Texts LLM Capabilities")
    print("=" * 50)
    print()
    
    for i, test in enumerate(test_prompts, 1):
        print(f"Test {i}: {test['category']}")
        print(f"Prompt: {test['prompt']}")
        print("-" * 40)
        
        response = run_ollama_command(model_name, test['prompt'])
        print(response)
        print()
        print("=" * 50)
        print()

def interactive_mode():
    """
    Interactive mode for chatting with the model
    """
    model_name = "sacred-texts-llm"
    
    print("Sacred Texts LLM - Interactive Mode")
    print("Type 'quit' or 'exit' to end the session")
    print("=" * 40)
    print()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
                
            if not user_input:
                continue
                
            print("\nSacred Texts LLM: ", end="")
            response = run_ollama_command(model_name, user_input)
            print(response)
            print()
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

def main():
    """
    Main function - choose between test mode and interactive mode
    """
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            test_model_capabilities()
        elif sys.argv[1] == "interactive":
            interactive_mode()
        else:
            print("Usage: python test_model.py [test|interactive]")
            print("  test        - Run predefined tests")
            print("  interactive - Start interactive chat mode")
    else:
        print("Sacred Texts LLM Test Script")
        print("Choose an option:")
        print("1. Run predefined tests")
        print("2. Interactive chat mode")
        
        choice = input("Enter your choice (1 or 2): ").strip()
        
        if choice == "1":
            test_model_capabilities()
        elif choice == "2":
            interactive_mode()
        else:
            print("Invalid choice. Please run the script again.")

if __name__ == "__main__":
    main()