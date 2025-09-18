
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Bird(db.Model):
    __tablename__ = "birds"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    species = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "species": self.species}
