from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer

Admin = get_user_model()

class AdminSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = Admin
        fields = ('email', 'username', 'contact', 'group', 'password', 'is_staff', 'is_superuser')