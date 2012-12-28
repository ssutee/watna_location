from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django_countries import CountryField
from django_countries.fields import Country

class Profile(models.Model):
    user = models.OneToOneField(User)

    map_type = models.CharField(max_length=10, default='ROADMAP')

class Status(models.Model):
    name = models.CharField(max_length=200, db_index=True, 
        verbose_name=_('Name'), unique=True)
    
    class Meta:
        verbose_name = _('Status')
        verbose_name_plural = _('Status')

    def __unicode__(self):
        return u'%s' % (self.name)
        
class Location(models.Model):
    user = models.ForeignKey(User, null=True)
    place_name = models.CharField(max_length=200, verbose_name=_('Place name'))
    organization = models.BooleanField(verbose_name=_('Organization'))
    status = models.ForeignKey(Status, verbose_name=_('Status'),
        related_name="locations", null=True)

    longitude = models.FloatField(verbose_name=_('Longitude'))
    latitude = models.FloatField(verbose_name=_('Latitude'))
    
    address = models.TextField(verbose_name=_('Address'))
    city = models.CharField(max_length=200, verbose_name=_('City'))
    country = CountryField(default='TH')
    phone_number = models.CharField(max_length=30, verbose_name=_('Phone number'))

    activities = models.ManyToManyField('Activity', related_name="locations", 
        blank=True, null=True, verbose_name=_('Activities'))
    
    additional_info = models.TextField(verbose_name=_('Additional information'), 
        blank=True, null=True)
    
    approved = models.BooleanField(default=False)
        
    class Meta:
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')

    def __unicode__(self):
        return u'%s' % (self.place_name)

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^location\.models\.ColorModelField"])

class ColorModelField(models.CharField):
    pass

class Activity(models.Model):
    name = models.CharField(max_length=200, db_index=True, 
        verbose_name=_('Name'), unique=True)
    priority = models.IntegerField(verbose_name=_('Priority'), 
        default=0)
    color = ColorModelField(max_length=7, verbose_name=_('Color'), 
        default="#FF776B")

    class Meta:
        verbose_name_plural = _('Activities')
        verbose_name = _('Activity')

    def __unicode__(self):
        return u'%s' % (self.name)    