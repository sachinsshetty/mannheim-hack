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

            if days_to_expire < 3 or (stock > 15 and demand < 10 and days_to_expire < 10):
                bundle_articles.append(article)

        except (ValueError, TypeError):
            print(f"Fehler beim Verarbeiten des Ablaufdatums für Artikel: {article.get('name', 'Unbekannt')} in bundle_function")

    return bundle_articles





def propose_recipes(bundle_articles, articles):
    if bundle_articles and articles:
        bundle_article_names = ', '.join([article.get('name', 'unknown item') for article in bundle_articles])

        article_names = ', '.join([article.get('name', 'unknown item') for article in articles])

        prompt = (
            f"Give me recipes where all these Bundle articles could be used. My goal is that all items in Bundle articles "
            f"are used in a recipe. You are only allowed to additionally use the articles in Articles.\n"
            f"Bundle articles: {bundle_article_names}\n"
            f"Articles: {article_names}"
        )

        return prompt

    else:
        return "Tell me a joke."







def discount_function():
    try:
        articles = get_json_objects()
        current_date = datetime.now()

        for article in articles:
            name = article.get('name')
            expiration_date_str = article.get('expiresAt')
            price = article.get('price')
            available = article.get('available')

            if name and price and available and expiration_date_str:
                try:
                    expiration_date = datetime.strptime(expiration_date_str, '%Y-%m-%d')

                    days_to_expiration = (expiration_date - current_date).days

                    if days_to_expiration < 30:
                        discount_price = price * 0.90  # 10% Rabatt
                        print(f"{name}: Originalpreis: {price:.2f}€, Rabattpreis: {discount_price:.2f}€, Ablaufdatum in {days_to_expiration} Tagen")

                except ValueError:
                    print(f"Fehler bei der Verarbeitung des Ablaufdatums für {name}")
            else:
                print(f"Unvollständige Daten für Artikel: {name if name else 'Unbekannt'}")

    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")


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
    
    # debug - 
    first_five_objects = json_object[:5]
    return first_five_objects
    #return json_object 

def main():
    
    try:
        #discount_function()
        # Opening JSON file
        json_objs = get_json_objects()
        level_1_prompt = json_parser(json_objs)
        #print(level_1_prompt)
        bundle_articles = bundle_function(json_objs)
        execute_prompt(propose_recipes(bundle_articles, json_objs))
    except FileNotFoundError:
        print("The file 'articles.json' was not found.")
    except json.JSONDecodeError:
        print("The file 'articles.json' is not a valid JSON file.")
    except Exception as e:
        print(f"An error occurred: {e}")
    

if __name__ == "__main__":
    main()