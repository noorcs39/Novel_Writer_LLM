# Novel Writer LLM

A powerful Large Language Model (LLM)-based tool designed to assist in writing, editing, and generating novel-length fiction. Novel Writer LLM provides AI-powered features such as plot generation, character development, dialogue assistance, and style suggestions to support authors throughout their writing process.

## 🚀 Features

- **Plot Generation**: Create compelling story arcs and plot structures
- **Character Development**: Build rich, multi-dimensional characters with backstories
- **Dialogue Assistance**: Generate realistic and engaging character conversations
- **Style Suggestions**: Adapt writing style to match different genres and tones
- **Chapter Planning**: Organize and structure your novel effectively
- **Genre-Specific Writing**: Tailored assistance for romance, thriller, sci-fi, fantasy, and more

## 📁 Actual Project Structure

```
Novel_Writer_LLM/
├── README.md                    # Project overview and setup
├── requirements.txt            # Python dependencies
├── src/                        # Core source code
│   ├── email_fine_tune.py      # Model fine-tuning utilities
│   ├── fine_tune_model.py      # Core fine-tuning logic
│   ├── pdf_to_json.py          # PDF processing utilities
│   └── scraper.py              # Data collection tools
├── data/                       # Training and reference data
│   └── finetune_dataset.json   # Fine-tuning dataset
├── scraped_data/               # Collected training data
│   ├── sacred_texts_content.json
│   ├── sacred_texts_training.txt
│   └── scraping_stats.json
├── results/                    # Model configurations and outputs
│   ├── EmailModelfile          # Email model configuration
│   └── Modelfile               # General model configuration
├── tests/                      # Test suites
│   ├── test_Novel_model.py     # Novel model tests
│   └── test_email_model.py     # Email model tests
└── docs/                       # Documentation
    └── Untitled document.pdf   # Additional documentation
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Ollama installed and running
- Git (for cloning the repository)

### Quick Start
1. **Clone the repository**:
   ```bash
   git clone https://github.com/noorcs39/Novel_Writer_LLM.git
   cd Novel_Writer_LLM
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Ollama models**:
   ```bash
   # Use existing model configurations
   ollama create novel-writer-llm -f results/Modelfile
   ```

4. **Test the installation**:
   ```bash
   python tests/test_Novel_model.py
   ```

## 🎯 Usage

### Basic Model Usage
```bash
# Test the novel writing capabilities
python tests/test_Novel_model.py

# Test email writing capabilities (for reference)
python tests/test_email_model.py
```

### Data Processing
```bash
# Process PDF documents for training data
python src/pdf_to_json.py

# Scrape additional training data
python src/scraper.py
```

### Model Fine-tuning
```bash
# Fine-tune the model with existing dataset
python src/fine_tune_model.py

# Fine-tune with email-specific data
python src/email_fine_tune.py
```

## 📊 Data Statistics

**Current Training Data**:
- **177 documents** scraped from sacred-texts.com
- **372,636 words** of training content
- **2,121,819 characters** of text data
- **182 URLs** successfully processed
- **0 failed** scrapes

## 🔧 Model Configuration

The project uses Ollama with custom configurations:

- **Base Model**: TinyLlama (via Ollama)
- **Model Files**: Available in `results/` directory
- **Training Data**: Based on classic literature and narrative texts

## 🧪 Testing

Run the available test suites:

```bash
# Test novel writing capabilities
python tests/test_Novel_model.py

# Test email writing capabilities
python tests/test_email_model.py
```

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Built with [Ollama](https://ollama.ai) for local LLM capabilities
- Training data sourced from public domain literature
- Inspired by creative writing and storytelling communities

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/noorcs39/Novel_Writer_LLM/issues)
- **Email**: noor.cs2@yahoo.com

---

## Implementation Credits

**Novel Writer LLM** was implemented by **Nooruddin Noonari**  
📧 **Contact**: noor.cs2@yahoo.com  
🔗 **GitHub**: [@noorcs39](https://github.com/noorcs39)

*This project represents a comprehensive AI-assisted creative writing platform, built upon robust data collection and fine-tuning capabilities.*
