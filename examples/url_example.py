#!/usr/bin/env python3
"""
URL Extraction Example
Demonstrates extracting information from web content (Project Gutenberg)
Note: This example uses conservative settings to avoid rate limits
"""

import langextract as lx
import textwrap
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    print("LangExtract URL Example: Romeo & Juliet from Project Gutenberg")
    print("=" * 65)
    
    # Simple extraction task optimized for longer text
    prompt = textwrap.dedent("""\
        Extract key characters and their main emotional states.
        Use exact text for extractions. Focus on major characters only.""")

    examples = [
        lx.data.ExampleData(
            text="HAMLET. To be, or not to be, that is the question.",
            extractions=[
                lx.data.Extraction(
                    extraction_class="character",
                    extraction_text="HAMLET",
                    attributes={"emotional_state": "contemplative"}
                ),
                lx.data.Extraction(
                    extraction_class="philosophical_question",
                    extraction_text="To be, or not to be, that is the question",
                    attributes={"theme": "existence"}
                ),
            ]
        )
    ]

    # Romeo & Juliet full text from Project Gutenberg
    test_url = "https://www.gutenberg.org/files/1513/1513-0.txt"
    
    print(f"📖 Extracting from: {test_url}")
    print("⚙️  Using conservative settings for demonstration...")
    print("⏳ This may take a few minutes...")

    try:
        # Run extraction with conservative settings to avoid hitting rate limits
        result = lx.extract(
            text_or_documents=test_url,
            prompt_description=prompt,
            examples=examples,
            model_id="gemini-2.5-flash",
            max_workers=2,  # Reduced for demonstration
            max_char_buffer=2000,  # Smaller chunks
            extraction_passes=1,  # Single pass for demo
        )
        
        print("\n📊 Extraction Results (first 15):")
        print("-" * 40)
        
        if result and result.extractions:
            for i, extraction in enumerate(result.extractions[:15], 1):
                text_preview = extraction.extraction_text[:50]
                if len(extraction.extraction_text) > 50:
                    text_preview += "..."
                print(f"{i:2d}. {extraction.extraction_class}: '{text_preview}'")
                if extraction.attributes:
                    print(f"    Attributes: {extraction.attributes}")
            
            if len(result.extractions) > 15:
                print(f"    ... and {len(result.extractions) - 15} more extractions")
            
            print(f"\n✅ Total extractions: {len(result.extractions)}")
            
            # Save results
            print("💾 Saving results...")
            lx.io.save_annotated_documents([result], output_name="url_extractions.jsonl", output_dir=".")
            
            # Generate visualization
            print("🎨 Generating visualization...")
            html_content = lx.visualize("url_extractions.jsonl")
            with open("url_visualization.html", "w") as f:
                if hasattr(html_content, 'data'):
                    f.write(html_content.data)
                else:
                    f.write(html_content)
            
            print("✅ URL extraction example completed!")
            print("📁 Generated files:")
            print("   - url_extractions.jsonl")
            print("   - url_visualization.html")
            
        else:
            print("❌ No extractions found.")
            
    except Exception as e:
        print(f"❌ Error during extraction: {e}")
        print("💡 This might be due to:")
        print("   - API rate limits")
        print("   - Network connectivity issues")
        print("   - Large document processing time")
        print("💡 Try running the basic examples first to verify setup.")

if __name__ == "__main__":
    main()