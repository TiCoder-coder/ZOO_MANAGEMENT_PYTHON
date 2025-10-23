from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

from zoo_app.serializers.enclosureSerializer.baseSerializerEnclosure import BaseEnclosureSerializer
from zoo_app.serializers.enclosureSerializer.createEnclosures import EnclosureCreate
from zoo_app.serializers.enclosureSerializer.updateEnclosures import EnclosureUpdate
from zoo_app.services.enclosuresService import EnclosureService
from zoo_app.middleware.authentication import JWTAuthentication

#-------------------------------------------------- DINH NGIA CAC API TREN SWAGGER -------------------------------------------------------------------
class EnclosureView(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]                                                        # Yeu cau client phai gui token
    permission_classes = [IsAuthenticated]                                                              # Cho phep truy cap neu xac thuc thanh cong


    # DINH NGHIA API POST CHO SWAGGER ----------------------------------------------------------------------------------------------------------------
    @swagger_auto_schema(tags=["Enclosures"], request_body=EnclosureCreate, responses={201: BaseEnclosureSerializer})
    def API_post(self, request):
        serializer = EnclosureCreate(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user

        try:
            
            # Goi toi service the them mot doi tuong moi vao database thong qua request ---- Kiem tra phan quyen user
            new_enclosure_id = EnclosureService.create_enclosure(user, serializer.validated_data)
            new_enclosure = EnclosureService.review_enclosure_by_id(user, new_enclosure_id)
            return Response(new_enclosure, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # DINH NGHIA API GET ALL CHO SWAGGER -------------------------------------------------------------------------------------------------------------
    @swagger_auto_schema(tags=["Enclosures"], responses={200: BaseEnclosureSerializer(many=True)})
    def API_all_get(self, request):
        user = request.user
        try:
            enclosures = EnclosureService.review_enclosure(user)
            return Response(enclosures, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # DINH NGHIA API GET BY ID CHO SWAGGER -----------------------------------------------------------------------------------------------------------
    @swagger_auto_schema(tags=["Enclosures"], responses={200: BaseEnclosureSerializer})
    def API_id_get(self, request, idEnclosure=None):
        user = request.user
        try:
            enclosure = EnclosureService.review_enclosure_by_id(user, idEnclosure)
            return Response(enclosure, status=status.HTTP_200_OK)
        except ValueError:
            return Response({"detail": "Invalid IdEnclosure format"}, status=status.HTTP_400_BAD_REQUEST)
        except LookupError:
            return Response({"detail": f"Not found enclosure with id: {idEnclosure}"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # DINH NGHIA API PUT CHO SWAGGER ----------------------------------------------------------------------------------------------------------------
    @swagger_auto_schema(tags=["Enclosures"], request_body=EnclosureUpdate, responses={200: BaseEnclosureSerializer})
    def API_put(self, request, idEnclosure=None):
        serializer = EnclosureUpdate(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = request.user

        try:
            data = serializer.validated_data
            if "idEnclosure" in data:
                data.pop("idEnclosure")

            EnclosureService.update_enclosure(user, idEnclosure, data)
            updated = EnclosureService.review_enclosure_by_id(user, idEnclosure)
            return Response(updated, status=status.HTTP_200_OK)
        except ValueError:
            return Response({"detail": "Invalid IdEnclosure format"}, status=status.HTTP_400_BAD_REQUEST)
        except LookupError:
            return Response({"detail": f"Not found enclosure with id: {idEnclosure}"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # DINH NGHIA API DELETE CHO SWAGGER -------------------------------------------------------------------------------------------------------------   
    @swagger_auto_schema(tags=["Enclosures"], responses={204: "Deleted successfully"})
    def API_delete(self, request, idEnclosure=None):
        user = request.user
        try:
            EnclosureService.delete_enclosure(user, idEnclosure)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError:
            return Response({"detail": "Invalid idEnclosure format"}, status=status.HTTP_400_BAD_REQUEST)
        except LookupError:
            return Response({"detail": f"Not found enclosure with id: {idEnclosure}"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
