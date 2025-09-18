
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///birds.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
api = Api(app)

# --- Model ---
class Bird(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    species = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "species": self.species}


# --- Resources ---
class BirdList(Resource):
    def get(self):
        birds = Bird.query.all()
        return [bird.to_dict() for bird in birds], 200

    def post(self):
        data = request.get_json()
        if not data.get("name") or not data.get("species"):
            return {"error": "Both 'name' and 'species' are required"}, 400

        new_bird = Bird(name=data["name"], species=data["species"])
        db.session.add(new_bird)
        db.session.commit()
        return new_bird.to_dict(), 201


class BirdById(Resource):
    def get(self, bird_id):
        bird = Bird.query.get_or_404(bird_id)
        return bird.to_dict(), 200

    def put(self, bird_id):
        bird = Bird.query.get_or_404(bird_id)
        data = request.get_json()

        bird.name = data.get("name", bird.name)
        bird.species = data.get("species", bird.species)

        db.session.commit()
        return bird.to_dict(), 200

    def delete(self, bird_id):
        bird = Bird.query.get_or_404(bird_id)
        db.session.delete(bird)
        db.session.commit()
        return {"message": f"Bird with id {bird_id} deleted"}, 200


# --- Routes ---
api.add_resource(BirdList, '/birds')
api.add_resource(BirdById, '/birds/<int:bird_id>')

@app.route('/')
def home():
    return {
        "message": "Welcome to the Bird API! 🚀",
        "endpoints": {
            "list": "/birds",
            "detail": "/birds/<id>"
        }
    }


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

