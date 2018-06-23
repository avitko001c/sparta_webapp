from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework.schemas import get_schema_view
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token
from rest_framework import routers
from . import views

app_name="apis"

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'sshkeys', views.SSHKeyViewSet)

urlpatterns = [
    path("", get_schema_view(), name="list"),
    path("~auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("~echo/", view=views.EchoView.as_view(), name="echo"),
    path("~auth/token/obtain/", obtain_jwt_token),
    path("~auth/token/verify/", verify_jwt_token),
]

urlpatterns += router.urls
