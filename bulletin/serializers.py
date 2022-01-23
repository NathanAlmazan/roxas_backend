from rest_framework import serializers
from .models import Bulletin

class BulletinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bulletin
        fields = ( 'id', 'uploaded_by', 'uploaded_for', 'meeting_date', 'image')