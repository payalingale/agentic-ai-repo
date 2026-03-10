import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.environ.get('API_KEY'))

class ImportanceMemory:
    def __init__(self, max_messages=20):
        self.messages = []
        self.max_messages = max_messages
        self.important_keywords = ['error', 'problem', 'issue', 'important', 'critical', 'name', 'payal']
    
    def add_message(self, role, content):
        # Mark importance
        is_important = any(keyword in content.lower() for keyword in self.important_keywords)
        
        self.messages.append({
            'role': role,
            'content': content,
            'important': is_important,
            'timestamp': len(self.messages)
        })
        
        # Prune if needed
        if len(self.messages) > self.max_messages:
            self._prune_messages()
    
    def _prune_messages(self):
        # Keep all important messages
        important = [msg for msg in self.messages if msg.get('important', False)]  # ← FIXED: use .get()
        
        # Keep recent messages
        recent = self.messages[-10:]
        
        # Combine (remove duplicates by position)
        kept_indices = set()
        kept = []
        
        # Add important messages
        for i, msg in enumerate(self.messages):
            if msg.get('important', False):
                kept_indices.add(i)
                kept.append(msg)
        
        # Add recent messages
        for i in range(max(0, len(self.messages) - 10), len(self.messages)):
            if i not in kept_indices:
                kept.append(self.messages[i])
        
        # Sort by original order
        kept.sort(key=lambda x: x['timestamp'])
        self.messages = kept[-self.max_messages:]
    
    def get_history(self):
        return [{'role': msg['role'], 'content': msg['content']} for msg in self.messages]

if __name__ == "__main__":
    memory = ImportanceMemory(max_messages=8)

memory.add_message('user', 'My name is Payal')  # ← 'name' keyword = important!
memory.add_message('assistant', 'Nice to meet you!')

memory.add_message('user', 'I like AI')
memory.add_message('assistant', 'Cool!')

memory.add_message('user', 'I work as a developer')
memory.add_message('assistant', 'Great!')

memory.add_message('user', 'I live in Abu Dhabi')
memory.add_message('assistant', 'Wonderful!')

memory.add_message('user', 'The weather is nice')
memory.add_message('assistant', 'Indeed!')

# Now we have 10 messages, max is 8
# Should prune, but keep message 1 (has 'name')

print(f"📊 Messages in memory: {len(memory.get_history())}")

memory.add_message('user', 'What is my name?')

response = client.messages.create(
    model='claude-sonnet-4-20250514',
    max_tokens=500,
    messages=memory.get_history()
)

print(f"\n🤖 Claude: {response.content[0].text}")