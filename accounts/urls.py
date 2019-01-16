from django.urls import path
from . import views


urlpatterns = [
    path('login/',views.userlogin,name="userlogin"),
    path('logout/',views.userlogout,name="userlogout"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('signup/patient',views.patientsignup,name="patientusersignup"),
    path('signup/',views.patientsignup,name="patientusersignup"),
    path('signup/doctor',views.doctorsignup,name="doctorusersignup"),
]