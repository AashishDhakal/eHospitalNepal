
from django.contrib.gis.db import models
from django.contrib.gis.geos import fromstr
from geopy.geocoders import Nominatim

class Hospital(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    location = models.PointField(u'latitude/longitude',geography=True,blank=True, null=True)
    logo = models.ImageField(upload_to='logo',blank=True,null=True)

    objects = models.Manager()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return '{},{}'.format(self.name,self.city)

    @property
    def popupContent(self):
      return '<p>{}</p><p><{}</p>'.format(
          self.name,
          self.location)

    def save(self, **kwargs):
        if not self.location:
            address = u'{0},{1}'.format(self.address,self.city)
            geocoder = Nominatim(user_agent='eHospitalNepal')
            loc = geocoder.geocode(address)
            point = "POINT({0} {1})".format(loc.latitude,loc.longitude)
            print(point)
            self.location = fromstr(point)
            print(self.location)
        super(Hospital, self).save()
