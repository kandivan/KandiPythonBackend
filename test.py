from database import Database, User

db = Database()
session = db.get_session()
# Insert data
# new_user = User(name='John Doe', email='john@example.com', password='securepassword')
# session.add(new_user)
# session.commit()

# Query data
users = session.query(User).filter(User.name == 'John Doe').all()
for user in users:
    print(user.email)
    session.delete(user)
session.commit()