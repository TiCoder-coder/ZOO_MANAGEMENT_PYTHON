from rest_framework.routers import DefaultRouter
from zoo_app.views.managersView import ManagerViewSet
from django.urls import path, include
from zoo_app.views.authsView import LoginView, RefreshView, VerifyView, LogoutView
from zoo_app.views.animalsView import AnimalView
from zoo_app.views.enclosuresView import EnclosureView
from zoo_app.views.feedRecordsView import FeedRecordView
from zoo_app.views.foodsView import FoodView
router = DefaultRouter()


# PHAN CHIA CAC API THANH CAC TAP--------------------------------------------------------------------------------------------------------
router.register(r"managers", ManagerViewSet, basename="managers")
print("EnclosureView loaded:", EnclosureView)

urlpatterns = [
    
    # Auth endpoints
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/refresh/", RefreshView.as_view(), name="token_refresh"),
    path("auth/verify/", VerifyView.as_view(), name="token_verify"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),

    # Include router
    path("api/", include(router.urls)),                                                         # Dam bao cho manage nam trong the thuc thi

    # Animals endpoints
    path("animals/", AnimalView.as_view({"get": "API_all_get", "post": "API_post"}), name="animal_list"),
    path("animals/<str:idAnimal>/", AnimalView.as_view({
        "get": "API_id_get",
        "put": "API_put",
        "delete": "API_delete"
    }), name="animal_detail"),

    # Enclosures endpoints
    path("enclosures/", EnclosureView.as_view({"get": "API_all_get", "post": "API_post"}), name="enclosure_list"),
    path("enclosures/<str:idEnclosure>/", EnclosureView.as_view({
        "get": "API_id_get",
        "put": "API_put",
        "delete": "API_delete"
    }), name="enclosure_detail"),

    # Foods endpoints
    path("api/foods/", FoodView.as_view({"get": "API_all_get", "post": "API_post"}), name="food_list"),
    path("api/foods/<str:idFood>/", FoodView.as_view({
        "get": "API_id_get",
        "put": "API_put",
        "delete": "API_delete"
    }), name="food_detail"),

    # FeedRecords endpoints
    path("api/feedRecords/", FeedRecordView.as_view({"get": "API_all_get", "post": "API_post"}), name="feedrecord_list"),
    path("api/feedRecords/<str:idFeedRecord>/", FeedRecordView.as_view({
        "get": "API_id_get",
        "put": "API_put",
        "delete": "API_delete"
    }), name="feedrecord_detail"),
]
