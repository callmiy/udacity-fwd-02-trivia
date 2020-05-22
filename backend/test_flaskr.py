import os
import unittest
import json

from flaskr import create_app
from flaskr import QUESTIONS_PER_PAGE
from models import setup_db
from models import Category
from models import Question

category_attrs = {"type": "Science"}


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(test_config=True)
        self.client = self.app.test_client

        self.database_name = "trivia_test"
        self.database_path = os.getenv(
            "DATABASE_TEST_URI",
            "postgres://{}/{}".format("localhost:5432", self.database_name),
        )

        self.db = setup_db(self.app, self.database_path)

        # reset tables data
        meta = self.db.metadata
        session = self.db.session
        for table in reversed(meta.sorted_tables):
            session.execute(table.delete())
        session.commit()

    def tearDown(self):
        """Executed after reach test"""
        self.db.session.close()

    def make_category(self):
        category = Category(**category_attrs)
        session = self.db.session
        session.add(category)
        session.commit()
        return category

    def make_questions(self, how_many=1):
        category = self.make_category()
        questions = [
            Question(
                **{
                    "category": category.id,
                    "question": "Q " + str(index),
                    "answer": "A " + str(index),
                    "difficulty": index + 1,
                }
            )
            for index in range(how_many)
        ]
        session = self.db.session
        session.add_all(questions)
        session.commit()
        return questions, category

    """
        TODO
        Write at least one test for each test for successful operation and for
        expected errors.
    """

    def test_get_categories_ok(self):
        self.make_category()
        response = self.client().get("/categories")

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        data = data["categories"]
        items = list(data.items())
        d_id, d_type = items[0]
        self.assertTrue(d_id is not None)
        self.assertEqual(d_type, category_attrs["type"])

    def test_get_categories_none_found(self):
        response = self.client().get("/categories")
        self.assertEqual(response.status_code, 404)

    def test_new_question_ok(self):
        category = self.make_category()
        category_id = category.id

        question_attrs = {
            "question": "Say",
            "answer": "no",
            "difficulty": 1,
            "category": category_id,
        }

        response = self.client().post("/questions", json=question_attrs)

        self.assertEqual(response.status_code, 201)

        data = json.loads(response.data)

        self.assertEqual(data["category"], category_id)
        self.assertTrue(data["id"] is not None)

    def test_new_question_not_ok(self):
        question_attrs = {
            "question": "Say",
            "answer": "no",
            "difficulty": 1,
            "category": 0,
        }

        response = self.client().post("/questions", json=question_attrs)

        self.assertEqual(response.status_code, 400)

    def test_get_questions(self):
        questions_models, category = self.make_questions(11)
        questions_models_id = [q.id for q in questions_models]
        response = self.client().get("/questions?page=1")

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data["total_questions"], len(questions_models))

        questions = data["questions"]
        questions_id = [q["id"] for q in questions]
        self.assertEqual(questions_id, questions_models_id[:QUESTIONS_PER_PAGE])

        current_category = data["current_category"]
        self.assertEqual(current_category["id"], category.id)

        categories = data["categories"]
        self.assertEqual(categories, {str(category.id): category.type})

        # PAGE 2
        response = self.client().get("/questions?page=2")
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data["total_questions"], len(questions_models))

        questions = data["questions"]
        question_id = questions[0]["id"]
        self.assertEqual(question_id, questions_models_id[QUESTIONS_PER_PAGE])

    def test_delete_question_ok(self):
        question_model = self.make_questions()[0][0]
        question_id = question_model.id
        response = self.client().delete("/questions/{}".format(question_id))

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data["id"], question_id)

    def test_delete_question_not_ok(self):
        response = self.client().delete("/questions/{}".format(0))
        self.assertEqual(response.status_code, 400)

    def test_search_questions(self):
        question_model = self.make_questions()[0][0]
        question_id = question_model.id
        response = self.client().post("/questions", json={"searchTerm": "0"})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)["questions"][0]
        self.assertEqual(data["id"], question_id)

    def test_get_questions_for_category_ok(self):
        questions_models, category = self.make_questions()
        question_id = questions_models[0].id
        response = self.client().get("/categories/{}/questions".format(category.id))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)["questions"][0]
        self.assertEqual(data["id"], question_id)

    def test_get_questions_for_category_category_not_found(self):
        response = self.client().get("/categories/0/questions")
        self.assertEqual(response.status_code, 404)

    def test_quizzes_selected_category_question_not_chosen(self):
        question = self.make_questions()[0][0]
        request_data = {"previous_questions": [question.id], "quiz_category": {"id": 0}}

        response = self.client().post("/quizzes", json=request_data)

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)["question"]
        self.assertEqual(data, None)

    def test_quizzes_bad_request(self):
        response = self.client().post("/quizzes", json={})
        self.assertEqual(response.status_code, 400)

    def test_quizzes_all(self):
        questions_models = self.make_questions()[0]
        question_id = questions_models[0].id
        request_data = {"previous_questions": [], "quiz_category": {"id": 0}}
        response = self.client().post("/quizzes", json=request_data)

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)["question"]
        self.assertEqual(data["id"], question_id)

    def test_quizzes_selected_category_question_chosen(self):
        questions_models, category = self.make_questions()
        question_id = questions_models[0].id
        request_data = {"previous_questions": [], "quiz_category": {"id": category.id}}
        response = self.client().post("/quizzes", json=request_data)

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)["question"]
        self.assertEqual(data["id"], question_id)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
