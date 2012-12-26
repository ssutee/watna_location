from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django_countries import CountryField
from django_countries.fields import Country

class Location(models.Model):
    user = models.ForeignKey(User, null=True)
    place_name = models.CharField(max_length=200, verbose_name=_('Place name'))
    longitude = models.FloatField(verbose_name=_('Longitude'))
    latitude = models.FloatField(verbose_name=_('Latitude'))
    
    address = models.TextField(verbose_name=_('Address'))
    city = models.CharField(max_length=200, verbose_name=_('City'))
    country = CountryField(default='TH')
    phone_number = models.CharField(max_length=30, verbose_name=_('Phone number'))

    activities = models.ManyToManyField('Activity', related_name="locations", blank=True, null=True, verbose_name=_('Activities'))
    
    additional_info = models.TextField(verbose_name=_('Additional information'), blank=True, null=True)
    
    approved = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')
    
class Activity(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name=_('Name'), unique=True)

    class Meta:
        verbose_name_plural = _('Activities')
        verbose_name = _('Activity')

    def __unicode__(self):
        return u'%s' % (self.name)    