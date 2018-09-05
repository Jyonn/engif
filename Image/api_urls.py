from django.urls import path

from Image.api_views import ImageView, ImageHistoryView

urlpatterns = [
    path('', ImageView.as_view()),
    path('history', ImageHistoryView.as_view()),
]
