
MAX_EXCHANGES = 40

class MemoryState:
    def __init__(self, max_exchanges=MAX_EXCHANGES):
        self.history = []
        self.max_exchanges = max_exchanges
    
    def add_exchange(self, user_msg, assistant_msg):
        self.history.append((user_msg, assistant_msg))
        if len(self.history) > self.max_exchanges:
            self.history.pop(0)
    
    def build_prompt(self, new_msg):
        prompt = ""
        for user_msg, assistant_msg in self.history:
            prompt += f"<|user|>{user_msg}<|end|><|assistant|>{assistant_msg}<|end|>"
        prompt += f"<|user|>{new_msg}<|end|><|assistant|>"
        return prompt