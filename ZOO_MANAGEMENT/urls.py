from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.shortcuts import redirect
from rest_framework.permissions import AllowAny
from decouple import config
from rest_framework.permissions import IsAuthenticated
from zoo_app.middleware.authentication import JWTAuthentication
from zoo_app.views.frontendView import home_page

# DINH NGHIA CAC THONG TIN VA PORT KHOI DONG-------------------------------------------------------------------------------------------
schema_view = get_schema_view(
    openapi.Info(
        title="ZOO MANAGEMENT API",
        default_version="v1",
        description="Secure Zoo Management API with JWT Authentication",
        contact=openapi.Contact(email=config("ADMIN_EMAIL", default="admin@example.com")),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[AllowAny],
    url='http://127.0.0.1:8000/api/',
)


# urlpatterns = [
#     path("", lambda request: redirect("/swagger/")),
#     path("admin/", admin.site.urls),
#     path("api/", include("zoo_app.urls")),
#     re_path(r"^swagger/$", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
#     re_path(r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
#     path('', home_page, name='home'),
# ]
urlpatterns = [
    path("", home_page, name="home"),
    path("admin/", admin.site.urls),
    path("api/", include("zoo_app.urls")),
    re_path(r"^swagger/$", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    re_path(r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

print("ZOO_MANAGEMENT urls loaded")