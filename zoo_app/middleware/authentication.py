#------------------------------------------------ TAO RA MOT CLASS DUNG DE XAC THUC DANG NHAP --- KIEM TRA TOKEN -----------------------------------------------------------------------

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .jwt_handler import verify_access_token
import jwt
from django.conf import settings
from django.contrib.auth.models import AnonymousUser


# ---- Tao user de authentication co the nhan dien la user ----
class TokenUser(AnonymousUser):  # TokenUser se ke thua lai AnonymousUser la user chua login --- sau do dieu chinh lai chuc nang
    def __init__(self, payload):
        self.id = payload.get("manager_id")                                     # Dinh nghia lai id
        self.role = payload.get("role")                                         # Dinh nghia lai role --- Manager

    # Sau khi tao xong thi authenticated se return ve True
    @property
    def is_authenticated(self):
        return True


# Dinh nghia mot class dung de xac minh token --- Khi call API thi no se kiem tra xem thong tin co hop le hay khong
class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        # Kiem tra header co dung khong
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        # Tach token ra: Token chinh la phan phia sau header
        token = auth_header.split(" ")[1]

        # Giai ma token de kiem tra
        try:
            payload = jwt.decode(
                token,                                                              # Chuoi jwt luc client gui
                settings.SECRET_KEY,                                                # Kiem tra secret_key
                algorithms=["HS256"],                                               # Thuat toan ky va giai ma token
                issuer="zoo_management_api",                                        # Xac minh token co duoc tao ra tu server
                audience="zoo_client_app"                                           # Dam bao token chi hop le cho zoo_app
            )

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token expired")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")

        # Neu dung thi tra ve user da duoc xac minh
        return (TokenUser(payload), None)
