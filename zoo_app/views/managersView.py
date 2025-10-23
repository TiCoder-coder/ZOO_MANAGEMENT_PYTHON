from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError, PermissionDenied, AuthenticationFailed
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from zoo_app.serializers.managersSerializer.createManagers import ManagerCreate
from zoo_app.serializers.managersSerializer.updateManagers import ManagerUpdate
from zoo_app.serializers.managersSerializer.baseSerializerManagers import BaseSerializerManager
from zoo_app.serializers.loginSerializer import LoginSerializer

from zoo_app.services.managersService import ManagerService
from zoo_app.middleware.authentication import JWTAuthentication
from zoo_app.middleware.jwt_handler import create_access_token
from zoo_app.enums.enums import Role
from zoo_app.middleware.auth import get_user_from_token, require_manager_or_admin
from rest_framework.permissions import IsAuthenticated

#-------------------------------------------------- DINH NGIA CAC API TREN SWAGGER -------------------------------------------------------------------

# DINH NGHIA MOT CLASS DUNG DE XAC THUC
class IsManagerOrReadOnly(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        user = getattr(request, "user", None)
        role = getattr(user, "role", None)

        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True  # Moi nguoi due co quyen doc

        return role == "Manager"  # Chi manager moi duoc post, put, delete


# DINH NGHIA CAC API HIEN THI CHO MANAGER/STAFF------------------------------------------------------------------------------------------------------
class ManagerViewSet(viewsets.ViewSet):
    
    # DINH NGHIA MOT HAM DUNG DE KIEM TRA ROLE KHI DANG NHAP-----------------------------------------------------------------------------------------
    def _get_user_role(self, request):
        # lấy role từ user object hoặc token payload
        if hasattr(request.user, "role"):
            return str(request.user.role).lower()
        if isinstance(request.user, dict) and "role" in request.user:
            return str(request.user["role"]).lower()
        return None

    authentication_classes = [JWTAuthentication]                            # Bat buoc tat ca deu phai gui token truoc khi thuc hien (ngoai tru login)
    
    permission_classes = [IsManagerOrReadOnly]                              # Thong bao khi dang nhap thanh cong
    permission_classes = [IsAuthenticated]
    
    
    # DINH NGHIA API LOGIN
    @swagger_auto_schema(method='post', tags=["Managers"], request_body=LoginSerializer)
    @action(detail=False, methods=["post"], url_path="login", authentication_classes=[], permission_classes=[AllowAny])
    def login(self, request):
        
        # Lay thong tin dang nhap de kiem tra
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        userName = serializer.validated_data["userName"]
        password = serializer.validated_data["password"]

        try:
            
            # Kiem tra thong tin dang nhap
            manager = ManagerService.authenticate(userName, password)
            
            # Dinh nghia tap du lieu dung de tao token
            payload = {
                "manager_id": str(manager["_id"]),
                "role": manager.get("role", "Manager")
            }
            
            # Tao token
            token = create_access_token(payload)
            
            # Tra ve token va kem theo trang thai thanh cong
            return Response({"token": token, "role": manager.get("role", "Staff")}, status=status.HTTP_200_OK)
        
        except (PermissionDenied, AuthenticationFailed) as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # DINH NGHIA API POST CHO SWAGGER ----------------------------------------------------------------------------------------------------------------
    @swagger_auto_schema(tags=["Managers"], request_body=ManagerCreate, responses={201: BaseSerializerManager})
    def create(self, request):
        try:
            # Lay thong tin user tu request duoc gui
            user = request.user

            # Kiem tra quyen de phan chia cho phu hop
            require_manager_or_admin(user)

            # Kiem tra du lieu
            serializer = ManagerCreate(data=request.data)
            serializer.is_valid(raise_exception=True)

            # Goi toi service the them mot doi tuong moi vao database thong qua request ---- Kiem tra phan quyen user
            created = ManagerService.create_manager(
                user=user,
                name=serializer.validated_data["name"],
                userName=serializer.validated_data["userName"],
                password=serializer.validated_data["password"],
                email=serializer.validated_data["email"],
                role=serializer.validated_data.get("role", "Staff")
            )
            
            # Tra va thong tin neu tao thanh cong
            return Response(created, status=status.HTTP_201_CREATED)

        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # DINH NGHIA API GET ALL CHO SWAGGER -------------------------------------------------------------------------------------------------------------
    @swagger_auto_schema(tags=["Managers"], responses={200: BaseSerializerManager(many=True)})
    def list(self, request):
        try:
            return Response(ManagerService.review_all_managers(request.user), status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # DINH NGHIA API GET BY ID CHO SWAGGER -----------------------------------------------------------------------------------------------------------
    @swagger_auto_schema(tags=["Managers"], responses={200: BaseSerializerManager})
    def retrieve(self, request, pk=None):
        try:
            
            # Kiem tra id
            manager = ManagerService.review_manager_by_id(request.user, pk)
            manager.pop("password", None)
            return Response(manager, status=status.HTTP_200_OK)
        
        except ValidationError:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # DINH NGHIA API PUT CHO SWAGGER ----------------------------------------------------------------------------------------------------------------
    @swagger_auto_schema(tags=["Managers"], request_body=ManagerUpdate, responses={200: BaseSerializerManager})
    def partial_update(self, request, pk=None):
        role = self._get_user_role(request)
        if role not in ["manager", "admin"]:
            return Response({"detail": "You do not have permission to update managers."}, status=status.HTTP_403_FORBIDDEN)

        serializer = ManagerUpdate(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        try:
            updated = ManagerService.update_manager(request.user, pk, serializer.validated_data)
            return Response(updated, status=status.HTTP_200_OK)
        
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # DINH NGHIA API DELETE CHO SWAGGER -------------------------------------------------------------------------------------------------------------
    @swagger_auto_schema(tags=["Managers"], responses={204: "No content"})
    def destroy(self, request, pk=None):                                                # Truyen vao request id
        role = self._get_user_role(request)
        if role not in ["manager", "admin"]:
            return Response({"detail": "You do not have permission to delete managers."},
                            status=status.HTTP_403_FORBIDDEN)
        try:
            deleted = ManagerService.delete_manager(request.user, pk)
            return Response(deleted, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
