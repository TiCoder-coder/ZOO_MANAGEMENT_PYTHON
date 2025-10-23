# ---------------------------------------------- DINH NGHIA CO CHE HOAT DONG CHO JWT TOKEN --------------------------------------------------------------------------------

import jwt
from datetime import datetime, timedelta, timezone
from decouple import config
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from pymongo import MongoClient
from django.conf import settings


# Load cac khoa bao mat tu .env de xu li thong tin
SECRET_KEY = settings.SECRET_KEY
JWT_SECRET = config("JWT_SECRET", default="changeme_jwt")
JWT_ALGORITHM = config("JWT_ALGORITHM", default="HS256")

ACCESS_TOKEN_EXPIRE_HOURS = int(config("ACCESS_TOKEN_EXPIRE_HOURS", default=1))
REFRESH_TOKEN_EXPIRE_DAYS = int(config("REFRESH_TOKEN_EXPIRE_DAYS", default=1))

# Load cac khoa bao mat de ket noi voi mongodb
MONGO_URI = config("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["zoo_management"]
revoked_tokens = db["revoked_tokens"]
revoked_tokens.create_index("token", unique=True)

# Kiem tra secret_key
if not SECRET_KEY or SECRET_KEY == "changeme":
    raise RuntimeError("SECRET_KEY must be set in environment for security.")

# Ham dung de tao ra access_token 
def create_access_token(payload: dict) -> str:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)

    # Chuan hoa role va id cho manager luc tao
    normalized_payload = {
        "manager_id": str(payload.get("manager_id")),
        "role": str(payload.get("role", "manager")).lower(),
    }

    # Dinh nghia body cho access token
    body = {
        **normalized_payload,
        "iat": now,
        "exp": exp,
        "iss": "zoo_management_api",
        "aud": "zoo_client_app"
    }

    # Tao token va return ra
    token = jwt.encode(body, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token if isinstance(token, str) else token.decode("utf-8")

# Ham dung de thu hoi token khi het han
def revoke_token(token):
    revoked_tokens.insert_one({"token": token, "revoked_at": datetime.now()})


# Kiem tra access token
def verify_access_token(token: str) -> dict:
    
    # Giai ma token de xac minh
    try:
        decoded = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
            issuer="zoo_management_api",
            audience="zoo_client_app"
        )

        # Kiem tra token con thoi gian su dung hay khong
        if is_token_revoked(token):
            raise AuthenticationFailed("Token has been revoked")

        # Neu kiem tra dung het thi return da giai ma
        return decoded
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Token expired")
    except jwt.InvalidTokenError:
        raise AuthenticationFailed("Invalid token")

# Tao ra mot refresh token --- Dung de lay lai mot access token ma khong can login lai
def create_refresh_token(payload: dict) -> str:
    exp = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    payload["exp"] = exp

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token if isinstance(token, str) else token.decode("utf-8")

# Ham dung de giai ma token
def decode_token(token: str):
    try:
        # Giai ma
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise ValidationError("Token expired")
    except jwt.InvalidTokenError:
        raise ValidationError("Invalid token")


# Kiem tra xem token co bi thu hoi hay chua
def is_token_revoked(token):
    return revoked_tokens.find_one({"token": token}) is not None

# Giai ma refresh token ---- thu hoi token cu va tao token moi
def refresh_access_token(refresh_token: str):
    decoded = decode_token(refresh_token)                                   # Giai ma token
    revoke_token(refresh_token)                                             # Thu hoi token
    return create_access_token({                                            # Tao token moi
        "manager_id": decoded.get("manager_id"),
        "role": decoded.get("role", "manager")
    })
