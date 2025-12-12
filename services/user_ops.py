from app.models import User
from sqlalchemy.orm import Session


def create_user(userName, userEmail, passwordHash, firstName, lastName, dateCreated):

    # Create a new user and add to the database
    new_user = User(
        userName=userName,
        userEmail=userEmail,
        passwordHash=passwordHash,
        firstName=firstName,
        lastName=lastName,
        dateCreated=dateCreated,
    )

    db: Session = Session()
    db.add(new_user)
    db.commit()
    
