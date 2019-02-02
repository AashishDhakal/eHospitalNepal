from django.db import models
from django.contrib.auth.models import User
from accounts.models import Patient
from hospital.models import Hospital
from django.utils import timezone


class Appointment(models.Model):
    """Contains info about appointment"""

    class Meta:
        unique_together = ('doctor', 'date', 'timeslot')
        get_latest_by = 'date'


    TIMESLOT_LIST = (
        (0, '09:00 – 10:00'),
        (1, '10:00 – 11:00'),
        (2, '11:00 – 12:00'),
        (3, '12:00 – 13:00'),
        (4, '13:00 – 14:00'),
        (5, '14:00 – 15:00'),
        (6, '15:00 – 16:00'),
        (7, '16:00 – 17:00'),
        (8, '17:00 – 18:00'),
    )
    user = models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE,related_name='sender')
    hospital = models.ForeignKey('hospital.Hospital',on_delete=models.CASCADE)
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE,related_name='reciever')
    date = models.DateField()
    timeslot = models.IntegerField(choices=TIMESLOT_LIST)
    patient_name = models.CharField(max_length=60)
    message = models.TextField(verbose_name='Symptoms',default='Fever')
    image = models.ImageField(verbose_name='Symptoms Image',null=True,blank=True)
    creation_date = models.DateTimeField(null=True,blank=True)


    def __str__(self):
        return '{} {} {}. Patient: {}'.format(self.date, self.time, self.doctor, self.patient_name)
 
    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = timezone.now()
        return super(Appointment, self).save(*args, **kwargs)

    @property
    def time(self):
        return self.TIMESLOT_LIST[self.timeslot][1]


class Doctor(models.Model):
    """Stores info about doctor"""
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20)
    NMC_Number = models.IntegerField(default=12345)
    is_doctor = models.BooleanField('Doctor',default=True)
    is_patient = models.BooleanField('Patient',default=False)
    profile_picture=models.ImageField(upload_to='profilepics_doctor',null=True,blank=True)
    specialty = models.CharField(max_length=20)
    balance = models.IntegerField(default=0)
    hospital = models.ForeignKey('hospital.Hospital',on_delete=models.CASCADE)

    def __str__(self):
        return '{}.{} {}'.format(self.specialty, self.short_name,self.hospital)

    @property
    def short_name(self):
        return '{} {}.{}.'.format(self.last_name.title(), self.first_name[0].upper(), self.middle_name[0].upper())

class Message(models.Model):
    user = models.ForeignKey('accounts.Patient',on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(verbose_name='Message',default='Visit Hospital')
    creation_date = models.DateTimeField(null=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = timezone.now()
        return super(Message, self).save(*args, **kwargs)

    def __str__(self):
        return '{} to {}'.format(self.user,self.doctor)

class PMessage(models.Model):
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.TextField(verbose_name='Message',default='Visit Hospital')
    creation_date = models.DateTimeField(null=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = timezone.now()
        return super(PMessage, self).save(*args, **kwargs)
    def __str__(self):
        return '{} to {}'.format(self.user,self.doctor)


