"""Generate demo logo and product images"""
from PIL import Image, ImageDraw, ImageFont
import random

def create_demo_logo():
    """Create a simple demo logo"""
    img = Image.new('RGB', (500, 500), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw gradient-like circles
    colors = ['#667eea', '#764ba2', '#5a67d8']
    for i, color in enumerate(colors):
        offset = i * 50
        draw.ellipse([100 + offset, 100 + offset, 400 - offset, 400 - offset], 
                     fill=color, outline=color, width=5)
    
    img.save('demo_assets/sample_logo.png')
    print("✅ Created demo_assets/sample_logo.png")

def create_demo_product():
    """Create a simple demo product image"""
    img = Image.new('RGB', (800, 800), color='#f8f9fa')
    draw = ImageDraw.Draw(img)
    
    # Draw a simple watch shape
    # Watch face
    draw.ellipse([250, 250, 550, 550], fill='#2c3e50', outline='#34495e', width=10)
    # Inner circle (display)
    draw.ellipse([290, 290, 510, 510], fill='#3498db', outline='#2980b9', width=5)
    
    # Watch band
    draw.rectangle([350, 100, 450, 250], fill='#2c3e50')
    draw.rectangle([350, 550, 450, 700], fill='#2c3e50')
    
    img.save('demo_assets/sample_product.png')
    print("✅ Created demo_assets/sample_product.png")

if __name__ == "__main__":
    import os
    os.makedirs('demo_assets', exist_ok=True)
    
    create_demo_logo()
    create_demo_product()
    
    print("\n✅ Demo assets created successfully!")
