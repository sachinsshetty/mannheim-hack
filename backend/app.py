from flask import Flask, jsonify, request
from flask_cors import CORS
from engine import execute_prompt, bundle_function, propose_recipes, get_json_objects, compute_reduced_prices
import json
app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

@app.route('/execute_prompt', methods=['POST'])
def execute_prompt_route():
    data = request.get_json()
    prompt = data.get('prompt')
    result = execute_prompt(prompt)
    return jsonify(result)

@app.route('/recipe_generate', methods=['GET'])
def bundle_articles_route():
    print('started function call')
    try:
        json_objs = compute_reduced_prices()
        obj= json.loads(json_objs)
        print(obj[:10])
        bundle_articles = bundle_function(obj[:10])
        result = execute_prompt(propose_recipes(bundle_articles))
    except FileNotFoundError:
        print("The file 'articles.json' was not found.")
    except json.JSONDecodeError:
        print("The file 'articles.json' is not a valid JSON file.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')