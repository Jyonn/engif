from django.urls import path

from Image.api_views import ImageView

urlpatterns = [
    path('', ImageView.as_view()),
]
