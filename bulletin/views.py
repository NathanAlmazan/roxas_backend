from django.shortcuts import render
from .serializers import BulletinSerializer
from .models import Bulletin
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
# Create your views here.

class BulletinView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        today = timezone.localdate() - timedelta(days=2)
    
        posts = Bulletin.objects.filter(meeting_date__gte=today).order_by('meeting_date')
        serializer = BulletinSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        posts_serializer = BulletinSerializer(data=request.data)
        if posts_serializer.is_valid():
            posts_serializer.save()
            return Response(posts_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(posts_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeletePost(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, format=None):
        post = Bulletin.objects.get(id=pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



