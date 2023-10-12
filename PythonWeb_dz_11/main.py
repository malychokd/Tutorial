from fastapi import FastAPI

from dz11.routes import contacts

app = FastAPI()

app.include_router(contacts.router, prefix='/api')


@app.get("/", name='Корінь проекту')
def read_root():
    return {"message": "REST APP v1.0"}

@app.get("/contacts")
async def read_contacts(id: int = 0, limit: int = 10):
    return {"message": f"Return all notes: id: {id}, limit: {limit}"}
