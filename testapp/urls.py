from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("adfs/", include("django_auth_adfs.urls")),
]
