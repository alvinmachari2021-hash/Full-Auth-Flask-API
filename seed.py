from app import create_app, db
from models import User, Note
from faker import Faker

fake = Faker()

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    users = []
    for i in range(3):
        user = User(username=fake.user_name())
        user.set_password("password123")
        db.session.add(user)
        users.append(user)
    db.session.commit()

    for user in users:
        for _ in range(5):
            note = Note(
                title=fake.sentence(nb_words=5),
                content=fake.paragraph(nb_sentences=3),
                user_id=user.id
            )
            db.session.add(note)
    db.session.commit()

    print("Database seeded successfully!")