# 🥷 Granite Agent

Semi-autonomous SLM agent powered by IBM Granite.

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

```bash
--- Granite Agent ---
Type 'exit' or 'quit' to stop.

User: search resident evil requiem metacritic pc, summary, no more than three sentences
Agent: 2026-03-05 11:50:13,008 - GraniteAgent - INFO - Sanitized query for search engine: 'resident evil requiem metacritic pc'
2026-03-05 11:50:13,044 - GraniteAgent - INFO - Broad Search Triggered: 'resident evil requiem metacritic pc'
2026-03-05 11:50:15,354 - GraniteAgent - INFO - Scraping URL: https://www.metacritic.com/game/resident-evil-requiem/
2026-03-05 11:50:15,917 - GraniteAgent - INFO - Successfully validated deep context from: https://www.metacritic.com/game/resident-evil-requiem/
2026-03-05 11:50:21,565 - GraniteAgent - INFO - Total valid sources compiled: 9

Resident Evil Requiem received widespread acclaim on PC, achieving the highest user score of 9.5 on Metacritic. Users praised its blend of classic survival horror and modern action elements, exceptional graphics via the RE Engine, and engaging dual protagonists. However, some critics noted minor issues like an underwhelming narrative and sluggish pacing.
```

## 🚀 Usage

### Start Agent

```bash
python cli.py
```

### Commands

```bash
Web Search
Activate using keyword: search

Save File
Activate using keyword: save

Trusted Sites
Activate using keyword: whitelist

Answer Format
Activate using one of these keywords:

bullet point
numbered
markdown
clean

Clean Output
To have cleaner output use one of these:

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
