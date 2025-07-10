# Flash Drive LLM

A portable LLM chatbot using guanaco-7b-uncensored model that you can run offline wth all dependancies bundled.

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/willowhughes/flashdrivellm
   cd flashdrivellm
   ```

2. **Download the model:**
   - Download the model file (~3GB): 
     [guanaco-7b-uncensored.Q4_K_M.gguf](https://huggingface.co/TheBloke/Guanaco-7B-Uncensored-GGUF/blob/main/guanaco-7b-uncensored.Q4_K_M.gguf)

3. **Put it in the right place:**
   ```
   flashdrivellm/
   ├── app/
   ├── llm_model/
   │   └── guanaco-7b-uncensored.Q4_K_M.gguf  ← Here!
   └── README.md
   ```

4. **Run the chatbot:**
   ```bash
   python main.py
   ```

## Requirements

- (for now) Python 3.8+
- ~4GB RAM minimum
- ~4GB disk space

## Model Information

- **Model**: guanaco-7b-uncensored.Q4_K_M.gguf
- **Quantization**: Q4_K_M
- **Size**: ~4GB
- **Context Length**: 4096 tokens

## Usage

- Simply run `python main.py` and start chatting! Type `/exit` or `/quit` to end the session.
- for an exe you'll need to run the command '''bash
   pyinstaller --name FlashDriveLLM --onedir app/main.py
   ```
   and then manually move the folder ..\flashdrivellm\venv\Lib\site-packages\llama_cpp into ..\FlashDriveLLM\dist\FlashDriveLLM\_internal

## Pro Tips

- **Copy-paste works!** Paste code, long text, whatever
- **Multi-line input:** End a line with `\` to continue typing
- **Remember conversations:** It keeps context throughout your session
- **Works offline:** Zero internet required once set up

## Dev Notes

- The model file is not included in this repository due to its size (3GB). You'll need to download it separately as described above.
- <create virtual environment (recommended):
   ```bash
   python -m venv venv
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   venv\Scripts\activate  # on Windows
   ```
- future: pyinstaller --onedir --name "FlashDriveLLM" app/main.py
