from llama_cpp import Llama
from MemoryState import MemoryState

import os
import sys

DOWNLOAD_LINK = "https://huggingface.co/bartowski/microsoft_Phi-4-mini-instruct-GGUF/blob/main/microsoft_Phi-4-mini-instruct-Q6_K_L.gguf"
MODEL_NAME = "microsoft_Phi-4-mini-instruct-Q6_K_L.gguf"

def check_model_exists():
    model_path = os.path.join("llm_model", MODEL_NAME)
    
    if not os.path.exists(model_path):
        print("Model file not found!")
        print(f"Expected location: {model_path}")
        print("\nPlease download the model:")
        print("1. Download a .gguf LLM model")
        print(f"    -> Download link for Microsoft phi4mini:\n    {DOWNLOAD_LINK}\n")
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

if __name__ == "__main__":
    model_path = check_model_exists()

    # suppress verbose loading output and configure for Phi-4
    llm = Llama(
        model_path=model_path,
        verbose=False,
        n_ctx=16384,  # ~2.5GB RAM usage for context
        n_batch=512 # (proccess in batches for efficiency)
    )

    print("Flash Drive LLM loaded successfully!")
    print("Your offline internet is ready. Type '/help' for commands.\n")

    memory = MemoryState()

    while True:
        prompt = get_input()
        
        if prompt.lower() in {"/exit", "/quit"}:
            break
            
        # Handle special commands
        cmd = handle_commands(prompt)
        if cmd == "clear":
            memory = MemoryState()
            print("Conversation cleared.\n")
            continue
        elif cmd in ["/help"]:
            continue
            
        if not prompt.strip():
            continue
        
        formatted_prompt = memory.build_prompt(prompt)
        
        output = llm(
            formatted_prompt, 
            max_tokens=1000, 
            stop=["<|end|>", "<|user|>"],
            temperature=0.7
        )
        
        response = output["choices"][0]["text"].strip()
        print(f"\nLLM: {response}\n")

        memory.add_exchange(prompt, response)


