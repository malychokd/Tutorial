import redis.asyncio as redis
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from fastapi.middleware.cors import CORSMiddleware

from dz11.conf.config import settings
from dz11.routes import contacts, auth, users

app = FastAPI()

origins = ["http://localhost:4000"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")
app.include_router(users.router, prefix="/api")

@app.on_event("startup")
async def startup():
    """
    The startup function is called when the application starts up.
    It's a good place to initialize things that are used by the app, such as
    connecting to databases or initializing caches.
    
    :return: The redis client, which is used by the limiter
    :doc-author: Trelent
    """
    r = await redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=0,
        encoding="utf-8",
        decode_responses=True,
    )
    await FastAPILimiter.init(r)


@app.get("/", name='Корінь проекту')
def read_root():
    """
    The read_root function returns a dictionary with the key &quot;message&quot; and value &quot;REST APP v0.0&quot;.
    
    
    :return: A dictionary
    :doc-author: Trelent
    """
    return {"message": "REST APP v1.0"}
























app.include_router(auth.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')

# hash_handler = Hash()
# security = HTTPBearer()

# class UserModel(BaseModel):
#     username: str
#     password: str

# app.include_router(contacts.router, prefix='/api')

@app.get("/", name='Корінь проекту')
def read_root():
    return {"message": "REST APP v1.0"}

# @app.post("/signup")
# async def signup(body: UserModel, db: Session = Depends(get_db)):
#     exist_user = db.query(User).filter(User.email == body.username).first()
#     if exist_user:
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
#     new_user = User(email=body.username, password=hash_handler.get_password_hash(body.password))
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return {"new_user": new_user.email}

# @app.post("/login")
# async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.email == body.username).first()
#     if user is None:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
#     if not hash_handler.verify_password(body.password, user.password):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
#     # Generate JWT
#     access_token = await create_access_token(data={"sub": user.email})
#     refresh_token = await create_refresh_token(data={"sub": user.email})
#     user.refresh_token = refresh_token
#     db.commit()
#     return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

# @app.get('/refresh_token')
# async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
#     token = credentials.credentials
#     email = await get_email_form_refresh_token(token)
#     user = db.query(User).filter(User.email == email).first()
#     if user.refresh_token != token:
#         user.refresh_token = None
#         db.commit()
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

#     access_token = await create_access_token(data={"sub": email})
#     refresh_token = await create_refresh_token(data={"sub": email})
#     user.refresh_token = refresh_token
#     db.commit()
#     return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

# @app.get("/contacts")
# async def read_contacts(id: int = 0, limit: int = 10):
#     return {"message": f"Return all contacts: id: {id}, limit: {limit}"}

# @app.get("/secret")
# async def read_item(current_user: User = Depends(get_current_user)):
#     return {"message": 'secret router', "owner": current_user.email}

