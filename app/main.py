from llama_cpp import Llama
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

if __name__ == "__main__":
    model_path = check_model_exists()

    # suppress verbose loading output and configure for Phi-4
    llm = Llama(
        model_path=model_path,
        verbose=False,
        n_ctx=16384  # ~2.5GB RAM usage for context
        # n_batch=512 (in batches for efficiency)
    )

    print("LLM loaded successfully! Type 'exit' or 'quit' to end.\n")

    while True:
        prompt = input("You: ")
        if prompt.lower() in {"exit", "quit"}:
            break
        
        formatted_prompt = f"<|user|>{prompt}<|end|><|assistant|>"
        
        output = llm(
            formatted_prompt, 
            max_tokens=150,
            stop=["<|end|>", "<|user|>"],
            temperature=0.7
        )
        
        response = output["choices"][0]["text"].strip()
        print("LLM:", response)


