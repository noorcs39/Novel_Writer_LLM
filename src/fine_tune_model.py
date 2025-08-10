import json
import os
import subprocess
from pathlib import Path

def create_modelfile(base_model="tinyllama", training_data_path="training_data/training_data.txt"):
    """
    Create a Modelfile for Ollama fine-tuning
    
    Args:
        base_model: Base model to fine-tune
        training_data_path: Path to training data
    """
    
    # Read training data
    if not os.path.exists(training_data_path):
        print(f"Training data not found at {training_data_path}")
        print("Please run the scraper and data preparation scripts first.")
        return False
    
    with open(training_data_path, 'r', encoding='utf-8') as f:
        training_content = f.read()
    
    # Create Modelfile content
    modelfile_content = f"""FROM {base_model}

# Set custom parameters for fine-tuning
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40
PARAMETER repeat_penalty 1.1

# System message for the fine-tuned model
SYSTEM You are a knowledgeable assistant trained on sacred texts, religious writings, philosophical works, and spiritual literature. You can write articles, explain concepts, and discuss topics related to religion, spirituality, philosophy, and ancient wisdom traditions. You provide thoughtful, respectful, and informative responses.

# Training examples (first 10000 characters as examples)
"""
    
    # Add some training examples (limited by Ollama's capabilities)
    training_examples = training_content[:10000]  # Limit size
    
    # Format as conversation examples
    examples = []
    lines = training_examples.split('\n')
    current_example = ""
    
    for line in lines:
        if line.strip():
            current_example += line + " "
            if len(current_example) > 500:  # Create chunks
                if current_example.strip():
                    examples.append(current_example.strip())
                current_example = ""
        if len(examples) >= 5:  # Limit number of examples
            break
    
    # Add examples to modelfile
    for i, example in enumerate(examples):
        modelfile_content += f"\n\n# Example {i+1}\n"
        modelfile_content += f'MESSAGE user "Write about this topic: {example[:100]}..."\n'
        modelfile_content += f'MESSAGE assistant "{example}"\n'
    
    # Save Modelfile
    with open('Modelfile', 'w', encoding='utf-8') as f:
        f.write(modelfile_content)
    
    print("Modelfile created successfully!")
    return True

def create_custom_model(model_name="sacred-texts-llm"):
    """
    Create a custom model using Ollama
    
    Args:
        model_name: Name for the custom model
    """
    try:
        print(f"Creating custom model '{model_name}'...")
        result = subprocess.run(
            ["ollama", "create", model_name, "-f", "Modelfile"],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"Model '{model_name}' created successfully!")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error creating model: {e}")
        print(f"Error output: {e.stderr}")
        return False
    except FileNotFoundError:
        print("Ollama not found. Please make sure Ollama is installed and in your PATH.")
        return False

def test_model(model_name="sacred-texts-llm"):
    """
    Test the fine-tuned model
    
    Args:
        model_name: Name of the model to test
    """
    test_prompts = [
        "Write an article about ancient wisdom traditions",
        "Explain the concept of spirituality in different religions",
        "Discuss the philosophical implications of sacred texts",
        "Write about the importance of religious tolerance"
    ]
    
    print(f"\nTesting model '{model_name}' with sample prompts...\n")
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"Test {i}: {prompt}")
        print("-" * 50)
        
        try:
            result = subprocess.run(
                ["ollama", "run", model_name, prompt],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                print(result.stdout)
            else:
                print(f"Error: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print("Request timed out")
        except Exception as e:
            print(f"Error testing model: {e}")
        
        print("\n" + "=" * 70 + "\n")

def main():
    print("Sacred Texts LLM Fine-tuning Script")
    print("=" * 40)
    
    # Check if training data exists
    training_data_paths = [
        "training_data/training_data.txt",
        "scraped_data/sacred_texts_training.txt"
    ]
    
    training_data_path = None
    for path in training_data_paths:
        if os.path.exists(path):
            training_data_path = path
            break
    
    if not training_data_path:
        print("No training data found. Please run the scraper first.")
        print("Expected files:")
        for path in training_data_paths:
            print(f"  - {path}")
        return
    
    print(f"Using training data from: {training_data_path}")
    
    # Create Modelfile
    if not create_modelfile(training_data_path=training_data_path):
        return
    
    # Create custom model
    model_name = "sacred-texts-llm"
    if create_custom_model(model_name):
        print(f"\nCustom model '{model_name}' created successfully!")
        
        # Test the model
        test_choice = input("\nWould you like to test the model now? (y/n): ").lower().strip()
        if test_choice == 'y':
            test_model(model_name)
        
        print(f"\nYou can now use your custom model with:")
        print(f"ollama run {model_name}")
    else:
        print("Failed to create custom model.")

if __name__ == "__main__":
    main()