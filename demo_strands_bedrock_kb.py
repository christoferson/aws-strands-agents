# kb_agent.py
import sys
import boto3
from datetime import datetime
from strands import Agent, tool
from strands.models import BedrockModel

# Initialize Bedrock client
bedrock_agent_runtime = boto3.client('bedrock-agent-runtime', region_name='us-east-1')

# Your Knowledge Base ID (replace with your actual KB ID)
KNOWLEDGE_BASE_ID = "YOUR_KB_ID_HERE"

@tool
def current_time() -> str:
    """
    Get the current date and time.

    Returns:
        str: Current date and time in a readable format
    """
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S %Z")

@tool
def retrieve_from_knowledge_base(query: str) -> str:
    """
    Retrieve relevant information from the Bedrock Knowledge Base.

    Args:
        query: The search query to find relevant documents

    Returns:
        str: Retrieved context from the knowledge base
    """
    try:
        response = bedrock_agent_runtime.retrieve(
            knowledgeBaseId=KNOWLEDGE_BASE_ID,
            retrievalQuery={
                'text': query
            },
            retrievalConfiguration={
                'vectorSearchConfiguration': {
                    'numberOfResults': 5
                }
            }
        )

        # Extract and format results
        results = []
        for result in response.get('retrievalResults', []):
            content = result.get('content', {}).get('text', '')
            score = result.get('score', 0)
            results.append(f"[Relevance: {score:.2f}] {content}")

        if not results:
            return "No relevant information found in the knowledge base."

        return "\n\n".join(results)

    except Exception as e:
        return f"Error retrieving from knowledge base: {str(e)}"

# Initialize Bedrock model
bedrock_model = BedrockModel(
    model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
    region_name="us-east-1",
    temperature=0.3,
)

# Create agent with both tools
agent = Agent(
    model=bedrock_model,
    system_prompt="""You are a helpful assistant with access to two tools:
1. current_time - to get the current date and time
2. retrieve_from_knowledge_base - to search for information in the knowledge base

Use these tools when appropriate to answer user questions accurately.""",
    tools=[current_time, retrieve_from_knowledge_base]
)

def main():
    if len(sys.argv) < 2:
        print("Usage: python kb_agent.py '<your question>'")
        print("\nExample:")
        print("  python kb_agent.py 'What time is it and what information do you have about AWS?'")
        sys.exit(1)

    # Get question from CLI argument
    question = ' '.join(sys.argv[1:])

    print("=" * 60)
    print("Bedrock Knowledge Base Agent")
    print("=" * 60)
    print(f"\nModel Config: {agent.model.config}\n")
    print(f"Question: {question}\n")
    print("-" * 60)

    try:
        response = agent(question)
        print(f"\nResponse: {response}\n")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()