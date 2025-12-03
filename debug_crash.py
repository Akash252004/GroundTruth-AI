
import os
import sys
from dotenv import load_dotenv
import time

# Add src to path
sys.path.insert(0, os.path.abspath("src"))

try:
    print("1. Importing dependencies...")
    from huggingface_hub import InferenceClient
    from PIL import Image
    import requests
    print("   Dependencies imported successfully.")
except Exception as e:
    print(f"CRITICAL: Failed to import dependencies: {e}")
    sys.exit(1)

load_dotenv()

def test_generation():
    print("\n2. Testing CreativeGenerator...")
    try:
        from src.creative_generator import CreativeGenerator
        generator = CreativeGenerator()
        print("   CreativeGenerator initialized.")
        
        print("3. Attempting generation (Pollinations fallback test)...")
        # Force a prompt that might trigger fallback if API key is invalid, or just test normal flow
        img = generator.generate_image("test prompt", "1:1")
        print(f"   Generation result: {type(img)}")
        
    except Exception as e:
        print(f"CRITICAL: Error during generation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_generation()
