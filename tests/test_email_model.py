#!/usr/bin/env python3
"""
Email Writing Model Test Script
Demonstrates various email writing capabilities of the fine-tuned model
"""

import subprocess
import sys
import json
from datetime import datetime

def run_email_model(model_name, prompt, max_retries=3):
    """
    Run the email model with a given prompt
    
    Args:
        model_name: Name of the email model
        prompt: Email writing prompt
        max_retries: Maximum number of retry attempts
        
    Returns:
        Generated email content
    """
    for attempt in range(max_retries):
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
                print(f"Attempt {attempt + 1} failed: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print(f"Attempt {attempt + 1} timed out")
        except Exception as e:
            print(f"Attempt {attempt + 1} error: {e}")
    
    return "Failed to generate email after multiple attempts"

def test_email_categories():
    """
    Test the model with different email categories
    """
    model_name = "email-writer-llm"
    
    email_tests = [
        {
            "category": "Business Communication",
            "prompts": [
                "Write a professional email requesting a project update from a team member",
                "Compose an email declining a business proposal politely",
                "Write an email announcing a new company policy to employees"
            ]
        },
        {
            "category": "Thank You Emails",
            "prompts": [
                "Write a thank you email after receiving help from a colleague",
                "Compose a thank you note for a client referral",
                "Write a thank you email after a successful project completion"
            ]
        },
        {
            "category": "Meeting & Scheduling",
            "prompts": [
                "Write an email scheduling a team meeting for next week",
                "Compose an email rescheduling a cancelled appointment",
                "Write a meeting follow-up email with action items"
            ]
        },
        {
            "category": "Customer Service",
            "prompts": [
                "Write an email responding to a customer complaint professionally",
                "Compose an email explaining a service delay to customers",
                "Write a welcome email for new customers"
            ]
        },
        {
            "category": "Networking & Introductions",
            "prompts": [
                "Write an email introducing yourself to a new business contact",
                "Compose an email connecting two professional contacts",
                "Write a LinkedIn connection follow-up email"
            ]
        }
    ]
    
    print("Email Writing Model - Category Testing")
    print("=" * 50)
    print()
    
    results = []
    
    for category_test in email_tests:
        category = category_test["category"]
        prompts = category_test["prompts"]
        
        print(f"📧 Testing Category: {category}")
        print("-" * 40)
        
        category_results = []
        
        for i, prompt in enumerate(prompts, 1):
            print(f"\nTest {i}: {prompt}")
            print("Response:")
            print("~" * 30)
            
            response = run_email_model(model_name, prompt)
            print(response)
            
            category_results.append({
                "prompt": prompt,
                "response": response
            })
            
            print("\n" + "=" * 50)
        
        results.append({
            "category": category,
            "tests": category_results
        })
        
        print("\n")
    
    return results

def test_email_tones():
    """
    Test the model with different email tones
    """
    model_name = "email-writer-llm"
    
    base_scenario = "requesting a deadline extension for a project"
    
    tone_tests = [
        {
            "tone": "Formal",
            "prompt": f"Write a formal, professional email {base_scenario}"
        },
        {
            "tone": "Friendly",
            "prompt": f"Write a friendly but professional email {base_scenario}"
        },
        {
            "tone": "Apologetic",
            "prompt": f"Write an apologetic email {base_scenario}"
        },
        {
            "tone": "Urgent",
            "prompt": f"Write an urgent email {base_scenario}"
        }
    ]
    
    print("Email Tone Variation Testing")
    print("=" * 40)
    print(f"Scenario: {base_scenario}")
    print()
    
    for test in tone_tests:
        print(f"🎭 Tone: {test['tone']}")
        print(f"Prompt: {test['prompt']}")
        print("-" * 30)
        
        response = run_email_model(model_name, test['prompt'])
        print(response)
        print("\n" + "=" * 50 + "\n")

def interactive_email_composer():
    """
    Interactive email composition mode
    """
    model_name = "email-writer-llm"
    
    print("Interactive Email Composer")
    print("Type 'quit' to exit, 'help' for examples")
    print("=" * 40)
    print()
    
    while True:
        try:
            user_input = input("📧 Email Request: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if user_input.lower() == 'help':
                print("\nExample prompts:")
                print("- Write a thank you email for a job interview")
                print("- Compose a follow-up email after a meeting")
                print("- Write an email requesting vacation time")
                print("- Create an email introducing a new team member")
                print("- Write an apology email for a mistake")
                print()
                continue
            
            if not user_input:
                continue
            
            print("\n📝 Generated Email:")
            print("-" * 30)
            
            response = run_email_model(model_name, user_input)
            print(response)
            print("\n" + "=" * 50 + "\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

def save_test_results(results, filename="email_test_results.json"):
    """
    Save test results to a JSON file
    
    Args:
        results: Test results to save
        filename: Output filename
    """
    output_data = {
        "timestamp": datetime.now().isoformat(),
        "model_name": "email-writer-llm",
        "test_results": results
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"Test results saved to {filename}")

def main():
    """
    Main function - choose testing mode
    """
    print("Email Writing Model Testing Suite")
    print("=" * 40)
    
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
    else:
        print("Choose a testing mode:")
        print("1. Category Testing (comprehensive)")
        print("2. Tone Variation Testing")
        print("3. Interactive Composer")
        print("4. Quick Test")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        mode_map = {
            "1": "categories",
            "2": "tones",
            "3": "interactive",
            "4": "quick"
        }
        
        mode = mode_map.get(choice, "quick")
    
    if mode == "categories":
        results = test_email_categories()
        save_choice = input("\nSave results to file? (y/n): ").lower().strip()
        if save_choice == 'y':
            save_test_results(results)
            
    elif mode == "tones":
        test_email_tones()
        
    elif mode == "interactive":
        interactive_email_composer()
        
    elif mode == "quick":
        model_name = "email-writer-llm"
        test_prompt = "Write a professional email requesting a meeting with a client"
        
        print(f"Quick Test: {test_prompt}")
        print("-" * 40)
        
        response = run_email_model(model_name, test_prompt)
        print(response)
        
        print(f"\n✅ Model '{model_name}' is working!")
        print("Use 'python test_email_model.py interactive' for more testing.")
    
    else:
        print(f"Unknown mode: {mode}")
        print("Available modes: categories, tones, interactive, quick")

if __name__ == "__main__":
    main()