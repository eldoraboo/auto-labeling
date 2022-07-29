from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import requests
import os

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        try:
            res = requests.get(os.environ["_JWTX_URL"]+"/verify/"+jwtoken)
            if res.status_code != 200:
                isTokenValid = False
            else:
                isTokenValid = res.json()
        except Exception as e:
            print(e)
            raise HTTPException(status_code=403, detail="Invalid authorization code.")
        return isTokenValid

def check_user(payload)->bool:
    try:
        res = requests.post(os.environ["_JWTX_URL"]+"/get_token", json=payload)
    except:
        raise HTTPException(status_code=403, detail="Invalid authorization code.")
    if res.status_code == 200:
        return True
    else:
        raise HTTPException(status_code=403, detail="Invalid authorization code.")
