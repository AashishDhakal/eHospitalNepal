from django.contrib import admin
from .models import Appointment, Doctor,Message,PMessage

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['user','doctor', 'date', 'timeslot', 'patient_name']
    list_filter = ['user', ]

admin.site.register(Appointment,AppointmentAdmin)
admin.site.register(Doctor)
admin.site.register(Message)
admin.site.register(PMessage)



