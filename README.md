# LangExtract Test Setup

A ready-to-use setup for Google's LangExtract library with working examples and complete documentation.

## Overview

LangExtract is a Python library that uses LLMs to extract structured information from unstructured text documents. This repository provides a complete, tested setup with examples that work out of the box.

## Features Demonstrated

- **Character & Emotion Extraction**: Extract literary characters and their emotional states
- **Medical Information Extraction**: Extract medications, dosages, and administration routes
- **Interactive Visualizations**: Generate HTML visualizations of extracted data
- **Multiple Input Sources**: Process text strings, files, or URLs
- **Structured Output**: JSON/JSONL format with precise text mapping

## Quick Start

### Prerequisites

- **miniconda** or **conda** installed ([Download here](https://docs.conda.io/en/latest/miniconda.html))
- **Gemini API Key** ([Get one here](https://aistudio.google.com/app/apikey))

### 1. Clone and Setup

```bash
# Clone this repository
git clone https://github.com/Project-Kobo/lang-extract-test.git
cd lang-extract-test

# Create conda environment with Python 3.11
conda create -n langextract python=3.11 -y

# Activate the environment
conda activate langextract

# Clone the original LangExtract repository
git clone https://github.com/google/langextract.git

# Install LangExtract with development dependencies
cd langextract
pip install -e ".[dev]"
cd ..
```

### 2. Configure API Key

```bash
# Create .env file with your API key
echo "LANGEXTRACT_API_KEY=your-api-key-here" > .env

# Ensure .env is git-ignored (already done in this repo)
echo ".env" >> .gitignore
```

### 3. Run Examples

```bash
# Basic Romeo & Juliet example
python examples/basic_example.py

# Medical information extraction
python examples/medical_example.py

# Test visualization generation
python examples/visualization_example.py
```

## Installation Details

### Critical Setup Steps

Based on our testing, here are the essential steps that must be followed:

1. **Conda Environment**: Python 3.11 is required. We tested with miniconda on macOS ARM64.

2. **API Key Loading**: The `.env` file must be explicitly loaded using `python-dotenv`. This is handled in all examples.

3. **Conda Path**: On macOS with Homebrew miniconda, the full conda path is:
   ```bash
   /opt/homebrew/Caskroom/miniconda/base/bin/conda
   ```

4. **Development Installation**: Use `pip install -e ".[dev]"` for the full feature set including visualization tools.

## Examples

### Basic Character Extraction

```python
import langextract as lx
from dotenv import load_dotenv

load_dotenv()  # Essential for API key loading

prompt = "Extract characters and emotions with exact text."
examples = [...]  # See examples/ directory
input_text = "Lady Juliet gazed longingly at the stars..."

result = lx.extract(
    text_or_documents=input_text,
    prompt_description=prompt,
    examples=examples,
    model_id="gemini-2.5-flash",
)
```

### Medical Information Extraction

```python
# Extract medications, dosages, routes
prompt = "Extract medications, dosages, and administration routes."
input_text = "Patient takes Aspirin 81mg once daily by mouth."

# Results include structured attributes:
# medication: "Aspirin" {drug_class: "antiplatelet"}
# dosage: "81mg" {amount: "81", unit: "mg"}
# frequency: "once daily" {times_per_day: "1"}
```

### Generate Visualizations

```python
# Save results to JSONL
lx.io.save_annotated_documents([result], "results.jsonl", ".")

# Generate interactive HTML visualization
html_content = lx.visualize("results.jsonl")
with open("visualization.html", "w") as f:
    f.write(html_content)
```

## File Structure

```
lang-extract-test/
├── README.md                    # This file
├── .env.example                # Template for API key
├── .gitignore                  # Includes .env protection
├── examples/
│   ├── basic_example.py        # Romeo & Juliet extraction
│   ├── medical_example.py      # Medical information extraction
│   ├── visualization_example.py # HTML visualization demo
│   └── url_example.py          # Extract from URLs
├── docs/
│   ├── setup_notes.md          # Detailed setup information
│   └── troubleshooting.md      # Common issues and solutions
└── langextract/                # Original repository (cloned)
```

## Expected Output

### Basic Example Results
```
1. Class: character
   Text: 'Lady Juliet'
   Attributes: {'emotional_state': 'longing'}

2. Class: emotion  
   Text: 'her heart aching for Romeo'
   Attributes: {'feeling': 'sorrowful desire'}
```

### Medical Example Results
```
1. medication: 'Aspirin'
   Attributes: {'drug_class': 'antiplatelet', 'generic_name': 'aspirin'}
   
2. dosage: '81mg'
   Attributes: {'amount': '81', 'unit': 'mg'}
   
3. frequency: 'once daily'
   Attributes: {'times_per_day': '1', 'interval': 'daily'}
```

### Generated Files
- `extraction_results.jsonl` - Structured extraction data
- `visualization.html` - Interactive HTML visualization
- `medical_extractions.jsonl` - Medical extraction data
- `medical_visualization.html` - Medical data visualization

## Troubleshooting

### Common Issues

1. **API Key Not Found**
   ```
   InferenceConfigError: Gemini models require either an API key...
   ```
   **Solution**: Ensure `.env` file exists and `load_dotenv()` is called.

2. **Conda Command Not Found**
   ```
   conda: command not found
   ```
   **Solution**: Use full path or initialize conda shell:
   ```bash
   eval "$(conda shell.bash hook)"
   ```

3. **Import Errors**
   ```
   ModuleNotFoundError: No module named 'langextract'
   ```
   **Solution**: Ensure you're in the correct conda environment and installed with `-e ".[dev]"`.

### Performance Notes

- **Rate Limits**: Gemini has rate limits. For large documents, use `max_workers=2` and `extraction_passes=1`.
- **Model Choice**: `gemini-2.5-flash` is recommended for speed and cost efficiency.
- **Chunk Size**: Use `max_char_buffer=2000` for better accuracy on complex texts.

## Advanced Usage

### URL Extraction
```python
# Extract from Romeo & Juliet full text
result = lx.extract(
    text_or_documents="https://www.gutenberg.org/files/1513/1513-0.txt",
    prompt_description=prompt,
    examples=examples,
    model_id="gemini-2.5-flash",
    extraction_passes=3,    # Multiple passes for higher recall
    max_workers=20,         # Parallel processing
    max_char_buffer=1000    # Smaller chunks for accuracy
)
```

### Custom Extraction Classes
Define your own extraction categories by modifying the examples and prompt descriptions.

## Contributing

This repository demonstrates LangExtract setup and usage. For contributing to the main LangExtract project, see the [official repository](https://github.com/google/langextract).

## License

This setup repository is provided as-is for demonstration purposes. LangExtract itself is licensed under the Apache 2.0 License by Google LLC.

## Resources

- [LangExtract Official Repository](https://github.com/google/langextract)
- [Google AI Studio (API Keys)](https://aistudio.google.com/app/apikey)
- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [Miniconda Download](https://docs.conda.io/en/latest/miniconda.html)

---

**Need Help?** Check the [troubleshooting guide](docs/troubleshooting.md) or refer to the [setup notes](docs/setup_notes.md) for detailed installation steps.