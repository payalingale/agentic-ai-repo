import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.environ.get('API_KEY'))

def test_no_system():
    """Without system prompt"""
    response = client.messages.create(
        model='claude-sonnet-4-20250514',
        max_tokens=500,
        messages=[
            {'role': 'user', 'content': 'Explain what Python is'}
        ]
    )
    return response.content[0].text

def test_with_system():
    """With system prompt"""
    response = client.messages.create(
        model='claude-sonnet-4-20250514',
        max_tokens=500,
        system="You are a concise teacher. Always use bullet points. Never use more than 3 sentences total.",
        messages=[
            {'role': 'user', 'content': 'Explain what Python is'}
        ]
    )
    return response.content[0].text

# Test both
print("="*60)
print("TEST 1: NO SYSTEM PROMPT")
print("="*60)
response1 = test_no_system()
print(response1)

print("\n" + "="*60)
print("TEST 2: WITH SYSTEM PROMPT")
print("="*60)
response2 = test_with_system()
print(response2)