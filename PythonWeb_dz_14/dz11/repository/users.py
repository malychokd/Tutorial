from libgravatar import Gravatar
from sqlalchemy.orm import Session

from dz11.database.models import User
from dz11.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User:
    """
    The get_user_by_email function returns a user object from the database based on the email address provided.
        Args:
            email (str): The email address of the user to be retrieved.
            db (Session): A connection to a database session.
        Returns:
            User: A single user object matching the provided email address.
    
    :param email: str: Specify the type of data that will be passed into the function
    :param db: Session: Connect to the database
    :return: The first user in the database that matches the email address provided
    :doc-author: Trelent
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    The create_user function creates a new user in the database.
        Args:
            body (UserModel): The UserModel object containing the information to be added to the database.
            db (Session): The SQLAlchemy Session object used for querying and modifying data in the database.
        Returns:
            User: A User object representing a newly created user.
    
    :param body: UserModel: Pass the user model to the function
    :param db: Session: Pass the database session to the function
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
    
    :param user: User: Specify the user object that is being updated
    :param token: str | None: Pass in the token to update
    :param db: Session: Connect to the database
    :return: None, so the return type should be none
    :doc-author: Trelent
    """
    user.refresh_token = token
    db.commit()

async def confirmed_email(email: str, db: Session) -> None:
    """
    The confirmed_email function sets the confirmed field of a user to True.
    
    :param email: str: Specify the email of the user to be confirmed
    :param db: Session: Pass the database session to the function
    :return: None, so the type hint is correct
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
        db (Session, optional): A database session object to use instead of creating one locally. Defaults to None.  # noQA: E501 line too long
    
    :param email: Get the user from the database
    :param url: str: Specify the type of data that is being passed to the function
    :param db: Session: Pass the database session to the function
    :return: A user object
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user