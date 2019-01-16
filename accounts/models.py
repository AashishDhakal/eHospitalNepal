from django.db import models

from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,unique=True)
    is_doctor=models.BooleanField('Doctor',default=False)
    is_patient=models.BooleanField('Patient',default=True)
    #profile_picture=models.ImageField(upload_to='profile_pics_patients',null=True,blank=True)

    def __str__(self):
        return self.user.username
