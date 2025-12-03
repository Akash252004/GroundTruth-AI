
import streamlit as st
import sys
from pathlib import Path
import json
from PIL import Image

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from main import CreativeStudio

# Page config
st.set_page_config(
    page_title="AI Creative Studio",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    
    .tagline {
        text-align: center;
        color: #6c757d;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        border: none;
    }
    
    .stButton>button:hover {
        opacity: 0.9;
    }
    
    .creative-card {
        border: 2px solid #e9ecef;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🎨 AI Creative Studio</h1>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Generate brand-consistent marketing creatives in seconds • 100% FREE</p>', unsafe_allow_html=True)

# Initialize session state
if 'generated' not in st.session_state:
    st.session_state.generated = False
if 'result' not in st.session_state:
    st.session_state.result = None

# Sidebar - Input Form
with st.sidebar:
    st.header("📝 Project Details")
    
    with st.form("input_form"):
        # File uploads
        logo_file = st.file_uploader("Upload Brand Logo", type=['png', 'jpg', 'jpeg'])
        
        # Text inputs
        brand_name = st.text_input("Brand Name", value="MyBrand", placeholder="e.g., TechStyle")
        product_name = st.text_input("Product Name", value="New Product", placeholder="e.g., Smart Watch")
        
        # Dropdowns
        tone = st.selectbox(
            "Brand Tone",
            ["luxury", "playful", "minimal", "bold"],
            help="Select the tone that matches your brand personality"
        )
        
        target_audience = st.text_input(
            "Target Audience (Optional)", 
            placeholder="e.g., young professionals",
            value="general consumers"
        )
        
        # Multi-select for formats
        st.write("**Output Formats:**")
        format_1x1 = st.checkbox("Instagram Post (1:1)", value=True)
        format_9x16 = st.checkbox("Instagram Story (9:16)", value=True)
        format_16x9 = st.checkbox("YouTube Thumbnail (16:9)", value=True)
        
        num_variations = st.slider("Number of Variations", 1, 3, 2)
        
        # Submit button
        submitted = st.form_submit_button("🚀 Generate Creatives")
    
    # API Status
    st.divider()
    st.caption("💡 **API Status**")
    
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    hf_key = os.getenv("HUGGINGFACE_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    if hf_key:
        st.success("✅ HuggingFace API")
    else:
        st.warning("⚠️ HuggingFace API not set")
    
    if gemini_key:
        st.success("✅ Gemini API")
    else:
        st.warning("⚠️ Gemini API not set")

# Main Content Area
if submitted and logo_file and brand_name and product_name:
    
    # Save uploaded logo temporarily
    temp_logo_path = Path("temp_logo.png")
    with open(temp_logo_path, "wb") as f:
        f.write(logo_file.read())
    
    # Determine aspect ratios
    aspect_ratios = []
    if format_1x1:
        aspect_ratios.append("1:1")
    if format_9x16:
        aspect_ratios.append("9:16")
    if format_16x9:
        aspect_ratios.append("16:9")
    
    if not aspect_ratios:
        st.error("⚠️ Please select at least one output format!")
    else:
        # Show progress
        with st.spinner("🎨 Analyzing brand style..."):
            studio = CreativeStudio()
            
            try:
                result = studio.run_pipeline(
                    logo_path=str(temp_logo_path),
                    brand_name=brand_name,
                    product_name=product_name,
                    tone=tone,
                    target_audience=target_audience,
                    num_variations=num_variations,
                    aspect_ratios=aspect_ratios
                )
                
                st.session_state.result = result
                st.session_state.generated = True
                
                # Cleanup
                temp_logo_path.unlink()
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.error("Please check your API keys in .env file")

elif submitted:
    st.warning("⚠️ Please fill in all required fields (logo, brand name, product name)")

# Display Results
if st.session_state.generated and st.session_state.result:
    result = st.session_state.result
    
    st.success(f"✅ Successfully generated {result['num_creatives']} creatives!")
    
    # Download button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if Path(result['zip_path']).exists():
            with open(result['zip_path'], 'rb') as f:
                st.download_button(
                    label="📦 Download All Creatives (ZIP)",
                    data=f.read(),
                    file_name=Path(result['zip_path']).name,
                    mime="application/zip",
                    use_container_width=True
                )
    
    st.divider()
    
    # Brand Profile
    st.subheader("🎨 Brand Profile")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Dominant Color", result['brand_profile']['dominant_color']['hex'])
    
    with col2:
        st.metric("Brand Mood", result['brand_profile']['mood'].title())
    
    with col3:
        st.metric("Brightness", result['brand_profile']['brightness'].title())
    
    # Color palette
    st.write("**Color Palette:**")
    palette_cols = st.columns(5)
    for i, color in enumerate(result['brand_profile']['palette']):
        with palette_cols[i]:
            st.markdown(
                f'<div style="background-color:{color["hex"]}; height:50px; border-radius:5px; border:1px solid #ddd;"></div>',
                unsafe_allow_html=True
            )
            st.caption(color['hex'])
    
    st.divider()
    
    # Generated Creatives
    st.subheader("🖼️ Generated Creatives")
    
    session_folder = Path(result['session_folder'])
    
    # Group by aspect ratio
    for ratio in ["1x1", "9x16", "16x9"]:
        ratio_folder = session_folder / ratio
        
        if ratio_folder.exists():
            images = list(ratio_folder.glob("*.png"))
            
            if images:
                st.write(f"**{ratio.replace('x', ':')} Format** ({len(images)} images)")
                
                cols = st.columns(min(len(images), 3))
                
                for i, img_path in enumerate(images):
                    with cols[i % 3]:
                        # Use use_column_width for compatibility
                        st.image(str(img_path), use_column_width=True, caption=img_path.name)
    
    st.divider()
    
    # Captions
    st.subheader("✍️ Generated Captions")
    
    if result['captions']:
        for caption in result['captions'].get('captions', []):
            with st.expander(f"📝 Caption Variation #{caption['variation']}"):
                st.write(f"**Headline:** {caption['headline']}")
                st.write(f"**Subheadline:** {caption['subheadline']}")
                st.write(f"**CTA:** {caption['cta']}")
                st.write(f"**Long Caption:** {caption['long_caption']}")
                st.write(f"**Hashtags:** {' '.join(caption['hashtags'])}")

else:
    # Welcome message
    st.info("""
    👋 **Welcome to AI Creative Studio!**
    
    This tool helps you generate brand-consistent marketing creatives automatically using FREE AI models.
    
    **How it works:**
    1. Upload your brand logo
    2. Enter brand and product details
    3. Select your brand tone
    4. Choose output formats
    5. Click "Generate Creatives"
    6. Download your complete creative package!
    
    **Features:**
    - 🎨 Automatic brand color extraction
    - 🖼️ AI-generated marketing visuals
    - ✍️ AI-written marketing copy
    - 📱 Multiple platform formats
    - 📦 Downloadable ZIP package
    
    💡 **First time setup:**
    1. Copy `.env.example` to `.env`
    2. Add your FREE API keys (HuggingFace + Google Gemini)
    3. Run `pip install -r requirements.txt`
    """)
    
    # Example showcase
    st.subheader("Example Output")
    st.write("Here's what you'll get:")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📸 **Creatives**\n\n10-15 unique images in multiple formats")
    with col2:
        st.info("✍️ **Captions**\n\nMarketing copy with headlines, CTAs, hashtags")
    with col3:
        st.info("📦 **ZIP Package**\n\nOrganized folder structure ready to use")
