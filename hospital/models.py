from urllib.request import URLError

from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import GEOSGeometry
from django.db import models
from geopy.geocoders.openmapquest import Nominatim
from geopy.exc import GeopyError
#from geopy.geocoders.googlev3 import GoogleV3
#from geopy.geocoders.googlev3 import GeocoderQueryError


class Hospital(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    location = gis_models.PointField(u"longitude/latitude",
                                     geography=True, blank=True, null=True)

    gis = gis_models.Manager()
    objects = models.Manager()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return '{},{}'.format(self.name,self.city)

    def save(self, **kwargs):
        if not self.location:
            address = u'%s %s' % (self.city, self.address)
            address = address.encode('utf-8')
            geocoder = Nominatim(user_agent='eHospitalNepal')
            try:
                _,latlon = geocoder.geocode('address')
            except (URLError,GeopyError,ValueError,TypeError):
                pass
            else:
                point = "POINT(%s %s)" % (latlon[1], latlon[0])
                self.location = GEOSGeometry(point, srid=4326)
        super(Hospital, self).save()