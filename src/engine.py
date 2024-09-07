import requests
import json

def execute_prompt():


    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "mistral",
        "prompt": "What is water made of?",
        "stream": False
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        responses = response.text.strip().split('\n')
        for resp in responses:
            try:
                result = json.loads(resp)
                print(result.get('response', ''))
            except json.JSONDecodeError:
                print(f"Error decoding JSON: {resp}")

    else:
        print(f"Error: {response.status_code}")


def main():
    execute_prompt()

if __name__ == "__main__":
    main()