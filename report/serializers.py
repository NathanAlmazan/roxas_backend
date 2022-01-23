from rest_framework import serializers
from .models import Report, Pioneer

class ReportSerializer(serializers.ModelSerializer):
    publisher_name = serializers.CharField(source='publisher.name', read_only=True)

    class Meta:
        model = Report
        fields = ['id', 'publisher', 'publisher_name', 'group', 'month', 'year', 'hours', 'placements', 'videos', 'return_visit', 'bible_study', 'remarks', 'pending', 'auxiPr']

class PioneerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pioneer
        fields = '__all__'