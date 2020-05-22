import os
from sqlalchemy import Column, String, Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

database_path = os.environ.get(
    "DATABASE_URI", "postgres://{}/{}".format("localhost:5432", "trivia")
)


db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    return db


"""
Category

"""


class Category(db.Model):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    type = Column(String)
    questions = relationship("Question", back_populates="category_parent")

    def format(self):
        return {"id": self.id, "type": self.type}


"""
Question

"""


class Question(db.Model):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False,)
    answer = Column(String, nullable=False,)
    category = Column(Integer, ForeignKey("categories.id"), nullable=False)
    difficulty = Column(Integer, nullable=False,)

    category_parent = relationship(
        "Category", back_populates="questions"
    )

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "question": self.question,
            "answer": self.answer,
            "category": self.category,
            "difficulty": self.difficulty,
        }
