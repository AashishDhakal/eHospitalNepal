from django.shortcuts import render

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import fromstr
from django.contrib.gis import measure
from geopy.geocoders import Nominatim
from django.contrib.auth.decorators import login_required
#from django.contrib.gis.geoip2 import GeoIP2



from hospital import forms
from hospital import models

def geocode_address(address):
    geocoder = Nominatim(user_agent='eHospitalNepal')
    latlon = geocoder.geocode(address)
    return latlon


def get_hospitals(latitude,longitude):
    #g = GeoIP2()
    #current_point = Point(g.lat_lon('google.com.np'))
    #print(current_point)
    current_point = fromstr('POINT(%s %s)' % (latitude,longitude))
    hospitals = models.Hospital.objects.filter(location__distance_lte=(current_point, measure.D(km=10))).annotate(distance=Distance('location' , current_point)).order_by('distance')
    return hospitals

@login_required(login_url='/accounts/login/')
def home(request):
    form = forms.AddressForm()
    hospitals = []
    if request.POST:
        form = forms.AddressForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            location = geocode_address(address)
            if location:
                hospitals = get_hospitals(location.latitude,location.longitude)
    return render(request,
        'hospital/nearbyhospital.html',
        {'form': form, 'hospitals': hospitals})

def embed(request):
    form = forms.AddressForm()
    hospitals = []
    if request.POST:
        form = forms.AddressForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            location = geocode_address(address)
            if location:
                hospitals = get_hospitals(location.latitude,location.longitude)
    return render(request,
        'hospital/near.html',
        {'form': form, 'hospitals': hospitals})
