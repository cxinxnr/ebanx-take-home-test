from fastapi import FastAPI, Query, Request, Response
from app import store
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/reset")
def reset():
    store.reset_store()
    return Response('OK')

@app.get("/balance")
def get_balance(account_id: str = Query(..., alias="account_id")):
    balance = store.get_account(account_id)
    if balance is None:
        return JSONResponse(content=0, status_code=404)
    return JSONResponse(content=balance, status_code=200)

@app.post("/event")
async def handle_event(request: Request):
    data = await request.json()
    event_type = data.get("type")

    if event_type == "deposit":
        destination = data["destination"]
        amount = data["amount"]

        current_balance = store.get_account(destination) or 0
        new_balance = current_balance + amount

        store.set_account(destination, new_balance)

        return JSONResponse(
            content={"destination": {"id": destination, "balance": new_balance}},
            status_code=201,
        )
    
    elif event_type == "withdraw":
      origin = data["origin"]
      amount = data["amount"]

      current_balance = store.get_account(origin)
      if current_balance is None:
          return JSONResponse(content=0, status_code=404)
      
      new_balance = current_balance - amount
      store.set_account(origin, new_balance)

      return JSONResponse(
          content={"origin": {"id": origin, "balance": new_balance}},
          status_code=201,
      )
    elif event_type == "transfer":
      origin = data["origin"]
      destination = data["destination"]
      amount = data["amount"]

      current_balance_origin = store.get_account(origin)
      if current_balance_origin is None:
            return JSONResponse(content=0, status_code=404)

      current_balance_destination = store.get_account(destination) or 0

      new_balance_origin = current_balance_origin - amount
      store.set_account(origin, new_balance_origin)

      new_balance_destination = current_balance_destination + amount
      store.set_account(destination, new_balance_destination)

      return JSONResponse(
          content={
              "origin": {"id": origin, "balance": new_balance_origin},
              "destination": {"id": destination, "balance": new_balance_destination},
          },
          status_code=201,
      )

    return JSONResponse(status_code=400, content={"error": "Invalid event type"})