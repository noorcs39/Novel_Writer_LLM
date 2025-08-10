import json
import os
import subprocess
from pathlib import Path
import re

class EmailModelTrainer:
    def __init__(self, base_model="tinyllama"):
        """
        Initialize the email model trainer
        
        Args:
            base_model: Base model to fine-tune (default: tinyllama)
        """
        self.base_model = base_model
        self.email_data = []
        
    def load_email_dataset(self, dataset_path):
        """
        Load email dataset from various formats (JSON, CSV, TXT)
        
        Args:
            dataset_path: Path to the email dataset file
            
        Returns:
            bool: Success status
        """
        if not os.path.exists(dataset_path):
            print(f"Dataset file not found: {dataset_path}")
            return False
            
        file_ext = Path(dataset_path).suffix.lower()
        
        try:
            if file_ext == '.json':
                with open(dataset_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self.email_data = data
                    else:
                        self.email_data = [data]
                        
            elif file_ext == '.txt':
                with open(dataset_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Split by common email separators
                    emails = re.split(r'\n\s*---\s*\n|\n\s*===\s*\n|\n\s*###\s*\n', content)
                    self.email_data = [{'content': email.strip()} for email in emails if email.strip()]
                    
            elif file_ext == '.csv':
                import csv
                with open(dataset_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    self.email_data = list(reader)
                    
            else:
                print(f"Unsupported file format: {file_ext}")
                return False
                
            print(f"Loaded {len(self.email_data)} email examples from {dataset_path}")
            return True
            
        except Exception as e:
            print(f"Error loading dataset: {e}")
            return False
    
    def clean_email_text(self, text):
        """
        Clean and normalize email text
        
        Args:
            text: Raw email text
            
        Returns:
            Cleaned email text
        """
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove email headers that might confuse training
        text = re.sub(r'^(From|To|Subject|Date|CC|BCC):\s*.*?\n', '', text, flags=re.MULTILINE | re.IGNORECASE)
        
        # Clean up email signatures (common patterns)
        text = re.sub(r'\n--\s*\n.*$', '', text, flags=re.DOTALL)
        text = re.sub(r'\nBest regards?.*$', '', text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'\nSincerely.*$', '', text, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove email addresses and phone numbers for privacy
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
        text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]', text)
        
        return text.strip()
    
    def prepare_training_examples(self):
        """
        Prepare email examples for training
        
        Returns:
            List of formatted training examples
        """
        training_examples = []
        
        for email in self.email_data:
            # Handle different data structures
            if isinstance(email, dict):
                # Try common field names
                content = email.get('content') or email.get('body') or email.get('text') or email.get('email')
                subject = email.get('subject', '')
                email_type = email.get('type', 'general')
            else:
                content = str(email)
                subject = ''
                email_type = 'general'
            
            if not content:
                continue
                
            cleaned_content = self.clean_email_text(content)
            
            if len(cleaned_content) < 20:  # Skip very short emails
                continue
            
            # Create training examples with different prompt formats
            examples = [
                {
                    'prompt': f"Write a {email_type} email",
                    'response': cleaned_content
                },
                {
                    'prompt': f"Compose an email about: {subject[:50]}" if subject else "Write a professional email",
                    'response': cleaned_content
                }
            ]
            
            # Add specific email type prompts
            if 'thank' in cleaned_content.lower():
                examples.append({
                    'prompt': "Write a thank you email",
                    'response': cleaned_content
                })
            elif 'follow' in cleaned_content.lower() and 'up' in cleaned_content.lower():
                examples.append({
                    'prompt': "Write a follow-up email",
                    'response': cleaned_content
                })
            elif 'meeting' in cleaned_content.lower():
                examples.append({
                    'prompt': "Write an email about a meeting",
                    'response': cleaned_content
                })
            
            training_examples.extend(examples)
        
        return training_examples[:50]  # Limit for Ollama
    
    def create_email_modelfile(self, model_name="email-writer-llm"):
        """
        Create Modelfile for email writing model
        
        Args:
            model_name: Name for the custom model
            
        Returns:
            bool: Success status
        """
        training_examples = self.prepare_training_examples()
        
        if not training_examples:
            print("No training examples prepared. Please check your dataset.")
            return False
        
        modelfile_content = f"""FROM {self.base_model}

# Email writing model parameters
PARAMETER temperature 0.8
PARAMETER top_p 0.9
PARAMETER top_k 40
PARAMETER repeat_penalty 1.1

# System message for email writing
SYSTEM You are a professional email writing assistant. You help users compose clear, concise, and appropriate emails for various purposes including business communication, follow-ups, thank you notes, meeting requests, and general correspondence. You maintain a professional yet friendly tone and structure emails properly with appropriate greetings and closings.

"""
        
        # Add training examples
        for i, example in enumerate(training_examples[:20]):  # Limit to prevent too large modelfile
            modelfile_content += f"\n# Email Example {i+1}\n"
            modelfile_content += f'MESSAGE user "{example["prompt"]}"\n'
            modelfile_content += f'MESSAGE assistant "{example["response"]}"\n'
        
        # Save Modelfile
        with open('EmailModelfile', 'w', encoding='utf-8') as f:
            f.write(modelfile_content)
        
        print(f"Email Modelfile created with {len(training_examples)} training examples!")
        return True
    
    def create_email_model(self, model_name="email-writer-llm"):
        """
        Create the custom email writing model
        
        Args:
            model_name: Name for the custom model
            
        Returns:
            bool: Success status
        """
        try:
            print(f"Creating email writing model '{model_name}'...")
            result = subprocess.run(
                ["ollama", "create", model_name, "-f", "EmailModelfile"],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"Email model '{model_name}' created successfully!")
            print(result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error creating model: {e}")
            print(f"Error output: {e.stderr}")
            return False
        except FileNotFoundError:
            print("Ollama not found. Please make sure Ollama is installed.")
            return False
    
    def test_email_model(self, model_name="email-writer-llm"):
        """
        Test the email writing model
        
        Args:
            model_name: Name of the model to test
        """
        test_prompts = [
            "Write a professional thank you email after a job interview",
            "Compose a follow-up email for a business meeting",
            "Write an email requesting a meeting with a colleague",
            "Create an email introducing yourself to a new team",
            "Write an apology email for a delayed response"
        ]
        
        print(f"\nTesting email model '{model_name}'...\n")
        
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
                print(f"Error: {e}")
            
            print("\n" + "=" * 70 + "\n")

def main():
    print("Email Writing LLM Fine-tuning Script")
    print("=" * 40)
    
    # Get dataset path from user
    dataset_path = input("Enter path to your email dataset file: ").strip()
    
    if not dataset_path:
        print("No dataset path provided. Exiting.")
        return
    
    # Initialize trainer
    trainer = EmailModelTrainer()
    
    # Load dataset
    if not trainer.load_email_dataset(dataset_path):
        return
    
    # Create model
    model_name = "email-writer-llm"
    
    if trainer.create_email_modelfile(model_name):
        if trainer.create_email_model(model_name):
            print(f"\nEmail writing model '{model_name}' created successfully!")
            
            # Test the model
            test_choice = input("\nWould you like to test the model? (y/n): ").lower().strip()
            if test_choice == 'y':
                trainer.test_email_model(model_name)
            
            print(f"\nYou can now use your email writing model with:")
            print(f"ollama run {model_name}")
        else:
            print("Failed to create email model.")
    else:
        print("Failed to create Modelfile.")

if __name__ == "__main__":
    main()