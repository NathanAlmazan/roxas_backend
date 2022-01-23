from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from publishers import views

urlpatterns = [
    path('publisher-list/<str:pk>', views.PublisherList.as_view(), name='publisher_list'),
    path('publisher-search/<str:sr>', views.PublisherSearch.as_view(), name='publisher_search'),
    path('elder-search/<str:sr>', views.ElderSearch.as_view(), name='elder_search'),
    path('service-group/<str:pk>', views.ServiceGroup.as_view(), name='service_group'),
    path('inactive/<str:pk>', views.CheckInactive.as_view(), name='inactive')

]
