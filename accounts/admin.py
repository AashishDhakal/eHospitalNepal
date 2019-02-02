from django.contrib import admin
from .models import Patient,ReportUpload,Ambulance,Pathology

# Register your models here.
admin.site.register(Patient)
admin.site.register(ReportUpload)
admin.site.register(Ambulance)
admin.site.register(Pathology)