from django.urls import path
from .views import AgentMetricsView

urlpatterns = [
    path('metrics/', AgentMetricsView.as_view(), name='agent_metrics'),
]
