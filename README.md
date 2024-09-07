# mannheim-hack

- Installation

-   Ubuntu 
    python -m venv venv
    source venv/bin/activate

    pip install -r requirements.txt

- Windows
    - python.exe -m venv venv
    - .\venv\Scripts\activate
    - pip install -r requirements.txt

- Run program
    - cd src
    - python engine.py


- Build Frontend
    - docker build -t slabstech/mannheim-ui -f Dockerfile .

- Run Docker
    - docker compose -f docker-compose.yml up -d


curl -X POST -H "Content-Type: application/json" -d '{"prompt": "Your prompt here"}' http://localhost:5000/execute_prompt


curl -X GET http://localhost:5000/recipe_generate



Challenge for Hackfestiva


https://hackathon-products-api.apps.01.cf.eu01.stackit.cloud/api/articles


We want to avoid a surplus of stock wherever it’s possible.
Design and create a solution to manage and optimize the surplus of food items
Identify soon expired food items
Find ways to redistribute these items
Utilize excess inventory
Reduce the need for disposal and the associated environmental impacts