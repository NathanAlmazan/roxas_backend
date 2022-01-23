#libraries and deco
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.http import Http404
#project classes
from .models import Report, get_current_year, Pioneer
from publishers.models import Publishers
from .serializers import ReportSerializer, PioneerSerializer
import json

#Save Report
class SaveReport(APIView):
    permission_classes = [IsAuthenticated]
    year = get_current_year()

    def post(self, request, pk, mt, yr, format=None):
        if Report.objects.filter(publisher=pk, month=mt, year=self.year, pending=False).exists():
            report_exist = { 'alert': 'report already exist' }
            return Response(report_exist)
        else:
            json_request = json.dumps(request.data)
            request_data = json.loads(json_request)

            if Pioneer.objects.filter(publisher=pk, month=mt, year=self.year).exists() or Publishers.objects.filter(id=pk, privilage='Auxillary Pioneer').exists():
                request_data['auxiPr'] = True
            else:
                request_data['auxiPr'] = False

            serializer = ReportSerializer(data=request_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, mt, yr, format=None):
        group_report = Report.objects.filter(publisher__group=pk, month=mt, year=yr)
        serializer = ReportSerializer(group_report, many=True)
        return Response(serializer.data)

class ReportCheck(APIView):
    permission_classes = [IsAuthenticated]
    year = get_current_year()

    def post(self, request, pk, mt, yr, format=None):
        pending_rep = Report.objects.filter(pending=True)
        serializer = ReportSerializer(pending_rep, many=True)
        return Response(serializer.data)

    def get(self, request, pk, mt, yr, format=None):
        reports = Report.objects.filter(publisher__group=pk, month=mt, year=yr)
        publishers = Publishers.objects.filter(group=pk)

        publisher_names = []
        for pub in publishers:
            publisher_names += [pub.name]

        report_data = []
        for rep in reports:
            report_data += [rep.publisher.name]
        
        no_report = []
        for name in publisher_names:
            reported = name in report_data
            if reported == False:
                no_report += [name]
        
        needs_report = { 'no_report': no_report }
       
        return Response(needs_report)

class CongPioneer(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pr, mt, yr, format=None):
        pr_report = Report.objects.filter(month=mt, year=yr)
        
        if pr == 'reg':
            regPioneers = Publishers.objects.filter(privilage='Regular Pioneer')

            reg_names = []
            for report in pr_report:
                if report.publisher.privilage == 'Regular Pioneer':
                    reg_names += [report.publisher.name]

            regular_pioneers = []
            for pioneer in regPioneers:
                regular_pioneers += [pioneer.name]

            no_report = []
            for name in regular_pioneers:
                reported = name in reg_names
                if reported == False:
                    no_report += [name]

        
            Regular_Pioneer = { 'Reported': reg_names, 'Not_Reported': no_report }
       
            return Response(Regular_Pioneer)

        elif pr == 'auxi':
            auxiPioneers = Pioneer.objects.filter(month=mt, year=yr)

            auxi_names = []
            for report in pr_report:
                if report.auxiPr == True:
                    auxi_names += [report.publisher.name]

            auxi_pioneers = []
            for pioneer in auxiPioneers:
                auxi_pioneers += [pioneer.publisher.name]

            no_report = []
            for name in auxi_pioneers:
                reported = name in auxi_names
                if reported == False:
                    no_report += [name]

        
            Auxilary_Pioneer = { 'Reported': auxi_names, 'Not_Reported': no_report }
       
            return Response(Auxilary_Pioneer)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ReportMonthSummary(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, mt, yr, format=None):
        report_update = Report.objects.get(id=mt)
        serializer = ReportSerializer(instance=report_update, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, mt, yr, format=None):
        month_reports = Report.objects.filter(month=mt, year=yr)

        month_hours = 0
        month_placements = 0
        month_videos = 0
        month_return_visits = 0
        month_bible_studies = 0
        total_publishers = 0

        auxi_hours = 0
        auxi_placements = 0
        auxi_videos = 0
        auxi_return_visits = 0
        auxi_bible_studies = 0
        total_auxi = 0

        regPr_hours = 0
        regPr_placements = 0
        regPr_videos = 0
        regPr_return_visits = 0
        regPr_bible_studies = 0
        total_regPr = 0

        for report in month_reports:
            hours = float(report.hours)
            placements = int(report.placements)
            videos = int(report.videos)
            return_visits = int(report.return_visit)
            bible_studies = int(report.bible_study)
                
            if report.auxiPr == True:
                auxi_hours += hours
                auxi_placements += placements
                auxi_videos += videos
                auxi_return_visits += return_visits
                auxi_bible_studies += bible_studies
                total_auxi += 1
            elif report.publisher.privilage == 'Regular Pioneer':
                regPr_hours += hours
                regPr_placements += placements
                regPr_videos += videos
                regPr_return_visits += return_visits
                regPr_bible_studies += bible_studies
                total_regPr += 1
            else:
                month_hours += hours
                month_placements += placements
                month_videos += videos
                month_return_visits += return_visits
                month_bible_studies += bible_studies
                total_publishers += 1


        pub_summary = { 'total_hours': month_hours, 'total_placements': month_placements, 'total_videos': month_videos, 'total_rv': month_return_visits, 'total_bs': month_bible_studies, 'total_pub': total_publishers }
        auxi_summary = { 'total_hours': auxi_hours, 'total_placements': auxi_placements, 'total_videos': auxi_videos, 'total_rv': auxi_return_visits, 'total_bs': auxi_bible_studies, 'total_pub': total_auxi }
        regPr_summary = { 'total_hours': regPr_hours, 'total_placements': regPr_placements, 'total_videos': regPr_videos, 'total_rv': regPr_return_visits, 'total_bs': regPr_bible_studies, 'total_pub': total_regPr }
        month_summary = { 'publishers': pub_summary, 'auxi': auxi_summary, 'regPr': regPr_summary }

        return Response(month_summary)

class publisher_history(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk, yr, format=None):

        report = Report.objects.filter(year=yr, publisher=pk)
        serializer = ReportSerializer(report, many=True)

        return Response(serializer.data)

    def post(self, request, pk, yr, format=None):
        json_request = json.dumps(request.data)
        request_data = json.loads(json_request)
        pub_ID = request_data['publisher']
        serializer = PioneerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            try: 
                report = Report.objects.get(publisher=pub_ID, month=pk, year=yr, pending=False)
                report.auxiPr = True
                report.save()
            except:
                pass
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk, yr, format=None):
        if yr == 'false':
            try:
                publisher = Publishers.objects.get(id=pk)
                publisher.privilage = 'Auxillary Pioneer'
                publisher.save()

            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_201_CREATED)
        else:
            try:
                publisher = Publishers.objects.get(id=pk)
                publisher.privilage = 'Publisher'
                publisher.save()
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_201_CREATED)