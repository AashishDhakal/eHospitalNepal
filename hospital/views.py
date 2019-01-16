from django.shortcuts import render

from urllib.request import URLError
from django.contrib.gis.db.models.functions import Distance

from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis import measure
from django.shortcuts import render_to_response
from django.template import RequestContext
from geopy.geocoders.openmapquest import Nominatim
from geopy.exc import GeopyError
from django.contrib.auth.decorators import login_required

#from geopy.geocoders.googlev3 import GoogleV3
#from geopy.geocoders.googlev3 import GeocoderQueryError



from hospital import forms
from hospital import models

def geocode_address(address):
    address = address.encode('utf-8')
    geocoder = Nominatim(user_agent='eHospitalNepal')
    try:
        _,latlon = geocoder.geocode('address')
    except (URLError,GeopyError,ValueError,TypeError):
        return None
    else:
        return latlon

def get_hospitals(longitude, latitude):
    current_point = GEOSGeometry('POINT(%s %s)' % (longitude,latitude), srid=4326)
    hospitals = models.Hospital.gis.filter(location__distance_lte=(current_point, measure.D(km=10))).annotate(distance=Distance('location' , current_point)).order_by('distance')
    #hospitals = hospitals.annotate(distance=Distance('location' , current_point)).order_by('distance')
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
                latitude, longitude = location
                hospitals = get_hospitals(longitude,latitude)
    return render(request,
        'hospital/nearbyhospital.html',
        {'form': form, 'hospitals': hospitals})
