#!/usr/bin/env python3
"""
Medical Information Extraction Example
Demonstrates extraction of medications, dosages, and administration routes
"""

import langextract as lx
import textwrap
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    print("LangExtract Medical Example: Medication Extraction")
    print("=" * 55)
    
    # 1. Define the prompt for medical information extraction
    prompt = textwrap.dedent("""\
        Extract medications, dosages, and administration routes from clinical text.
        Use exact text for extractions. Do not paraphrase or overlap entities.
        Provide meaningful attributes for each entity including dosage amounts and frequencies.""")

    # 2. Provide examples to guide the model
    examples = [
        lx.data.ExampleData(
            text="Patient was prescribed Metformin 500mg twice daily by mouth.",
            extractions=[
                lx.data.Extraction(
                    extraction_class="medication",
                    extraction_text="Metformin",
                    attributes={"drug_class": "antidiabetic", "generic_name": "metformin"}
                ),
                lx.data.Extraction(
                    extraction_class="dosage",
                    extraction_text="500mg",
                    attributes={"amount": "500", "unit": "mg"}
                ),
                lx.data.Extraction(
                    extraction_class="frequency",
                    extraction_text="twice daily",
                    attributes={"times_per_day": "2", "interval": "daily"}
                ),
                lx.data.Extraction(
                    extraction_class="route",
                    extraction_text="by mouth",
                    attributes={"administration": "oral"}
                ),
            ]
        )
    ]

    # Test cases with different medical scenarios
    test_cases = [
        "Patient takes Aspirin 81mg once daily for cardioprotection.",
        "Prescribed Amoxicillin 875mg every 12 hours orally for 7 days.",
        "Insulin injection 10 units subcutaneously before meals.",
        "Apply topical hydrocortisone cream 1% to affected area twice daily."
    ]

    all_results = []

    for i, input_text in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print(f"Input: {input_text}")
        print("-" * 50)
        
        # Run the extraction
        result = lx.extract(
            text_or_documents=input_text,
            prompt_description=prompt,
            examples=examples,
            model_id="gemini-2.5-flash",
        )
        
        if result and result.extractions:
            for j, extraction in enumerate(result.extractions, 1):
                print(f"  {j}. {extraction.extraction_class}: '{extraction.extraction_text}'")
                if extraction.attributes:
                    print(f"     Attributes: {extraction.attributes}")
            all_results.append(result)
        else:
            print("  No extractions found.")

    # Save all results to a comprehensive JSONL file
    if all_results:
        print(f"\nSaving {len(all_results)} results to medical_extractions.jsonl...")
        lx.io.save_annotated_documents(all_results, output_name="medical_extractions.jsonl", output_dir=".")
        
        print("✅ Medical extraction example completed successfully!")
        print("📁 Generated: medical_extractions.jsonl")
        
    return all_results

if __name__ == "__main__":
    main()