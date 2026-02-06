import requests
import json

def test_chat_api():
    base_url = 'http://localhost:8000/api/1/chat'

    # Test messages
    test_messages = [
        "add a task to buy groceries",
        "show my tasks",
        "add a task to finish homework",
        "show my tasks",
        "mark task 1 as complete",
        "show my tasks",
        "delete task 2"
    ]

    conversation_id = None

    for message in test_messages:
        data = {
            'message': message
        }
        if conversation_id:
            data['conversation_id'] = conversation_id

        try:
            response = requests.post(base_url, json=data)
            print(f"\nMessage: '{message}'")
            print(f"Status Code: {response.status_code}")

            if response.status_code == 200:
                result = response.json()
                print(f"Response: {result['response']}")
                if 'conversation_id' in result:
                    conversation_id = result['conversation_id']
            else:
                print(f"Error: {response.text}")

        except Exception as e:
            print(f"Error sending request: {e}")

if __name__ == "__main__":
    test_chat_api()
