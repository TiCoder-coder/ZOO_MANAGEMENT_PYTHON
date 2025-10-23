# zoo_app/views/authsView.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from zoo_app.serializers.loginSerializer import LoginSerializer
from zoo_app.middleware.jwt_handler import (
    create_access_token, create_refresh_token, decode_token
)
from zoo_app.services.managersService import ManagerService
from zoo_app.middleware.authentication import JWTAuthentication
from zoo_app.middleware.auth import require_manager, require_staff_or_manager

# ----------------------------------------------- DINH NGHIA CAC ENDPOINT DUNG DE DANG NHAP CO AUTH -------------------------------------------------------------


# Tao mot set de luu token tam thoi --- Sau khi logout hay thoat chuong trinh thi token se tu dong xoa sach 
BLACKLISTED_REFRESH_TOKENS = set()


# Class dung de kiem tra chuoi du lieu json ma luc gui request len phai la JSON
class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)


# DINH NGHIA CAC ENDPOINT CHO AUTH LOGIN
class LoginView(APIView):
    permission_classes = [AllowAny]

    # DINH NGHIA API POST LOGIN SWAGGER ----------------------------------------------------------------------------------------------------------------
    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={200: openapi.Response(                                                # Neu thanh cong thi tra ra cac token de dang nhap
            "Login success",
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "access": openapi.Schema(type=openapi.TYPE_STRING),
                    "refresh": openapi.Schema(type=openapi.TYPE_STRING),
                    "role": openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        )}
    )
    def post(self, request):
        
        # Xac thuc danh nhap (xac dinh username va password)
        s = LoginSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        userName = s.validated_data["userName"]
        password = s.validated_data["password"]

        # Goi ham authenticate tu service len de thuc hien danh nhap
        try:
            manager = ManagerService.authenticate(userName, password)
            payload = {
                "manager_id": str(manager["_id"]),                                      # Chuan hoa id thanh string
                "role": manager.get("role", "staff").lower()                            # Chuan hoa role thanh chu thuong
            }
            
            # Neu thanh cong thi tra ra access_token va refresh token
            access_token = create_access_token(payload)
            refresh_token = create_refresh_token(payload)
            
            # Return ra thong tin
            return Response({
                "access": access_token,
                "refresh": refresh_token,
                "role": payload["role"]
            })
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

# DINH NGHIA CHO API DUNG DE LAM MOI TOKEN --- GUI REFRESH TOKEN LEN DE LAY ACCESS_TOKEN KHONG CAN DANG NHAP LAI-----------------------------------------
class RefreshView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=RefreshSerializer)
    def post(self, request):
        
        # Kiem tra daam bao client co gui refresh_token
        s = RefreshSerializer(data=request.data)

        s.is_valid(raise_exception=True)
        token = s.validated_data["refresh"]
        
        # Kiem tra xem co dung token duoc luu tru khong
        if token in BLACKLISTED_REFRESH_TOKENS:
            return Response({"detail": "Token already used or logged out"}, status=status.HTTP_403_FORBIDDEN)

        # Giai ma token kiem tra xem co dung role khong
        try:
            decoded = decode_token(token)
            new_access = create_access_token({
                "manager_id": decoded["manager_id"],
                "role": decoded.get("role", "staff").lower()
            })
            
            # Tra ve access_token moi cho client
            return Response({"access": new_access})
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# DINH NGHI MOT CLASS DUNG DE KIEM TRA ACCESS TOKEN CO DUNG KHONG
class VerifyView(APIView):
    authentication_classes = [JWTAuthentication]                                                        # Yeu cau client phai gui token
    permission_classes = [IsAuthenticated]                                                              # Cho phep truy cap neu xac thuc thanh cong

    # Staff hay manager deu co quyen xac thuc
    def get(self, request):
        user = request.user
        require_staff_or_manager(user)                                                                  # Phan quyen --- chi co staff hay manager moi duoc
        
        # Tra ve thong tin sau khi xac thuc thanh cong
        return Response({
            "manager_id": getattr(user, "id", None),
            "role": getattr(user, "role", None),
            "is_authenticated": user.is_authenticated
        })


# DINH NGHIA MOT CLASS DUNG DE QUAN LI HIEN THI
class AdminOnlyView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        require_manager(user)                                                                           # Chi co manager moi duoc su dung
        return Response({
            "message": f"Welcome manager {getattr(user, 'id', 'unknown')}! You have full access."
        })

# DINH NGHI API CHO DANG XUAT --- VO HIEU HOA REFRESH TOKEN CUA NGUOI DUNG
class LogoutView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=RefreshSerializer)
    def post(self, request):
        
        # Lay token
        s = RefreshSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        
        # THEM TOKEN VAO DANH SACH DEN
        token = s.validated_data["refresh"]
        BLACKLISTED_REFRESH_TOKENS.add(token)
        
        return Response({"detail": "Logged out successfully"}, status=status.HTTP_200_OK)
