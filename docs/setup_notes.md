# Detailed Setup Notes

This document provides comprehensive setup information and troubleshooting steps for LangExtract.

## Environment Setup

### 1. Conda Installation Verification

```bash
# Check if conda is available
which conda

# If conda is not in PATH, you may need to initialize it
eval "$(conda shell.bash hook)"

# Or use the full path (example for macOS with Homebrew miniconda)
/opt/homebrew/Caskroom/miniconda/base/bin/conda --version
```

### 2. Environment Creation

```bash
# Create environment with specific Python version
conda create -n langextract python=3.11 -y

# Activate environment
conda activate langextract

# Verify Python version
python --version  # Should show Python 3.11.x
```

### 3. LangExtract Installation

```bash
# Clone the official repository
git clone https://github.com/google/langextract.git
cd langextract

# Install in development mode with all dependencies
pip install -e ".[dev]"

# Verify installation
python -c "import langextract as lx; print('LangExtract imported successfully')"
```

## API Key Configuration

### Option 1: Environment File (Recommended)

```bash
# Create .env file
echo "LANGEXTRACT_API_KEY=your-actual-api-key" > .env

# Verify git ignores this file
echo ".env" >> .gitignore
```

### Option 2: Environment Variable

```bash
# Set environment variable (temporary)
export LANGEXTRACT_API_KEY="your-actual-api-key"

# Add to shell profile for persistence (bash)
echo 'export LANGEXTRACT_API_KEY="your-actual-api-key"' >> ~/.bashrc
source ~/.bashrc

# Add to shell profile for persistence (zsh)
echo 'export LANGEXTRACT_API_KEY="your-actual-api-key"' >> ~/.zshrc
source ~/.zshrc
```

## Required Python Packages

The development installation includes these key dependencies:

```
Core Dependencies:
- absl-py>=1.0.0
- aiohttp>=3.8.0
- google-genai>=0.1.0
- pydantic>=1.8.0
- python-dotenv>=0.19.0
- requests>=2.25.0

Development Dependencies:
- pyink~=24.3.0
- isort>=5.13.0
- pylint>=3.0.0
- tox>=4.0.0
```

## Code Implementation Notes

### Essential Imports for Examples

```python
import langextract as lx
import textwrap
from dotenv import load_dotenv  # Critical for .env file loading
import os

# Must call this before using LangExtract
load_dotenv()
```

### Model Configuration

```python
# Recommended model for balance of speed/cost/quality
model_id = "gemini-2.5-flash"

# For complex tasks requiring deeper reasoning
model_id = "gemini-2.5-pro"

# For production with higher throughput
# Consider Tier 2 Gemini quota
```

### Rate Limit Management

```python
# Conservative settings for large documents
result = lx.extract(
    text_or_documents=input_text,
    prompt_description=prompt,
    examples=examples,
    model_id="gemini-2.5-flash",
    max_workers=2,          # Reduce concurrent requests
    max_char_buffer=2000,   # Smaller chunks
    extraction_passes=1,    # Single pass
)
```

## File Structure Best Practices

```
your-project/
├── .env                    # API keys (git-ignored)
├── .env.example           # Template
├── .gitignore             # Include .env protection
├── examples/
│   ├── basic_example.py
│   ├── medical_example.py
│   └── visualization_example.py
├── langextract/           # Cloned repository
├── requirements.txt       # Optional: pin versions
└── README.md
```

## Testing Your Setup

### Step 1: Basic Import Test

```python
#!/usr/bin/env python3
import langextract as lx
from dotenv import load_dotenv

load_dotenv()
print("✅ LangExtract setup verified")
print("Available modules:", [attr for attr in dir(lx) if not attr.startswith('_')])
```

### Step 2: API Connection Test

```python
#!/usr/bin/env python3
import langextract as lx
from dotenv import load_dotenv
import os

load_dotenv()

# Simple test extraction
result = lx.extract(
    text_or_documents="Hello world",
    prompt_description="Extract greetings",
    examples=[],
    model_id="gemini-2.5-flash",
)

print("✅ API connection successful")
```

### Step 3: Full Feature Test

Run the provided examples in order:
1. `python examples/basic_example.py`
2. `python examples/medical_example.py`
3. `python examples/visualization_example.py`

## Performance Optimization

### For Large Documents

```python
# Optimized settings for full books/documents
result = lx.extract(
    text_or_documents=large_text,
    prompt_description=prompt,
    examples=examples,
    model_id="gemini-2.5-flash",
    extraction_passes=3,    # Multiple passes for higher recall
    max_workers=20,         # High parallelism
    max_char_buffer=1000,   # Smaller chunks for accuracy
)
```

### For Development/Testing

```python
# Conservative settings for testing
result = lx.extract(
    text_or_documents=test_text,
    prompt_description=prompt,
    examples=examples,
    model_id="gemini-2.5-flash",
    max_workers=2,
    max_char_buffer=2000,
    extraction_passes=1,
)
```

## Output Management

### Saving Results

```python
# Save to JSONL format
lx.io.save_annotated_documents([result], "output.jsonl", ".")

# Generate visualization
html_content = lx.visualize("output.jsonl")
with open("visualization.html", "w") as f:
    if hasattr(html_content, 'data'):
        f.write(html_content.data)
    else:
        f.write(html_content)
```

### File Organization

```bash
# Create output directory
mkdir -p outputs

# Save with timestamps
python -c "
import datetime
timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
# Use timestamp in filenames
"
```

## Advanced Configuration

### Custom Model Parameters

```python
# Using Vertex AI instead of AI Studio
result = lx.extract(
    text_or_documents=input_text,
    prompt_description=prompt,
    examples=examples,
    model_id="gemini-2.5-flash",
    language_model_params={
        "vertexai": True,
        "project": "your-project-id",
        "location": "global"
    }
)
```

### Schema Constraints

```python
# For structured output (Gemini models support this)
result = lx.extract(
    text_or_documents=input_text,
    prompt_description=prompt,
    examples=examples,
    model_id="gemini-2.5-flash",
    use_schema_constraints=True,  # Default for Gemini
    fence_output=False,           # Default for Gemini
)
```

## Next Steps

1. **Verify Setup**: Run all example scripts successfully
2. **Customize Prompts**: Modify examples for your specific use case
3. **Scale Up**: Test with larger documents using optimized settings
4. **Production**: Consider rate limits and error handling for production use

For more information, see the [troubleshooting guide](troubleshooting.md).