# 🥷 Granite Agent

**Semi-autonomous** SLM agent powered by IBM Granite with chain-of-thought.

Granite Agent is blazing fast leveraging Granite 3.3 2B model and 4-bit quantization.

## ✨ Key Features
- **Web Search:** Injects live data into the model context to ensure factual accuracy and eliminate hallucinations.
  
- **VRAM Optimization:** Engineered for consumer hardware using 4-bit quantization and a rolling history window.
  
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

## Example (Web Search)

```
User: search latest news about US-Israeli attack on Iran today

Okay, let me start by analyzing the provided sources to find the most recent news articles about the US-Israeli attacks on Iran. 

First, looking at source [1], it mentions that "The death toll from a US - Israeli missile strike on a girls’ school in southern Iran has risen to almost 150..." with details like 133 civilian deaths and 200 injuries. This seems to be a significant event.

Source [2] also talks about the same incident, confirming the death toll as 150+ civilians. It includes quotes from Iranian officials stating they were targeting military sites but civilians were harmed. There's also mention of Iran retaliating after the attacks.

Sources [5] and [6] discuss the US acknowledging there was no prior intel about Iran planning an attack against them, which adds context to the timing of these strikes. Source [7] is a TASS article citing Russian sources saying the US admitted there was no intelligence about Iran planning to attack first, which aligns with [5].

So, putting all this together, the main sources discussing the US-Israeli attacks on Iran include [1][2][5][6]. They report high casualties among civilians and Iran's retaliatory actions following the strikes. The key takeaway is the severity of the attacks and subsequent Iranian responses.
</think>

**Latest Reports on US-Israeli Strikes on Iran:**  
- **Casualty Count**: Over 150 civilians killed, 200 injured in missile strikes on a girls' school in southern Iran (sources [1][2]).  
- **Targeted Infrastructure**: Initial reports claimed targets included military facilities, though civilian areas were disproportionately affected (source [2]).  
- **Iranian Retaliation**: Immediate counterattacks followed, with Iranian leaders accusing both countries of escalating tensions without provocation (sources [1][2][5]).  
- **Intelligence Gaps**: Both the US and Israel denied preemptive knowledge of Iranian plans to attack first, despite conflicting claims (sources [5][6]).  

**Immediate Aftermath**:  
- Ayatollah Ali Khamenei reportedly killed in the assault (source [1]), leading to Iranian government condemnations of the operations as "unprecedented aggression" (source [1]).  
- Iranian forces launched counter-strikes across the region, targeting US bases and military assets (sources [1][2][5]).  

**Geopolitical Implications**:  
- The incident strained relations between the US, Israel, and Iran, raising concerns over nuclear proliferation and regional stability (sources [5][6]).  
- International bodies like the UN called for de-escalation efforts amidst heightened tensions (source [6]).
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
