import logging
from strands import Agent

# Enables Strands debug log level
logging.getLogger("strands").setLevel(logging.DEBUG)

# Sets the logging format and streams logs to stderr
logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler()]
)

agent = Agent()

# Agents display their reasoning and responses in real-time to the console by default. You can disable this output by setting callback_handler=None when creating your agent:

# agent = Agent(
#     tools=[calculator, current_time, letter_counter],
#     callback_handler=None,
# )

print(agent.model.config)

agent("Hello!")