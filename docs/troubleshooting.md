# Troubleshooting Guide

Common issues and solutions for LangExtract setup and usage.

## Installation Issues

### 1. Conda Command Not Found

**Error:**
```
conda: command not found
```

**Solutions:**

Option A: Initialize conda shell
```bash
eval "$(conda shell.bash hook)"
conda --version
```

Option B: Use full path (macOS with Homebrew)
```bash
/opt/homebrew/Caskroom/miniconda/base/bin/conda --version
```

Option C: Add to PATH
```bash
echo 'export PATH="/opt/homebrew/Caskroom/miniconda/base/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### 2. Python Version Issues

**Error:**
```
Python 3.9 found, but 3.11+ required
```

**Solution:**
```bash
# Create environment with specific Python version
conda create -n langextract python=3.11 -y
conda activate langextract
python --version  # Verify 3.11.x
```

### 3. Import Errors

**Error:**
```
ModuleNotFoundError: No module named 'langextract'
```

**Solutions:**

Check environment:
```bash
conda activate langextract
conda list | grep langextract
```

Reinstall if needed:
```bash
cd langextract
pip install -e ".[dev]"
```

## API Key Issues

### 1. API Key Not Found

**Error:**
```
InferenceConfigError: Gemini models require either:
- An API key via api_key parameter or LANGEXTRACT_API_KEY env var
- Vertex AI configuration with vertexai=True, project, and location
```

**Solutions:**

Verify .env file exists:
```bash
ls -la .env
cat .env  # Should show LANGEXTRACT_API_KEY=your-key
```

Check dotenv loading in code:
```python
from dotenv import load_dotenv
import os

load_dotenv()
print("API Key loaded:", bool(os.getenv('LANGEXTRACT_API_KEY')))
```

### 2. Invalid API Key

**Error:**
```
HTTP 403: API key not valid
```

**Solutions:**

1. Verify key at [AI Studio](https://aistudio.google.com/app/apikey)
2. Check for extra spaces/characters:
   ```bash
   # Remove any trailing whitespace
   sed -i 's/[[:space:]]*$//' .env
   ```
3. Generate new API key if needed

### 3. Rate Limits

**Error:**
```
HTTP 429: Too Many Requests
```

**Solutions:**

Use conservative settings:
```python
result = lx.extract(
    text_or_documents=input_text,
    prompt_description=prompt,
    examples=examples,
    model_id="gemini-2.5-flash",
    max_workers=1,          # Reduce concurrency
    extraction_passes=1,    # Single pass
)
```

Add delays between requests:
```python
import time
time.sleep(1)  # Wait between extractions
```

## Runtime Issues

### 1. Extraction Returns No Results

**Symptoms:**
- Empty extractions list
- "No extractions found" message

**Solutions:**

Check prompt clarity:
```python
# Be specific about what to extract
prompt = "Extract ONLY medication names and dosages. Use exact text."
```

Improve examples:
```python
# Provide high-quality, relevant examples
examples = [
    lx.data.ExampleData(
        text="Patient takes Aspirin 81mg daily.",
        extractions=[
            lx.data.Extraction(
                extraction_class="medication",
                extraction_text="Aspirin",
                attributes={"dosage": "81mg"}
            )
        ]
    )
]
```

Test with simpler input:
```python
# Start with basic text
input_text = "John took medicine."
```

### 2. Extraction Quality Issues

**Symptoms:**
- Inaccurate extractions
- Missing important entities
- Overlapping extractions

**Solutions:**

Refine prompt instructions:
```python
prompt = textwrap.dedent("""\
    Extract medications and dosages.
    Rules:
    1. Use EXACT text from the source
    2. Do NOT paraphrase or overlap entities
    3. Extract complete dosage information
    4. Include units (mg, ml, etc.)
    """)
```

Use multiple extraction passes:
```python
result = lx.extract(
    text_or_documents=input_text,
    prompt_description=prompt,
    examples=examples,
    model_id="gemini-2.5-flash",
    extraction_passes=3,  # Multiple passes for better recall
)
```

### 3. Memory Issues with Large Documents

**Error:**
```
MemoryError: Unable to allocate array
```

**Solutions:**

Reduce chunk size:
```python
result = lx.extract(
    text_or_documents=large_text,
    prompt_description=prompt,
    examples=examples,
    model_id="gemini-2.5-flash",
    max_char_buffer=1000,  # Smaller chunks
    max_workers=2,         # Fewer parallel workers
)
```

Process in batches:
```python
# Split large documents manually
chunks = [large_text[i:i+5000] for i in range(0, len(large_text), 5000)]
all_results = []

for chunk in chunks:
    result = lx.extract(chunk, prompt, examples, model_id)
    all_results.append(result)
```

## Visualization Issues

### 1. HTML Not Generating

**Error:**
```
Empty visualization file
```

**Solutions:**

Check JSONL file:
```bash
wc -l results.jsonl  # Should show > 0 lines
head -1 results.jsonl  # Check format
```

Verify extractions exist:
```python
if result and result.extractions:
    print(f"Found {len(result.extractions)} extractions")
    lx.io.save_annotated_documents([result], "test.jsonl", ".")
else:
    print("No extractions to visualize")
```

### 2. HTML Display Issues

**Symptoms:**
- Blank page in browser
- JavaScript errors

**Solutions:**

Check file size:
```bash
ls -lh visualization.html  # Should be > 5KB typically
```

Open developer console in browser to check for errors.

Try different browser (Chrome/Firefox/Safari).

## Performance Issues

### 1. Slow Processing

**Symptoms:**
- Long wait times
- Timeouts

**Solutions:**

Optimize model settings:
```python
# Use faster model for testing
model_id = "gemini-2.5-flash"  # Instead of gemini-2.5-pro

# Reduce complexity
extraction_passes = 1
max_workers = 2
```

Profile your text:
```python
print(f"Text length: {len(input_text)} characters")
print(f"Estimated chunks: {len(input_text) // 2000}")
```

### 2. High API Costs

**Solutions:**

Monitor usage:
```python
# Use smaller test samples during development
test_text = input_text[:1000]  # First 1000 characters
```

Optimize prompts:
```python
# Shorter, more focused prompts
prompt = "Extract medications only."  # Instead of long instructions
```

## Environment Issues

### 1. Wrong Conda Environment

**Symptoms:**
- Import errors after installation
- Different Python version

**Solutions:**

Check active environment:
```bash
conda info --envs
# Should show * next to langextract
```

Activate correct environment:
```bash
conda activate langextract
which python  # Should point to langextract env
```

### 2. Package Conflicts

**Error:**
```
ImportError: cannot import name 'X' from 'Y'
```

**Solutions:**

Clean reinstall:
```bash
conda deactivate
conda remove -n langextract --all
conda create -n langextract python=3.11 -y
conda activate langextract
cd langextract
pip install -e ".[dev]"
```

## Network Issues

### 1. URL Extraction Fails

**Error:**
```
ConnectionError: Failed to fetch URL
```

**Solutions:**

Test URL accessibility:
```bash
curl -I https://www.gutenberg.org/files/1513/1513-0.txt
```

Use local file instead:
```python
# Download first, then process
import requests
response = requests.get(url)
with open("local_file.txt", "w") as f:
    f.write(response.text)

result = lx.extract("local_file.txt", prompt, examples, model_id)
```

## Getting Help

### 1. Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 2. Minimal Reproduction

Create a minimal test case:
```python
import langextract as lx
from dotenv import load_dotenv

load_dotenv()

result = lx.extract(
    text_or_documents="Test text",
    prompt_description="Extract anything",
    examples=[],
    model_id="gemini-2.5-flash"
)

print("Test result:", result)
```

### 3. Check Versions

```bash
conda list | grep -E "(python|langextract)"
pip show langextract
```

### 4. Community Resources

- [LangExtract GitHub Issues](https://github.com/google/langextract/issues)
- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [Google AI Studio](https://aistudio.google.com/)

If none of these solutions work, please open an issue with:
1. Full error message
2. Your environment details (`conda list`)
3. Minimal reproduction code
4. Expected vs actual behavior