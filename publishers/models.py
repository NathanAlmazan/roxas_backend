from django.db import models

# Create your models here.
class Publishers(models.Model):
    publisher_privilage = [
        ('Publisher', 'Publisher'),
        ('Unbaptized Publisher', 'Unbaptized Publisher'),
        ('Auxillary Pioneer', 'Auxillary Pioneer'),
        ('Regular Pioneer', 'Regular Pioneer')
    ]

    name = models.CharField(max_length=50)
    group = models.IntegerField(null=False, default=0)
    birthday = models.DateField(null=True, blank=True)
    baptismal_date = models.DateField(null=True, blank=True)
    contact = models.CharField(blank=True, max_length=12)
    email = models.EmailField(blank=True)
    privilage = models.CharField(max_length=50, choices=publisher_privilage, default='Publisher')
    elder = models.BooleanField(null=False, default=False)
    irregular = models.BooleanField(null=True, default=False)
    inactive = models.BooleanField(null=True, default=False)

    def __str__(self):
        return self.name
    
class Deleted(models.Model):
    name = models.CharField(max_length=50)
    group = models.IntegerField(null=False, default=0)
    birthday = models.DateField(null=True)
    baptismal_date = models.DateField(null=True)
    contact = models.CharField(blank=True, max_length=12)
    email = models.EmailField(blank=True)
    date_leaved = models.DateTimeField(auto_now_add=True)