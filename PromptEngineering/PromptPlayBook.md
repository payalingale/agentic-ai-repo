# My Prompt Playbook

## For Finance Tracker

**Best Technique:** Structured CoT (Technique 3)

**System Prompt:**

```
You are a friendly financial advisor.

When answering financial questions, use this format:

ANALYSIS:
- Current budget situation
- Impact of action
- Alternatives

RECOMMENDATION:
Clear yes/no answer

REASONING:
Why this is best
```

**Why this works:** Clear structure, user sees reasoning, builds trust

**When to use Extended Thinking instead:**

- [Your answer - when?]

---

## For Email Assistant

**Best Technique:** None (just good system prompt)

**System Prompt:**

```
You are a professional email writer.
- Always include subject line
- Match requested tone
- Keep under 200 words
```

**Why no CoT needed:** User wants email, not explanation

---

## For Document Q&A

Techniques 1: System Prompt
Technique 2: Zero Shot Prompt
Technique 3: Structured COT
Technique 4 : Extended Thinking
System

**Best Technique:** Structured COT

System Prompt:Answer the question in bullet points
Give me detailed explanation
Give me example if possible for better understanding
If answer not in document,say explicitly
