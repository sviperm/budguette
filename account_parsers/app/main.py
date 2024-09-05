from fastapi import FastAPI, HTTPException
from app.parsers import DeutscheBankParser, RevolutParser

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Bank Parser API"}


@app.post("/parse/deutsche_bank")
def parse_deutsche_bank_endpoint():
    try:
        transactions = DeutscheBankParser().parse()
        return {"transactions": transactions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/parse/revolut")
def parse_revolut_endpoint():
    try:
        transactions = RevolutParser().parse()
        return {"transactions": transactions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
