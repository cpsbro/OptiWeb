from django.urls import path
from .views import RegisterUserView, LoginUserView, UserMetricsView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('metrics/', UserMetricsView.as_view(), name='user-metrics'),
]
