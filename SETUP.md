 🚀 AI Creative Studio - Setup & Run Guide

AI Creative Studio is an AI-powered marketing automation tool that transforms brand logos into complete marketing campaigns with generated images and copy in under 60 seconds.

 📋 Prerequisites

- **Python 3.11+** (required)
- **Git** (for cloning)
- **Internet connection** (for AI API calls)

## 🛠️ Quick Setup (3 minutes)

### 1. Clone & Navigate
```bash
git clone https://github.com/Akash252004/GroundTruth-AI.git
cd GROUNDTRUTH
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup API Keys
```bash
# Copy the example file
cp .env.example .env

# Edit .env file and add your API keys:
# HUGGINGFACE_API_KEY=your_huggingface_token_here
# GEMINI_API_KEY=your_gemini_key_here
```

### 5. Run the Application
```bash
streamlit run app.py
```

## 🔑 Getting FREE API Keys

### HuggingFace API Key (1000 images/month FREE)
1. Go to [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Click "New token"
3. Name: `AI-Creative-Studio`
4. Role: `Read`
5. Copy the token

### Google Gemini API Key (1500 requests/day FREE)
1. Go to [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Click "Create API key"
3. Copy the API key

## 🧪 Testing Your Setup

Run the test script to verify everything works:
```bash
python test_setup.py
```

Expected output:
```
✅ All modules imported successfully
✅ Brand analyzer working
✅ API keys configured (if you added them)
```

## 🎯 Using the Application

### Web Interface (Recommended)
```bash
streamlit run app.py
```
- Open browser to `http://localhost:8501`
- Upload your brand logo
- Enter brand/product details
- Select tone and formats
- Click "Generate Creatives"

### Command Line Interface
```bash
python main.py --logo path/to/logo.png --brand "YourBrand" --product "YourProduct" --tone luxury
```

### Generate Demo Assets (Optional)
```bash
python create_demo_assets.py
```

## 📁 Project Structure

```
ai-creative-studio/
├── app.py                 # Streamlit web interface
├── main.py               # Core orchestration logic
├── requirements.txt      # Python dependencies
├── .env                  # API keys (create from .env.example)
├── .env.example          # API key template
├── .gitignore           # Git ignore rules
├── README.md            # Project documentation
├── src/                 # Core modules
│   ├── brand_analyzer.py    # Logo color extraction
│   ├── creative_generator.py # AI image generation
│   └── caption_writer.py     # AI copywriting
├── demo_assets/         # Sample logos (auto-generated)
├── output/              # Generated campaigns
└── test_setup.py        # Setup verification
```

## 🚨 Troubleshooting

### Common Issues:

**"Module not found" errors:**
```bash
# Activate virtual environment first
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Then reinstall
pip install -r requirements.txt
```

**API Key errors:**
- Check `.env` file exists and keys are correct
- Verify keys have proper permissions
- Check API quotas/limits

**Image generation fails:**
- System falls back to Pollinations.ai (no key needed)
- Check internet connection
- Wait for rate limits to reset

**Streamlit won't start:**
```bash
# Kill any existing processes
pkill -f streamlit

# Try different port
streamlit run app.py --server.port 8502
```

### Debug Mode
```bash
python debug_crash.py
```

## 📊 API Usage & Limits

| API | Free Tier | Usage |
|-----|-----------|-------|
| HuggingFace | 1000 images/month | Image generation |
| Google Gemini | 1500 requests/day | Marketing copy |
| Pollinations.ai | Unlimited | Backup image generation |

## 🎨 Features

- ✅ **Brand-aware AI**: Extracts colors from logos
- ✅ **Multi-format output**: Instagram, YouTube, display ads
- ✅ **AI copywriting**: Headlines, captions, hashtags
- ✅ **ZIP packaging**: Ready-to-use campaign folders
- ✅ **100% FREE**: No paid APIs required
- ✅ **Production-ready**: Error handling & fallbacks

## 💡 Tips

1. **Start with demo assets**: Use `create_demo_assets.py` for testing
2. **Test API keys**: Run `test_setup.py` before using
3. **Monitor usage**: Check API dashboards for quota limits
4. **Backup outputs**: `output/` folder contains all generations

---

**Need help?** Check the test output and ensure all API keys are properly configured.

Happy creating! 🎨
