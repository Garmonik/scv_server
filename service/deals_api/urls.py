from django.urls import path
from .views import DealUploadView, TopClientsView

urlpatterns = [
    path('upload/', DealUploadView.as_view()),
    path('top-clients/', TopClientsView.as_view()),
]