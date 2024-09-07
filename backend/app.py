from flask import Flask, jsonify, request
from flask_cors import CORS
from engine import execute_prompt, bundle_function, propose_recipes, get_json_objects, price_reduction

app = Flask(__name__)
CORS(app)

@app.route('/execute_prompt', methods=['POST'])
def execute_prompt_route():
    data = request.get_json()
    prompt = data.get('prompt')
    result = execute_prompt(prompt)
    return jsonify(result)

@app.route('/recipe_generate', methods=['GET'])
def bundle_articles_route():
    print('started function call')
    articles = get_json_objects()
    bundle_articles = bundle_function(articles)
    result = execute_prompt(propose_recipes(bundle_articles))
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')