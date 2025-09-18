
from app import app, db, Bird

with app.app_context():
    print("Deleting existing birds...")
    Bird.query.delete()

    print("Adding new birds...")
    birds = [
        Bird(name="Black-Capped Chickadee", species="Poecile atricapillus"),
        Bird(name="Grackle", species="Quiscalus quiscula"),
        Bird(name="Common Starling", species="Sturnus vulgaris"),
        Bird(name="Mourning Dove", species="Zenaida macroura"),
    ]

    db.session.add_all(birds)
    db.session.commit()
    print("Database seeded successfully!")
