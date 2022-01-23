from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from report import views

urlpatterns = [
    path('save-report/<str:pk>/<str:mt>/<str:yr>', views.SaveReport.as_view(), name='save_report'),
    path('no-report/<str:pk>/<str:mt>/<str:yr>', views.ReportCheck.as_view(), name='no_report'),
    path('month-sum/<str:mt>/<str:yr>', views.ReportMonthSummary.as_view(), name='report_summary'),
    path('pub-report/<str:pk>/<str:yr>', views.publisher_history.as_view(), name='publisher_report'),
    path('pioneers/<str:pr>/<str:mt>/<str:yr>', views.CongPioneer.as_view(), name='pioneer_report_')
]
