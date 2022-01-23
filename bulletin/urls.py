from django.urls import path
from bulletin import views

urlpatterns = [
    path('post', views.BulletinView.as_view(), name= 'bulletin_posts'),
    path('delete/<str:pk>', views.DeletePost.as_view(), name= 'delete_posts')
]
