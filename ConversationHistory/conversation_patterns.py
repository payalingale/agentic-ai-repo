import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.environ.get('API_KEY'))

conversation = []

def add_message(role, content):
    """Helper to add messages"""
    conversation.append({'role': role, 'content': content})

def count_tokens_estimate():
    """Rough token estimate"""
    total_chars = 0
    for msg in conversation:
        if isinstance(msg['content'], str):
            total_chars += len(msg['content'])
    return total_chars // 4  # Rough estimate

# Simulate a LONG conversation
print("Simulating long conversation...\n")

add_message('user', 'My favorite color is blue')
add_message('assistant', 'Got it! Blue is your favorite color.')

add_message('user', 'I like pizza')
add_message('assistant', 'Pizza is delicious!')

add_message('user', 'I work as a developer')
add_message('assistant', 'That\'s great! What kind of development?')

# Add 20 more exchanges (simulate chat history)
for i in range(20):
    add_message('user', f'This is user message {i}')
    add_message('assistant', f'This is assistant response {i}')

print(f"📊 Conversation has {len(conversation)} messages")
print(f"📊 Estimated tokens: ~{count_tokens_estimate()}")

# Now ask a question about something from the beginning
add_message('user', 'What is my favorite color?')

response = client.messages.create(
    model='claude-sonnet-4-20250514',
    max_tokens=500,
    messages=conversation
)

answer = response.content[0].text
print(f"\n🤖 Claude's answer: {answer}")

# Check actual usage
print(f"\n📊 Actual input tokens used: {response.usage.input_tokens}")
print(f"📊 Output tokens: {response.usage.output_tokens}")