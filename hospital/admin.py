from django.contrib import admin
from django.contrib.gis import admin
from .models import Hospital


admin.site.register(Hospital,admin.OSMGeoAdmin)
