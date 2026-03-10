import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.environ.get('API_KEY'))

class SlidingWindowMemory:
    def __init__(self, window_size=10):
        self.messages = []
        self.window_size = window_size
    
    def add_message(self, role, content):
        self.messages.append({'role': role, 'content': content})
        
        # Keep only last N messages
        if len(self.messages) > self.window_size:
            self.messages = self.messages[-self.window_size:]
    
    def get_history(self):
        return self.messages
    

# Your choice: SlidingWindowMemory, SummarizingMemory, or ImportanceMemory

memory = SlidingWindowMemory(window_size=6)  # Example

# Simulate conversation
memory.add_message('user', 'My name is Payal')
memory.add_message('assistant', 'Nice to meet you, Payal!')

memory.add_message('user', 'I like AI')
memory.add_message('assistant', 'AI is fascinating!')

memory.add_message('user', 'I work as a developer')
memory.add_message('assistant', 'Great!')

memory.add_message('user', 'I live in Abu Dhabi')
memory.add_message('assistant', 'Wonderful city!')

# Now with window=6, old messages should be gone
print(f"Messages in memory: {len(memory.get_history())}")

# Ask about something from the beginning
memory.add_message('user', 'What is my name?')

response = client.messages.create(
    model='claude-sonnet-4-20250514',
    max_tokens=500,
    messages=memory.get_history()
)

print(response.content[0].text)
