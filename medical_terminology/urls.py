from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from assessments import views  # Importing the home view

urlpatterns = [
    path("", views.home, name="home"),  # Home page path
    path("admin/", admin.site.urls),  # Admin site path
    path(
        "assessments/", include("assessments.urls")
    ),  # Including the assessments app URLs
    path("ckeditor5/", include("django_ckeditor_5.urls")),
]

# Media file handling during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
