#!/usr/bin/env python3
"""
Basic LangExtract example - Romeo and Juliet character extraction
"""

import langextract as lx
import textwrap
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def main():
    print("LangExtract Basic Example: Romeo & Juliet")
    print("=" * 50)
    
    # 1. Define the prompt and extraction rules
    prompt = textwrap.dedent("""\
        Extract characters, emotions, and relationships in order of appearance.
        Use exact text for extractions. Do not paraphrase or overlap entities.
        Provide meaningful attributes for each entity to add context.""")

    # 2. Provide a high-quality example to guide the model
    examples = [
        lx.data.ExampleData(
            text="ROMEO. But soft! What light through yonder window breaks? It is the east, and Juliet is the sun.",
            extractions=[
                lx.data.Extraction(
                    extraction_class="character",
                    extraction_text="ROMEO",
                    attributes={"emotional_state": "wonder"}
                ),
                lx.data.Extraction(
                    extraction_class="emotion",
                    extraction_text="But soft!",
                    attributes={"feeling": "gentle awe"}
                ),
                lx.data.Extraction(
                    extraction_class="relationship",
                    extraction_text="Juliet is the sun",
                    attributes={"type": "metaphor"}
                ),
            ]
        )
    ]

    # The input text to be processed
    input_text = "Lady Juliet gazed longingly at the stars, her heart aching for Romeo"

    print(f"Input text: {input_text}")
    print()

    # Run the extraction
    print("Running extraction...")
    result = lx.extract(
        text_or_documents=input_text,
        prompt_description=prompt,
        examples=examples,
        model_id="gemini-2.5-flash",
    )

    print("\nExtraction Results:")
    print("-" * 30)

    if result and result.extractions:
        for i, extraction in enumerate(result.extractions, 1):
            print(f"{i}. Class: {extraction.extraction_class}")
            print(f"   Text: '{extraction.extraction_text}'")
            print(f"   Attributes: {extraction.attributes}")
            print()
    else:
        print("No extractions found.")

    print("✅ Basic example completed successfully!")
    return result

if __name__ == "__main__":
    main()