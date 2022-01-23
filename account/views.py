from django.shortcuts import render
from .serializers import AdminSerializer
from .models import AdminAccounts
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

class SearchAdmin(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk, format=None):
        if AdminAccounts.objects.filter(email=pk).exists():
            success = { 'detail': 'account exist' }
            return Response(success)
        else:
            failed = { 'detail': 'account does not exist' }
            return Response(failed)

    def post(self, request, pk, format=None):
        if AdminAccounts.objects.filter(username=pk).exists():
            success = { 'detail': 'account exist' }
            return Response(success)
        else:
            failed = { 'detail': 'account does not exist' }
            return Response(failed)
    

