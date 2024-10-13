# urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path as url
from . import views

urlpatterns = [
    url(r'^upload/*', views.upload_image, name='upload_image'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
