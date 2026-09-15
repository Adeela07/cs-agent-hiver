from agent import handle_message
import json

test_messages = [
    "how do I check my iOS version?",
    "Apple Pay isn't showing up in my wallet, I need this fixed now",
    "my battery drains so fast since the update, this is ridiculous"
]

for msg in test_messages:
    result = handle_message(msg)
    print(json.dumps(result, indent=2))
    print("---")