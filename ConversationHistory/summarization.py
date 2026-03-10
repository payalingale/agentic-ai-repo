import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.environ.get('API_KEY'))

class SummarizingMemory:
    def __init__(self, client, summarize_after=5, keep_recent=10):
        self.client = client
        self.messages = []
        self.summary = ""
        self.summarize_after = summarize_after
        self.keep_recent = keep_recent
    
    def add_message(self, role, content):
        self.messages.append({'role': role, 'content': content})
        
        # Time to summarize?
        if len(self.messages) > self.summarize_after:
            self._summarize_old_messages()
    
    def _summarize_old_messages(self):
        # Messages to summarize
        to_summarize = self.messages[:-self.keep_recent]
        
        # Create summary prompt
        conversation_text = "\n".join([
            f"{msg['role']}: {msg['content']}" 
            for msg in to_summarize
        ])
        
        # Ask Claude to summarize
        response = self.client.messages.create(
            model='claude-sonnet-4-20250514',
            max_tokens=500,
            messages=[{
                'role': 'user',
                'content': f'Summarize this conversation in 2-3 sentences:\n\n{conversation_text}'
            }]
        )
        
        self.summary = response.content[0].text
        
        # Keep only recent messages
        self.messages = self.messages[-self.keep_recent:]
    
    def get_history(self):        # If we have a summary, prepend it
        if self.summary:
            return [
                {'role': 'user', 'content': f'Previous conversation summary: {self.summary}'}
            ] + self.messages
        return self.messages
    

# Your choice: SlidingWindowMemory, SummarizingMemory, or ImportanceMemory

memory = SummarizingMemory(client,summarize_after=20,keep_recent=10)  # Example

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