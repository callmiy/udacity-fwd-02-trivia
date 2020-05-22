# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```

## API Endpoints
### Error Handling
Errors are returned as JSON objects in the following format:

{
    "success": False,
    "error": 400,
    "message": "bad request"
}

The API will return three error types when requests fail:

400: Bad Request
404: Resource Not Found
422: Not Processable

### Category

GET /categories
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
- Sample: curl localhost:3000/categories
```
  {
    "1" : "Science",
    "2" : "Art",
    "3" : "Geography",
    "4" : "History",
    "5" : "Entertainment",
    "6" : "Sports"
  }
```

### Question

GET /questions
- Fetches an object including a list of questions
- Request Arguments: None
- Returns: An object with keys: `questions`, `categories`, `total_questions`, `current_category`
- Sample: `curl http://localhost:3000/questions`
```
  {
    "questions": [
      {
        "id": 1,
        "question": "Say what?",
        "answer": "Say up",
        "category": 1,
        "difficulty": 5
      }
    ],
    "categories": {
      "1": "History",
      "2": "Sports"
    },
    "total_questions": 1,
    "current_category": {
      "id": 1,
      "type": "Science"
    }
  }
```

POST /questions
- Creates a new question or searches for questions
  - Creating new question, example:
    ```
      curl http://localhost:3000/questions -X POST \
        -H "Content-Type: application/json" \
        -d '{ \
              "question": "Say what?", \
              "answer": "Say up", \
              "category": 1, \
              "difficulty": 5 \
           }'
    ```

    Response:
    ```
      {
          "id": 1,
          "question": "Say what?",
          "answer": "Say up",
          "category": 1,
          "difficulty": 5
      }
    ```
  - Searching for question, example:
    ```
      curl http://localhost:3000/questions -X POST \
        -H "Content-Type: application/json" \
        -d '{ \
              "searchTerm": "Say", \
           }'
    ```

    Response:
    ```
      {
        "questions": [
          {
            "id": 1,
            "question": "Say what?",
            "answer": "Say up",
            "category": 1,
            "difficulty": 5
          }
        ],
        "categories": {
          "1": "History",
          "2": "Sports"
        },
        "total_questions": 1,
        "current_category": {
          "id": 1,
          "type": "Science"
        }
      }   
    ```

DELETE /questions/{question_id}
- Deletes a question given by the ID
- Returns: An object representing deleted question
- Sample: `curl http://localhost:3000/questions/1`
```
  {
    "id": 1,
    "question": "Say what?",
    "answer": "Say up",
    "category": 1,
    "difficulty": 5
  }
```

GET /categories/{category_id}/questions
- Fetches questions belonging to the category specified by `category_id`
- Returns an object containing a list of questions belonging to specified category
- Sample `curl http://localhost:3000/categories/1/questions`
```
{
  "questions": [
    {
      "id": 1,
      "question": "Say what?",
      "answer": "Say up",
      "category": 1,
      "difficulty": 5
    }
  ],
  "categories": {
    "1": "History",
    "2": "Sports"
  },
  "total_questions": 1,
  "current_category": {
    "id": 1,
    "type": "Science"
  }
}
```

POST /quizzes
- Fetches a random question from a list of questions belonging to a particular category (if `quiz_category` argument is specified) or all questions if no category is specified
- Returns an object of the form:
```
  {
    "question": {
      "id": 1, // question ID
      "question": "Say what?", // question text 
      "answer": "The man", // answer text
      "difficulty": 1, // difficulty level
    }
  }
```
- POST body:
```
  {
    "previous_questions": [1,2],
    "quiz_category": 1
  }
```
  `previous_questions` a list of IDs of previous quiz questions
 
  `quiz_category` ID of category of questions we wish to quiz. If this key is missing or its value is invalid, then all questions in the database will be returned

Sample:
```
  curl http://localhost:3000/question_id -X POST
    -H "Content-Type: application/json" \
    -d '{ \
          "previous_questions": [1, 2], \
          "quiz_category": 1, \
       }'
```

```
{
  "question": {
    "id": 1,
    "question": "Say what?",
    "answer": "The man",
    "difficulty": 1,
  }
}
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
