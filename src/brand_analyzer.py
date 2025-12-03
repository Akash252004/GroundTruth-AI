"""
Brand Style Analyzer - Extracts colors and mood from logo/product images
Uses: Colorthief (FREE, local processing)
"""

import json
from colorthief import ColorThief
from PIL import Image
import numpy as np
from pathlib import Path


class BrandAnalyzer:
    """Analyzes brand visual identity from logo/product images"""
    
    def __init__(self, logo_path: str):
        self.logo_path = logo_path
        self.brand_profile = {}
    
    def extract_color_palette(self, num_colors: int = 5):
        """Extract dominant color palette from logo"""
        try:
            ct = ColorThief(self.logo_path)
            palette = ct.get_palette(color_count=num_colors, quality=1)
            dominant_color = ct.get_color(quality=1)
            
            return {
                "palette": palette,
                "dominant": dominant_color
            }
        except Exception as e:
            print(f"Error extracting colors: {e}")
            # Fallback to default palette
            return {
                "palette": [(64, 64, 64), (128, 128, 128), (192, 192, 192), (255, 255, 255), (0, 0, 0)],
                "dominant": (64, 64, 64)
            }
    
    def analyze_brightness(self, rgb_color: tuple) -> str:
        """Determine if color is dark, medium, or light"""
        brightness = sum(rgb_color) / 3
        
        if brightness < 85:
            return "dark"
        elif brightness < 170:
            return "medium"
        else:
            return "light"
    
    def predict_mood(self, dominant_color: tuple, palette: list) -> str:
        """Predict brand mood based on color analysis"""
        brightness = self.analyze_brightness(dominant_color)
        
        # Calculate color variance
        palette_array = np.array(palette)
        variance = np.std(palette_array)
        
        # Determine mood
        if brightness == "dark" and variance < 50:
            return "luxury"
        elif brightness == "light" and variance > 80:
            return "playful"
        elif variance < 40:
            return "minimal"
        else:
            return "bold"
    
    def rgb_to_hex(self, rgb: tuple) -> str:
        """Convert RGB to hex color code"""
        return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])
    
    def analyze(self) -> dict:
        """Complete brand analysis"""
        print(f"🎨 Analyzing brand style from: {self.logo_path}")
        
        # Extract colors
        color_data = self.extract_color_palette()
        palette = color_data["palette"]
        dominant = color_data["dominant"]
        
        # Predict mood
        mood = self.predict_mood(dominant, palette)
        brightness = self.analyze_brightness(dominant)
        
        # Build brand profile
        self.brand_profile = {
            "dominant_color": {
                "rgb": dominant,
                "hex": self.rgb_to_hex(dominant)
            },
            "palette": [
                {"rgb": color, "hex": self.rgb_to_hex(color)} 
                for color in palette
            ],
            "mood": mood,
            "brightness": brightness
        }
        
        print(f"✅ Brand Mood: {mood.upper()}")
        print(f"✅ Dominant Color: {self.rgb_to_hex(dominant)}")
        
        return self.brand_profile
    
    def save_profile(self, output_path: str):
        """Save brand profile to JSON"""
        with open(output_path, 'w') as f:
            json.dump(self.brand_profile, f, indent=2)
        print(f"💾 Brand profile saved to: {output_path}")


# Test function
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        logo_path = sys.argv[1]
        analyzer = BrandAnalyzer(logo_path)
        profile = analyzer.analyze()
        
        print("\n📊 Brand Profile:")
        print(json.dumps(profile, indent=2))
    else:
        print("Usage: python brand_analyzer.py <logo_path>")
