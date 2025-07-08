# Flash Drive LLM

A portable LLM chatbot using Microsoft Phi-4 Mini model that you can run offline.

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/willowhughes/flashdrivellm
   cd flashdrivellm
   ```

2. **Download the model:**
   - Download the model file (~3GB): 
     [microsoft_Phi-4-mini-instruct-Q6_K_L.gguf](https://huggingface.co/bartowski/microsoft_Phi-4-mini-instruct-GGUF/resolve/main/microsoft_Phi-4-mini-instruct-Q6_K_L.gguf)
   - Place it in: `llm_model/`

3. **Run the chatbot:**
   ```bash
   python main.py
   ```

## Requirements

- (for now) Python 3.8+
- ~4GB RAM minimum
- ~4GB disk space

## Model Information

- **Model**: Microsoft Phi-4 Mini Instruct
- **Quantization**: Q6_K_L (good balance of quality vs size)
- **Size**: ~3GB
- **Context Length**: 2048 tokens

## Usage

Simply run `python main.py` and start chatting! Type `exit` or `quit` to end the session.

## Dev Notes

- The model file is not included in this repository due to its size (3GB). You'll need to download it separately as described above.
- <create virtual environment (recommended):
   ```bash
   python -m venv venv
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   venv\Scripts\activate  # on Windows
   ```
- future: pyinstaller --onedir --name "FlashDriveLLM" app/main.py
