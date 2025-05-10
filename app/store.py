accounts = {}
def reset_store():
    global accounts
    accounts = {}

def get_account(account_id: str) -> int | None:
    return accounts.get(account_id)

def set_account(account_id: str, balance: int):
    accounts[account_id] = balance
