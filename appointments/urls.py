from django.urls import path
from . import views


urlpatterns = [
    path('',views.new_appointment,name="makeappointment"),
    path('message/doctor',views.new_message,name="dmessage"),
    path('message/patient',views.pmessage,name="pmessage"),
    path('ticket/<appointment_id>',views.ticket,name='viewticket'),
]