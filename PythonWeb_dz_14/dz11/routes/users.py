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
    The read_user_me function returns the current user's information.
        ---
        get:
          tags: [user]
          summary: Returns the current user's information.
          responses:
            200:  # HTTP status code 200 means &quot;OK&quot;
              description: The requested resource was returned successfully.
              content:{'application/json': {'schema': User}}  # This is a JSON schema for a User object, which we'll define later in this file.
    
    :param current_user: User: Pass the current user to the function
    :return: The current_user object
    :doc-author: Trelent
    """
    return current_user

@router.patch("/avatar", response_model=UserDb)
async def update_avatar_user(file: UploadFile = File(), db: Session = Depends(get_db),
                             current_user: User = Depends(auth_service.get_current_user)):
    """
    The update_avatar_user function updates the avatar of a user.
        Args:
            file (UploadFile): The file to be uploaded.
            db (Session): The database session object.
            current_user (User): The currently logged in user object, which is used to get the username and id for cloudinary uploads.
    
    :param file: UploadFile: Upload the file to cloudinary
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the user that is currently logged in
    :return: An object of the user class, which is defined in models
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