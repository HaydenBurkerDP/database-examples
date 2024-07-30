from flask import Blueprint, Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

import csv
import os
import marshmallow as ma

app = Flask(__name__)

folder_path = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(folder_path, "example_flask_sqlalchemy.db")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{database_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False

db = SQLAlchemy(app)


class Examples(db.Model):
    __tablename__ = "Examples"

    example_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(), nullable=False)

    def __init__(self, name):
        self.name = name


class ExampleSchema(ma.Schema):
    class Meta:
        fields = ["example_id", "name"]


example_schema = ExampleSchema()


examples = Blueprint("examples", __name__)


@examples.route("/example", methods=["POST"])
def example_add():
    post_data = request.json
    name = post_data.get("name")

    example = Examples(name)

    db.session.add(example)
    db.session.commit()

    return jsonify({"message": "example added", "example": example_schema.dump(example)}), 201


@examples.route("/examples", methods=["GET"])
def examples_get_all():
    examples = db.session.query(Examples).all()

    return jsonify({"message": "examples found", "examples": example_schema.dump(examples, many=True)})


@examples.route("/example/<example_id>", methods=["GET"])
def get_example_by_id(example_id):
    example = db.session.query(Examples).filter(Examples.example_id == example_id).first()

    if not example:
        return jsonify({"message": "example not found"}), 200

    return jsonify({"message": "example found", "example": example_schema.dump(example)}), 200


@examples.route("/example/<example_id>", methods=["PUT"])
def example_update(example_id):
    example = db.session.query(Examples).filter(Examples.example_id == example_id).first()

    if not example:
        return jsonify({"message": "example not found"}), 404

    post_data = request.json
    name = post_data.get("name")

    example.name = name
    db.session.commit()

    return jsonify({"message": "example updated", "example": example_schema.dump(example)}), 200


@examples.route("/example/<example_id>", methods=["DELETE"])
def example_delete(example_id):
    example = db.session.query(Examples).filter(Examples.example_id == example_id).first()

    if not example:
        return jsonify({"message": "example not found"}), 404

    db.session.delete(example)
    db.session.commit()

    return jsonify({"message": "example deleted"}), 200


app.register_blueprint(examples)


def create_examples_from_csv(file_name):
    with open(file_name, 'r') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)

        for row in reader:
            name = row[0]
            example = Examples(name)

            db.session.add(example)

        db.session.commit()


with app.app_context():
    db.create_all()

    if (db.session.query(Examples).count() == 0):
        print("Creating examples...")
        create_examples_from_csv("examples.csv")

if __name__ == "__main__":
    app.run(port=8086, debug=True)
