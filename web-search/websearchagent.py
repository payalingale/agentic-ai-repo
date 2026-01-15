from serpapi import GoogleSearch
import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

serpApi_key = os.environ.get('SERP_API_KEY')
api_key = os.environ.get('API_KEY')
client = anthropic.Anthropic(api_key=api_key)  # ← Fixed!

# ============================================
# TOOL IMPLEMENTATIONS
# ============================================

def web_search(query):
    """Search Google using SerpAPI"""
    try:
        print(f"🔍 Searching: {query}")
        
        params = {
            'q': query,
            'api_key': serpApi_key,
            'num': 5
        }
        
        search = GoogleSearch(params)
        results = search.get_dict()
        
        organic_results = results.get('organic_results', [])
        
        formatted_results = []
        for result in organic_results[:5]:
            formatted_results.append({
                'title': result.get('title', ''),
                'link': result.get('link', ''),
                'snippet': result.get('snippet', '')
            })
        
        print(f"✅ Found {len(formatted_results)} results\n")
        return {"results": formatted_results}
        
    except Exception as e:
        return {"error": str(e)}

def calculator(data):
    """Calculate mathematical expressions"""
    try:
        print(f"🔢 Calculating: {data}")
        import math
        allowed = {
            '__builtins__': None,
            'sqrt': math.sqrt,
            'pow': pow,
            'abs': abs
        }
        result = eval(data, allowed)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

def python_executor(code):
    """Execute Python code"""
    try:
        print(f"💻 Executing Python code...")
        from io import StringIO
        import sys
        
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        exec(code)
        
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        
        return {"output": output if output else "Code executed successfully"}
    except Exception as e:
        sys.stdout = old_stdout
        return {"error": str(e)}

def wikipedia_search(keyword):
    """Search Wikipedia"""
    try:
        print(f"📚 Searching Wikipedia: {keyword}")
        import wikipedia
        summary = wikipedia.summary(keyword, sentences=2)
        return {"summary": summary}
    except Exception as e:
        return {"error": str(e)}

# ============================================
# TOOL DISPATCHER
# ============================================

def process_tool(tool_name, tool_input):
    """Execute the appropriate tool"""
    if tool_name == "web_search":  # ← Match your tool name
        return web_search(tool_input["query"])
    elif tool_name == "calculate":
        return calculator(tool_input["data"])
    elif tool_name == "PythonComplier":
        return python_executor(tool_input["code"])
    elif tool_name == "Search":
        return wikipedia_search(tool_input["keyword"])
    else:
        return {"error": f"Unknown tool: {tool_name}"}

# ============================================
# TOOL DEFINITIONS
# ============================================

tools = [
    {
        'name': 'web_search',  # ← Use underscore, not hyphen
        'description': 'Search Google for current information using SerpAPI',
        'input_schema': {
            'type': 'object',
            'properties': {
                'query': {
                    'type': 'string',
                    'description': 'Search query (e.g., "latest AI news 2026")'
                }
            },
            'required': ['query']
        }
    },
    {
        "name": "calculate",
        "description": "Evaluate mathematical expressions",
        "input_schema": {
            "type": "object",
            "properties": {
                "data": {
                    "type": "string",
                    "description": "Math expression to evaluate"
                }
            },
            "required": ["data"]
        }
    },
    {
        "name": "PythonComplier",
        "description": "Execute Python code and return output",
        "input_schema": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Python code to execute"
                }
            },
            "required": ["code"]
        }
    },
    {
        "name": "Search",
        "description": "Search Wikipedia for information",
        "input_schema": {
            "type": "object",
            "properties": {
                "keyword": {
                    "type": "string",
                    "description": "Wikipedia search query"
                }
            },
            "required": ["keyword"]
        }
    }
]

# ============================================
# AGENT WITH TOOL USE LOOP
# ============================================

def web_search_agent(question):
    """Agent that can use all 4 tools"""
    
    conversation_history = [
        {"role": "user", "content": question}
    ]
    
    thinking_text = None
    tools_used = []
    
    # Loop until final answer
    while True:
        response = client.messages.create(
            max_tokens=6000,
            thinking={
                'type': 'enabled',
                'budget_tokens': 5000
            },
            model='claude-sonnet-4-20250514',
            tools=tools,
            messages=conversation_history
        )
        
        # Extract thinking
        for block in response.content:
            if block.type == "thinking" and thinking_text is None:
                thinking_text = block.thinking
        
        # Check if Claude wants to use a tool
        if response.stop_reason == "tool_use":
            print("\n🔧 Claude is using a tool...\n")
            
            # Process all tool use blocks
            for block in response.content:
                if block.type == "tool_use":
                    tool_name = block.name
                    tool_input = block.input
                    tool_id = block.id
                    
                    tools_used.append(tool_name)
                    
                    print(f"Tool: {tool_name}")
                    print(f"Input: {tool_input}")
                    
                    # ⭐ EXECUTE THE TOOL ⭐
                    tool_result = process_tool(tool_name, tool_input)
                    
                    print(f"Result: {tool_result}\n")
                    
                    # Add assistant response to history
                    conversation_history.append({
                        "role": "assistant",
                        "content": response.content
                    })
                    
                    # Add tool result to history
                    conversation_history.append({
                        "role": "user",
                        "content": [{
                            "type": "tool_result",
                            "tool_use_id": tool_id,
                            "content": str(tool_result)
                        }]
                    })
            
            # Continue loop
            continue
        
        # No tool use - extract final text
        final_text = ""
        for block in response.content:
            if block.type == "text":
                final_text += block.text
        
        return {
            "thinking": thinking_text,
            "tools_used": tools_used,
            "response": final_text
        }

# ============================================
# MAIN PROGRAM
# ============================================

print("🌐 Web Search Agent with 4 Tools!")
print("Tools: Web Search (Google), Calculator, Python Executor, Wikipedia")
print("Type 'quit' to exit\n")

while True:
    question = input("You: ").strip()
    
    if question.lower() in ['quit', 'exit']:
        print("👋 Goodbye!")
        break
    
    if not question:
        continue
    
    try:
        result = web_search_agent(question)
        
        # Display results
        if result["thinking"]:
            print(f"\n💭 Thinking: {result['thinking'][:200]}...\n")
        
        if result["tools_used"]:
            print(f"🔧 Tools used: {', '.join(result['tools_used'])}\n")
        
        print(f"Claude: {result['response']}\n")
        print("-" * 60 + "\n")
        
    except Exception as e:
        print(f"❌ Error: {e}\n")
