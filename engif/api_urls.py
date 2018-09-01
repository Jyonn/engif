from django.urls import path, include

urlpatterns = [
    path('image/', include('Image.api_urls'))
]
