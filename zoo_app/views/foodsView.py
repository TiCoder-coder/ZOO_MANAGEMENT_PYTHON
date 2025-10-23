from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

from zoo_app.serializers.foodsSerializer.baseSerializerFoods import BaseSerializerFood
from zoo_app.serializers.foodsSerializer.createFoods import FoodCreate
from zoo_app.serializers.foodsSerializer.updateFoods import FoodUpdate
from zoo_app.services.foodsService import FoodService
from zoo_app.middleware.authentication import JWTAuthentication

#-------------------------------------------------- DINH NGIA CAC API TREN SWAGGER -------------------------------------------------------------------
class FoodView(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]                                                        # Yeu cau client phai gui token
    permission_classes = [IsAuthenticated]                                                              # Cho phep truy cap neu xac thuc thanh cong

    # DINH NGHIA API POST CHO SWAGGER ----------------------------------------------------------------------------------------------------------------
    @swagger_auto_schema(tags=["Foods"], request_body=FoodCreate, responses={201: BaseSerializerFood})
    def API_post(self, request):
        user = request.user
        serializer = FoodCreate(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            
            # Goi toi service the them mot doi tuong moi vao database thong qua request ---- Kiem tra phan quyen user
            food_id = FoodService.create_food(user, serializer.validated_data)
            food = FoodService.review_food_by_id(user, food_id)

            if "_id" in food:
                food["_id"] = str(food["_id"])

            return Response(food, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # DINH NGHIA API GET ALL CHO SWAGGER -------------------------------------------------------------------------------------------------------------
    @swagger_auto_schema(tags=["Foods"], responses={200: BaseSerializerFood(many=True)})
    def API_all_get(self, request):
        user = request.user
        try:
            foods = FoodService.review_all_foods(user)
            
            for food in foods:
                if "_id" in food:
                    food["_id"] = str(food["_id"])
            return Response(foods, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # DINH NGHIA API GET BY ID CHO SWAGGER -----------------------------------------------------------------------------------------------------------
    @swagger_auto_schema(tags=["Foods"], responses={200: BaseSerializerFood})
    def API_id_get(self, request, idFood=None):
        
        user = request.user
        try:
            food = FoodService.review_food_by_id(user, idFood)
            return Response(food, status=status.HTTP_200_OK)
        except Exception as e:
            if "No food found" in str(e):
                return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # DINH NGHIA API PUT CHO SWAGGER ----------------------------------------------------------------------------------------------------------------
    @swagger_auto_schema(tags=["Foods"], request_body=FoodUpdate, responses={200: BaseSerializerFood})
    def API_put(self, request, idFood=None):
        user = request.user
        serializer = FoodUpdate(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            updated_food = FoodService.update_food(user, idFood, serializer.validated_data)
            if "_id" in updated_food:
                updated_food["_id"] = str(updated_food["_id"])
            return Response(updated_food, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # DINH NGHIA API DELETE CHO SWAGGER -------------------------------------------------------------------------------------------------------------
    @swagger_auto_schema(tags=["Foods"], responses={204: "No Content"})
    def API_delete(self, request, idFood=None):
        user = request.user
        try:
            FoodService.delete_food(user, idFood)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError:
            return Response({"detail": "Invalid idFood format"}, status=status.HTTP_400_BAD_REQUEST)
        except LookupError:
            return Response({"detail": f"Error, not found food has id: {idFood}"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
