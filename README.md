# 🥷 Granite Agent

**Semi-autonomous** SLM agent powered by IBM Granite with chain-of-thought.

Granite Agent is blazing fast leveraging Granite 3.3 2B model and 4-bit quantization.

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
