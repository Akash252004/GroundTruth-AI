"""
Creative Generator - Generates marketing creatives using Hugging Face API
Model: Stable Diffusion v1.5 (FREE tier: 1000 requests/month)
"""

import requests
import os
from io import BytesIO
from PIL import Image
import time
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()


class CreativeGenerator:
    """Generates brand-consistent marketing creatives using AI"""
    
    # HuggingFace models (all FREE)
    MODELS = {
        "primary": "stabilityai/stable-diffusion-xl-base-1.0",
        "fallback": "runwayml/stable-diffusion-v1-5"
    }
    
    ASPECT_RATIOS = {
        "1:1": (1024, 1024),    # SDXL prefers 1024x1024
        "9:16": (768, 1344),    # SDXL portrait
        "16:9": (1344, 768),    # SDXL landscape
    }
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("HUGGINGFACE_API_KEY")
        if not self.api_key:
            raise ValueError("HuggingFace API key not found!")
        
        self.client = InferenceClient(token=self.api_key)
        self.model = self.MODELS["primary"]
    
    def build_prompt(self, brand_profile: dict, product_name: str, tone: str) -> str:
        """Build AI prompt using brand colors and style"""
        
        dominant_hex = brand_profile["dominant_color"]["hex"]
        mood = brand_profile["mood"]
        
        # Build color description
        palette_colors = [p["hex"] for p in brand_profile["palette"][:3]]
        color_desc = f"color scheme: {', '.join(palette_colors)}"
        
        # Tone-specific styles
        tone_styles = {
            "luxury": "elegant, premium, sophisticated, minimal, high-end, 8k",
            "playful": "fun, colorful, energetic, dynamic, youthful, vibrant",
            "minimal": "clean, simple, modern, minimalist, white space, studio",
            "bold": "vibrant, eye-catching, dramatic, strong, impactful, cinematic"
        }
        
        style = tone_styles.get(tone.lower(), "professional, modern")
        
        prompt = f"""professional product photography of {product_name}, 
        {style} aesthetic, {color_desc}, 
        studio lighting, marketing campaign, advertisement quality, 
        commercial photography, sharp focus, high resolution, 
        {mood} mood, brand advertisement"""
        
        return prompt.replace("\n", " ").strip()
    
    def generate_image(self, prompt: str, aspect_ratio: str = "1:1", retries: int = 3) -> Image:
        """Generate image using HuggingFace API with Pollinations.ai fallback"""
        
        # Adjust dimensions based on model (SDXL needs higher res)
        width, height = self.ASPECT_RATIOS[aspect_ratio]
        
        # Try primary model first, then fallback, then Pollinations
        models_to_try = [self.MODELS["primary"], self.MODELS["fallback"], "pollinations"]
        
        for model in models_to_try:
            print(f"🎨 Trying model: {model}...")
            
            # Special handling for Pollinations.ai (No API Key needed)
            if model == "pollinations":
                for attempt in range(retries):
                    try:
                        print(f"   Attempt {attempt + 1}/{retries} (Pollinations)...")
                        # Pollinations uses GET request with URL parameters
                        encoded_prompt = requests.utils.quote(prompt)
                        # Random seed to ensure variation
                        import random
                        seed = random.randint(0, 10000)
                        image_url = f"https://pollinations.ai/p/{encoded_prompt}?width={width}&height={height}&model=flux&seed={seed}"
                        
                        response = requests.get(image_url, timeout=60)
                        
                        if response.status_code == 200:
                            image = Image.open(BytesIO(response.content))
                            print(f"✅ Generated {aspect_ratio} creative successfully with Pollinations!")
                            return image
                        else:
                            print(f"❌ Pollinations error {response.status_code}")
                            time.sleep(2)
                            continue
                    except Exception as e:
                        print(f"❌ Error with Pollinations: {e}")
                        time.sleep(2)
                        continue
                
                # If Pollinations fails after retries, continue to next model (if any)
                continue

            # Hugging Face Logic
            # Use smaller dimensions for v1.5 fallback
            if model == self.MODELS["fallback"]:
                if aspect_ratio == "1:1": width, height = 512, 512
                elif aspect_ratio == "9:16": width, height = 512, 910
                elif aspect_ratio == "16:9": width, height = 910, 512
            
            for attempt in range(retries):
                try:
                    print(f"   Attempt {attempt + 1}/{retries}...")
                    
                    # Use InferenceClient for robust generation
                    image = self.client.text_to_image(
                        prompt,
                        model=model,
                        width=width,
                        height=height,
                        num_inference_steps=30,
                        guidance_scale=7.5
                    )
                    
                    print(f"✅ Generated {aspect_ratio} creative successfully with {model}!")
                    return image
                        
                except Exception as e:
                    print(f"❌ Error generating image: {e}")
                    if "503" in str(e) or "loading" in str(e).lower():
                        print(f"⏳ Model {model} loading, waiting 15 seconds...")
                        time.sleep(15)
                    else:
                        time.sleep(2)
            
            print(f"⚠️ Failed with {model}, switching to next model...")
        
        # Return blank image if all models and retries fail
        print("⚠️ Failed to generate image with all models, returning placeholder")
        placeholder = Image.new('RGB', (512, 512), color=(50, 50, 50))
        from PIL import ImageDraw
        draw = ImageDraw.Draw(placeholder)
        text = f"Generation Failed\nCheck Internet"
        draw.text((100, 256), text, fill=(255,255,255))
        return placeholder
    
    def generate_creative_set(
        self, 
        brand_profile: dict, 
        product_name: str, 
        tone: str,
        num_variations: int = 3,
        aspect_ratios: list = None
    ) -> list:
        """Generate multiple creatives with different variations"""
        
        if aspect_ratios is None:
            aspect_ratios = ["1:1", "9:16", "16:9"]
        
        base_prompt = self.build_prompt(brand_profile, product_name, tone)
        creatives = []
        
        print(f"\n🎯 Base Prompt: {base_prompt}\n")
        
        # Generate variations
        variation_modifiers = [
            "centered composition",
            "lifestyle scene with product",
            "close-up product shot"
        ]
        
        creative_id = 1
        for i in range(min(num_variations, len(variation_modifiers))):
            modifier = variation_modifiers[i]
            prompt = f"{base_prompt}, {modifier}"
            
            for ratio in aspect_ratios:
                image = self.generate_image(prompt, ratio)
                
                creatives.append({
                    "id": creative_id,
                    "variation": i + 1,
                    "aspect_ratio": ratio,
                    "prompt": prompt,
                    "image": image
                })
                
                creative_id += 1
                time.sleep(2)  # Rate limiting
        
        return creatives


# Test function
if __name__ == "__main__":
    print("Testing Creative Generator...")
    
    # Sample brand profile
    sample_profile = {
        "dominant_color": {"rgb": (64, 64, 64), "hex": "#404040"},
        "palette": [
            {"rgb": (64, 64, 64), "hex": "#404040"},
            {"rgb": (128, 128, 128), "hex": "#808080"}
        ],
        "mood": "luxury",
        "brightness": "dark"
    }
    
    try:
        generator = CreativeGenerator()
        prompt = generator.build_prompt(sample_profile, "Premium Watch", "luxury")
        print(f"Generated Prompt: {prompt}")
    except ValueError as e:
        print(f"⚠️ {e}")
        print("Please set HUGGINGFACE_API_KEY in .env file")
