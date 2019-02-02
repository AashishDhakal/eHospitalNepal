from django.shortcuts import render
from .forms import patientusersignup,patientuserinfo,doctoruserinfo,doctorusersignup,ReportUploadForm,SendSMSForm,SMSForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import reverse 
from django.contrib.auth.decorators import login_required
from appointments.models import Appointment,Message,PMessage,Doctor
from .models import Patient,ReportUpload,Ambulance,Pathology
from twilio.rest import Client

@login_required(login_url='/accounts/login/')
def dashboard(request):
    appointments=Appointment.objects.filter(user=request.user.id)
    dappointments=Appointment.objects.filter(doctor=request.user.id)
    inbox=Appointment.objects.filter(doctor=request.user.id)
    sent=Appointment.objects.filter(user=request.user.id)
    dinbox=Message.objects.filter(user=request.user.id)
    dsent=Message.objects.filter(doctor=request.user.id)
    psent=PMessage.objects.filter(user=request.user.id)
    pinbox=PMessage.objects.filter(doctor=request.user.id)
    is_patient = Patient.objects.filter(user=request.user.id)
    reports = ReportUpload.objects.filter(user=request.user.id)
    doctorbalance = 0
    patientbalance = 0
    try:
        patientbalance = Patient.objects.filter(user=request.user.id).values_list('balance',flat=True)[0]
        doctorbalance = Doctor.objects.filter(user=request.user.id).values_list('balance',flat=True)[0]
    except IndexError:
        pass
    for appointment in appointments:
        patientbalance = patientbalance - 50
    for appointment in dappointments:
        doctorbalance = doctorbalance + 50
    return render(request,"accounts/dashboard.html",{'appointments':appointments,'dappointments':dappointments,'inbox':inbox,'sent':sent,'dinbox':dinbox,'dsent':dsent,'pinbox':pinbox,'psent':psent,'is_patient':is_patient,'reports':reports,'doctorbalance':doctorbalance,'patientbalance':patientbalance})

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

            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']
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
            doctor.is_active = False
            doctor.save()

            profile=doctoruserinfo_form.save(commit=False)
            profile.user=doctor

            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']
            profile.save()
            
            registered=True
        else:
            print(doctorusersignup_form.errors,doctoruserinfo_form.errors)
    else:
        doctorusersignup_form=doctorusersignup()
        doctoruserinfo_form=doctoruserinfo()
    
    return render(request,"accounts/signup.html",{'usersignup_form':doctorusersignup_form,'userinfo_form':doctoruserinfo_form,'registered':registered})

def reportupload(request):
    if request.POST:
        reportuploadform = ReportUploadForm(request.POST,request.FILES)
        if reportuploadform.is_valid():
            reportuploadform.save()
            return HttpResponse("File Uploaded")
    else:
        reportuploadform = ReportUploadForm()
    return render(request,"accounts/reportupload.html",{'reportuploadform':reportuploadform})

def sendmessage(request):
    if request.POST:
        form = SendSMSForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['full_name']
            text = form.cleaned_data['location']
            global phone_number 
            phone_number= form.cleaned_data['phone_number']
            smsbody = "{} needs an ambulance at {} Contact:{} . If you are available reply this message with 'yes' else ignore this message. ".format(name,text,phone_number)
            client = Client('AC665bee72b19abfcec12478cfae131d5a', 'b6b3158813ba7f0a57fb27da46afe0a6')
            recipients = Ambulance.objects.all()
            for number in recipients:
                client.messages.create(body=smsbody,to=number.phone_number, from_='+12039416081')
                print(number.phone_number)
    else:
        form = SendSMSForm()
    return render(request, 'accounts/smsform.html', {'form':form})

@csrf_exempt
def replymessage(request):
    client = Client('AC665bee72b19abfcec12478cfae131d5a', 'b6b3158813ba7f0a57fb27da46afe0a6')
    message=client.messages.create(body='Your Ambulance is on its way',to=phone_number, from_='+12039416081')
    return HttpResponse(message.sid)
   
def sendmessagetest(request):
    if request.POST:
        form = SMSForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['full_name']
            text = form.cleaned_data['location']
            type = form.cleaned_data['test_type']
            global test_phone_number
            test_phone_number= form.cleaned_data['phone_number']
            smsbody = "{} needs {} at {} Contact:{} . If you are available reply this message with 'yes' else ignore this message. ".format(name,type,text,test_phone_number)
            client = Client('ACe7a53ba58797cb785d65dd63e359dbef', 'e14769933efc0eae653544bbb3792f15')
            recipients = Pathology.objects.all()
            for number in recipients:
                client.messages.create(body=smsbody,to=number.phone_number, from_='+12039873594')
                print(number.phone_number)
    else:
        form = SMSForm()
    return render(request, 'accounts/testsmsform.html', {'form':form})


@csrf_exempt
def replymessagetest(request):
    client = Client('ACe7a53ba58797cb785d65dd63e359dbef', 'e14769933efc0eae653544bbb3792f15')
    message=client.messages.create(body='Your pathologist is on his/her way',to=test_phone_number, from_='+12039873594')
    return HttpResponse(message.sid)



