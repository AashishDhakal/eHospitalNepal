from django.shortcuts import render,redirect,get_object_or_404,reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.template.loader import render_to_string
import weasyprint
from .models import Appointment,Doctor
from accounts.models import Patient
from .forms import AppointmentForm
from .forms import MessageForm,PMessageForm

@login_required(login_url='/accounts/login/')
def new_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST,request.FILES)
        if form.is_valid():
            appnt=form.save(commit=False)
            appnt.user = request.user
            appnt.save()
            return HttpResponseRedirect(reverse('viewticket', args=(appnt.pk,)))
    else:
        form = AppointmentForm()
    return render(request,'appointments/makeappointment.html',{'form': form})

@login_required(login_url='/accounts/login')
def new_message(request):
    if request.method == 'POST':
        messageform = MessageForm(request.POST)
        if messageform.is_valid():
            msg=messageform.save(commit=False)
            msg.doctor = request.user
            msg.save()
            return HttpResponse("Message Sent")
    else:
        messageform = MessageForm()
    return render(request,'appointments/newmessage.html',{'messageform':messageform})

@login_required(login_url='/accounts/login')
def pmessage(request):
    if request.method == 'POST':
        messageform = PMessageForm(request.POST)
        if messageform.is_valid():
            msg=messageform.save(commit=False)
            msg.user = request.user
            msg.save()
            return HttpResponse("Message Sent")
    else:
        messageform = PMessageForm()
    return render(request,'appointments/newmessage.html',{'messageform':messageform})
            

def ticket(request,appointment_id):
    appointmentticket = get_object_or_404(Appointment,id=appointment_id)
    html = render_to_string('pdf.html',{'appointmentticket':appointmentticket})
    response = HttpResponse(content_type='application/pdf')
    response['content-deposition'] = 'filename = "appointment.{}.pdf"'.format(appointment_id)
    weasyprint.HTML(string=html,base_url=request.build_absolute_uri()).write_pdf(response,stylesheets = [weasyprint.CSS(settings.STATIC_DIR + '/pdf.css')])
    return response

