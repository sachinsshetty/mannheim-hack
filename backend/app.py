from flask import Flask, jsonify, request
from engine import execute_prompt, bundle_function, propose_recipes, discount_function, get_json_objects

app = Flask(__name__)

@app.route('/execute_prompt', methods=['POST'])
def execute_prompt_route():
    data = request.get_json()
    prompt = data.get('prompt')
    print(prompt)
    result = execute_prompt(prompt)
    return jsonify(result)

@app.route('/bundle_articles', methods=['GET'])
def bundle_articles_route():
    articles = get_json_objects()
    bundle_articles = bundle_function(articles)
    return jsonify(bundle_articles)

@app.route('/propose_recipes', methods=['GET'])
def propose_recipes_route():
    articles = get_json_objects()
    bundle_articles = bundle_function(articles)
    prompt = propose_recipes(bundle_articles)
    result = execute_prompt(prompt)
    return jsonify(result)

@app.route('/discount_function', methods=['GET'])
def discount_function_route():
    result = discount_function()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
