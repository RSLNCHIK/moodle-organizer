from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash

from jose import jwt, JWTError

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from db.database import SessionLocal
from db.repository import get_user_by_id


password_hash = PasswordHash.recommended()

SECRET_KEY = "spaeter-aus-env-laden"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30



# hash password
def hash_password(password: str) -> str:
    return password_hash.hash(password)

# verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)


    # the payload dictionary contains the claims that will be included in the JWT. The "sub" claim is set to the user_id, which uniquely identifies the user for whom the token is being created. The "exp" claim is set to the expiration time of the token, whoch is calculated by adding the ACCESS_TOKEN_EXPIRE_MINUTES to the current UTC time. This ensures that the token will be valid for a limited period of time, after which it will expire and no longer be used.  
    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    # The jwt.encode function is used to create the JWT by encoding the payload with the specified SECRET_KEY and ALGORITHM. The result is a string representating the JWT, which can be sent to the client for authentication purposes.
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> int | None:

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("sub")

        if user_id is None:
            return None

        return int(user_id)

    except JWTError:
        return None
    


oath2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Depends is a FastAPI dependency injection system that allows us to declare dependencies for oauth2_scheme. It automatically extracts the token from the request and passes it to the get_current_user function, which can then use it to authenticate the user.
def get_current_user(token: str = Depends(oath2_scheme)):
    user_id = decode_access_token(token)

    if user_id is None:
        raise HTTPException(status_code=401, detail="Ungueltiger oder abgelaufener Token")

    with SessionLocal() as db:
        user = get_user_by_id(db, user_id)

        if user is None:
            raise HTTPException(status_code=401, detail="Benutzer nicht gefunden.")

        return user