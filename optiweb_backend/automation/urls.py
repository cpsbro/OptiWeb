from django.urls import path
from .views import FixIssueView, GetAutomationLogsView

urlpatterns = [
    path('fix_issue/', FixIssueView.as_view(), name='fix_issue'),
    path('logs/', GetAutomationLogsView.as_view(), name='get_automation_logs'),
]
