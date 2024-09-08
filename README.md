# mannheim-hack


- Run Docker - Full integration
    - docker compose -f docker-compose-integration.yml up -d

- Development
    - Run local LLM
        - docker compose -f docker-compose.yml up -d
    - Front End
        - cd frontend
        - npm install
        - npm run dev
    - Backend
        - cd backend
        - Ubuntu 
            - python -m venv venv
            - source venv/bin/activate
            - pip install -r requirements.txt
            - python app.py

        - Windows
            - python.exe -m venv venv
            - .\venv\Scripts\activate
            - pip install -r requirements.txt
            - python.exe app.py




curl -X POST -H "Content-Type: application/json" -d '{"prompt": "Your prompt here"}' http://localhost:5000/execute_prompt


curl -X GET http://localhost:5000/recipe_generate


- Challenge for Hackfestival
    - Data - https://hackathon-products-api.apps.01.cf.eu01.stackit.cloud/api/articles
    - We want to avoid a surplus of stock wherever it’s possible.
    - Design and create a solution to manage and optimize the surplus of food items
Identify soon expired food items
Find ways to redistribute these items
Utilize excess inventory
Reduce the need for disposal and the associated environmental impacts

- Additional Data
    
    - Build Frontend - Docker
        - cd frontend 
        - docker build -t slabstech/frontend-store -f Dockerfile .

