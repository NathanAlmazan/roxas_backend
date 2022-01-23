from django.db import models
from datetime import timedelta
from django.utils import timezone
from publishers.models import Publishers

# Get Current Year
def get_current_year():
    current_date = timezone.localdate()
    report_date = current_date - timedelta(days=27)
    current_year = report_date.year

    return current_year

# Report Model
class Report(models.Model):
    publisher = models.ForeignKey(Publishers, null=True, on_delete=models.SET_NULL)
    group = models.IntegerField(null=False, default=0)
    month = models.CharField(max_length=50)
    year = models.IntegerField(null=False, default=get_current_year)
    hours = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    placements = models.IntegerField(null=False, default=0)
    videos = models.IntegerField(null=False, default=0)
    return_visit = models.IntegerField(null=False, default=0)
    bible_study = models.IntegerField(null=False, default=0)
    remarks = models.TextField(max_length=200, blank=True)
    pending = models.BooleanField(null=True, default=False)
    auxiPr = models.BooleanField(null=False, default=False)

    def __str__(self):
        return self.month

class Pioneer(models.Model):
    publisher = models.ForeignKey(Publishers, null=True, on_delete=models.SET_NULL)
    auxi_pioneer = models.BooleanField(null=True, default=True)
    month = models.CharField(max_length=50)
    year = models.IntegerField(null=False, default=get_current_year)