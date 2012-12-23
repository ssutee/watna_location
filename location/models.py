from django.db import models
from django.utils.translation import ugettext_lazy as _

class Location(models.Model):
    place_name = models.CharField(max_length=200, verbose_name=_('Place Name'))
    longitude = models.FloatField(verbose_name=_('Longitude'))
    latitude = models.FloatField(verbose_name=_('Latitude'))

    contact_name = models.CharField(max_length=200, verbose_name=_('Contact Name'))
    address = models.TextField(verbose_name=_('Address'))
    email = models.EmailField(blank=True, null=True, verbose_name=_('Email'))
    phone_number = models.CharField(max_length=30, blank=True, null=True, verbose_name=_('Phone Number'))
    fax_number = models.CharField(max_length=30, blank=True, null=True, verbose_name=_('Fax Number'))

    activities = models.ManyToManyField('Activity', related_name="locations", blank=True, null=True, verbose_name=_('Activities'))
    
    additional_info = models.TextField(verbose_name=_('Additional information'))
    
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