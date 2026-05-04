from django.urls import path
from .views import PredictFailureView

urlpatterns = [
    path('predict/', PredictFailureView.as_view(), name='predict_failure'),
]
