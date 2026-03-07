# 🥷 Granite Agent

Semi-autonomous intelligent small agent powered by IBM Granite.

Granite Agent is blazing fast using Granite 2B model and 4-bit quantization.

## ⭐ Key Features

- **Web Search:** Injects live data into the model context to ensure factual accuracy and prevent hallucination.

- **Memory Management:** Implements cache flushing and manual garbage collection to maintain stability.

- **Reasoning:** Employs dedicated <think> block for step-by-step logic before delivering the final result.

- **Uncensored:** Fused with specialized LoRA adapter for unrestricted access to sensitive data.

- **Deep Scraping:** System uses Browser-impersonation scraping to bypass bot protection.

- **Plain-Text:** Strips away complex formatting to focus model's attention on raw logic.

- **VRAM Optimization:** Engineered for consumer hardware using 4-bit quantization.

## 🛠️ Installation

### 1. Prerequisites
* **Nvidia GPU** (At least 4GB+ VRAM recommended)
* **Python 3.11+** installed on your system
* **PyTorch** with CUDA 12.1

### 2. Setup Environment
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Mac/Linux
```

### 3. Install PyTorch (CUDA)
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```
### 4. Install Requirements
```bash
pip install -r requirements.txt
```

## Example

```
User: search top 5 lightweight Linux distros to use in 2026, bullet point, no more than five sentences, save
Agent: 2026-03-06 12:13:58,336 - GraniteAgent - INFO - Sanitized query for search engine: 'top 5 lightweight linux distros to use in 2026'
2026-03-06 12:13:58,363 - GraniteAgent - INFO - Broad Search Triggered: 'top 5 lightweight linux distros to use in 2026'
2026-03-06 12:14:01,084 - GraniteAgent - INFO - Scraping URL: https://thishosting.rocks/best-lightweight-linux-distros/
2026-03-06 12:14:02,679 - GraniteAgent - INFO - Successfully validated deep context from: https://thishosting.rocks/best-lightweight-linux-distros/
2026-03-06 12:14:06,878 - GraniteAgent - INFO - Total valid sources compiled: 8

**Top 5 Lightweight Linux Distros for 2026:**  

1. **Slax (Debian-based)**  
   - Portable, under 300MB, uses Xfce for simplicity. Ideal for reviving old devices.  
2. **Linux Lite (Ubuntu-based)**  
   - User-friendly, Xfce desktop, perfect for beginners needing minimalism.  
3. **Puppy Linux**  
   - Extremely small (44MB base), customizable via Puppy Package Manager.  
4. **Lubuntu (Ubuntu variant)**  
   - Retains Ubuntu’s polish while reducing resource usage.  
5. **Tails OS**  
   - Preconfigured for privacy/anonymity; starts with browser, email, etc.

2026-03-06 12:14:56,800 - GraniteAgent - INFO - Successfully exported research to: outputs\search_top_5_lightweight_Linux_distros_to_use_in_2.txt
```

## 🚀 Usage

### Start Agent

```bash
python cli.py
```

### Prompt Keywords

```bash
## Web Search
keyword: search

## Save File
keyword: save

## Trusted Sites
keyword: whitelist

## Summary
keyword: summary

## Answer Format
use one of these keywords:

bullet point
numbered
markdown
clean

## Shorter Sentence
use one of these keywords:

no more than three sentences
no more than five sentences
no more than ten sentences
```

## ☕ Support
If you find this project valuable, consider supporting my work:

[![Buy Me A Coffee](https://img.shields.io/badge/Buy_Me_A_Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/vpakarinen)
[![Ko-Fi](https://img.shields.io/badge/Ko--fi-F16061?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ko-fi.com/vpakarinen)

## Author

Ville Pakarinen (@vpakarinen2)
