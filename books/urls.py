from django.urls import path, include
from .views import AuthorsView

urlpatterns = [
    path('authors/', AuthorsView.as_view(), name='authors'),
]
