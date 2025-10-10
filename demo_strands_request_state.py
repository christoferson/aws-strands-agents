from strands import Agent

def custom_callback_handler(**kwargs):
    # Access request state
    if "request_state" in kwargs:
        state = kwargs["request_state"]
        # Use or modify state as needed
        if "counter" not in state:
            state["counter"] = 0
        state["counter"] += 1
        print(f"Callback handler event count: {state['counter']}")

agent = Agent(callback_handler=custom_callback_handler)
print("\n")
result = agent("Hi there!")
print("\n")
print(result.state)