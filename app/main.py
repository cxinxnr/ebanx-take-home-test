from fastapi import FastAPI
from app import store
app = FastAPI()

@app.post("/reset")
def reset():
    store.reset_store()
    return {}, 200
