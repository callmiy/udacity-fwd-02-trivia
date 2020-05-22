import random

from flask import Flask, abort, jsonify, request
from flask_cors import CORS

from models import Category, Question, setup_db

QUESTIONS_PER_PAGE = 10


def get_random_question(previous_ids, questions):
    used_ids = []
    questions_len = len(questions)

    while True:
        question = random.choice(questions)
        current_id = question.id

        if current_id in used_ids:
            continue

        if current_id not in previous_ids:
            return question

        used_ids.append(current_id)
        if questions_len == len(used_ids):
            return None


def process_questions_data(questions):
    categories = Category.query.order_by(Category.id.desc()).all()
    total_questions = Question.query.count()

    questions_formatted = [q.format() for q in questions]
    categories_formatted = {c.id: c.type for c in categories}
    current_category = categories[0].format()

    data = {
        "questions": questions_formatted,
        "categories": categories_formatted,
        "total_questions": total_questions,
        "current_category": current_category,
    }

    return data


def questions_route_get(request_object):
    page = request_object.args.get("page", 1, type=int)
    offset = (page - 1) * QUESTIONS_PER_PAGE
    query = (
        Question.query.order_by(Question.id).offset(offset).limit(QUESTIONS_PER_PAGE)
    )
    questions = query.all()
    data = process_questions_data(questions)
    return jsonify(data)


def questions_route_post(request_data):
    search_term = "searchTerm"
    if search_term in request_data:
        sql_search_term = "%{}%".format(request_data[search_term])
        query = Question.query.filter(Question.question.ilike(sql_search_term))
        questions = query.all()

        data = process_questions_data(questions)
        return jsonify(data)

    try:
        request_data_valid = all(
            request_data[x] for x in ["question", "answer", "category", "difficulty"]
        )

        if not request_data_valid:
            raise ValueError("Invalid data")

        new_question = Question(**request_data)
        new_question.insert()
        response_data = new_question.format()
        return jsonify(response_data), 201

    except:  # noqa E722
        # print(sys.exc_info())
        abort(400)


def questions_one_route_delete(request_object, question_id):
    try:
        question = Question.query.get(question_id)
        question.delete()
        data = question.format()
        return jsonify(data)
    except:
        abort(400)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if not test_config:
        setup_db(app)

    CORS(app, resources={r"/*": {"origins": "*"}})

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )

        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )

        response.headers.add("Access-Control-Allow-Credentials", "true")

        return response

    @app.route("/categories")
    def get_categories():
        categories = Category.query.all()

        if len(categories):
            data = {q.id: q.type for q in categories}
            return jsonify({"categories": data})
        abort(404)

    @app.route("/questions", methods=["POST", "GET"])
    def questions_route():
        if request.method == "GET":
            return questions_route_get(request)
        elif request.method == "POST":
            return questions_route_post(request.get_json())

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def questions_one_route(question_id):
        return questions_one_route_delete(request, question_id)

    @app.route("/categories/<int:category_id>/questions")
    def categories_questions_route(category_id):
        category = Category.query.get(category_id)

        if not category:
            abort(404)

        questions = Question.query.join(Category).filter(Category.id == category.id)
        data = process_questions_data(questions)
        return jsonify(data)

    @app.route("/quizzes", methods=["POST"])
    def quizzes_route():
        try:
            request_data = request.get_json()
            previous_questions_ids = request_data["previous_questions"]
            category_request_data = request_data.get("quiz_category", 0)
            category = Category.query.get(category_request_data["id"])
            query = Question.query.join(Category)

            if category:
                query = query.filter(Category.id == category.id)
            questions = query.all()
            question = get_random_question(previous_questions_ids, questions)

            data = {"question": question.format() if question else None}
            return jsonify(data)
        except:
            abort(400)

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({"success": False, "error": 400, "message": "bad request"}),
            400,
        )

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return (
            jsonify(
                {"success": False, "error": 422, "message": "Unprocessable Entity"}
            ),
            422,
        )

    return app


"""
    DONE
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after
    completing the TODOs

    DONE
    @TODO: Create an endpoint to handle GET requests for all available categories.

    DONE
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.

    DONE
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question
    will be removed.
    This removal will persist in the database and when you refresh the page.

    DONE
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text, category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.

    DONE
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.

    DONE
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that category
    to be shown.

    DONE
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.

    DONE
    @TODO: Create error handlers for all expected errors including 404 and 422.
"""
