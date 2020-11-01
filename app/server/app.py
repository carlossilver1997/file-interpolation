from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


from app.server.routes.person import router as PersonRouter

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(PersonRouter, tags=["Person"], prefix="/person")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
