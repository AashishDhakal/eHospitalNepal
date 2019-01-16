from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required


from .forms import AppointmentForm

@login_required(login_url='/accounts/login/')
def new_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = AppointmentForm()
    return render(request,'appointments/makeappointment.html',{'form': form})

