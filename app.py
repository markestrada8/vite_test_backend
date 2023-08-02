from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.attributes import flag_modified
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
# SWITCH OUT LOCAL SQLITE ADDRESS STRING WITH HEROKU POSTGRESQL ADDRESS STRING
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'app.sqlite')}"

db = SQLAlchemy(app)
ma = Marshmallow(app)

CORS(app)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)

    def __init__(self, title, content):
        self.title = title
        self.content = content


class NoteSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "content", "note")


note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)

@app.route("/", methods=["GET"])
def test_route():
    return jsonify("Hello World!")


@app.route("/note", methods=["POST"])
def add_note():
    title = request.json.get("title")
    content = request.json.get("content")

    record = Note(title, content)
    db.session.add(record)
    db.session.commit()

    return jsonify(note_schema.dump(record))


@app.route("/note", methods=["GET"])
def get_all_notes():
    all_notes = Note.query.all()
    return jsonify(notes_schema.dump(all_notes))

if __name__ == "__main__":
    app.run(debug=True)