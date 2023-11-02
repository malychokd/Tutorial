from libgravatar import Gravatar
from sqlalchemy.orm import Session

from dz11.database.models import User
from dz11.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User:
    """
    The get_user_by_email function takes in an email and a database session, then returns the user with that email.
    
    :param email: str: Specify the type of parameter that is being passed in
    :param db: Session: Pass the database session to the function
    :return: The user object with the given email
    :doc-author: Trelent
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    The create_user function creates a new user in the database.
        Args:
            body (UserModel): The UserModel object containing the information to be added to the database.
            db (Session): The SQLAlchemy Session object used for querying and updating data in the database.
        Returns:
            User: A User object representing a newly created user.
    
    :param body: UserModel: Pass in the request body to create a new user
    :param db: Session: Connect to the database
    :return: A user object
    :doc-author: Trelent
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    The update_token function updates the refresh token for a user.
    
    :param user: User: Identify the user that is being updated
    :param token: str | None: Set the user's refresh token
    :param db: Session: Commit the changes to the database
    :return: None, so the return type is none
    :doc-author: Trelent
    """
    user.refresh_token = token
    db.commit()

async def confirmed_email(email: str, db: Session) -> None:
    """
    The confirmed_email function sets the confirmed field of a user to True.
    
    :param email: str: Pass the email address of a user to the function
    :param db: Session: Pass the database session to the function
    :return: None, but the type hint says it returns none
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()

async def update_avatar(email, url: str, db: Session) -> User:
    """
    The update_avatar function updates the avatar of a user.
    
    Args:
        email (str): The email address of the user to update.
        url (str): The URL for the new avatar image.
        db (Session, optional): SQLAlchemy Session instance; defaults to None.  If not provided, a new session will be created and closed automatically after use.
    
    :param email: Get the user from the database
    :param url: str: Specify the type of data that is expected to be passed into the function
    :param db: Session: Pass the database session to the function
    :return: A user object
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user