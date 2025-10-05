from strands import Agent
from strands.agent.conversation_manager import SlidingWindowConversationManager
import json

# Create a conversation manager with custom window size
# By default, SlidingWindowConversationManager is used even if not specified
conversation_manager = SlidingWindowConversationManager(
    window_size=10,  # Maximum number of message pairs to keep
)

initial_messages = [
    {"role": "user", "content": [{"text": "Hello, my name is Strands!"}]},
    {"role": "assistant", "content": [{"text": "Hi there! How can I help you today?"}]}
]

# Use the conversation manager with your agent
agent = Agent(messages=initial_messages, conversation_manager=conversation_manager)

print("\nCall Agent:")
agent("What is my name?")

# Access the conversation history
print("\n\nMessge History:")
#print(agent.messages)  # Shows all messages exchanged so far
print(json.dumps(agent.messages, indent=2))