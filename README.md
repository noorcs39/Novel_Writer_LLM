# Novel Email LLM

## Project Overview
This project focuses on fine-tuning and utilizing a language model for email-related tasks. It includes scripts for data scraping, fine-tuning, and testing the model, as well as datasets and documentation.

## Folder Structure

- `src/` - Contains source code files for fine-tuning, scraping, and other utilities.
- `tests/` - Includes test files for validating the functionality of the model and scripts.
- `data/` - Stores datasets and related files.
- `scripts/` - Utility scripts for various tasks.
- `docs/` - Documentation and related files.

## Key Files

- `src/email_fine_tune.py` - Script for fine-tuning the email model.
- `src/fine_tune_model.py` - Core fine-tuning logic.
- `src/pdf_to_json.py` - Converts PDF content to JSON format.
- `src/scraper.py` - Scrapes data for training and testing.
- `tests/test_email_model.py` - Tests for the email model.
- `tests/test_model.py` - General model tests.
- `data/finetune_dataset.json` - Dataset for fine-tuning.

## How to Use

1. **Setup Environment**: Install dependencies using the `requirements.txt` file.
2. **Run Scripts**: Use the scripts in the `src/` folder for fine-tuning and data processing.
3. **Testing**: Run the test files in the `tests/` folder to validate functionality.

## Requirements

Install the required Python packages:
```bash
pip install -r requirements.txt
```

## Contributing
Feel free to contribute by submitting issues or pull requests. Ensure that your code is well-documented and tested.

## License
This project is licensed under the MIT License.
