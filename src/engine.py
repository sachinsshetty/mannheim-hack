import requests
import json

def execute_prompt(prompt):


    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "mistral",
        "prompt": prompt,
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


def json_parser(api_json):

    prompt = """
    1. State the name of the food item.
    2. Mention the expiration date to raise awareness about freshness.
    3. Describe the best storage practices to prolong shelf life.
    4. List creative ways to use the food item to encourage consumption before it spoils.
    5. Provide actionable tips for minimizing waste, such as recipes or preservation methods.
    JSON DATA = {}
    """.format(api_json)
    
    return prompt
  
def main():
    
    try:
        # Opening JSON file
        with open('../data/articles.json', 'r') as openfile:
        # Reading from json file
            json_object = json.load(openfile)

        #print(json_object)
        # Get the first 5 objects
        first_five_objects = json_object[:5]
        print(first_five_objects)
        level_1_prompt = json_parser(first_five_objects)
        print(level_1_prompt)
        execute_prompt(level_1_prompt)
    except FileNotFoundError:
        print("The file 'articles.json' was not found.")
    except json.JSONDecodeError:
        print("The file 'articles.json' is not a valid JSON file.")
    except Exception as e:
        print(f"An error occurred: {e}")
    

if __name__ == "__main__":
    main()