from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from zoo_app.serializers.feedRecordsSerializer.baseSerializerFeedRecord import BaseSerializerFeedRecord
from zoo_app.serializers.feedRecordsSerializer.createFeedRecords import FeedRecordCreate
from zoo_app.serializers.feedRecordsSerializer.updateFeedRecords import FeedRecordUpdate
from zoo_app.services.feedRecordsService import FeedRecordService
from zoo_app.middleware.authentication import JWTAuthentication

#-------------------------------------------------- DINH NGIA CAC API TREN SWAGGER -------------------------------------------------------------------
class FeedRecordView(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]                                                        # Yeu cau client phai gui token
    permission_classes = [IsAuthenticated]                                                              # Cho phep truy cap neu xac thuc thanh cong


    # DINH NGHIA API POST CHO SWAGGER ----------------------------------------------------------------------------------------------------------------
    @swagger_auto_schema(tags=["FeedRecords"], request_body=FeedRecordCreate, responses={201: BaseSerializerFeedRecord})
    def API_post(self, request):
        user = request.user
        serializer = FeedRecordCreate(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            
            # Goi toi service the them mot doi tuong moi vao database thong qua request ---- Kiem tra phan quyen user
            feedRecordId = FeedRecordService.create_feedRecord(user, serializer.validated_data)
            feedRecord = FeedRecordService.review_feedRecord_by_id(user, feedRecordId)
            return Response(feedRecord, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # DINH NGHIA API GET ALL CHO SWAGGER -------------------------------------------------------------------------------------------------------------
    @swagger_auto_schema(tags=["FeedRecords"], responses={200: BaseSerializerFeedRecord(many=True)})
    def API_all_get(self, request):
        user = request.user
        try:
            records = FeedRecordService.review_feedRecord(user)
            return Response(records, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # DINH NGHIA API GET BY ID CHO SWAGGER -----------------------------------------------------------------------------------------------------------
    @swagger_auto_schema(tags=["FeedRecords"], responses={200: BaseSerializerFeedRecord})
    def API_id_get(self, request, idFeedRecord=None):
        user = request.user
        try:
            record = FeedRecordService.review_feedRecord_by_id(user, idFeedRecord)
            return Response(record, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # DINH NGHIA API PUT CHO SWAGGER ----------------------------------------------------------------------------------------------------------------
    @swagger_auto_schema(tags=["FeedRecords"], request_body=FeedRecordUpdate, responses={200: BaseSerializerFeedRecord})
    def API_put(self, request, idFeedRecord=None):
        user = request.user
        serializer = FeedRecordUpdate(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            updated = FeedRecordService.update_feedRecord(user, idFeedRecord, serializer.validated_data)
            if "_id" in updated:
                updated["_id"] = str(updated["_id"])
            return Response(updated, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # DINH NGHIA API DELETE CHO SWAGGER -------------------------------------------------------------------------------------------------------------
    @swagger_auto_schema(tags=["FeedRecords"], responses={204: "No Content"})
    def API_delete(self, request, idFeedRecord=None):
        user = request.user
        try:
            FeedRecordService.delete_feedRecord(user, idFeedRecord)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
