from fastapi import FastAPI, HTTPException
from datetime import datetime, timedelta
from jose import JWTError, jwt

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10
SECRET_KEY = "mysecretkey_1234"

app = FastAPI()

def create_token(uname: str):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"username": uname, "expire": expire.timestamp()}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["username"]
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

@app.post("/login")
def login(uname: str, password: str):
    if uname == "admin" and password == "1234":
        token = create_token(uname)
        return {"access_token": token}
    raise HTTPException(status_code=400, detail="Invalid username or password")

@app.get("/secure_data")
def secure_data(token: str):
    uname = verify_token(token)
    return {"message": f"Hello {uname}, this is a secure endpoint"}
