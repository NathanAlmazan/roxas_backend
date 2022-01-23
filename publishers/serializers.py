from rest_framework import serializers
from .models import Publishers, Deleted

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publishers
        fields = '__all__'

class RemovedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deleted
        fields = '__all__'