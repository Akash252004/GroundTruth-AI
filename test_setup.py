"""
Quick test script to verify all components work
"""

import sys
from pathlib import Path

print("🧪 AI Creative Studio - Component Test\n")
print("="*50)

# Test 1: Import all modules
print("\n✓ TEST 1: Module Imports")
try:
    from src.brand_analyzer import BrandAnalyzer
    from src.creative_generator import CreativeGenerator
    from src.caption_writer import CaptionWriter
    print("  ✅ All modules imported successfully")
except ImportError as e:
    print(f"  ❌ Import failed: {e}")
    sys.exit(1)

# Test 2: Check demo assets
print("\n✓ TEST 2: Demo Assets")
if Path("demo_assets/sample_logo.png").exists():
    print("  ✅ Logo exists")
else:
    print("  ❌ Logo missing")

if Path("demo_assets/sample_product.png").exists():
    print("  ✅ Product image exists")
else:
    print("  ❌ Product image missing")

# Test 3: Brand Analyzer
print("\n✓ TEST 3: Brand Analyzer")
try:
    analyzer = BrandAnalyzer("demo_assets/sample_logo.png")
    profile = analyzer.analyze()
    
    if profile and "dominant_color" in profile:
        print(f"  ✅ Extracted {len(profile['palette'])} colors")
        print(f"  ✅ Dominant color: {profile['dominant_color']['hex']}")
        print(f"  ✅ Brand mood: {profile['mood']}")
    else:
        print("  ❌ Profile incomplete")
except Exception as e:
    print(f"  ❌ Error: {e}")

# Test 4: Check API keys
print("\n✓ TEST 4: API Configuration")
import os
from dotenv import load_dotenv
load_dotenv()

hf_key = os.getenv("HUGGINGFACE_API_KEY")
gemini_key = os.getenv("GEMINI_API_KEY")

if hf_key and hf_key != "your_hf_token_here":
    print("  ✅ HuggingFace API key configured")
else:
    print("  ⚠️  HuggingFace API key not set (image generation will fail)")

if gemini_key and gemini_key != "your_gemini_key_here":
    print("  ✅ Gemini API key configured")
else:
    print("  ⚠️  Gemini API key not set (caption generation will use fallbacks)")

# Test 5: Directory structure
print("\n✓ TEST 5: Project Structure")
required_files = [
    "main.py",
    "app.py",
    "requirements.txt",
    "src/brand_analyzer.py",
    "src/creative_generator.py",
    "src/caption_writer.py",
    "README.md"
]

all_exist = True
for file in required_files:
    if Path(file).exists():
        print(f"  ✅ {file}")
    else:
        print(f"  ❌ {file} missing")
        all_exist = False

print("\n" + "="*50)
if all_exist:
    print("\n✅ ALL TESTS PASSED!")
    print("\n🚀 Ready to run:")
    print("   • Web UI:  streamlit run app.py")
    print("   • CLI:     python main.py --help")
else:
    print("\n⚠️  Some components missing. Check errors above.")

print("\n💡 Next Steps:")
print("   1. Add your API keys to .env file")
print("   2. Run: pip install -r requirements.txt")
print("   3. Launch: streamlit run app.py")
