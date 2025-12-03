

import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()


class CaptionWriter:
    """Generates marketing captions using AI"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key not found!")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def generate_captions(
        self, 
        brand_name: str, 
        product_name: str, 
        tone: str,
        target_audience: str = "general consumers",
        num_variations: int = 3
    ) -> dict:
        """Generate marketing captions with variations"""
        
        prompt = f"""You are an expert marketing copywriter. Create {num_variations} different ad caption sets for:

Brand: {brand_name}
Product: {product_name}
Tone: {tone}
Target Audience: {target_audience}

For each caption set, provide:
1. Headline (5-7 words, punchy and attention-grabbing)
2. Subheadline (10-15 words, explains the value proposition)
3. CTA (2-4 words, action-oriented)
4. Long Caption (25-40 words, for social media posts)
5. Hashtags (3-5 relevant hashtags)

Format your response as JSON:
{{
  "captions": [
    {{
      "variation": 1,
      "headline": "...",
      "subheadline": "...",
      "cta": "...",
      "long_caption": "...",
      "hashtags": ["...", "..."]
    }},
    ...
  ]
}}

Make sure the tone matches: {tone}
Be creative, persuasive, and authentic. No placeholder text."""

        try:
            print(f"✍️ Generating {num_variations} caption variations...")
            response = self.model.generate_content(prompt)
            
            # Parse JSON from response
            text = response.text.strip()
            
            # Extract JSON from markdown code blocks if present
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            
            captions_data = json.loads(text)
            print(f"✅ Generated {len(captions_data.get('captions', []))} caption variations!")
            
            return captions_data
            
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON parsing error: {e}")
            print(f"Raw response: {response.text[:500]}")
            
            # Fallback captions
            return self._generate_fallback_captions(brand_name, product_name, tone, num_variations)
        
        except Exception as e:
            print(f"❌ Error generating captions: {e}")
            return self._generate_fallback_captions(brand_name, product_name, tone, num_variations)
    
    def _generate_fallback_captions(self, brand_name: str, product_name: str, tone: str, num: int) -> dict:
        """Generate simple fallback captions if API fails"""
        
        tone_templates = {
            "luxury": {
                "headline": f"Elevate Your {product_name} Experience",
                "subheadline": f"Discover the premium quality of {brand_name}",
                "cta": "Explore Now",
                "long_caption": f"Experience luxury redefined with {brand_name}'s {product_name}. Crafted for those who appreciate excellence.",
                "hashtags": ["#Luxury", "#Premium", f"#{brand_name}"]
            },
            "playful": {
                "headline": f"Make Every Day Fun!",
                "subheadline": f"{product_name} that brings joy to your life",
                "cta": "Get Yours",
                "long_caption": f"Life's too short for boring! {brand_name}'s {product_name} adds a spark to your everyday routine.",
                "hashtags": ["#Fun", "#Lifestyle", f"#{brand_name}"]
            },
            "minimal": {
                "headline": f"Simply {product_name}",
                "subheadline": f"Clean design meets perfect functionality",
                "cta": "Shop Now",
                "long_caption": f"Less is more. {brand_name} brings you {product_name} with elegant simplicity.",
                "hashtags": ["#Minimalist", "#Design", f"#{brand_name}"]
            },
            "bold": {
                "headline": f"Stand Out With {product_name}",
                "subheadline": f"Make a statement with {brand_name}",
                "cta": "Be Bold",
                "long_caption": f"Don't blend in. {brand_name}'s {product_name} is for those who dare to be different.",
                "hashtags": ["#Bold", "#BeYou", f"#{brand_name}"]
            }
        }
        
        template = tone_templates.get(tone.lower(), tone_templates["minimal"])
        
        return {
            "captions": [
                {**template, "variation": i + 1} 
                for i in range(num)
            ]
        }
    
    def format_caption_display(self, caption: dict) -> str:
        """Format caption for display"""
        return f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 CAPTION VARIATION #{caption['variation']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 HEADLINE
{caption['headline']}

📄 SUBHEADLINE
{caption['subheadline']}

🎯 CTA
{caption['cta']}

📱 LONG CAPTION
{caption['long_caption']}

#️⃣ HASHTAGS
{' '.join(caption['hashtags'])}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""


# Test function
if __name__ == "__main__":
    print("Testing Caption Writer...")
    
    try:
        writer = CaptionWriter()
        captions = writer.generate_captions(
            brand_name="TechStyle",
            product_name="Smart Watch",
            tone="luxury",
            num_variations=2
        )
        
        print("\n📋 Generated Captions:")
        for caption in captions.get("captions", []):
            print(writer.format_caption_display(caption))
    
    except ValueError as e:
        print(f"⚠️ {e}")
        print("Please set GEMINI_API_KEY in .env file")
