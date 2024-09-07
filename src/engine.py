import random

import pandas as pd
import numpy as np
import requests
import json


def execute_prompt(prompt):


    url = "http://10.211.137.191:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {
        #"model": "mistral",
        "model": "mistral-nemo",
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


from datetime import datetime

def bundle_function(articles):
    current_date = datetime.now()
    bundle_articles = []

    for article in articles:
        demand = article.get('demand')
        stock = article.get('stock')
        expires_at_str = article.get('expiresAt')

        try:
            expires_at = datetime.strptime(expires_at_str, '%Y-%m-%d')
            days_to_expire = (expires_at - current_date).days

            #TODO change days to expire to e.g. 3 / 10
            if days_to_expire<300 or (stock > 15 and demand < 10 and days_to_expire<500):
                bundle_articles.append(article)

        except (ValueError, TypeError):
            print(f"Fehler beim Verarbeiten des Ablaufdatums für Artikel: {article.get('name', 'Unbekannt')} in bundle_function")

    return bundle_articles





def propose_recipes(bundle_articles):
    if bundle_articles:
        bundle_article_names = ', '.join([article.get('name') for article in bundle_articles])

        prompt = (
            f"Give me recipes where all these Bundle articles could be used. My goal is that all items in Bundle articles "
            f"are used in a recipe. Seperate the response in three parts. 1. Name of the recipe, 2. Ingredients for the recipe, 3. Steps in the recipe. Answer in a JSON Format"
            f"Bundle articles: {bundle_article_names}"
        )

        return prompt

    else:
        return "Tell me a joke."



def price_reduction(time_to_expiration, product_type, demand, stock):
    """ Calculate the price reduction percentage based on normalized values
    (between 0 and 1) for time to expiration, product type, demand, and stock.

    Args:
        time_to_expiration (float):
            Normalized time to expiration, 0 means expiring today, 1 means maximum time.
    product_type (float):
        Normalized product type (0 = non-perishable, 0.5 = semi-perishable, 1 = highly perishable).
    demand (float):
        Normalized demand (0 to 1), where 1 is high demand and 0 is no demand.
    stock (float):
        Normalized stock level (0 to 1), where 0 is low stock and 1 is high stock.

    Returns:
    reduction_percentage (float): Percentage of price reduction.
    """

    # Maximum discouts
    MAX_EXPIRATION = 0.05
    MAX_STOCK_DEMAND = 0.05

    if time_to_expiration > 0.5:
        return 0

    # Time to expiration: Closer to expiration means higher discount (inverted)
    # Maximum factor when time_to_expiration is 0
    expiration_factor = (1 - time_to_expiration) * MAX_EXPIRATION

    # Stock: Higher stock means higher discount
    # Demand: Lower demand should increase discount
    # Maximum factor when stock is 1 (high stock) and demand is 0 (low demand)
    stock_demand_factor = (stock - demand) * MAX_STOCK_DEMAND

    # Product type: Non-perishable (0), semi-perishable (0.5), perishable (1) impact
    # Factor ranges from 1.0 (non-perishable) to 1.4 (highly perishable)
    product_factor = 1 + (product_type * 6.0)

    # Combine all factors to calculate total reduction
    reduction_percentage = ((expiration_factor + stock_demand_factor) * product_factor)
    # Cap the discount between 0% and 80%
    return min(max(reduction_percentage * 100, 0), 80)


def compute_reduced_prices(json_file, as_json=True):
    df = pd.read_json(json_file)
    df["product_type"] = 1
    df["time_to_expiration"] = np.random.rand(len(df.index))
    df["demand"] = np.random.rand(len(df.index))
    df["stock"] = np.random.rand(len(df.index))
    df["discount"] = df.apply(lambda row: price_reduction(row['time_to_expiration'], row['product_type'], row['demand'], row['stock']), axis=1)
    df["discounted_price"] = df["price"] * (1 - df["discount"] / 100)
    return df.to_json() if as_json is True else df


def json_parser(api_json):

    explicit_prompt = """
    1. State the name of the food item.
    2. Mention the expiration date to raise awareness about freshness.
    3. Describe the best storage practices to prolong shelf life.
    4. List creative ways to use the food item to encourage consumption before it spoils.
    5. Provide actionable tips for minimizing waste, such as recipes or preservation methods.
    JSON DATA = {}
    """.format(api_json)
    

    implicit_prompt = """
    Analyse the data about food items, Lets think step by step
    JSON DATA = {}
    """.format(api_json)

    few_shot_cots = """
    JSON DATA = {}
    """.format(api_json)

    categorize_articles=  """
    Put the food into 3 categories. Long living food, middle living food, short living food.
    JSON DATA = {}
    """.format(api_json)

    return explicit_prompt
  
def get_json_objects():
    try:
        with open('../data/articles.json', 'r') as openfile:
        # Reading from json file
            json_object = json.load(openfile)


    except Exception as e:
        print(f"An error occurred: {e}")

    for article in json_object:
        article['demand'] = random.randint(1, 10)
        article['stock'] = random.randint(15, 90)


    # debug -
    first_ten_objects = json_object[:10]
    return first_ten_objects
    #return json_object 

def main():
    
    try:
        #discount_function()
        # Opening JSON file
        json_objs = get_json_objects()
        level_1_prompt = json_parser(json_objs)
        #print(level_1_prompt)
        bundle_articles = bundle_function(json_objs)
        execute_prompt(propose_recipes(bundle_articles))
    except FileNotFoundError:
        print("The file 'articles.json' was not found.")
    except json.JSONDecodeError:
        print("The file 'articles.json' is not a valid JSON file.")
    except Exception as e:
        print(f"An error occurred: {e}")
    

if __name__ == "__main__":
    main()