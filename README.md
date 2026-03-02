# 🥷 Granite Agent

Semi-autonomous SLM agent powered by IBM Granite.

Granite Agent is blazing fast leveraging Granite 3.3 2B model.

## ✨ Key Features
- **Web Search:** Injects live data into the model context to ensure factual accuracy and eliminate hallucinations.

- **Deep Scraping:** System uses Browser-impersonation scraping to bypass bot protections and deep-read articles.
  
- **VRAM Optimization:** Engineered for consumer hardware using 4-bit quantization and rolling history window.
  
- **Plain-Text:** Strips away Markdown and complex formatting to focus model's attention on raw logic and data.
  
- **Memory Management:** Implements hard cache flushing and manual garbage collection to maintain stability.

- **Reasoning:** Employs dedicated <think> block for step-by-step logic before delivering the final result.

- **Uncensored:** Fused with specialized LoRA adapter for unrestricted access to sensitive data.

## 🛠️ Installation

### 1. Prerequisites
* **Nvidia GPU** (At least 4GB+ VRAM recommended)
* **Python 3.11+** installed on your system
* **PyTorch** with CUDA 12.1

### 2. Setup Environment
```
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Mac/Linux
```

### 3. Install PyTorch (CUDA)
```
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```
### 4. Install Requirements
```
pip install -r requirements.txt
```

## Examples

```
User: search what is genie 3, do not add more than three sentences
Agent: 2026-03-03 00:58:21,816 - GraniteAgent - INFO - External Search Triggered: 'search what is genie 3, do not add more than three sentences'
2026-03-03 00:58:24,510 - GraniteAgent - INFO - Scraping URL for deep context: https://deepmind.google/models/genie/
Genie 3 is a **real-time, interactive 3D world generator** developed by Google DeepMind. It transforms textual descriptions into photorealistic environments running at 24 fps, allowing users to navigate and manipulate the scene indefinitely. Key features include dynamic world events, 720p resolution, and no frame drops during prolonged interaction.
---
User: search what is nanobanana 2, do not add more than three sentences
Agent: 2026-03-03 00:59:08,945 - GraniteAgent - INFO - External Search Triggered: 'search what is nanobanana 2, do not add more than three sentences'
2026-03-03 00:59:10,422 - GraniteAgent - INFO - Scraping URL for deep context: https://www.ainanobanana2.com/
Nanobanana 2 is a cutting-edge AI image generator and editor, now integrated as Google's default tool. It supports 1K, 2K, and 4K resolutions for high-quality output, including physical prints. Its sophisticated algorithms enable precise text-to-image conversion, iterative refinement, and realistic scene reconstruction.
```

## 🚀 Usage

### Start Agent

```
python cli.py
```

### Web Search
you can activate web search using keyword **search**:

```
search <query>
```

## Author

Ville Pakarinen (@vpakarinen2)
