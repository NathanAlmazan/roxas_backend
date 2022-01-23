from django.urls import path
from account import views

urlpatterns = [
    path('account-search/<str:pk>', views.SearchAdmin.as_view(), name= 'account_search'),
]