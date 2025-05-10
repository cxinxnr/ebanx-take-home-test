from fastapi import FastAPI, Query
from app import store
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/reset")
def reset():
    store.reset_store()
    return {}, 200
@app.get("/balance")
def get_balance(account_id: str = Query(..., alias="account_id")):
    balance = store.get_account(account_id)
    if balance is None:
        return JSONResponse(content=0, status_code=404)
    return JSONResponse(content=balance, status_code=200)