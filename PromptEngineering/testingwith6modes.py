import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.environ.get('API_KEY'))

# TEST 1 & 2: With vs Without System
def test_no_system():
    response = client.messages.create(
        model='claude-sonnet-4-20250514',
        max_tokens=500,
        messages=[{'role': 'user', 'content': 'Explain what Python is'}]
    )
    return response.content[0].text

def test_with_system():
    response = client.messages.create(
        model='claude-sonnet-4-20250514',
        max_tokens=500,
        system="You are a concise teacher. Always use bullet points. Never use more than 3 sentences total.",
        messages=[{'role': 'user', 'content': 'Explain what Python is'}]
    )
    return response.content[0].text

# TEST 3 & 4: Expert vs Beginner (Different Personalities)
def test_expert():
    response = client.messages.create(
        model='claude-sonnet-4-20250514',
        max_tokens=500,
        system="You are a senior software engineer with 15 years experience. Use technical jargon. Be direct and assume the user knows programming.",
        messages=[{'role': 'user', 'content': 'Explain what Python is'}]
    )
    return response.content[0].text

def test_beginner():
    response = client.messages.create(
        model='claude-sonnet-4-20250514',
        max_tokens=500,
        system="You are teaching a 10-year-old child who has never programmed. Use simple words. Use analogies. Be encouraging.",
        messages=[{'role': 'user', 'content': 'Explain what Python is'}]
    )
    return response.content[0].text

# TEST 5 & 6: Format Control (JSON and Table)
def test_json_format():
    response = client.messages.create(
        model='claude-sonnet-4-20250514',
        max_tokens=500,
        system='Always respond in valid JSON format. Use this structure: {"answer": "...", "confidence": "high/medium/low"}',
        messages=[{'role': 'user', 'content': 'Is Python good for beginners?'}]
    )
    return response.content[0].text

def test_table_format():
    response = client.messages.create(
        model='claude-sonnet-4-20250514',
        max_tokens=500,
        system="Always respond in markdown table format. Use columns: Feature | Description | Example",
        messages=[{'role': 'user', 'content': 'What are Python features?'}]
    )
    return response.content[0].text

# RUN ALL TESTS
print("="*60)
print("TEST 1: NO SYSTEM PROMPT")
print("="*60)
print(test_no_system())

print("\n" + "="*60)
print("TEST 2: WITH SYSTEM PROMPT (Concise + Bullets)")
print("="*60)
print(test_with_system())

print("\n" + "="*60)
print("TEST 3: EXPERT MODE")
print("="*60)
print(test_expert())

print("\n" + "="*60)
print("TEST 4: BEGINNER MODE")
print("="*60)
print(test_beginner())

print("\n" + "="*60)
print("TEST 5: JSON FORMAT")
print("="*60)
print(test_json_format())

print("\n" + "="*60)
print("TEST 6: TABLE FORMAT")
print("="*60)
print(test_table_format())