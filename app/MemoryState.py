
MAX_EXCHANGES = 40

class MemoryState:
    def __init__(self, system_prompt="", max_exchanges=MAX_EXCHANGES):
        self.system_prompt = system_prompt
        self.history = []
        self.max_exchanges = max_exchanges
    
    def add_exchange(self, user_msg, assistant_msg):
        self.history.append((user_msg, assistant_msg))
        if len(self.history) > self.max_exchanges:
            self.history.pop(0)
    
    def build_prompt(self, new_msg):
        # start with the system prompt if it exists
        if self.system_prompt:
            prompt = f"<|system|>\n{self.system_prompt}<|end|>\n"
        else:
            prompt = ""

        # add past exchanges
        for user_msg, assistant_msg in self.history:
            prompt += f"<|user|>\n{user_msg}<|end|>\n<|assistant|>\n{assistant_msg}<|end|>\n"
            
        # add the new user message
        prompt += f"<|user|>\n{new_msg}<|end|>\n<|assistant|>"
        return prompt