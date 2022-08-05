from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.loading, name='loading'),
    path('calendar/', views.index, name='index'),
    path('home/', views.home, name='home'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)