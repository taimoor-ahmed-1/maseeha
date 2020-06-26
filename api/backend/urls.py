from django.urls import include, path
from rest_framework import routers
from . import views
from django.conf.urls.static import static
from django.conf.urls import include
from django.conf import settings

urlpatterns = [
    path('speech/',views.Speech.as_view()),
    path('emergency/',views.Emergency.as_view()),
    path('corona/',views.Corona.as_view()),
]
