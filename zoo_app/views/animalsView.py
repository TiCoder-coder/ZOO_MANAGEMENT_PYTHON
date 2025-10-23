from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from zoo_app.serializers.animalsSerializer.baseSerializerAnimal import BaseSerializerAnimal
from zoo_app.serializers.animalsSerializer.createAnimals import AnimalCreate
from zoo_app.serializers.animalsSerializer.updateAnimals import AnimalUpdate
from zoo_app.services.animalsService import AnimalService
from zoo_app.middleware.authentication import JWTAuthentication

#-------------------------------------------------- DINH NGIA CAC API TREN SWAGGER -------------------------------------------------------------------
class AnimalView(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]                                                        # Yeu cau client phai gui token
    permission_classes = [IsAuthenticated]                                                              # Cho phep truy cap neu xac thuc thanh cong

    # DINH NGHIA API POST CHO SWAGGER ----------------------------------------------------------------------------------------------------------------
    @swagger_auto_schema(tags=["Animals"], request_body=AnimalCreate, responses={201: BaseSerializerAnimal})
    def API_post(self, request):
        serializer = AnimalCreate(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            
            # Goi toi service the them mot doi tuong moi vao database thong qua request ---- Kiem tra phan quyen user
            new_animal = AnimalService.create_animal(request.user, serializer.validated_data)
            response_data = BaseSerializerAnimal(new_animal).data
            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # DINH NGHIA API GET ALL CHO SWAGGER -------------------------------------------------------------------------------------------------------------
    @swagger_auto_schema(tags=["Animals"], responses={200: BaseSerializerAnimal(many=True)})
    def API_all_get(self, request):
        try:
            # Goi ham review animal o service de thuc hien
            animals = AnimalService.review_animal(request.user)
            return Response(animals, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # DINH NGHIA API GET BY ID CHO SWAGGER -----------------------------------------------------------------------------------------------------------
    @swagger_auto_schema(tags=["Animals"], responses={200: BaseSerializerAnimal})
    def API_id_get(self, request, idAnimal=None):
        try:
            
            animal = AnimalService.review_animal_by_id(request.user, idAnimal)
            return Response(animal, status=status.HTTP_200_OK)
        except ValueError:
            return Response({"detail": "Invalid IdAnimal format"}, status=status.HTTP_400_BAD_REQUEST)
        except LookupError:
            return Response({"detail": f"Error, not found animal has id: {idAnimal}"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # DINH NGHIA API PUT CHO SWAGGER ----------------------------------------------------------------------------------------------------------------
    @swagger_auto_schema(tags=["Animals"], request_body=AnimalUpdate, responses={200: BaseSerializerAnimal})
    def API_put(self, request, idAnimal=None):
        serializer = AnimalUpdate(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            AnimalService.update_animal(request.user, idAnimal, serializer.validated_data)
            updated = AnimalService.review_animal_by_id(request.user, idAnimal)
            return Response(updated, status=status.HTTP_200_OK)
        except ValueError:
            return Response({"detail": "Invalid IdAnimal format"}, status=status.HTTP_400_BAD_REQUEST)
        except LookupError:
            return Response({"detail": f"Error, not found animal has id: {idAnimal}"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # DINH NGHIA API DELETE CHO SWAGGER -------------------------------------------------------------------------------------------------------------
    @swagger_auto_schema(tags=["Animals"], responses={200: BaseSerializerAnimal})
    def API_delete(self, request, idAnimal=None):
        try:
            AnimalService.delete_animal(request.user, idAnimal)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError:
            return Response({"detail": "Invalid IdAnimal format"}, status=status.HTTP_400_BAD_REQUEST)
        except LookupError:
            return Response({"detail": f"Error, not found animal has id: {idAnimal}"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
