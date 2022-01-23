from django.db import models
from datetime import date
from publishers.models import Publishers

# Create your models here.
class Bulletin(models.Model):
    purposes = [
        ('Announcement', 'Announcement'),
        ('Midweek Meeting Schedule', 'Midweek Meeting Schedule'),
        ('Field Service Schedule', 'Field Service Schedule'),
        ('Weekend Meeting Schedule', 'Weekend Meeting Schedule')
    ]

    uploaded_by = models.ForeignKey(Publishers, default=0, on_delete=models.SET_DEFAULT)
    uploaded_for = models.CharField(max_length=50, choices=purposes, default='Announcement')
    meeting_date = models.DateField(null=False, default=date.today)
    image = models.ImageField(upload_to='post_images')
    