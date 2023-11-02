from fastapi import APIRouter, Depends, UploadFile, File
import cloudinary
import cloudinary.uploader

from sqlalchemy.orm import Session

from dz11.database.db import get_db
from dz11.database.models import User
from dz11.schemas import UserDb
from dz11.repository import users as repository_users
from dz11.services.auth import auth_service
from dz11.conf.config import settings

router = APIRouter(prefix='/users', tags=['users'])

@router.get("/me", response_model=UserDb)
async def read_user_me(current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_users_me function returns the current user's information.
        ---
        get:
          tags: [users] # This is a tag that can be used to group operations by resources or any other qualifier.
          summary: Returns the current user's information.
          description: Returns the current user's information based on their JWT token in their request header.
          responses: # The possible responses this operation can return, along with descriptions and examples of each response type (if applicable).
            &quot;200&quot;:  # HTTP status code 200 indicates success! In this case, it means we successfully returned a User
    
    :param current_user: User: Get the current user
    :return: The current user
    :doc-author: Trelent
    """
    return current_user

@router.patch("/avatar", response_model=UserDb)
async def update_avatar_user(file: UploadFile = File(), db: Session = Depends(get_db),
                             current_user: User = Depends(auth_service.get_current_user)):
    """
    The update_avatar_user function updates the avatar of a user.
        Args:
            file (UploadFile): The image to be uploaded.
            current_user (User): The currently logged in user.
            db (Session): A database session object for interacting with the database.
    
    :param file: UploadFile: Get the file from the request body
    :param current_user: User: Get the current user from the database
    :param db: Session: Connect to the database
    :return: A user object, which is the same as the user_schema
    :doc-author: Trelent
    """
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )
    public_id = f"ContactsApp/{current_user.username}{current_user.id}"
    r = cloudinary.uploader.upload(file.file, public_id=public_id, owerwrite=True)
    avatar_url = cloudinary.CloudinaryImage(public_id).build_url(width=250, height=250, crop='fill', version=r.get('version'))
    user = await repository_users.update_avatar(current_user.email, avatar_url, db)
    
    return user