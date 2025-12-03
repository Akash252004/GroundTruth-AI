"""
Main Orchestrator - Coordinates the entire creative generation pipeline
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
import zipfile

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.brand_analyzer import BrandAnalyzer
from src.creative_generator import CreativeGenerator
from src.caption_writer import CaptionWriter


class CreativeStudio:
    """Main orchestration class for AI Creative Studio"""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.session_dir = None
        self.brand_profile = None
        self.creatives = []
        self.captions = None
    
    def create_session_folder(self, brand_name: str) -> Path:
        """Create timestamped session folder"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_name = f"{brand_name}_{timestamp}".replace(" ", "_")
        
        session_path = self.output_dir / session_name
        session_path.mkdir(parents=True, exist_ok=True)
        
        # Create subfolders
        (session_path / "creatives").mkdir(exist_ok=True)
        (session_path / "1x1").mkdir(exist_ok=True)
        (session_path / "9x16").mkdir(exist_ok=True)
        (session_path / "16x9").mkdir(exist_ok=True)
        
        self.session_dir = session_path
        return session_path
    
    def run_pipeline(
        self,
        logo_path: str,
        brand_name: str,
        product_name: str,
        tone: str,
        target_audience: str = "general consumers",
        num_variations: int = 3,
        aspect_ratios: list = None
    ) -> dict:
        """Run the complete creative generation pipeline"""
        
        if aspect_ratios is None:
            aspect_ratios = ["1:1", "9:16", "16:9"]
        
        print("\n" + "="*60)
        print("🚀 AI CREATIVE STUDIO - PIPELINE STARTED")
        print("="*60 + "\n")
        
        # Create session folder
        session_folder = self.create_session_folder(brand_name)
        print(f"📁 Session folder: {session_folder}\n")
        
        # Step 1: Analyze Brand
        print("STEP 1/3: Brand Analysis")
        print("-" * 40)
        analyzer = BrandAnalyzer(logo_path)
        self.brand_profile = analyzer.analyze()
        
        profile_path = session_folder / "brand_profile.json"
        analyzer.save_profile(str(profile_path))
        print()
        
        # Step 2: Generate Creatives
        print("STEP 2/3: Creative Generation")
        print("-" * 40)
        
        try:
            generator = CreativeGenerator()
            self.creatives = generator.generate_creative_set(
                brand_profile=self.brand_profile,
                product_name=product_name,
                tone=tone,
                num_variations=num_variations,
                aspect_ratios=aspect_ratios
            )
            
            # Save images
            for creative in self.creatives:
                ratio = creative["aspect_ratio"]
                creative_id = creative["id"]
                
                filename = f"creative_{creative_id}_{ratio.replace(':', 'x')}.png"
                filepath = session_folder / ratio.replace(":", "x") / filename
                
                creative["image"].save(filepath)
                creative["filepath"] = str(filepath)
                print(f"💾 Saved: {filename}")
            
            print(f"\n✅ Generated {len(self.creatives)} creatives across {len(aspect_ratios)} formats\n")
            
        except Exception as e:
            print(f"⚠️ Creative generation error: {e}")
            print("Continuing with caption generation...\n")
        
        # Step 3: Generate Captions
        print("STEP 3/3: Caption Generation")
        print("-" * 40)
        
        try:
            writer = CaptionWriter()
            self.captions = writer.generate_captions(
                brand_name=brand_name,
                product_name=product_name,
                tone=tone,
                target_audience=target_audience,
                num_variations=num_variations
            )
            
            # Save captions
            captions_path = session_folder / "captions.json"
            with open(captions_path, 'w') as f:
                json.dump(self.captions, f, indent=2)
            
            print(f"\n💾 Captions saved to: captions.json\n")
            
        except Exception as e:
            print(f"⚠️ Caption generation error: {e}\n")
        
        # Create summary report
        self._create_summary_report(session_folder, brand_name, product_name, tone)
        
        # Create ZIP package
        zip_path = self._create_zip_package(session_folder)
        
        print("\n" + "="*60)
        print("✅ PIPELINE COMPLETE!")
        print("="*60)
        print(f"\n📦 Download Package: {zip_path}")
        print(f"📁 Session Folder: {session_folder}\n")
        
        return {
            "session_folder": str(session_folder),
            "zip_path": str(zip_path),
            "brand_profile": self.brand_profile,
            "num_creatives": len(self.creatives),
            "captions": self.captions
        }
    
    def _create_summary_report(self, session_folder: Path, brand_name: str, product_name: str, tone: str):
        """Create summary report"""
        
        report = f"""
# 🎨 AI Creative Studio - Generation Report

**Brand:** {brand_name}
**Product:** {product_name}
**Tone:** {tone}
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## 📊 Brand Profile

**Dominant Color:** {self.brand_profile['dominant_color']['hex']}
**Mood:** {self.brand_profile['mood'].title()}
**Brightness:** {self.brand_profile['brightness'].title()}

**Color Palette:**
{chr(10).join([f"- {p['hex']}" for p in self.brand_profile['palette']])}

---

## 🎨 Generated Creatives

Total: {len(self.creatives)} images
Formats: 1:1, 9:16, 16:9

---

## ✍️ Caption Variations

{len(self.captions.get('captions', []))} caption sets generated

Check `captions.json` for full details.

---

Generated by AI Creative Studio
"""
        
        report_path = session_folder / "REPORT.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
    
    def _create_zip_package(self, session_folder: Path) -> Path:
        """Create downloadable ZIP package"""
        
        zip_path = self.output_dir / f"{session_folder.name}.zip"
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in session_folder.rglob('*'):
                if file.is_file():
                    arcname = file.relative_to(session_folder)
                    zipf.write(file, arcname)
        
        print(f"📦 Created ZIP package: {zip_path.name}")
        return zip_path


# CLI Interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Creative Studio - Generate marketing creatives")
    parser.add_argument("--logo", required=True, help="Path to brand logo")
    parser.add_argument("--brand", required=True, help="Brand name")
    parser.add_argument("--product", required=True, help="Product name")
    parser.add_argument("--tone", default="luxury", choices=["luxury", "playful", "minimal", "bold"])
    parser.add_argument("--variations", type=int, default=2, help="Number of variations")
    parser.add_argument("--demo", action="store_true", help="Run demo mode")
    
    args = parser.parse_args()
    
    if args.demo:
        print("🎬 Running in DEMO mode...\n")
        print("⚠️ This will use placeholder images if APIs are not configured.\n")
    
    studio = CreativeStudio()
    
    result = studio.run_pipeline(
        logo_path=args.logo,
        brand_name=args.brand,
        product_name=args.product,
        tone=args.tone,
        num_variations=args.variations
    )
    
    print(f"\n✅ All done! Check: {result['session_folder']}")
