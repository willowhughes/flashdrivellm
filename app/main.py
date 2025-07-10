from llama_cpp import Llama
from MemoryState import MemoryState
import os
import sys
import json

def get_config_path():
    # use the folder where the exe is located
    if getattr(sys, 'frozen', False):
        # running as a bundled exe
        base_path = os.path.dirname(sys.executable)
    else:
        # running as script
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, "config.json")

def check_model_exists():
    model_path = os.path.join("llm_model", config["model_name"])
    
    if not os.path.exists(model_path):
        print("Model file not found!")
        print(f"Expected location: {model_path}")
        print("\nPlease download the model:")
        print("1. Download a .gguf LLM model")
        print(f"    -> Download link for the model:\n    {config['download_link']}\n")
        print("2. Place it in the llm_model/ directory")
        sys.exit(1)
    
    return model_path

def get_input():
    """enhanced input with copy-paste support"""
    try:
        prompt = input("You: ")
        
        if prompt.lower() in {"/exit", "/quit"}:
            return prompt
            
        # handle multi-line continuation with backslash
        if prompt.endswith("\\"):
            lines = [prompt[:-1]]  # Remove backslash
            print("... (continue typing, empty line to finish)")
            
            while True:
                try:
                    line = input("... ")
                    if line.strip() == "":
                        break
                    lines.append(line)
                except EOFError:
                    break
                    
            return "\n".join(lines)
            
        return prompt
        
    except EOFError:
        return "exit"

def handle_commands(prompt):
    """handle special commands"""
    if prompt.lower() == "/clear":
        return "clear"
    elif prompt.lower() == "/help":
        print("""
            FLASH DRIVE LLM - Your Offline Internet

            COMMANDS:
            /help     - Show this help
            /clear    - Clear conversation history  
            /exit     - Exit program

            FEATURES:
            • Copy-paste support (paste multiple lines)
            • Multi-line input (end line with \\ to continue)
            • Conversation memory
            • Works completely offline

            ASK ME ANYTHING:
            • Programming questions & code review
            • Explanations of concepts
            • Writing assistance
            • Math & calculations
            • General knowledge
            """)
        return "/help"
    
    return None

def load_config():
    config_path = get_config_path()
    # Default config in case file is missing or incomplete
    default_config = {
        "model_name": "guanaco-7b-uncensored.Q4_K_M.gguf",
        "download_link": "https://huggingface.co/TheBloke/Guanaco-7B-Uncensored-GGUF/blob/main/guanaco-7b-uncensored.Q4_K_M.gguf",
        "intro_message": "Flash Drive LLM loaded successfully!\nYour offline internet is ready. Type 'help' for commands.\n",
        "system_prompt": "You are a helpful AI assistant.",
        "max_tokens": 600,
        "temperature": 0.7,
        "context_window": 4096,
        "llm_name": "LLM"
    }
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            user_config = json.load(f)
        # Merge user config with defaults
        config = default_config.copy()
        config.update(user_config)
        return config
    except Exception as e:
        print(f"Could not load config.json: {e}\nUsing default settings.")
        return default_config

if __name__ == "__main__":
    config = load_config()
    model_path = check_model_exists()

    # suppress verbose loading output and configure for Phi-4
    llm = Llama(
        model_path=model_path,
        verbose=False,
        n_ctx=config["context_window"],  # 16384 is ~2.5GB RAM usage for context
        n_batch=512 # (proccess in batches for efficiency)
    )

    print(config["intro_message"])

    memory = MemoryState(system_prompt=config["system_prompt"])

    while True:
        prompt = get_input()
        
        if prompt.lower() in {"/exit", "/quit"}:
            break
            
        # Handle special commands
        cmd = handle_commands(prompt)
        if cmd == "clear":
            memory = MemoryState(system_prompt=config["system_prompt"])
            print("Conversation cleared.\n")
            continue
        elif cmd in ["/help"]:
            continue
            
        if not prompt.strip():
            continue
        
        formatted_prompt = memory.build_prompt(prompt)
        prompt_tokens = len(llm.tokenize(formatted_prompt.encode("utf-8", errors="ignore")))
        
        output = llm(
            formatted_prompt, 
            max_tokens=config["max_tokens"], 
            stop=["<|end|>", "<|user|>"],
            temperature=config["temperature"]
        )
        
        response = output["choices"][0]["text"].strip()
        print(f"\n{config['llm_name']}: {response}\n")
        print(f"({prompt_tokens}/{config['context_window']} tokens used)")
        memory.add_exchange(prompt, response)



