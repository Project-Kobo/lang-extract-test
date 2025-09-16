#!/usr/bin/env python3
"""
Quick Test Example - Minimal LangExtract validation

This script runs a minimal test to verify your LangExtract setup is working.
Run this first before trying the more complex examples.

Usage:
    python examples/00_quick_test.py
"""

import sys
import os
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test that all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import langextract as lx
        print("  ✅ langextract imported successfully")
    except ImportError as e:
        print(f"  ❌ Failed to import langextract: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("  ✅ python-dotenv imported successfully")
    except ImportError as e:
        print(f"  ❌ Failed to import python-dotenv: {e}")
        return False
    
    return True

def test_environment():
    """Test environment configuration"""
    print("\n🔧 Testing environment...")
    
    from dotenv import load_dotenv
    
    # Load .env file
    env_loaded = load_dotenv()
    print(f"  📄 .env file loaded: {env_loaded}")
    
    # Check API key
    api_key = os.getenv('LANGEXTRACT_API_KEY')
    if api_key:
        if api_key == 'your-api-key-here':
            print("  ⚠️  API key is still placeholder - update .env file")
            return False
        else:
            key_preview = f"{api_key[:8]}..." if len(api_key) > 8 else "***"
            print(f"  ✅ API key found: {key_preview}")
            return True
    else:
        print("  ❌ LANGEXTRACT_API_KEY not found in environment")
        return False

def test_basic_extraction():
    """Test basic LangExtract functionality"""
    print("\n🚀 Testing basic extraction...")
    
    try:
        import langextract as lx
        from dotenv import load_dotenv
        
        load_dotenv()
        
        # Simple test with minimal prompt
        print("  📝 Running extraction test...")
        result = lx.extract(
            text_or_documents="Hello world! This is a test.",
            prompt_description="Extract any greetings or test phrases",
            examples=[],
            model_id="gemini-2.5-flash",
        )
        
        if result:
            print("  ✅ Extraction completed successfully")
            
            if hasattr(result, 'extractions') and result.extractions:
                count = len(result.extractions)
                print(f"  📊 Found {count} extraction(s)")
                
                # Show first extraction as example
                first = result.extractions[0]
                print(f"     Example: '{first.extraction_text}' ({first.extraction_class})")
            else:
                print("  📊 No extractions found (this is normal for simple test)")
            
            return True
        else:
            print("  ❌ Extraction returned no result")
            return False
            
    except Exception as e:
        error_msg = str(e)
        print(f"  ❌ Extraction failed: {error_msg}")
        
        # Provide helpful error guidance
        if "API key" in error_msg or "authentication" in error_msg.lower():
            print("     💡 Check your API key in .env file")
        elif "rate limit" in error_msg.lower():
            print("     💡 Rate limit hit - wait a moment and try again")
        elif "network" in error_msg.lower():
            print("     💡 Check your internet connection")
        
        return False

def test_output_capabilities():
    """Test output directory and file creation"""
    print("\n📁 Testing output capabilities...")
    
    # Check/create outputs directory
    outputs_dir = project_root / "outputs"
    if not outputs_dir.exists():
        outputs_dir.mkdir(exist_ok=True)
        print("  ✅ Created outputs/ directory")
    else:
        print("  ✅ outputs/ directory exists")
    
    # Test writing to outputs directory
    try:
        test_file = outputs_dir / "quick_test.txt"
        with open(test_file, "w") as f:
            f.write("Quick test successful!")
        print("  ✅ Can write to outputs/ directory")
        
        # Clean up test file
        test_file.unlink()
        return True
        
    except Exception as e:
        print(f"  ❌ Cannot write to outputs/ directory: {e}")
        return False

def main():
    """Run all quick tests"""
    print("🎯 LangExtract Quick Test")
    print("=" * 40)
    
    tests = [
        ("Imports", test_imports),
        ("Environment", test_environment), 
        ("Basic Extraction", test_basic_extraction),
        ("Output Capabilities", test_output_capabilities),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
    
    # Summary
    print(f"\n{'='*40}")
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("  • python examples/basic_example.py")
        print("  • python examples/medical_example.py")
        print("  • python examples/visualization_example.py")
        return True
    elif passed >= total - 1:
        print("⚠️  Setup mostly working with minor issues.")
        print("You can proceed but may want to fix the failing test.")
        return True
    else:
        print("❌ Setup has significant issues.")
        print("Please run 'python validate_setup.py' for detailed diagnostics.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)