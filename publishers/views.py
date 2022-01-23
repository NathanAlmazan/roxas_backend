#libraries and deco
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.http import Http404
from django.utils import timezone
from datetime import timedelta
#project classes
from .models import Publishers, Deleted
from .serializers import PublisherSerializer, RemovedSerializer
from report.models import Report
#csrf
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie

def get_current_month():
    months_review = [30, 60, 90, 120, 150, 180]
    year = ["m", "january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
    month_reviewed = []
    current_date = timezone.localdate()
    for month in months_review:
        report_date = current_date - timedelta(days=month)
        current_month = report_date.month
        month_reviewed.append(year[current_month])

    return month_reviewed

def get_current_year():
    current_date = timezone.localdate()
    report_date = current_date - timedelta(days=27)
    current_year = report_date.year

    return current_year

# publisher views
class PublisherList(APIView):

    permission_classes = [AllowAny]
    def get(self, request, pk, format=None):
        publishers = Publishers.objects.filter(group=pk)
        serializer = PublisherSerializer(publishers, many=True)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        publisher_update = Publishers.objects.get(id=pk)
        serializer = PublisherSerializer(instance=publisher_update, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ServiceGroup(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        service_group = Publishers.objects.filter(group=pk)
        serializer = PublisherSerializer(service_group, many=True)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        pub = Publishers.objects.get(id=pk)
        deleted_pub = Deleted(name=pub.name, group=pub.group, birthday=pub.birthday, baptismal_date=pub.baptismal_date, contact=pub.contact, email=pub.email)
        deleted_pub.save()
        pub.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PublisherSearch(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, sr, format=None):
        service_publishers = Publishers.objects.filter(name__icontains=sr)
        serializer = PublisherSerializer(service_publishers, many=True)
        return Response(serializer.data)

    def post(self, request, sr, format=None):
        if Publishers.objects.filter(id=sr).exists():
            publisher_update = Publishers.objects.get(id=sr)
            serializer = PublisherSerializer(instance=publisher_update, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = PublisherSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ElderSearch(APIView):
    permission_classes = [AllowAny]

    def get(self, request, sr, format=None):
        service_publishers = Publishers.objects.filter(name__icontains=sr, elder=True)
        serializer = PublisherSerializer(service_publishers, many=True)
        return Response(serializer.data)

    def post(self, request, sr, format=None):
        service_group = Publishers.objects.get(name=sr)
        serializer = PublisherSerializer(service_group, many=False)
        return Response(serializer.data)

class CheckInactive(APIView):
    permission_classes = [AllowAny]

    def post(self, request, pk, format=None):
        publishers = Publishers.objects.filter(group=pk)
        months = get_current_month()
        current_year = get_current_year()

        for pub in publishers:
            counter = 0
            for check in months:
                if Report.objects.filter(publisher=pub.id, year=current_year, month=check).exists() == False:
                    counter += 1
            
            if counter > 2 and counter < 5:
                pub.irregular = True
                pub.save()
            elif counter > 4 and counter < 7:
                pub.inactive = True
                pub.save()
            elif counter < 2:
                pub.irregular = False
                pub.inactive = False
                pub.save()

        return Response(status=status.HTTP_201_CREATED)
    
    def get(self, request, pk, format=None):
        removed = Deleted.objects.all()
        serializer = RemovedSerializer(removed, many=True)
        return Response(serializer.data)








