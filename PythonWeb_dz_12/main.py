from fastapi import FastAPI
from dz11.routes import contacts, auth

app = FastAPI()

app.include_router(auth.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')

@app.get("/", name='Корінь проекту')
def read_root():
    return {"message": "REST APP v1.0"}



