import os
import anthropic
from dotenv import load_dotenv
import PyPDF2

load_dotenv()
api_key = os.environ.get('API_KEY')
client = anthropic.Anthropic(api_key=api_key)

# Global variable to store document content
DOCUMENT_CONTENT = None

# Tool definition
tools = [
    {
        'name': 'search_document',
        'description': 'Search the loaded document for information. Returns relevant sentences from the document.',
        'input_schema': {
            'type': 'object',
            'properties': {
                'query': {
                    'type': 'string',
                    'description': 'What to search for in the document'
                }
            },
            'required': ['query']
        }
    }
]

STOP_WORDS = {
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
    'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
    'to', 'was', 'will', 'with', 'this', 'but', 'they', 'have',
    'had', 'what', 'when', 'where', 'who', 'which', 'why', 'how',
    'all', 'tell', 'me', 'about', '?', '!'
}

# ============================================
# HELPER FUNCTIONS
# ============================================

def load_pdf(filepath):
    """Extract text from PDF file"""
    try:
        text = ""
        with open(filepath, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            num_pages = len(pdf_reader.pages)
            
            print(f"📄 Reading PDF: {num_pages} pages...")
            
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
        
        return text
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        return None

def load_document(filepath):
    """Load document from filepath (supports TXT and PDF)"""
    try:
        if not os.path.exists(filepath):
            print(f'❌ File not found: {filepath}')
            return None
        
        # Check file extension
        file_ext = filepath.lower().split('.')[-1]
        
        if file_ext == 'pdf':
            return load_pdf(filepath)
        elif file_ext in ['txt', 'md']:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            print(f"❌ Unsupported file type: .{file_ext}")
            print("   Supported: .txt, .pdf, .md")
            return None
            
    except Exception as e:
        print(f'❌ Error: {e}')
        return None

def get_stats(content):
    """Display document statistics"""
    if not content:
        return
    
    print(f'   - Characters: {len(content):,}')
    print(f'   - Words: {len(content.split())}')
    print(f'   - Lines: {len(content.splitlines())}')

def split_into_sentences(content):
    """Split content into sentences"""
    if not content:
        return []
    
    sentences = []
    for sentence in content.split('.'):
        cleaned = sentence.strip()
        if cleaned:
            sentences.append(cleaned.lower())
    return sentences

def extract_keywords(query):
    """Extract keywords from query, removing stop words"""
    if not query:
        return []
    
    words = query.lower().split()
    keywords = []
    
    for word in words:
        # Remove punctuation
        word = word.strip('.,!?;:')
        # Keep if not a stop word
        if word and word not in STOP_WORDS:
            keywords.append(word)
    
    # If all words were stop words, use original
    if not keywords:
        keywords = [w.strip('.,!?;:') for w in words if w]
    
    return keywords

def search_in_sentences(sentences, keywords):
    """Find sentences containing any keywords"""
    if not sentences or not keywords:
        return []
    
    matches = []
    for sentence in sentences:
        for keyword in keywords:
            if keyword in sentence:
                # Capitalize first letter for display
                formatted = sentence[0].upper() + sentence[1:] if sentence else sentence
                matches.append(formatted)
                break  # Found a match, move to next sentence
    
    return matches

# ============================================
# TOOL IMPLEMENTATION
# ============================================

def tool_search_document(query):
    """
    Tool implementation - searches document and returns results
    Claude calls this through the API
    """
    if not DOCUMENT_CONTENT:
        return {"error": "No document loaded"}
    
    # Split into sentences
    sentences = split_into_sentences(DOCUMENT_CONTENT)
    
    # Extract keywords
    keywords = extract_keywords(query)
    
    # Search for matches
    matches = search_in_sentences(sentences, keywords)
    
    if matches:
        # Return top 5 matches
        result = "\n".join(matches[:5])
        return {
            "results": result,
            "num_matches": len(matches),
            "keywords_used": keywords
        }
    else:
        return {
            "results": "No relevant information found",
            "num_matches": 0
        }

# ============================================
# AI INTEGRATION
# ============================================

def ask_claude(question):
    """
    Ask Claude to answer a question using the document
    """
    conversation_history = [
        {
            "role": "user",
            "content": f"Based on the document, please answer this question: {question}"
        }
    ]
    
    print("🤖 AI is analyzing...")
    
    while True:
        response = client.messages.create(
            model='claude-sonnet-4-20250514',
            max_tokens=2048,
            tools=tools,
            messages=conversation_history
        )
        
        # Check if Claude wants to use the tool
        if response.stop_reason == 'tool_use':
            # Extract tool call
            for block in response.content:
                if block.type == "tool_use":
                    tool_name = block.name
                    tool_input = block.input
                    tool_id = block.id
                    
                    print(f"🔍 Searching: '{tool_input['query']}'")
                    
                    # Execute the tool
                    if tool_name == "search_document":
                        tool_result = tool_search_document(tool_input['query'])
                    else:
                        tool_result = {"error": "Unknown tool"}
                    
                    print(f"   Found {tool_result.get('num_matches', 0)} matches")
                    
                    # Add to conversation
                    conversation_history.append({
                        "role": "assistant",
                        "content": response.content
                    })
                    conversation_history.append({
                        "role": "user",
                        "content": [{
                            "type": "tool_result",
                            "tool_use_id": tool_id,
                            "content": str(tool_result)
                        }]
                    })
            
            continue  # Keep looping
        
        # Extract final answer
        final_answer = ""
        for block in response.content:
            if block.type == "text":
                final_answer += block.text
        
        return final_answer

# ============================================
# MAIN PROGRAM
# ============================================

def main():
    global DOCUMENT_CONTENT
    
    print("📄 Document Q&A Agent with AI\n")
    
    # Load document
    filepath = input("Enter document path: ").strip()
    content = load_document(filepath)
    
    if not content:
        print("\n❌ Failed to load document.")
        return
    
    # Store in global variable
    DOCUMENT_CONTENT = content
    
    # Show stats
    print("\n✅ Document loaded successfully!")
    print("📊 Stats:")
    get_stats(content)
    print("\n✅ Ready for AI-powered questions! (Type 'quit' to exit)\n")
    
    # Q&A Loop with AI
    while True:
        print("-" * 50)
        question = input("\nYou: ").strip()
        
        if question.lower() in ['quit', 'exit', 'bye']:
            print("\n👋 Goodbye!")
            break
        
        if not question:
            continue
        
        try:
            answer = ask_claude(question)
            print(f"\n🤖 Answer:\n{answer}\n")
        except Exception as e:
            print(f"\n❌ Error: {e}\n")

if __name__ == '__main__':
    main()