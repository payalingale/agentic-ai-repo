import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.environ.get('API_KEY'))

# Test question we'll use for all techniques
TEST_QUESTION = "I have $500 monthly budget. I spent $380. Should I buy a $200 item?"

print("="*80)
print("COT TECHNIQUE COMPARISON")
print("="*80)
print(f"\nTest Question: {TEST_QUESTION}\n")

# Technique 1: Explicit CoT in System Prompt
def test_explicit_cot():
    response = client.messages.create(
        model='claude-sonnet-4-20250514',
        max_tokens=1000,
        system="When answering, always explain your reasoning step-by-step before giving your final answer.",
        messages=[{'role': 'user', 'content': TEST_QUESTION}]
    )
    return response.content[0].text

# Technique 2: Zero-shot CoT (Magic phrase)
def test_zero_shot_cot():
    response = client.messages.create(
        model='claude-sonnet-4-20250514',
        max_tokens=1000,
        messages=[{
            'role': 'user',
            'content': f"{TEST_QUESTION} Let's think step by step."
        }]
    )
    return response.content[0].text

# Technique 3: Structured CoT
def test_structured_cot():
    response = client.messages.create(
        model='claude-sonnet-4-20250514',
        max_tokens=1000,
        system="""When answering financial questions, use this format:

ANALYSIS:
- Current situation
- Impact of purchase
- Alternatives

RECOMMENDATION:
Your clear yes/no answer

REASONING:
Why this is the best choice""",
        messages=[{'role': 'user', 'content': TEST_QUESTION}]
    )
    return response.content[0].text

# Technique 4: Extended Thinking
def test_extended_thinking():
    response = client.messages.create(
        model='claude-sonnet-4-20250514',
        max_tokens=4000,
        thinking={'type': 'enabled', 'budget_tokens': 3000},
        messages=[{'role': 'user', 'content': TEST_QUESTION}]
    )
    
    thinking = ""
    answer = ""
    
    for block in response.content:
        if block.type == 'thinking':
            thinking = block.thinking
        elif block.type == 'text':
            answer = block.text
    
    return thinking, answer

# Run all techniques
print("="*80)
print("TECHNIQUE 1: Explicit CoT (System Prompt)")
print("="*80)
result1 = test_explicit_cot()
print(result1)
print(f"\nLength: {len(result1)} characters\n")

print("="*80)
print("TECHNIQUE 2: Zero-Shot CoT ('Let's think step by step')")
print("="*80)
result2 = test_zero_shot_cot()
print(result2)
print(f"\nLength: {len(result2)} characters\n")

print("="*80)
print("TECHNIQUE 3: Structured CoT")
print("="*80)
result3 = test_structured_cot()
print(result3)
print(f"\nLength: {len(result3)} characters\n")

print("="*80)
print("TECHNIQUE 4: Extended Thinking")
print("="*80)
thinking, answer = test_extended_thinking()
print("\n--- PRIVATE THINKING (user doesn't see) ---")
print(thinking)
print(f"\nThinking length: {len(thinking)} characters")

print("\n--- PUBLIC ANSWER (user sees) ---")
print(answer)
print(f"\nAnswer length: {len(answer)} characters\n")

# Summary
print("="*80)
print("SUMMARY")
print("="*80)
print(f"Technique 1 length: {len(result1)}")
print(f"Technique 2 length: {len(result2)}")
print(f"Technique 3 length: {len(result3)}")
print(f"Technique 4 (answer only): {len(answer)}")
print(f"Technique 4 (with thinking): {len(thinking) + len(answer)}")