from django.db import models

from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,unique=True)
    is_doctor=models.BooleanField('Doctor',default=False)
    is_patient=models.BooleanField('Patient',default=True)
    profile_picture=models.ImageField(upload_to='profilepics_patient',null=True,blank=True)
    address = models.CharField(default='ktm',max_length=50)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class ReportUpload(models.Model):
    user = models.ForeignKey('accounts.Patient',on_delete=models.CASCADE)
    report_name = models.CharField(max_length=250)
    report_date = models.DateField()
    report = models.FileField(upload_to='medicalreports',null=True,blank=True)

    def __str__(self):
        return '{},{}'.format(self.report_name,self.report_date)


class Ambulance(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return '{} {} {}'.format(self.first_name,self.last_name,self.phone_number)

class Pathology(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return '{} {} {}'.format(self.first_name, self.last_name, self.phone_number)