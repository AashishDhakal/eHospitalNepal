from django.shortcuts import render
from .forms import patientusersignup,patientuserinfo,doctoruserinfo,doctorusersignup

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import reverse 
from django.contrib.auth.decorators import login_required
from appointments.models import Appointment

@login_required(login_url='/accounts/login/')
def dashboard(request):
    appointments=Appointment.objects.filter(user=request.user.id)
    return render(request,"accounts/dashboard.html",{'appointments':appointments})

@login_required
def userlogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))


def userlogin(request):
    if request.POST:
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('dashboard'))
            else:
                return HttpResponse("Account Not Active")
        else:
            print("Username:{} and Password:{} didnt match".format(username,password))
            return HttpResponse("Invalid Login")
    return render(request,"accounts/login.html",{})

def patientsignup(request):
    registered=False
    if request.POST:
        patientusersignup_form = patientusersignup(data=request.POST)
        patientuserinfo_form=patientuserinfo(data=request.POST)
        
        if patientusersignup_form.is_valid() and patientuserinfo_form.is_valid():
            patient=patientusersignup_form.save()
            patient.set_password(patient.password)
            patient.save()

            profile=patientuserinfo_form.save(commit=False)
            profile.user=patient

            #if 'profile_picture' in request.FILES:
            #    profile.profile_picture = request.FILES['profile_picture']
            profile.save()

            registered=True
        else:
            print(patientusersignup_form.errors,patientuserinfo_form.errors)
    else:
        patientusersignup_form=patientusersignup()
        patientuserinfo_form=patientuserinfo()
    
    return render(request,"accounts/signup.html",{'usersignup_form':patientusersignup_form,'userinfo_form':patientuserinfo_form,'registered':registered})


def doctorsignup(request):
    registered=False
    if request.POST:
        doctorusersignup_form = doctorusersignup(data=request.POST)
        doctoruserinfo_form=doctoruserinfo(data=request.POST)
        
        if doctorusersignup_form.is_valid() and doctoruserinfo_form.is_valid():
            doctor=doctorusersignup_form.save()
            doctor.set_password(doctor.password)
            doctor.save()

            profile=doctoruserinfo_form.save(commit=False)
            profile.user=doctor
            profile.save()

            #if 'profile_picture' in request.FILES:
            #    profile.profile_picture = request.FILES['profile_picture']
            registered=True
        else:
            print(doctorusersignup_form.errors,doctoruserinfo_form.errors)
    else:
        doctorusersignup_form=doctorusersignup()
        doctoruserinfo_form=doctoruserinfo()
    
    return render(request,"accounts/signup.html",{'usersignup_form':doctorusersignup_form,'userinfo_form':doctoruserinfo_form,'registered':registered})
