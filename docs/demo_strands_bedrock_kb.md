What This Demo Does
This agent demonstrates multi-tool orchestration using the Strands framework. The agent intelligently decides which tools to use based on the user's question.

Available Tools
1. current_time()
Returns the current date and time in format: YYYY-MM-DD HH:MM:SS

When used:

User asks about current time/date
User needs timestamp information
2. retrieve_from_knowledge_base(query: str)
Searches your Bedrock Knowledge Base and returns top 5 relevant results with relevance scores.

Parameters:

query: Search text to find relevant documents
Returns:

Formatted results with relevance scores (0.00 to 1.00)
Each result shows: [Relevance: X.XX] content text
Configuration:

numberOfResults: 5 - Returns top 5 matches (adjustable in code)
Uses vector search for semantic matching
Usage Examples
Basic Usage
python demo_strands_bedrock_kb.py "your question here"

Single Tool - Time
python demo_strands_bedrock_kb.py "What time is it?"

Agent behavior:

Recognizes time-related query
Calls current_time() tool
Returns formatted timestamp
Single Tool - Knowledge Base
python demo_strands_bedrock_kb.py "What does the knowledge base say about AWS security?"

Agent behavior:

Recognizes information retrieval need
Calls retrieve_from_knowledge_base() with query
Returns top 5 relevant results with scores
Multiple Tools
python demo_strands_bedrock_kb.py "What is the current time and what information do you have about machine learning?"

Agent behavior:

Identifies two separate requests
Calls current_time() first
Then calls retrieve_from_knowledge_base() with ML query
Combines both results in response
Complex Query
python demo_strands_bedrock_kb.py "Search the knowledge base for data privacy policies and tell me what time this search was performed"

Agent behavior:

Understands compound request
Retrieves KB information about data privacy
Gets current timestamp
Provides comprehensive answer with both pieces of information
How It Works
Agent Architecture
User Question
     ↓
Agent (Claude Sonnet 4)
     ↓
Tool Selection Logic
     ↓
┌────────────────┬──────────────────────┐
│                │                      │
current_time()   retrieve_from_kb()    Both Tools
     ↓                ↓                     ↓
Returns time    Searches KB          Sequential calls
     ↓                ↓                     ↓
     └────────────────┴─────────────────────┘
                      ↓
              Formatted Response

System Prompt
The agent is configured with this system prompt:

You are a helpful assistant with access to two tools:
1. current_time - to get the current date and time
2. retrieve_from_knowledge_base - to search for information in the knowledge base

Use these tools when appropriate to answer user questions accurately.

This prompt guides the agent to:

Understand available tools
Know when to use each tool
Combine tool results effectively
Model Configuration
BedrockModel(
    model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
    region_name="us-east-1",
    temperature=0.3,  # Lower = more focused/deterministic
)

Temperature 0.3 means:

More consistent, predictable responses
Less creative/random output
Better for factual information retrieval
Knowledge Base Retrieval
The retrieve_from_knowledge_base() tool:

Sends query to Bedrock Knowledge Base
Vector search finds semantically similar content
Returns top 5 results ranked by relevance
Formats output with scores for transparency
Relevance scores:

0.90-1.00: Highly relevant
0.70-0.89: Moderately relevant
0.50-0.69: Somewhat relevant
< 0.50: Low relevance
Key Concepts
Tool Decorator
@tool
def current_time() -> str:
    """
    Get the current date and time.

    Returns:
        str: Current date and time in a readable format
    """

The @tool decorator:

Registers function as an agent tool
Uses docstring to help agent understand tool purpose
Type hints guide input/output expectations
Agent Decision Making
The agent uses the system prompt and tool docstrings to decide:

Which tool(s) to call
What parameters to pass
How to combine results
Example decision flow:

Question: "What time is it?"
→ Agent reads: "current_time - to get the current date and time"
→ Matches intent with tool description
→ Calls current_time()
→ Returns result

Error Handling
try:
    response = bedrock_agent_runtime.retrieve(...)
    # Process results
except Exception as e:
    return f"Error retrieving from knowledge base: {str(e)}"

Graceful error handling ensures:

Agent continues even if KB is unavailable
User gets informative error messages
Application doesn't crash
Customization
Adjust Number of Results
Change line 46:

'numberOfResults': 10  # Get more results

Change Model Temperature
Line 68:

temperature=0.7,  # Higher = more creative responses

Modify System Prompt
Lines 74-79 - customize for your domain:

system_prompt="""You are a technical documentation assistant.
Always search the knowledge base first before answering.
Provide code examples when relevant."""

Add Custom Tools
@tool
def search_web(query: str) -> str:
    """Search the web for current information."""
    # Implementation
    return results

agent = Agent(
    model=bedrock_model,
    tools=[current_time, retrieve_from_knowledge_base, search_web]
)

Output Format
============================================================
Bedrock Knowledge Base Agent
============================================================

Model Config: {'model_id': 'us.anthropic.claude-sonnet-4...', ...}

Question: What time is it and what's in the KB about AWS?

------------------------------------------------------------

Response: The current time is 2025-03-10 15:30:45.

Based on the knowledge base, here's information about AWS:

[Relevance: 0.92] AWS (Amazon Web Services) is a comprehensive cloud...
[Relevance: 0.88] Key AWS services include EC2 for compute...