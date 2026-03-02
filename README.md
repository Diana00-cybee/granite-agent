# 🥷 Granite Agent

Small language model (SLM) agent using IBM Granite 2B with reasoning.

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
