#!/usr/bin/env python3
"""
LangExtract Visualization Example
Demonstrates generating interactive HTML visualizations of extracted data
"""

import langextract as lx
import textwrap
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    print("LangExtract Visualization Example")
    print("=" * 40)
    
    # Define extraction task
    prompt = textwrap.dedent("""\
        Extract characters, emotions, and relationships in order of appearance.
        Use exact text for extractions. Do not paraphrase or overlap entities.
        Provide meaningful attributes for each entity to add context.""")

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

    # Extended input text for better visualization
    input_text = """Lady Juliet gazed longingly at the stars, her heart aching for Romeo. 
    She whispered his name softly into the night air. Meanwhile, Romeo wandered the streets below, 
    consumed by passionate love for his beloved Juliet. Their families' ancient feud 
    seemed meaningless in the face of such pure affection."""

    print("Processing text for visualization...")
    print(f"Input: {input_text}")
    print()

    # Run the extraction
    result = lx.extract(
        text_or_documents=input_text,
        prompt_description=prompt,
        examples=examples,
        model_id="gemini-2.5-flash",
    )

    if result and result.extractions:
        print(f"✅ Found {len(result.extractions)} extractions")
        
        # Display results
        for i, extraction in enumerate(result.extractions, 1):
            print(f"  {i}. {extraction.extraction_class}: '{extraction.extraction_text}'")
        
        # Save results to JSONL file
        print("\n📝 Saving results to JSONL file...")
        lx.io.save_annotated_documents([result], output_name="visualization_results.jsonl", output_dir=".")
        
        # Generate visualization
        print("🎨 Generating interactive visualization...")
        html_content = lx.visualize("visualization_results.jsonl")
        
        # Save visualization to HTML file
        with open("interactive_visualization.html", "w") as f:
            if hasattr(html_content, 'data'):
                f.write(html_content.data)  # For Jupyter/Colab
            else:
                f.write(html_content)
        
        print("✅ Visualization example completed successfully!")
        print("📁 Generated files:")
        print("   - visualization_results.jsonl")
        print("   - interactive_visualization.html")
        print("💡 Open 'interactive_visualization.html' in a web browser to see the results!")
        
    else:
        print("❌ No extractions found.")

    return result

if __name__ == "__main__":
    main()